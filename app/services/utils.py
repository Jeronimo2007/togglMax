from typing import Optional
import bcrypt
import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from ..core.database import supabase


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