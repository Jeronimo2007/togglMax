from fastapi import Depends
from ..core.database import supabase


def create_project(name:str, id:int):
    response = supabase.table("projects").insert({
        'name': name,
        'owner_id': id
    } 
    ).execute()
    return response



def delete_project(project_name:str):
    response = supabase.table("projects").delete().eq("name", project_name).execute()

    if response.data:
        return response.data
    else:
        return None


