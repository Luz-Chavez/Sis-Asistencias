from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

<<<<<<< HEAD

class AsistenciaCreate(BaseModel):
    pasante_id: int
    latitud_entrada:  Optional[float] = Field(None)
    longitud_entrada: Optional[float] = Field(None)


class FichajePublicoEntrada(BaseModel):
    username: str


class FichajePublicoSalida(BaseModel):
    username: str


class AsistenciaUpdate(BaseModel):
    latitud_salida:  Optional[float] = None
    longitud_salida: Optional[float] = None


class AsistenciaResponse(BaseModel):
    id:               int
    pasante_id:       int
    fecha:            datetime
    hora_entrada:     datetime
    hora_salida:      Optional[datetime] = None
    horas_trabajadas: Optional[float]    = None
    esta_en_facultad: Optional[bool]     = None
    mensaje_alerta:   Optional[str]      = None

    class Config:
        from_attributes = True
=======
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
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
