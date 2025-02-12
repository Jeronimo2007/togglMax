from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from ..core.database import supabase

def crear_evento(descripcion: str, duracion: float, fecha_inicio: datetime, 
                fecha_fin: datetime, project: str, user_id: int) -> Dict[str, Any]:
    """
    Crea un nuevo evento en la base de datos asociado directamente al usuario.
    """
    try:
        data = {
            "descripcion": descripcion,
            "duracion": duracion,
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "project": project,
            "user_id": user_id
        }
        
        response = supabase.table('eventos').insert(data).execute()
        
        if not response.data:
            raise ValueError("No se pudo crear el evento")
            
        return response.data[0]
        
    except Exception as e:
        print(f"❌ Error en crear_evento: {str(e)}")
        raise ValueError(f"Error al crear evento: {str(e)}")

def obtener_eventos(user_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todos los eventos asociados directamente al usuario mediante user_id.
    """
    try:
        print(f"🔍 Buscando eventos para usuario {user_id}")
        
        # Obtenemos eventos directamente por user_id
        eventos_response = (
            supabase.table('eventos')
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if not eventos_response.data:
            print("ℹ️ No se encontraron eventos para el usuario")
            return []

        eventos = eventos_response.data
        print(f"✅ Eventos encontrados: {len(eventos)}")

        # Procesamos las fechas si existen
        for evento in eventos:
            if "fecha_inicio" in evento and "fecha_fin" in evento:
                try:
                    if "." in evento["fecha_inicio"]:
                        evento["fecha_inicio"] = evento["fecha_inicio"].split(".")[0]
                    if "." in evento["fecha_fin"]:
                        evento["fecha_fin"] = evento["fecha_fin"].split(".")[0]

                    evento["fecha_inicio"] = datetime.fromisoformat(evento["fecha_inicio"]).isoformat() + "Z"
                    evento["fecha_fin"] = datetime.fromisoformat(evento["fecha_fin"]).isoformat() + "Z"
                except ValueError as e:
                    print(f"⚠️ Error al procesar fechas del evento {evento.get('id', 'unknown')}: {e}")

        return eventos

    except Exception as e:
        print(f"❌ Error en obtener_eventos: {str(e)}")
        raise ValueError(f"Error al obtener eventos: {str(e)}")

def remove_evento(event_id: int, user_id: int) -> Dict[str, Any]:
    """
    Elimina un evento específico verificando que pertenezca al usuario.
    
    Args:
        event_id: ID del evento a eliminar
        user_id: ID del usuario que intenta eliminar el evento
    
    Returns:
        Dict[str, Any]: Datos del evento eliminado
        
    Raises:
        HTTPException: Si el evento no existe o no pertenece al usuario
        ValueError: Si hay un error en la operación de eliminación
    """
    try:
        print(f"🗑️ Intentando eliminar evento {event_id} para usuario {user_id}")
        
        # Primero verificamos que el evento exista y pertenezca al usuario
        verificacion = (
            supabase.table('eventos')
            .select("*")
            .eq("id", event_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        print(f"📋 Resultado de verificación: {verificacion.data}")
        
        if not verificacion.data:
            print(f"⚠️ Evento {event_id} no encontrado o no pertenece al usuario {user_id}")
            raise HTTPException(
                status_code=404, 
                detail="Evento no encontrado o no tienes permiso para eliminarlo"
            )
        
        # Si llegamos aquí, el evento existe y pertenece al usuario
        print(f"✅ Verificación exitosa, procediendo a eliminar evento {event_id}")
        
        # Realizamos la eliminación
        response = (
            supabase.table('eventos')
            .delete()
            .eq("id", event_id)
            .execute()
        )
        
        if not response.data:
            print(f"❌ Error: La eliminación no retornó datos")
            raise ValueError("No se pudo eliminar el evento")
            
        print(f"✅ Evento {event_id} eliminado correctamente")
        return response.data[0]
        
    except HTTPException as he:
        print(f"⚠️ HTTP Exception en remove_evento: {str(he)}")
        raise he
    except Exception as e:
        print(f"❌ Error inesperado en remove_evento: {str(e)}")
        print(f"❌ Tipo de error: {type(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado al eliminar el evento: {str(e)}")