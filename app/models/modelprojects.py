from typing import Dict, Any, List
from fastapi import HTTPException
from app.services.utils import get_current_user
from ..core.database import supabase


def add_project(project_name: str, user_id: int) -> Dict[Any, Any]:
    """Agrega un nuevo proyecto a la base de datos con el usuario autenticado."""
    try:
        print(f"🔹 Insertando proyecto '{project_name}' para usuario {user_id}")  # Debug log

        response = (
            supabase.table("togglProjects")
            .insert({"name": project_name, "user_id": user_id})
            .execute()
        )

        print(f"✅ Respuesta de la BD: {response}")  # Log para ver respuesta de Supabase

        if not response.data:
            raise HTTPException(
                status_code=500, detail="Error al crear el proyecto en la base de datos"
            )

        return response.data

    except Exception as e:
        print(f"❌ Error en add_project: {str(e)}")  # Muestra error en terminal
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al crear el proyecto: {str(e)}"
        )

def get_user_projects(user_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todos los proyectos del usuario autenticado.
    """
    try:
        print(f"🔹 Buscando proyectos para user_id {user_id}")  # Debug log

        response = (
            supabase.table("togglProjects")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        print(f"✅ Respuesta de la BD: {response}")  # Log para ver respuesta

        if response.data is None:
            raise HTTPException(
                status_code=404, detail="No se encontraron proyectos"
            )

        return response.data

    except Exception as e:
        print(f"❌ Error en get_user_projects: {str(e)}")  # Log del error
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al obtener los proyectos: {str(e)}"
        )
