from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict, List

from app.models.modelprojects import add_project, get_user_projects
from app.services.utils import payload

router = APIRouter(prefix="/project", tags=["proyecto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class ProjectCreate(BaseModel):
    project_name: str


class ProjectResponse(BaseModel):
    status: str
    message: str
    data: List[Dict] | Dict | None


@router.post("/add", response_model=ProjectResponse)
def create_project(data: ProjectCreate, token: str = Depends(oauth2_scheme)):
    """Crea un nuevo proyecto"""
    try:
        print(f"🔹 Recibida petición para crear proyecto: {data.project_name}")

        user_data = payload(token)
        print(f"✅ Usuario autenticado: {user_data}")

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = add_project(data.project_name, user_data["id"])
        print(f"✅ Proyecto creado: {response}")

        if not response:
            raise HTTPException(status_code=500, detail="No se pudo crear el proyecto")

        return ProjectResponse(
            status="success",
            message="Proyecto creado exitosamente",
            data=response
        )

    except Exception as e:
        print(f"❌ Error interno en /project/add: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/get", response_model=ProjectResponse)
def read_project(token: str = Depends(oauth2_scheme)):
    """Obtiene todos los proyectos del usuario"""
    try:
        print(f"🔹 Recibida petición GET para obtener proyectos")

        user_data = payload(token)
        print(f"✅ Usuario autenticado: {user_data}")

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        # Pasamos el user_data completo en lugar de solo el ID
        response = get_user_projects(user_data)
        print(f"✅ Proyectos obtenidos: {response}")

        return ProjectResponse(
            status="success",
            message="Proyectos obtenidos exitosamente",
            data=response if response else []
        )

    except Exception as e:
        print(f"❌ Error interno en /project/get: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")