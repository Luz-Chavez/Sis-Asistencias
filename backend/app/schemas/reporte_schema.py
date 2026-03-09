from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReporteCreate(BaseModel):
    asistencia_id: int
    actividades_realizadas: str
    archivo_adjunto_url: Optional[str] = None 
    
class ReporteEvaluar(BaseModel):
    estado: str 
    comentarios_director: Optional[str] = None

class ReporteResponse(BaseModel):
    id: int
    asistencia_id: int
    actividades_realizadas: str
    estado: str
    comentarios_director: Optional[str] = None
    creado_en: datetime
    nombre_pasante: Optional[str] = None
    horas_trabajadas: Optional[float] = None  # <-- ¡Agrega esta línea!

    class Config:
        from_attributes = True