from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

from app.models.carrera import Rol, Carrera


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    carnet_identidad = Column(String(20), unique=True, index=True, nullable=False)
    # ✅ NUEVO: username generado automáticamente (1ra inicial nombre + 1ra inicial apellido + CI)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=True)
    estado = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    rol = relationship("Rol")
    carrera = relationship("Carrera")
    asistencias = relationship("Asistencia", back_populates="pasante")