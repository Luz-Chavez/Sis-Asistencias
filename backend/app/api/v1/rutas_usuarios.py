from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, Token, UsuarioUpdate
from app.crud import crud_usuario
from app.core.security import verificar_password, crear_token_acceso
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.models.usuario import Usuario
from app.models.carrera import Rol

router = APIRouter()


def _usuario_a_dict(user: Usuario, db: Session = None) -> dict:
    nombre_rol = None
    if hasattr(user, "rol") and user.rol and hasattr(user.rol, "nombre"):
        nombre_rol = user.rol.nombre
    elif db and user.rol_id:
        rol_db = db.query(Rol).filter(Rol.id == user.rol_id).first()
        nombre_rol = rol_db.nombre if rol_db else None
    return {
        "id":         user.id,
        "nombres":    user.nombres,
        "apellidos":  user.apellidos,
        "username":   user.username,
        "email":      user.email,
        "rol_id":     user.rol_id,
        "carrera_id": user.carrera_id,
        "estado":     user.estado,
        "rol":        nombre_rol,
    }


# ──────────────────────────────────────────────────────────────────────────────
# POST /registro
# ADMINISTRADOR → ENCARGADO o PASANTE (cualquier carrera)
# ENCARGADO     → solo PASANTE de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")
    rol_nuevo = db.query(Rol).filter(Rol.id == usuario.rol_id).first()
    if not rol_nuevo:
        raise HTTPException(status_code=400, detail="El rol_id indicado no existe.")

    if nombre_rol_actual == "ENCARGADO":
        if rol_nuevo.nombre != "PASANTE":
            raise HTTPException(403, detail="Un Encargado solo puede registrar Pasantes.")
        if usuario.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail=f"Solo puedes registrar pasantes en tu carrera (ID: {usuario_actual.carrera_id}).")

    if crud_usuario.obtener_usuario_por_email(db, email=usuario.email):
        raise HTTPException(400, detail="El email ya está registrado.")

    username_candidato = crud_usuario.generar_username(usuario.nombres, usuario.apellidos, usuario.carnet_identidad)
    if crud_usuario.obtener_usuario_por_username(db, username=username_candidato):
        raise HTTPException(400, detail=f"El username '{username_candidato}' ya existe. Verifica el carnet de identidad.")

    nuevo_usuario = crud_usuario.crear_usuario(db=db, usuario=usuario)
    return _usuario_a_dict(nuevo_usuario, db)


# ──────────────────────────────────────────────────────────────────────────────
# POST /login
# ──────────────────────────────────────────────────────────────────────────────
@router.post("/login", response_model=Token, summary="Iniciar Sesión")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = crud_usuario.obtener_usuario_por_email(db, email=form_data.username)
    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos",
                            headers={"WWW-Authenticate": "Bearer"})
    if not usuario.estado:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Tu cuenta está desactivada.")

    return {"access_token": crear_token_acceso(data={"sub": usuario.email}), "token_type": "bearer"}


# ──────────────────────────────────────────────────────────────────────────────
# GET /listar
# ADMINISTRADOR → todos | ENCARGADO → PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/listar", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    es_encargado = getattr(usuario_actual.rol, "nombre", "") == "ENCARGADO"
    carrera_id   = usuario_actual.carrera_id if es_encargado else None
    usuarios_db  = crud_usuario.obtener_usuarios(db=db, skip=skip, limit=limit, carrera_id=carrera_id)
    return [_usuario_a_dict(u) for u in usuarios_db]


# ──────────────────────────────────────────────────────────────────────────────
# PUT /editar/{usuario_id}
# ADMINISTRADOR → edita cualquier usuario
# ENCARGADO     → solo puede editar PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.put("/editar/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")

    # Verificar que el ENCARGADO solo edite pasantes de su carrera
    if nombre_rol_actual == "ENCARGADO":
        objetivo = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Usuario no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes editar pasantes de tu carrera.")

    usuario_actualizado = crud_usuario.actualizar_usuario(db=db, usuario_id=usuario_id, datos_actualizar=datos)
    if not usuario_actualizado:
        raise HTTPException(404, detail="Usuario no encontrado.")
    return _usuario_a_dict(usuario_actualizado, db)


# ──────────────────────────────────────────────────────────────────────────────
# DELETE /desactivar/{usuario_id}
# ADMINISTRADOR → desactiva cualquier usuario
# ENCARGADO     → solo puede desactivar PASANTES de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.delete("/desactivar/{usuario_id}", response_model=UsuarioResponse)
def desactivar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol_actual = getattr(usuario_actual.rol, "nombre", "")

    if nombre_rol_actual == "ENCARGADO":
        objetivo = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Usuario no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes desactivar pasantes de tu carrera.")

    usuario_borrado = crud_usuario.desactivar_usuario(db=db, usuario_id=usuario_id)
    if not usuario_borrado:
        raise HTTPException(404, detail="Usuario no encontrado.")
    return _usuario_a_dict(usuario_borrado, db)


# ──────────────────────────────────────────────────────────────────────────────
# GET /me
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/me", response_model=UsuarioResponse)
def leer_usuario_actual(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return _usuario_a_dict(usuario_actual)