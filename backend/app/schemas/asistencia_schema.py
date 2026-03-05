from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AsistenciaCreate(BaseModel):
    pasante_id: int
    latitud_entrada: float = Field(..., description="Latitud GPS desde el navegador")
    longitud_entrada: float = Field(..., description="Longitud GPS desde el navegador")

class AsistenciaUpdate(BaseModel):
    latitud_salida: float
    longitud_salida: float

class AsistenciaResponse(BaseModel):
    id: int
    pasante_id: int
    fecha: datetime
    hora_entrada: datetime
    hora_salida: Optional[datetime] = None
    horas_trabajadas: Optional[float] = None

    esta_en_facultad: Optional[bool] = None 
    mensaje_alerta: Optional[str] = None

    class Config:
        from_attributes = True 