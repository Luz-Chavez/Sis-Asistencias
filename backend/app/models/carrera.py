<<<<<<< HEAD
﻿from sqlalchemy import Column, Integer, String, Boolean, Text, text
=======
from sqlalchemy import Column, Integer, String, Boolean, Text
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
from app.db.database import Base

class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
<<<<<<< HEAD
    logo_url = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, server_default=text('true'), default=True)
=======
    estado = Column(Boolean, default=True)
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
    nombre = Column(String(50), unique=True, nullable=False)
=======
    nombre = Column(String(50), unique=True, nullable=False)
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
