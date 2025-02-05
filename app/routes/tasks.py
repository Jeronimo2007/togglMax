from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from app.models.ModelTaks import add_task, delete_task, get_task_details, update_task
from app.services.utils import get_current_user, payload


router = APIRouter(prefix='/task', tags= ['tareas'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

@router.post('/create')
def create_task(
    project_name: str, 
    user_name: str, 
    title: str, 
    description: str, 
    token: str = Depends(oauth2_scheme)
):
    
    current_user = get_current_user(token)

    
    response = add_task(project_name, user_name, title, description, current_user)

    return response



@router.get('/read')
def get_task(project_name:str = Query(..., description='titulo de la proyecto'), token: str = Depends(oauth2_scheme)):

    payload(token)

    current_user = get_current_user(token)

    response = get_task_details(project_name, current_user)

    return response


@router.put('/update')
def change_title_or_description(project_name: str, task_id: int,title: str = None, description: str = None,token: str = Depends(oauth2_scheme)):
    
    payload(token)

    current_user = get_current_user(token)

    response = update_task(project_name,task_id,current_user ,title, description)

    return response

@router.delete('/remove_task')
def remove_task(project_name: str, task_id: int,token: str = Depends(oauth2_scheme)):

    payload(token)

    current_user = get_current_user(token)

    response = delete_task(project_name, task_id, current_user)

    return response
