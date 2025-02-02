from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.ModelProjects import create_project, delete_project, project_update
from app.models.ModelUser import create_user, get_user
from app.services.utils import get_current_user, create_access_token, decode_access_token, payload, verify_password, get_projects

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Ruta principal de bienvenida"""
    return {"message": "Bienvenido a la API con Supabase"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(username: str, password: str, adminRole: bool):
    """Registra un nuevo usuario con contraseña hasheada."""
    user = create_user(username, password, adminRole)
    if not user:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return {"message": "Usuario creado exitosamente"}


@app.post("/login")
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


@app.get("/users/me", status_code=status.HTTP_200_OK)
async def read_current_user(user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    """Devuelve la información del usuario autenticado."""
    payload(token)

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@app.post("/projects/add")
async def add_project(project_name: str, token: str = Depends(oauth2_scheme)):
    """Crea un proyecto y asigna el usuario autenticado como propietario."""
    
    payload = decode_access_token(token)
   
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user_id = int(payload.get("sub"))

    if not user_id:
        raise HTTPException(status_code=400, detail="ID de usuario no encontrado en el token")

    project = create_project(project_name, user_id)
    if not project:
        raise HTTPException(status_code=400, detail="No se pudo crear el proyecto")

    return {"message": "Proyecto creado exitosamente", "project": project}


@app.get('/projects/get_projects')
async def read_project(projects: dict = Depends(get_projects), token: str = Depends(oauth2_scheme)):
    """Buscar proyectos en la base de datos"""
    payload(token)

    if not projects:
        raise HTTPException(status_code=404,detail='sin proyectos encontrados')
    return projects


@app.put('/projects/update')
def update_project(project_name: str = Query(..., description="Nombre actual del proyecto"),
                   new_name: str = Query(..., description="Nuevo nombre para el proyecto") ,
                   token: str = Depends(oauth2_scheme)):
    payload(token)
    
    response = project_update(project_name, new_name)

    if not response:
        raise HTTPException(status_code=404,detail='Proyecto no encontrado')


@app.post("/projects/remove_project")
def remove_project(name: str, token: str = Depends(oauth2_scheme)):
    payload(token)

    response = delete_project(name)
    if not response:
        raise HTTPException(status_code=404,detail='proyecto ya eliminado o no existe')
    
    return "Eliminado correctamente"



@app.post('/projects/add_member')
async def add_member():
    pass