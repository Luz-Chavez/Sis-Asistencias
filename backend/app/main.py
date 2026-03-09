from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Cargar variables desde .env si existe (desarrollo)
try:
    from pathlib import Path
    from dotenv import load_dotenv

    # Intentar cargar .env desde ubicaciones comunes, sin depender del CWD
    # - repo root:   <repo>/.env
    # - backend dir: <repo>/backend/.env
    here = Path(__file__).resolve()
    repo_root = here.parents[2]
    backend_dir = here.parents[1]

    load_dotenv(dotenv_path=repo_root / '.env', override=False)
    load_dotenv(dotenv_path=backend_dir / '.env', override=False)
except Exception:
    pass



from app.api.v1 import rutas_usuarios, rutas_asistencias, rutas_reportes
from app.db.database import engine, Base, SessionLocal
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.models.notificacion_pasantia import NotificacionPasantia  # noqa: F401
from app.core.security import obtener_password_hash

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Control de Asistencia - Facultad de Ciencias Sociales",
    description="API con FastAPI, PostgreSQL y JWT para la gestión de pasantes.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(rutas_usuarios.router,   prefix="/api/v1/usuarios",    tags=["Usuarios y Autenticación"])
app.include_router(rutas_asistencias.router, prefix="/api/v1/asistencias", tags=["Control de Asistencia"])
app.include_router(rutas_reportes.router,   prefix="/api/v1/reportes",    tags=["Reportes Diarios"])


# ──────────────────────────────────────────────────────────────────────────────
# Al arrancar: garantizar que existan los 3 roles y un admin por defecto
# ──────────────────────────────────────────────────────────────────────────────
@app.on_event("startup")
def inicializar_datos():
    db: Session = SessionLocal()
    try:
        _crear_roles_si_no_existen(db)
        _crear_admin_por_defecto(db)
    finally:
        db.close()


def _crear_roles_si_no_existen(db: Session):
    """Inserta los 3 roles del sistema si todavía no están en la BD."""
    roles_requeridos = ["ADMINISTRADOR", "ENCARGADO", "PASANTE"]
    for nombre in roles_requeridos:
        if not db.query(Rol).filter(Rol.nombre == nombre).first():
            db.add(Rol(nombre=nombre))
    db.commit()


def _crear_admin_por_defecto(db: Session):
    """
    Crea un ADMINISTRADOR inicial solo si no existe ninguno en la BD.
    Credenciales por defecto (¡cámbialas en producción!):
        email    : admin@facultad.edu.bo
        password : Admin1234
        username : aa00000000  (generado de 'Admin' + 'Admin' + '00000000')
    """
    rol_admin = db.query(Rol).filter(Rol.nombre == "ADMINISTRADOR").first()
    if not rol_admin:
        return  # No debería pasar tras _crear_roles_si_no_existen

    ya_existe_admin = (
        db.query(Usuario)
        .filter(Usuario.rol_id == rol_admin.id)
        .first()
    )
    if ya_existe_admin:
        return  # Ya hay al menos un admin, no hacemos nada

    admin = Usuario(
        nombres         = "Admin",
        apellidos       = "Sistema",
        carnet_identidad= "00000000",
        username        = "as00000000",   # a(Admin) + s(Sistema) + 00000000
        email           = "admin@facultad.edu.bo",
        password_hash   = obtener_password_hash("Admin1234"),
        rol_id          = rol_admin.id,
        carrera_id      = None,
        estado          = True,
    )
    db.add(admin)
    db.commit()
    print("=" * 55)
    print("  ✅ Admin por defecto creado:")
    print("     Email    : admin@facultad.edu.bo")
    print("     Password : Admin1234")
    print("     ⚠️  ¡Cámbiala en producción!")
    print("=" * 55)


@app.get("/", tags=["Inicio"])
def read_root():
    return {
        "estado": "Online",
        "mensaje": "Bienvenido al Sistema de Control de Asistencia. Visita /docs para la documentación."
    }
