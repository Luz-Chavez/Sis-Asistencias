from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.database import Base

class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Boolean, default=True)

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)