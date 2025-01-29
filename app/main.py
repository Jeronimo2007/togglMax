from fastapi import FastAPI, HTTPException, Depends, Request, status
from .models.models import create_user, get_user
from .core.database import supabase
from .services.utils import verify_password
from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from  app.services.utils import get_current_user,create_access_token

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Bienvenido a la API con Supabase"}

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def register_user(username: str, password: str, adminRole: bool):
    """Registra un nuevo usuario con contraseña hasheada."""
    user = create_user(username, password, adminRole)
    if not user:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return {"message": "Usuario creado exitosamente"}

@app.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Verifica credenciales y devuelve un token JWT."""
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", status_code=status.HTTP_200_OK)
async def read_current_user(username: str = Depends(get_current_user)):
    """Devuelve la información del usuario autenticado."""
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"username": user["username"], "adminRole": user["adminRole"]}
