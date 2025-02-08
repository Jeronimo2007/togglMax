import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Union
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..core.database import supabase

# Configuración del contexto de hashing con passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Constantes
SECRET_KEY = os.getenv("SECRET_KEY", "_pEE_GC1P2Z-HWU0aSqmABrXyGgr5Mm1Q5JmhP1tOq4")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando passlib.
    Args:
        password: Contraseña en formato string
    Returns:
        str: Hash de la contraseña
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash.
    Args:
        plain_password: Contraseña sin procesar
        hashed_password: Hash de la contraseña almacenada
    Returns:
        bool: True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un JWT con los datos del usuario.
    Args:
        data: Diccionario con los datos a codificar
        expires_delta: Tiempo de expiración opcional
    Returns:
        str: Token JWT generado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> Optional[Dict]:
    """
    Verifica y decodifica el JWT.
    Args:
        token: Token JWT a decodificar
    Returns:
        Dict | None: Payload del token si es válido, None si no lo es
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Verifica el JWT y extrae el usuario.
    Args:
        token: Token JWT a verificar
    Returns:
        Dict: Datos del usuario
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return response.data[0]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

async def get_projects(token: str = Depends(oauth2_scheme)):
    """
    Obtiene los proyectos desde Supabase.
    Args:
        token: Token JWT para autenticación
    Returns:
        Response: Respuesta de Supabase con los proyectos
    """
    response = supabase.table('projects').select("*").execute()
    return response if response.data else None

def payload(token: str) -> Dict:
    """
    Verifica y retorna el payload del token.
    Args:
        token: Token JWT a verificar
    Returns:
        Dict: Payload del token
    Raises:
        HTTPException: Si el token es inválido
    """
    decoded_payload = decode_access_token(token)
    if not decoded_payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return decoded_payload
