from datetime import datetime, timedelta
from ..services.utils import get_current_user, payload
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..models import modelEvent


router = APIRouter(prefix="/event", tags=["events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



@router.post("/eventos/")
async def crear_evento(descripcion: str, duracion: float,token: str = Depends(oauth2_scheme)):

    payload(token)

    user = get_current_user(token)
    user_id = user["id"]
    

    fecha_inicio = datetime.utcnow()  # Fecha cuando empieza el temporizador
    fecha_fin = fecha_inicio + timedelta(seconds=duracion)  # Fecha de fin del temporizador
    response = modelEvent.crear_evento(descripcion, duracion, fecha_inicio, fecha_fin, user_id)

    return response


@router.get("/eventos/")
async def obtener_eventos(token: str = Depends(oauth2_scheme)):
    payload(token)
    response = modelEvent.obtener_eventos()
    return response

    
@router.delete("/eventos/{event_id}/")
async def eliminar_evento(event_id: int, token: str = Depends(oauth2_scheme)):
    payload(token)
    user = get_current_user(token)
    user_id = user["id"]

    response = modelEvent.remove_evento(event_id, user_id)
    return response





