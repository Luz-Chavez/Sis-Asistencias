from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ReporteCreate(BaseModel):
    asistencia_id: int
    actividades_realizadas: str
    archivo_adjunto_url: Optional[str] = None 
    
class ReporteEvaluar(BaseModel):
    estado: str
    comentarios_director: str

    @validator("comentarios_director")
    def validar_comentario_obligatorio(cls, v):
        if v is None:
            raise ValueError("comentarios_director es obligatorio")
        if not str(v).strip():
            raise ValueError("comentarios_director es obligatorio")
        return str(v).strip()

class ReporteResponse(BaseModel):
    id: int
    asistencia_id: int
    actividades_realizadas: str
    estado: str
    comentarios_director: Optional[str] = None
    creado_en: datetime
    verificado_por: Optional[int] = None
    verificado_en: Optional[datetime] = None
    aprobado_por: Optional[int] = None
    aprobado_en: Optional[datetime] = None

    nombre_pasante: Optional[str] = None

    class Config:
        from_attributes = True


class ReporteHistorialItem(BaseModel):
    id: int
    reporte_id: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    comentarios: str
    actor_id: int
    actor_nombre: Optional[str] = None
    creado_en: datetime
