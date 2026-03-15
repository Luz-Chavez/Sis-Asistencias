<<<<<<< HEAD
from pydantic import BaseModel, field_validator
from typing import Optional, List
=======
from pydantic import BaseModel
from typing import Optional
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
from datetime import datetime

class ReporteCreate(BaseModel):
    asistencia_id: int
    actividades_realizadas: str
    archivo_adjunto_url: Optional[str] = None 
    
class ReporteEvaluar(BaseModel):
<<<<<<< HEAD
    estado: str
    comentarios_director: str
    es_rectificacion: Optional[bool] = False  # Para saber si es una rectificación

    @field_validator("comentarios_director")
    @classmethod
    def validar_comentario_obligatorio(cls, v):
        if not v or not str(v).strip():
            raise ValueError("El comentario es obligatorio para evaluar el reporte.")
        return str(v).strip()
=======
    estado: str 
    comentarios_director: Optional[str] = None
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32

class ReporteResponse(BaseModel):
    id: int
    asistencia_id: int
    actividades_realizadas: str
<<<<<<< HEAD
    estado_encargado: Optional[str] = None
    estado_admin: Optional[str] = None
    comentarios_director: Optional[str] = None
    creado_en: datetime
    verificado_por: Optional[int] = None
    verificado_en: Optional[datetime] = None
    aprobado_por: Optional[int] = None
    aprobado_en: Optional[datetime] = None
=======
    estado: str
    comentarios_director: Optional[str] = None
    creado_en: datetime
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32

    nombre_pasante: Optional[str] = None

    class Config:
<<<<<<< HEAD
        from_attributes = True


class ReporteHistorialItem(BaseModel):
    id: int
    reporte_id: int
    estado_anterior: Optional[str] = None
    estado_nuevo: str
    comentarios: str
    actor_id: int
    # Añadimos esto para que el frontend sepa quién hizo el cambio
    actor_nombre: Optional[str] = None 
    creado_en: datetime

    class Config:
        from_attributes = True
=======
        from_attributes = True
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
