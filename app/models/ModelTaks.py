
from fastapi import Depends, HTTPException
from app.services.utils import get_current_user, get_current_user_id, get_project_id, get_user_id
from ..core.database import supabase



def add_task(project_name: str, user_name: str, title: str, description: str, current_user: dict):
    project_id = get_project_id(project_name)
    current_user_id = get_current_user_id(current_user)
    user_id = get_user_id(user_name)

    
    response_member = supabase.table('projects_members').select('id_user', 'admin_role')\
        .eq('id_proyecto', project_id).eq('id_user', current_user_id).execute()
    if not response_member.data:
        raise HTTPException(status_code=403, detail="El usuario autenticado no está en el proyecto")
    
    if not response_member.data[0]['admin_role']:
        raise HTTPException(status_code=403, detail="El usuario autenticado no tiene permisos para crear tareas en este proyecto")

    
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



def get_task_details(project_name: str, current_user: dict):
    project_id = get_project_id(project_name)
    current_user_id = get_current_user_id(current_user)
    
    response_member = supabase.table('projects_members').select('id_user', 'admin_role')\
        .eq('id_proyecto', project_id).eq('id_user', current_user_id).execute()
    if not response_member.data:
        raise HTTPException(status_code=403, detail="El usuario autenticado no está en el proyecto")
    
    if not response_member.data[0]['admin_role']:
        raise HTTPException(status_code=403, detail="El usuario autenticado no tiene permisos para crear o eliminar tareas en este proyecto")
    
    response_tasks = supabase.table('task').select('*').eq('id_proyecto', project_id).execute()

    return response_tasks



def update_task(project_name: str, task_id: int, current_user: dict ,title: str = None, description: str = None):
    project_id = get_project_id(project_name)
    current_user_id = get_current_user_id(current_user)
    
    response_member = supabase.table('projects_members').select('id_user', 'admin_role')\
        .eq('id_proyecto', project_id).eq('id_user', current_user_id).execute()
    if not response_member.data:
        raise HTTPException(status_code=403, detail="El usuario autenticado no está en el proyecto")
    
    if not response_member.data[0]['admin_role']:
        raise HTTPException(status_code=403, detail="El usuario autenticado no tiene permisos para crear o eliminar tareas en este proyecto")
    
    
    update_data = {}
    if title:
        update_data['title'] = title
    if description:
        update_data['description'] = description
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron cambios válidos")
    
    
    response_update = supabase.table('task').update(update_data).eq('id', task_id).execute()
    
    return {"message": "Tarea actualizada correctamente"}
    


def delete_task(project_name: str, task_id: int, current_user: dict):
    project_id = get_project_id(project_name)
    current_user_id = get_current_user_id(current_user)

    response_member = supabase.table('projects_members').select('id_user', 'admin_role')\
        .eq('id_proyecto', project_id).eq('id_user', current_user_id).execute()
    if not response_member.data:
        raise HTTPException(status_code=403, detail="El usuario autenticado no está en el proyecto")
    
    if not response_member.data[0]['admin_role']:
        raise HTTPException(status_code=403, detail="El usuario autenticado no tiene permisos para crear o eliminar tareas en este proyecto")


    response_delete_tasks = supabase.table('task').delete().eq('id', task_id).execute()
    if not response_delete_tasks:
        return "no se pudieron eliminar las tareas del proyeto revisar por favor "
    else:
        return "tarea eliminada exitosamente"
    
    
    

    








