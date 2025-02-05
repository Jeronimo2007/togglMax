from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer

from app.models.ModelProjects import add_user_to_project, create_project, delete_member, delete_project, project_update
from app.services.utils import decode_access_token, get_members, get_projects, payload


router = APIRouter(prefix='/projects', tags=["proyectos"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post("/add")
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


@router.get('/get_projects')
async def read_project(projects: dict = Depends(get_projects), token: str = Depends(oauth2_scheme)):
    """Buscar proyectos en la base de datos"""
    payload(token)

    if not projects:
        raise HTTPException(status_code=404,detail='sin proyectos encontrados')
    return projects


@router.put('/update')
def update_project(project_name: str = Query(..., description="Nombre actual del proyecto"),
                   new_name: str = Query(..., description="Nuevo nombre para el proyecto") ,
                   token: str = Depends(oauth2_scheme)):
    payload(token)
    
    response = project_update(project_name, new_name)

    if not response:
        raise HTTPException(status_code=404,detail='Proyecto no encontrado')
    
    return "creado exitosamente: ", new_name


@router.delete("/remove_project")
def remove_project(name: str, token: str = Depends(oauth2_scheme)):
    payload(token)

    response = delete_project(name)
    if not response:
        raise HTTPException(status_code=404,detail='proyecto ya eliminado o no existe')
    
    return "Eliminado correctamente"



@router.post('/add_member')
async def add_member(project_name: str = Query(..., description="Nombre actual del proyecto"),
                   member_name: str = Query(..., description="Nombre de el usuario") ,
                   token: str = Depends(oauth2_scheme)):
    
    payload(token)

    response = add_user_to_project(project_name, member_name)
    if not response:
        raise HTTPException(status_code=404,detail='Usuario o proyecto no existente')
    
    return "agregado correctamente"


@router.get('/get_members')
def read_members(project_name: str, token: str = Depends(oauth2_scheme)):
    
    payload(token)

    response = get_members(project_name)

    return response


@router.delete('/remove_member')
def remove_member(project_name: str = Query(..., description="Nombre actual del proyecto"),
                   member_name: str = Query(..., description="Nombre de el usuario") ,
                   token: str = Depends(oauth2_scheme)):
    
    payload(token)


    response = delete_member(project_name, member_name)


    if not response:
        raise HTTPException(status_code=404,detail='Usuario o proyecto no existente')
    
    return "eliminado exitosamente"