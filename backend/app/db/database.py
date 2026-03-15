<<<<<<< HEAD
import os

=======
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
# Permite configurar por .env/variables de entorno.
# Ejemplo:
#   DATABASE_URL=postgresql://postgres:postgre@localhost/asistencia
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:123456@localhost/sis",
)

engine_kwargs = {
    "pool_pre_ping": True,
}

# Evita que la app se quede colgada mucho tiempo si la BD no responde.
if SQLALCHEMY_DATABASE_URL.startswith("postgresql"):
    engine_kwargs["connect_args"] = {"connect_timeout": 5}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
=======
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/asistencia"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

<<<<<<< HEAD

=======
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
<<<<<<< HEAD
        db.close()
=======
        db.close()
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
