from typing import Dict, Any, List
from fastapi import HTTPException, Depends
from app.services.utils import get_current_user
from ..core.database import supabase


def add_project(project_name: str, user_id: int, bill: int, color: str) -> Dict[Any, Any]:
    
    try:
        print(f"🔹 Insertando proyecto '{project_name}' para usuario {user_id} con bill {bill}")  # Debug log

        response = (
            supabase.table("togglProjects")
            .insert({"name": project_name, "user_id": user_id, "bill": bill, "color": color})
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
    




def update_project_details(project_name: str, user_id: int, bill: int, color: str) -> Dict[str, Any]:
    try:
        print(f"🔹 Actualizando proyecto '{project_name}' para usuario {user_id} con bill {bill} y color {color}")
        response = (
            supabase.table("togglProjects")
            .update({"bill": bill, "color": color})
            .eq("name", project_name)
            .eq("user_id", user_id)
            .execute()
        )
        print(f"✅ Proyecto actualizado: {response}")

        if not response.data:
            raise HTTPException(
                status_code=404, detail="Proyecto no encontrado o no se pudo actualizar"
            )

        return response.data

    except Exception as e:
        print(f"❌ Error en update_project_details: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al actualizar el proyecto: {str(e)}"
        )
    

    
    

def delete_project_and_events_by_name(project_name: str, user_id: int) -> Dict[str, Any]:
    try:
        print(f"🔹 Eliminando proyecto con nombre: {project_name} para usuario {user_id}")

        # Obtener el ID del proyecto basado en el nombre y el ID del usuario
        project_response = (
            supabase.table("togglProjects")
            .select("id")
            .eq("name", project_name)
            .eq("user_id", user_id)
            .execute()
        )

        if not project_response.data:
            raise HTTPException(
                status_code=404, detail="Proyecto no encontrado"
            )

        project_id = project_response.data[0]['id']

        # Eliminar eventos relacionados con el proyecto usando el nombre del proyecto
        events_response = (
            supabase.table("eventos")
            .delete()
            .eq("project", project_name)  # Cambiado a 'project' en lugar de 'project_id'
            .execute()
        )

        print(f"✅ Eventos eliminados: {events_response}")

        # Eliminar el proyecto
        project_delete_response = (
            supabase.table("togglProjects")
            .delete()
            .eq("id", project_id)
            .execute()
        )

        print(f"✅ Proyecto eliminado: {project_delete_response}")

        return {
            "project_deleted": project_delete_response.data,
            "events_deleted": events_response.data
        }

    except Exception as e:
        print(f"❌ Error en delete_project_and_events_by_name: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error inesperado al eliminar el proyecto y eventos: {str(e)}"
        )
