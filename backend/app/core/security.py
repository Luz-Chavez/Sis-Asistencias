<<<<<<< HEAD
﻿import os
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "una_clave_super_secreta_y_larga_para_la_facultad")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))


def verificar_password(plain_password: str, hashed_password: str) -> bool:
    # Convertimos las contraseñas a bytes, que es el formato que exige bcrypt
    password_bytes = plain_password.encode('utf-8')
    
    if isinstance(hashed_password, str):
        hash_bytes = hashed_password.encode('utf-8')
    else:
        hash_bytes = hashed_password
        
    try:
        return bcrypt.checkpw(password_bytes, hash_bytes)
    except ValueError:
        # Esto atrapa el error si el hash guardado tiene un formato inválido
        return False


def obtener_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    # Lo devolvemos como string para guardarlo en la base de datos sin problemas
    return hashed_password.decode('utf-8')


def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

=======
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "una_clave_super_secreta_y_larga_para_la_facultad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def obtener_password_hash(password):
    return pwd_context.hash(password)

def crear_token_acceso(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
>>>>>>> 01ae768219e574b7569fd6ef9d0968c847a4bb32
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt