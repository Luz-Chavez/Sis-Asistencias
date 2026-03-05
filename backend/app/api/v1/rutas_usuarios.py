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

router = APIRouter()

@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = crud_usuario.obtener_usuario_por_email(db, email=usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return crud_usuario.crear_usuario(db=db, usuario=usuario)

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
    carrera_id = usuario_actual.carrera_id if usuario_actual.rol.nombre == "DIRECTOR" else None
    
    usuarios = crud_usuario.obtener_usuarios(db=db, skip=skip, limit=limit, carrera_id=carrera_id)
    return usuarios

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