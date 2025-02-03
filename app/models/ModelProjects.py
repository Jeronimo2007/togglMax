from fastapi import Depends
from ..core.database import supabase


def create_project(name: str, user_id: int):
    
    response = supabase.table("projects").insert({
        'name': name,
        'owner_id': user_id
    }).execute()

    project_id = response.data[0]['id']  

    if response.data:
        response2 = supabase.table("projects_members").insert({
        'id_proyecto': project_id,
        'id_user': user_id,
        'admin_role': True
    }).execute()
        
    if not response2.data:
        return None

    return response


def project_update(project_name: str, new_project_name: str):
    
    project_response = supabase.table("projects").select("id").eq("name", project_name).execute()
    
    if not project_response.data:
        return None
    
    project_id = project_response.data[0]["id"]

    
    update_response = supabase.table("projects").update({"name": new_project_name}).eq("id", project_id).execute()

    return update_response.data 




def delete_project(project_name: str):
    
    project_response = supabase.table("projects").select("id").eq("name", project_name).execute()

    if not project_response.data:
        return None

    project_id = project_response.data[0]["id"]

    
    supabase.table("projects_members").delete().eq("id_proyecto", project_id).execute()

    
    response = supabase.table("projects").delete().eq("id", project_id).execute()

    return response.data


def add_user_to_project(project_name: str, member_name: str):
    
    project_response = supabase.table("projects").select("id").eq("name", project_name).execute()
    if not project_response.data:
        return None

    project_id = project_response.data[0]["id"]

   
    member_response = supabase.table("users").select("id").eq("username", member_name).execute()
    if not member_response.data:
        return None

    member_id = member_response.data[0]["id"]

   
    insert_response = supabase.table("projects_members").insert({
        "id_proyecto": project_id,
        "id_user": member_id,
        "admin_role": False
    }).execute()

    return insert_response.data


def delete_member(project_name: str, member_name: str):
    
    project_response = supabase.table("projects").select("id").eq("name", project_name).execute()
    if not project_response.data:
        return None

    project_id = project_response.data[0]["id"]

    
    member_response = supabase.table("users").select("id").eq("username", member_name).execute()
    if not member_response.data:
        return None

    member_id = member_response.data[0]["id"]

    
    delete_response = supabase.table("projects_members").delete().eq("id_proyecto", project_id).eq("id_user", member_id).execute()

    return delete_response.data


