from typing import Optional
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from ..core.database import supabase
from jose import JWTError, jwt
import bcrypt


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "_pEE_GC1P2Z-HWU0aSqmABrXyGgr5Mm1Q5JmhP1tOq4")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verifica el JWT y extrae el usuario."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("sub")
        id = int(id)
        if id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        response = supabase.table("users").select("*").eq("id", id).execute()

        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return response.data[0]

    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Genera un JWT con los datos del usuario."""
    to_encode = data.copy()

   
    if "sub" in to_encode and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire  

    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Verifica y decodifica el JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       
        return payload
    except JWTError as e:
        
        return None
    


def get_projects(token: str = Depends(oauth2_scheme)):
    response = supabase.table('projects').select("name").execute()
    if response.data:
        return response
    else:
        return None
    

def payload(token):
    payload = decode_access_token(token)
   
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    

def get_members(project_name: str):
    
    project_response = supabase.table("projects").select("id").eq("name", project_name).execute()
    if not project_response.data:
        return "no se pudo encontrar el proyecto"

    project_id = project_response.data[0]["id"]

    
    members_response = supabase.table("projects_members").select("id_user", "admin_role").eq("id_proyecto", project_id).execute()
    if not members_response.data:
        return "no se encontraron miembros en el proyecto"

    members_data = members_response.data

    
    user_ids = [member["id_user"] for member in members_data]
    users_response = supabase.table("users").select("id", "username").in_("id", user_ids).execute()
    if not users_response.data:
        return "no se pudieron obtener los detalles de los usuarios"

   
    user_info = []
    for member in members_data:
        user = next((user for user in users_response.data if user["id"] == member["id_user"]), None)
        if user:
            user_info.append({
                "username": user["username"],
                "admin_role": member["admin_role"]
            })

    return user_info




def get_project_id(project_name: str):
    response = supabase.table('projects').select('id').eq('name', project_name).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return response.data[0]['id']



def get_current_user_id(current_user: dict):
    return current_user['id']


def get_user_id(user_name: str):
    response = supabase.table('users').select('id').eq('username', user_name).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return response.data[0]['id']


