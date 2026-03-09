from sqlalchemy.orm import Session
from app.models.asistencia import Reporte, Asistencia
from app.models.usuario import Usuario
from app.schemas.reporte_schema import ReporteCreate, ReporteEvaluar

def crear_reporte(db: Session, reporte: ReporteCreate):
    db_reporte = Reporte(
        asistencia_id=reporte.asistencia_id,
        actividades_realizadas=reporte.actividades_realizadas,
        archivo_adjunto_url=reporte.archivo_adjunto_url
    )
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte

# def obtener_reportes(db: Session, carrera_id: int = None):
#     query = db.query(Reporte)
#     if carrera_id:
#         query = query.join(Asistencia).join(Usuario).filter(Usuario.carrera_id == carrera_id)
#     return query.all()

# def evaluar_reporte(db: Session, reporte_id: int, evaluacion: ReporteEvaluar, revisado_por_id: int):
#     db_reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
#     if db_reporte:
#         db_reporte.estado = evaluacion.estado
#         db_reporte.comentarios_director = evaluacion.comentarios_director
#         db_reporte.revisado_por = revisado_por_id
#         db.commit()
#         db.refresh(db_reporte)
#     return db_reporte


# MODIFICADO ------------
def obtener_reportes(db: Session, carrera_id: int = None):
    query = (
        db.query(Reporte)
        .join(Asistencia, Reporte.asistencia_id == Asistencia.id)
        .join(Usuario,    Asistencia.pasante_id  == Usuario.id)
    )

    if carrera_id is not None:
        query = query.filter(Usuario.carrera_id == carrera_id)

    return query.order_by(Reporte.creado_en.desc()).all()


# MODIFICADO --------------
def evaluar_reporte(db: Session, reporte_id: int, estado: str, comentarios: str = None, revisado_por: int = None):
    db_reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if db_reporte:
        db_reporte.estado               = estado
        db_reporte.comentarios_director = comentarios
        db_reporte.revisado_por         = revisado_por
        db.commit()
        db.refresh(db_reporte)
    return db_reporte