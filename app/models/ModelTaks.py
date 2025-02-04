
from fastapi import Depends, HTTPException

from app.services.utils import get_current_user
from ..core.database import supabase



def add_task(project_name: str, user_name: str, title: str, description: str, current_user: dict):
    # Obtener el id del proyecto
    response_project_id = supabase.table('projects').select('id').eq('name', project_name).execute()
    if not response_project_id.data:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    project_id = response_project_id.data[0]['id']

    # Obtener el id del usuario autenticado (current_user)
    current_user_id = current_user['id']

    # Verificar que el usuario autenticado esté en el proyecto y tenga el rol de administrador
    response_member = supabase.table('projects_members').select('id_user', 'admin_role')\
        .eq('id_proyecto', project_id).eq('id_user', current_user_id).execute()
    if not response_member.data:
        raise HTTPException(status_code=403, detail="El usuario autenticado no está en el proyecto")
    
    if not response_member.data[0]['admin_role']:
        raise HTTPException(status_code=403, detail="El usuario autenticado no tiene permisos para crear tareas en este proyecto")

    # Obtener el id del usuario al que se le asignará la tarea
    response_user_id = supabase.table('users').select('id').eq('username', user_name).execute()
    if not response_user_id.data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_id = response_user_id.data[0]['id']

    # Verificar que el usuario al que se le asignará la tarea esté en el proyecto
    response_assignee_member = supabase.table('projects_members').select('id_user')\
        .eq('id_proyecto', project_id).eq('id_user', user_id).execute()
    if not response_assignee_member.data:
        raise HTTPException(status_code=403, detail="El usuario al que se le asignará la tarea no está en el proyecto")

    # Crear la tarea
    task_data = {
        'title': title,
        'description': description,
        'state': 'pendiente',
        'id_proyecto': project_id,
        'id_user': user_id
    }
    response_task = supabase.table('task').insert(task_data).execute()

    return {"message": f"Tarea creada correctamente para {user_name}"}



def update_task(task_title: str, new_title: str , new_description: str):
    pass




