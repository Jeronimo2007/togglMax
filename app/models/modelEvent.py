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

def crear_evento(descripcion: str, duracion: float, fecha_inicio: datetime, fecha_fin: datetime, project: str):
   
   
    evento = {
        "descripcion": descripcion,
        "duracion": duracion,
        "fecha_inicio": fecha_inicio.isoformat(),  
        "fecha_fin": fecha_fin.isoformat() , 
        'project': project
    }
    
    try:
        response = supabase.table("eventos").insert(evento).execute()
        return response.data
    except Exception as e:
        raise ValueError(f"Error al crear evento: {str(e)}")

def obtener_eventos():
    try:
        response = supabase.table('eventos').select("*").execute()
        if not response.data:
            return []

        eventos = response.data

        # 🔹 Convertir fechas correctamente
        for evento in eventos:
            try:
                # Remover microsegundos si están presentes
                if "." in evento["fecha_inicio"]:
                    evento["fecha_inicio"] = evento["fecha_inicio"].split(".")[0]

                if "." in evento["fecha_fin"]:
                    evento["fecha_fin"] = evento["fecha_fin"].split(".")[0]

                # Convertir a formato ISO 8601 estándar
                evento["fecha_inicio"] = datetime.fromisoformat(evento["fecha_inicio"]).isoformat() + "Z"
                evento["fecha_fin"] = datetime.fromisoformat(evento["fecha_fin"]).isoformat() + "Z"

            except ValueError as e:
                print(f"⚠️ Error al convertir la fecha del evento {evento['id']}: {e}")
        
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
