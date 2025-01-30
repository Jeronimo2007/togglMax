from fastapi import Depends
from ..core.database import supabase


def create_project(name:str, id:int):
    response = supabase.table("projects").insert({
        'name': name,
        'owner_id': id
    } 
    ).execute()
    return response



def delete_project():
    pass