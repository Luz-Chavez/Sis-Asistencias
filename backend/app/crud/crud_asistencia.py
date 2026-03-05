from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.asistencia import Asistencia
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaUpdate

def crear_entrada(db: Session, asistencia_data: AsistenciaCreate):
    # 1. Verificar si el pasante ya marcó entrada hoy
    hoy = datetime.now(timezone.utc).date()
    registro_existente = db.query(Asistencia).filter(
        Asistencia.pasante_id == asistencia_data.pasante_id,
        Asistencia.fecha == hoy
    ).first()

    if registro_existente:
        return None # Ya existe un registro para hoy

    # 2. Crear el nuevo registro
    nueva_asistencia = Asistencia(
        pasante_id=asistencia_data.pasante_id,
        fecha=hoy,
        hora_entrada=datetime.now(timezone.utc),
        latitud_entrada=asistencia_data.latitud_entrada,
        longitud_entrada=asistencia_data.longitud_entrada
    )
    
    db.add(nueva_asistencia)
    db.commit()
    db.refresh(nueva_asistencia)
    return nueva_asistencia

def registrar_salida(db: Session, asistencia_id: int, datos_salida: AsistenciaUpdate):
    registro = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()
    
    if not registro or registro.hora_salida is not None:
        return None # No existe o ya marcó salida

    hora_actual = datetime.now(timezone.utc)
    registro.hora_salida = hora_actual
    registro.latitud_salida = datos_salida.latitud_salida
    registro.longitud_salida = datos_salida.longitud_salida

    # Calcular horas trabajadas
    diferencia = hora_actual - registro.hora_entrada
    registro.horas_trabajadas = round(diferencia.total_seconds() / 3600, 2)

    db.commit()
    db.refresh(registro)
    return registro

def obtener_asistencias_por_pasante(db: Session, pasante_id: int, skip: int = 0, limit: int = 100):
    return db.query(Asistencia).filter(Asistencia.pasante_id == pasante_id).order_by(Asistencia.fecha.desc()).offset(skip).limit(limit).all()

def obtener_todas_asistencias(db: Session, carrera_id: int = None):
    query = db.query(Asistencia)
    if carrera_id:
        from app.models.usuario import Usuario
        query = query.join(Usuario).filter(Usuario.carrera_id == carrera_id)
    return query.order_by(Asistencia.fecha.desc()).all()