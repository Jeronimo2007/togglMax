from datetime import timedelta
from fastapi import APIRouter, Depends,status,Query, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.ModelUser import create_user, get_user
from app.services.utils import create_access_token, get_current_user, payload, verify_password





router = APIRouter(prefix="/users", tags=["usuarios"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(username: str, password: str):
    """Registra un nuevo usuario con contraseña hasheada."""
    user = create_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return {"message": "Usuario creado exitosamente"}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Verifica credenciales y devuelve un token JWT."""
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    
    access_token = create_access_token(
        data={"sub": user["id"]},  
        expires_delta=timedelta(minutes=60)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", status_code=status.HTTP_200_OK)
async def read_current_user(user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """Devuelve la información del usuario autenticado."""
    payload(token)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user