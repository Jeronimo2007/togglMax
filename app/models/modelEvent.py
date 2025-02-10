from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from ..core.database import supabase

class Event(BaseModel):
    descripcion: str
    duracion: float
    fecha_inicio: datetime
    fecha_fin: datetime
    user_id: Optional[int] = None

def crear_evento(descripcion: str, duracion: float, fecha_inicio: datetime, fecha_fin: datetime, user_id: int):
   
   
    evento = {
        "descripcion": descripcion,
        "duracion": duracion,
        "fecha_inicio": fecha_inicio.isoformat(),  
        "fecha_fin": fecha_fin.isoformat() , 
        "user_id": user_id
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
            
            evento['fecha_inicio'] = datetime.fromisoformat(evento['fecha_inicio'])
            evento['fecha_fin'] = datetime.fromisoformat(evento['fecha_fin'])
            eventos.append(evento)
            
        return eventos
    except Exception as e:
        raise ValueError(f"Error al obtener eventos: {str(e)}")
    


def remove_evento(event_id: int, user_id: int):
    try:
        # Verificar si el evento pertenece al usuario
        response = supabase.table("eventos").select("user_id").eq("id", event_id).execute()

        if not response.data:
            raise ValueError("Evento no encontrado")

        if response.data[0]["user_id"] != user_id:
            raise ValueError("No tienes permiso para eliminar este evento")

        # Eliminar el evento
        supabase.table("eventos").delete().eq("id", event_id).execute()
        
        return {"message": "Evento eliminado correctamente"}
    
    except Exception as e:
        raise ValueError(f"Error al eliminar evento: {str(e)}")
