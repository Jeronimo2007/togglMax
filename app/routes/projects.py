from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict, List, Optional

from app.models.modelprojects import add_project, delete_project_and_events_by_name, get_user_projects, update_project_details
from app.services.utils import payload

router = APIRouter(prefix="/project", tags=["proyecto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class ProjectCreate(BaseModel):
    project_name: str
    bill: Optional[int]  
    color: Optional[str] = "#f79aff"


class ProjectUpdate(BaseModel):
    bill: int
    color: str


class ProjectResponse(BaseModel):
    status: str
    message: str
    data: List[Dict] | Dict | None


@router.post("/add", response_model=ProjectResponse)
def create_project(data: ProjectCreate, token: str = Depends(oauth2_scheme)):
    
    try:
        

        user_data = payload(token)
        

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = add_project(data.project_name, user_data["id"], data.bill, data.color)
        

        if not response:
            raise HTTPException(status_code=500, detail="No se pudo crear el proyecto")

        return ProjectResponse(
            status="success",
            message="Proyecto creado exitosamente",
            data=response
        )

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/get", response_model=ProjectResponse)
def read_project(token: str = Depends(oauth2_scheme)):
    
    try:
        

        user_data = payload(token)
        

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = get_user_projects(user_data)
        

        return ProjectResponse(
            status="success",
            message="Proyectos obtenidos exitosamente",
            data=response if response else []
        )

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")



@router.put("/update/{project_name}", response_model=ProjectResponse)
def update_project(project_name: str, data: ProjectUpdate, token: str = Depends(oauth2_scheme)):
    try:
        print(f"🔹 Recibida petición para actualizar proyecto: {project_name} con bill: {data.bill} y color: {data.color}")

        user_data = payload(token)
        print(f"✅ Usuario autenticado: {user_data}")

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = update_project_details(project_name, user_data["id"], data.bill, data.color)
        print(f"✅ Proyecto actualizado: {response}")

        return ProjectResponse(
            status="success",
            message="Proyecto actualizado exitosamente",
            data=response
        )

    except Exception as e:
        print(f"❌ Error interno en /project/update: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    

@router.delete("/delete/{project_name}", response_model=ProjectResponse)
def delete_project(project_name: str, token: str = Depends(oauth2_scheme)):
    try:
        

        user_data = payload(token)
        

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = delete_project_and_events_by_name(project_name, user_data["id"])
        
        if not response:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado o no se pudo eliminar")

        return ProjectResponse(
            status="success",
            message="Proyecto y eventos eliminados exitosamente",
            data=response
        )

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")