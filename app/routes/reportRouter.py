from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, validator, Field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..services.utils import payload
from ..core.database import supabase

router = APIRouter(prefix="/report", tags=["report"])

class ReportRequest(BaseModel):
    start: str = Field(..., description="Fecha inicial en formato YYYY-MM-DD")
    end: str = Field(..., description="Fecha final en formato YYYY-MM-DD")

    @validator('start', 'end')
    def validate_date_format(cls, v):
        try:
            if not v or len(v.split('-')) != 3:
                raise ValueError("Formato de fecha inválido")
            
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD")

    @validator('end')
    def validate_date_range(cls, v, values):
        if 'start' in values:
            try:
                start_date = datetime.strptime(values['start'], "%Y-%m-%d")
                end_date = datetime.strptime(v, "%Y-%m-%d")
                if end_date < start_date:
                    raise ValueError("La fecha final no puede ser anterior a la fecha inicial")
                return v
            except ValueError as e:
                raise ValueError(str(e))
        return v

    class Config:
        schema_extra = {
            "example": {
                "start": "2025-02-11",
                "end": "2025-02-11"
            }
        }

@router.post("/get")
async def obtener_reporte(
    request: ReportRequest,
    user_data: Dict = Depends(payload)
) -> Dict[str, Any]:
    """
    Obtiene el reporte de tiempo trabajado en un rango de fechas para el usuario actual.

    Args:
        request: ReportRequest con fechas inicio y fin en formato YYYY-MM-DD
        user_data: Datos del usuario autenticado

    Returns:
        Dict con status, message, data (eventos) y summary (resumen por proyecto)
    """
    try:
        # Verificar que tenemos el ID del usuario
        if not user_data or 'id' not in user_data:
            raise HTTPException(status_code=401, detail="Usuario no autenticado")

        user_id = user_data['id']
        start_date = datetime.strptime(request.start, "%Y-%m-%d").date()
        end_date = datetime.strptime(request.end, "%Y-%m-%d").date()

        # Consulta filtrada por usuario y fechas
        response = supabase.table("eventos")\
            .select("id, descripcion, duracion, fecha_inicio, fecha_fin, project")\
            .eq("user_id", user_id)\
            .gte("fecha_inicio", start_date.isoformat())\
            .lte("fecha_inicio", end_date.isoformat())\
            .execute()

        if not response.data:
            return {
                "status": "success",
                "message": "No hay eventos en este rango de fechas",
                "data": [],
                "summary": []
            }

        # Calcular resumen por proyecto
        resumen_proyectos = {}
        for evento in response.data:
            project = evento.get("project")
            duracion = evento.get("duracion", 0)
            if project and isinstance(duracion, (int, float)):
                resumen_proyectos[project] = resumen_proyectos.get(project, 0) + duracion

        resumen_lista = [
            {"project": project, "total_seconds": total_seconds}
            for project, total_seconds in resumen_proyectos.items()
        ]

        return {
            "status": "success",
            "message": "Datos de reportes obtenidos correctamente",
            "data": response.data,
            "summary": resumen_lista
        }

    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    except Exception as e:
        print(f"❌ Error en obtener_reporte: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )