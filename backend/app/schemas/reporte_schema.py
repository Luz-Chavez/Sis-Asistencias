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

    class Config:
        from_attributes = True