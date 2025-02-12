from typing import Dict, Any, List
from fastapi import HTTPException, Depends
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

def get_user_projects(current_user: Dict = Depends(get_current_user)) -> List[Dict[str, Any]]:
    """
    Obtiene todos los proyectos del usuario autenticado utilizando el token JWT.
    
    Args:
        current_user: Usuario actual obtenido del token JWT mediante get_current_user
    
    Returns:
        List[Dict[str, Any]]: Lista de proyectos del usuario autenticado
    """
    try:
        # Verificamos si current_user es un diccionario
        if isinstance(current_user, dict):
            user_id = current_user.get('id')
        else:
            # Si no es un diccionario, asumimos que es el ID directamente
            user_id = current_user

        print(f"🔹 Buscando proyectos para user_id {user_id}")
        print(f"🔍 Tipo de user_id: {type(user_id)}")
        
        if user_id is None:
            raise HTTPException(status_code=400, detail="ID de usuario no válido")
        
        response = (
            supabase.table("togglProjects")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        print(f"✅ Respuesta completa de la BD: {response}")
        print(f"📋 Datos de la respuesta: {response.data}")

        if not response.data:
            print("⚠️ No se encontraron proyectos para el usuario")
            return []

        print(f"✅ Número de proyectos encontrados: {len(response.data)}")
        return response.data

    except Exception as e:
        print(f"❌ Error en get_user_projects: {str(e)}")
        print(f"❌ Tipo de error: {type(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al obtener los proyectos: {str(e)}"
        )