from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Asistencia Pasantes"
<<<<<<< HEAD
    DATABASE_URL: str = "postgresql://postgres:123456@localhost/sis"
=======
    DATABASE_URL: str = "postgresql://postgres:tu_password@localhost/asistencia_facultad"
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
    SECRET_KEY: str = "super_secreta_clave_para_jwt_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480 

    class Config:
        env_file = ".env"

settings = Settings()