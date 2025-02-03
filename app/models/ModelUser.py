from supabase import Client
from ..core.database import supabase  
from ..services.utils import hash_password  


def create_user(username: str, password: str):
    hashed_password = hash_password(password)  
    response = supabase.table("users").insert({
        "username": username,
        "hashed_password": hashed_password,
    }).execute()
    
    if response.data:
        return {"message": "Usuario creado exitosamente", "user": response.data}
    else:
        return {"error": "Error al crear el usuario", "details": response.error}

def get_user(username: str):
    """ Obtiene los datos de un usuario por su username """
    response = supabase.table("users").select("id,username, hashed_password").eq("username", username).execute()
    if response.data:
        return response.data[0]  
    else:
        return None  

def get_all_users():
    """ Obtiene la lista de todos los usuarios """
    response = supabase.table("users").select("username, adminRole").execute()
    
    return response.data if response.data else []