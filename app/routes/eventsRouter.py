from datetime import datetime, timedelta
from ..services.utils import payload
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from ..models import modelEvent


router = APIRouter(prefix="/event", tags=["events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")



@router.post("/eventos/")
async def crear_evento(descripcion: str, duracion: float,token: str = Depends(oauth2_scheme)):

    payload(token)

    fecha_inicio = datetime.utcnow()  # Fecha cuando empieza el temporizador
    fecha_fin = fecha_inicio + timedelta(seconds=duracion)  # Fecha de fin del temporizador
    response = modelEvent.crear_evento(descripcion, duracion, fecha_inicio, fecha_fin)

    return response


@router.get("/eventos/")
async def obtener_eventos(token: str = Depends(oauth2_scheme)):
    payload(token)
    response = modelEvent.obtener_eventos()
    return response