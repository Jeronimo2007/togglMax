from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.models.modelprojects import add_project, get_user_projects
from app.services.utils import payload

router = APIRouter(prefix="/project", tags=["proyecto"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class ProjectCreate(BaseModel):
    project_name: str


@router.post("/add")
def create_project(data: ProjectCreate, token: str = Depends(oauth2_scheme)):
    """Crea un nuevo proyecto"""
    try:
        print(f"🔹 Recibida petición para crear proyecto: {data.project_name}")  # Log para debug

        user_data = payload(token)  # Obtiene el usuario autenticado
        print(f"✅ Usuario autenticado: {user_data}")  # Log para ver usuario

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = add_project(data.project_name, user_data["id"])  # Pasa el user_id
        print(f"✅ Proyecto creado: {response}")  # Log para ver respuesta

        if not response:
            raise HTTPException(status_code=500, detail="No se pudo crear el proyecto")

        return {"status": "success", "message": "Proyecto creado exitosamente", "data": response}

    except Exception as e:
        print(f"❌ Error interno en /project/add: {str(e)}")  # Muestra el error en logs
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")



@router.get("/get")
def read_project(token: str = Depends(oauth2_scheme)):
    """Obtiene todos los proyectos del usuario"""
    try:
        print(f"🔹 Recibida petición GET para obtener proyectos")  # Log de depuración

        user_data = payload(token)  # ✅ Obtiene el usuario autenticado
        print(f"✅ Usuario autenticado: {user_data}")  # Log para ver usuario

        if not user_data or "id" not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        response = get_user_projects(user_data["id"])  # ✅ Pasa el user_id
        print(f"✅ Proyectos obtenidos: {response}")  # Log para ver respuesta de la BD

        if not response:
            return {"status": "error", "message": "No se encontraron proyectos", "data": []}

        return {"status": "success", "message": "Proyectos obtenidos exitosamente", "data": response}

    except Exception as e:
        print(f"❌ Error interno en /project/get: {str(e)}")  # Log del error
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

