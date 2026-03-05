from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    carnet_identidad: str
    email: EmailStr
    password: str
    rol_id: int
    carrera_id: Optional[int] = None 

class UsuarioResponse(BaseModel):
    id: int
    nombres: str
    apellidos: str
    email: EmailStr
    rol_id: int
    carrera_id: Optional[int]
    estado: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    carnet_identidad: Optional[str] = None
    email: Optional[EmailStr] = None
    carrera_id: Optional[int] = None
    estado: Optional[bool] = None