from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import rutas_usuarios, rutas_asistencias
from app.db.database import engine, Base
from app.api.v1 import rutas_usuarios, rutas_asistencias, rutas_reportes

from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Control de Asistencia - Facultad de Ciencias Sociales",
    description="API robusta con FastAPI, PostgreSQL y JWT para la gestión de pasantes, directores y decanatura.",
    version="1.0.0"
)

origenes_permitidos = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(rutas_usuarios.router, prefix="/api/v1/usuarios", tags=["Usuarios y Autenticación"])
app.include_router(rutas_asistencias.router, prefix="/api/v1/asistencias", tags=["Control de Asistencia"])
app.include_router(rutas_reportes.router, prefix="/api/v1/reportes", tags=["Reportes Diarios"]) # <-- LÍNEA NUEVA

@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "estado": "Online",
        "mensaje": "Bienvenido a la API del Sistema de Control de Asistencia. Visita /docs para la documentación interactiva."
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)