from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from ..core.database import supabase

class Event(BaseModel):
    descripcion: str
    duracion: float
    fecha_inicio: datetime
    fecha_fin: datetime

def crear_evento(descripcion: str, duracion: float, fecha_inicio: datetime, fecha_fin: datetime):
    evento = {
        "descripcion": descripcion,
        "duracion": duracion,
        "fecha_inicio": fecha_inicio.isoformat(),  # Convertir a string ISO
        "fecha_fin": fecha_fin.isoformat()  # Convertir a string ISO
    }
    
    try:
        response = supabase.table("eventos").insert(evento).execute()
        return response.data
    except Exception as e:
        raise ValueError(f"Error al crear evento: {str(e)}")

def obtener_eventos() -> List[dict]:
    try:
        response = supabase.table("eventos").select("*").execute()
        eventos = []
        
        for evento in response.data:
            # Convertir strings ISO a objetos datetime
            evento['fecha_inicio'] = datetime.fromisoformat(evento['fecha_inicio'])
            evento['fecha_fin'] = datetime.fromisoformat(evento['fecha_fin'])
            eventos.append(evento)
            
        return eventos
    except Exception as e:
        raise ValueError(f"Error al obtener eventos: {str(e)}")