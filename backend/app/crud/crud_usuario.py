from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate
from app.core.security import obtener_password_hash
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate 

def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def crear_usuario(db: Session, usuario: UsuarioCreate):
    password_encriptada = obtener_password_hash(usuario.password)
    
    db_usuario = Usuario(
        nombres=usuario.nombres,
        apellidos=usuario.apellidos,
        carnet_identidad=usuario.carnet_identidad,
        email=usuario.email,
        password_hash=password_encriptada,
        rol_id=usuario.rol_id,
        carrera_id=usuario.carrera_id
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100, carrera_id: int = None):
    query = db.query(Usuario)
    if carrera_id:
        query = query.filter(Usuario.carrera_id == carrera_id)
    return query.offset(skip).limit(limit).all()

def desactivar_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.estado = False 
        db.commit()
    return usuario

def actualizar_usuario(db: Session, usuario_id: int, datos_actualizar: UsuarioUpdate):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        return None 

    update_data = datos_actualizar.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario