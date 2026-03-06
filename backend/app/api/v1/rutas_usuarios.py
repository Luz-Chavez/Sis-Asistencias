from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List # <-- NUEVO
from app.db.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, Token, UsuarioUpdate
from app.crud import crud_usuario
from app.core.security import verificar_password, crear_token_acceso

from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.models.usuario import Usuario
from app.models.carrera import Rol

router = APIRouter()

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = crud_usuario.obtener_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # 1. Creamos el usuario en la base de datos
    nuevo_usuario = crud_usuario.crear_usuario(db=db, usuario=usuario)
    
    # 2. Copiamos los datos a un diccionario
    usuario_datos = {
        "id": nuevo_usuario.id,
        "nombres": nuevo_usuario.nombres,
        "apellidos": nuevo_usuario.apellidos,
        "email": nuevo_usuario.email,
        "rol_id": nuevo_usuario.rol_id,
        "carrera_id": nuevo_usuario.carrera_id,
        "estado": nuevo_usuario.estado
    }
    
    # 3. Extraemos el nombre del rol en texto
    if nuevo_usuario.rol:
        usuario_datos["rol"] = nuevo_usuario.rol.nombre
    else:
        # Por si la base de datos demora en cargar la relación
        rol_db = db.query(Rol).filter(Rol.id == nuevo_usuario.rol_id).first()
        usuario_datos["rol"] = rol_db.nombre if rol_db else None

    # 4. Devolvemos los datos ya masticados para el frontend
    return usuario_datos

@router.post(
    "/login", 
    response_model=Token,
    summary="Iniciar Sesión",
    description="Genera un Token JWT. **Nota:** Ingresa tu correo electrónico en el campo `username` y tu contraseña en `password`. Los demás campos déjalos en blanco."
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_usuario.obtener_usuario_por_email(db, email=form_data.username)
    
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = crear_token_acceso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/listar", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["DECANO", "COORDINADOR", "DIRECTOR"]))
):
    # 1. Filtro estricto: El Director solo ve pasantes de su misma carrera
    es_director = False
    if hasattr(usuario_actual, 'rol') and usuario_actual.rol and hasattr(usuario_actual.rol, 'nombre'):
        es_director = (usuario_actual.rol.nombre == "DIRECTOR")
    elif isinstance(getattr(usuario_actual, 'rol', None), str):
        es_director = (usuario_actual.rol == "DIRECTOR")
        
    carrera_id = usuario_actual.carrera_id if es_director else None
    
    # 2. Consultamos la base de datos
    usuarios_db = crud_usuario.obtener_usuarios(db=db, skip=skip, limit=limit, carrera_id=carrera_id)
    
    # 3. Formateamos los datos para evitar el Error 500 de Pydantic (Extraemos el texto del Rol)
    usuarios_listos = []
    for user in usuarios_db:
        user_dict = {
            "id": user.id,
            "nombres": user.nombres,
            "apellidos": user.apellidos,
            "email": user.email,
            "rol_id": user.rol_id,
            "carrera_id": user.carrera_id,
            "estado": user.estado
        }
        
        # Mapeo del rol
        if hasattr(user, 'rol') and user.rol and hasattr(user.rol, 'nombre'):
            user_dict["rol"] = user.rol.nombre
        else:
            user_dict["rol"] = "Desconocido"
            
        usuarios_listos.append(user_dict)
        
    return usuarios_listos

@router.put("/editar/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int, 
    datos: UsuarioUpdate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["DECANO", "COORDINADOR"]))
):
    usuario_actualizado = crud_usuario.actualizar_usuario(db=db, usuario_id=usuario_id, datos_actualizar=datos)
    
    if not usuario_actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return usuario_actualizado

@router.delete("/desactivar/{usuario_id}", response_model=UsuarioResponse)
def desactivar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["DECANO", "COORDINADOR"]))
):
    usuario_borrado = crud_usuario.desactivar_usuario(db=db, usuario_id=usuario_id)
    
    if not usuario_borrado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return usuario_borrado

@router.get("/me", response_model=UsuarioResponse)
def leer_usuario_actual(
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Retorna la información del usuario autenticado actualmente,
    convirtiendo su relación de Rol a un texto simple para el frontend.
    """
    # 1. Copiamos los datos del usuario a un diccionario
    usuario_datos = {
        "id": usuario_actual.id,
        "nombres": usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "email": usuario_actual.email,
        "rol_id": usuario_actual.rol_id,
        "carrera_id": usuario_actual.carrera_id,
        "estado": usuario_actual.estado
    }
    
    # 2. Extraemos mágicamente la palabra del rol (Ej. "DIRECTOR")
    if usuario_actual.rol:
        usuario_datos["rol"] = usuario_actual.rol.nombre
    else:
        usuario_datos["rol"] = None
        
    # 3. Retornamos el diccionario listo y masticado para Vue
    return usuario_datos