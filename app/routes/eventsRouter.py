from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

from ..services.utils import get_current_user, payload
from ..models import modelEvent

router = APIRouter(prefix="/event", tags=["events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

class EventCreate(BaseModel):
    project: str
    descripcion: Optional[str] = None  
    duracion: float

class ManualEventCreate(BaseModel):
    project: str
    descripcion: Optional[str] = None  
    fecha_inicio: datetime
    fecha_fin: datetime

@router.post("/eventos/")
async def crear_evento(data: EventCreate, token: str = Depends(oauth2_scheme)):
    
    user_data = payload(token)  
    user_id = user_data["id"]

    fecha_inicio = datetime.utcnow()  
    fecha_fin = fecha_inicio + timedelta(seconds=data.duracion) 

    response = modelEvent.crear_evento(
        data.descripcion, 
        data.duracion, 
        fecha_inicio, 
        fecha_fin, 
        data.project,
        user_id
    )

    return {"status": "success", "message": "Evento creado exitosamente", "data": response}

@router.post("/eventos/manual/")
async def crear_evento_manual(data: ManualEventCreate, token: str = Depends(oauth2_scheme)):
    
    user_data = payload(token)  
    user_id = user_data["id"]

    duracion = (data.fecha_fin - data.fecha_inicio).total_seconds()

    if duracion <= 0:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )

    response = modelEvent.crear_evento(
        data.descripcion,
        duracion,
        data.fecha_inicio,
        data.fecha_fin,
        data.project,
        user_id
    )

    return {"status": "success", "message": "Evento manual creado exitosamente", "data": response}

@router.get("/eventos/")
async def obtener_eventos(token: str = Depends(oauth2_scheme)):
    
    user_data = payload(token)
    user_id = user_data["id"]
    response = modelEvent.obtener_eventos(user_id)

    
    for evento in response:
        
        bill = modelEvent.get_project_bill(evento['project'])
        evento['bill'] = bill

    return {"status": "success", "message": "Eventos obtenidos exitosamente", "data": response}

@router.delete("/eventos/{event_id}/")
async def eliminar_evento(event_id: int, token: str = Depends(oauth2_scheme)):
    
    user = get_current_user(token)
    user_id = user["id"]

    response = modelEvent.remove_evento(event_id, user_id)
    return {"status": "success", "message": "Evento eliminado correctamente", "data": response}