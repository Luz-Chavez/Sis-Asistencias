from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.asistencia import Asistencia
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaUpdate


def crear_entrada(db: Session, asistencia_data: AsistenciaCreate):
    hoy = datetime.now(timezone.utc).date()
    if db.query(Asistencia).filter(
        Asistencia.pasante_id == asistencia_data.pasante_id,
        Asistencia.fecha == hoy
    ).first():
        return None

    nueva = Asistencia(
        pasante_id       = asistencia_data.pasante_id,
        fecha            = hoy,
        hora_entrada     = datetime.now(timezone.utc),
        latitud_entrada  = asistencia_data.latitud_entrada,
        longitud_entrada = asistencia_data.longitud_entrada,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def crear_entrada_por_pasante_id(db: Session, pasante_id: int):
    """Para fichaje pÃºblico sin GPS."""
    hoy = datetime.now(timezone.utc).date()
    if db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first():
        return None

    nueva = Asistencia(
        pasante_id       = pasante_id,
        fecha            = hoy,
        hora_entrada     = datetime.now(timezone.utc),
        latitud_entrada  = None,
        longitud_entrada = None,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def registrar_salida(db: Session, asistencia_id: int, datos_salida: AsistenciaUpdate):
    registro = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()
    if not registro or registro.hora_salida is not None:
        return None

    hora_actual = datetime.now(timezone.utc)
    registro.hora_salida     = hora_actual
    registro.latitud_salida  = datos_salida.latitud_salida
    registro.longitud_salida = datos_salida.longitud_salida
    horas = round((hora_actual - registro.hora_entrada).total_seconds() / 3600, 2)
    registro.horas_trabajadas = horas if horas > 0 else 0.01
    db.commit()
    db.refresh(registro)
    return registro


def registrar_salida_por_pasante_id(db: Session, pasante_id: int):
    """Para fichaje pÃºblico sin GPS. Retorna (registro, estado)."""
    hoy = datetime.now(timezone.utc).date()
    registro = db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first()

    if not registro:
        return None, "no_entrada"
    if registro.hora_salida is not None:
        return None, "ya_salio"

    hora_actual = datetime.now(timezone.utc)
    registro.hora_salida      = hora_actual
    registro.latitud_salida   = None
    registro.longitud_salida  = None
    horas = round((hora_actual - registro.hora_entrada).total_seconds() / 3600, 2)
    registro.horas_trabajadas = horas if horas > 0 else 0.01
    db.commit()
    db.refresh(registro)
    return registro, "ok"


def obtener_asistencia_hoy(db: Session, pasante_id: int):
    hoy = datetime.now(timezone.utc).date()
    return db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante_id,
        Asistencia.fecha == hoy
    ).first()


def obtener_asistencias_por_pasante(db: Session, pasante_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Asistencia)
        .filter(Asistencia.pasante_id == pasante_id)
        .order_by(Asistencia.fecha.desc())
        .offset(skip).limit(limit).all()
    )


def obtener_todas_asistencias(db: Session, carrera_id: int = None):
    query = db.query(Asistencia)
    if carrera_id:
        from app.models.usuario import Usuario
        query = query.join(Usuario).filter(Usuario.carrera_id == carrera_id)
    return query.order_by(Asistencia.fecha.desc()).all()
