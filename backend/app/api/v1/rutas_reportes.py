from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.reporte_schema import ReporteCreate, ReporteResponse, ReporteEvaluar
from app.crud import crud_reporte
from app.models.usuario import Usuario

from app.api.dependencias import obtener_usuario_actual, rol_requerido

from fastapi.responses import StreamingResponse # Para enviar el PDF
from app.utils.generador_pdf import generar_comprobante_pdf
from app.models.asistencia import Reporte

router = APIRouter()

@router.post("/subir", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
def subir_reporte(
    reporte: ReporteCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"])) 
):
    reporte_existente = db.query(Reporte).filter(Reporte.asistencia_id == reporte.asistencia_id).first()
    
    if reporte_existente:
        reporte_existente.actividades_realizadas = reporte.actividades_realizadas
        db.commit()
        db.refresh(reporte_existente)
        return reporte_existente
        
    else:
        nuevo_reporte = crud_reporte.crear_reporte(db=db, reporte=reporte)
        return nuevo_reporte


@router.get("/listar")
def listar_reportes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["DECANO", "COORDINADOR", "DIRECTOR"]))
):
    # LA REGLA DE ORO: 
    # Si es Director, filtramos por su carrera. Si es Decano/Coord, carrera_id = None (ven todo)
    es_director = False
    if hasattr(usuario_actual, 'rol') and usuario_actual.rol and hasattr(usuario_actual.rol, 'nombre'):
        es_director = (usuario_actual.rol.nombre == "DIRECTOR")
    elif isinstance(getattr(usuario_actual, 'rol', None), str):
        es_director = (usuario_actual.rol == "DIRECTOR")
        
    filtro_carrera = usuario_actual.carrera_id if es_director else None
    
    # El CRUD debe estar preparado para que si filtro_carrera es None, devuelva todos los reportes
    reportes_db = crud_reporte.obtener_reportes(db=db, carrera_id=filtro_carrera)
    
    reportes_con_nombres = []
    for rep in reportes_db:
        rep_dict = rep.__dict__.copy()
        if rep.asistencia and rep.asistencia.pasante:
            nombres = rep.asistencia.pasante.nombres
            apellidos = rep.asistencia.pasante.apellidos
            rep_dict["nombre_pasante"] = f"{nombres} {apellidos}"
        else:
            rep_dict["nombre_pasante"] = "Pasante sin registro"
            
        reportes_con_nombres.append(rep_dict)

    return reportes_con_nombres

@router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
def evaluar_reporte(
    reporte_id: int, 
    evaluacion: ReporteEvaluar, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["DIRECTOR"]))
):
    reporte_actualizado = crud_reporte.evaluar_reporte(
        db=db, 
        reporte_id=reporte_id, 
        evaluacion=evaluacion, 
        revisado_por_id=usuario_actual.id
    )
    
    if not reporte_actualizado:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
    return reporte_actualizado

@router.get("/descargar/{reporte_id}")
def descargar_reporte_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE", "DECANO", "COORDINADOR", "DIRECTOR"]))
):
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")

    asistencia = reporte.asistencia
    pasante = asistencia.pasante
    carrera = pasante.carrera

    datos_pdf = {
        "pasante_nombre": f"{pasante.nombres} {pasante.apellidos}",
        "carrera_nombre": carrera.nombre if carrera else "No asignada",
        "fecha": asistencia.fecha.strftime("%d/%m/%Y"),
        "hora_entrada": asistencia.hora_entrada.strftime("%H:%M") if asistencia.hora_entrada else "",
        "hora_salida": asistencia.hora_salida.strftime("%H:%M") if asistencia.hora_salida else "Pendiente",
        "horas_trabajadas": asistencia.horas_trabajadas or 0,
        "actividades": reporte.actividades_realizadas
    }

    pdf_buffer = generar_comprobante_pdf(datos_reporte=datos_pdf)

    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    mes_abreviado = meses[asistencia.fecha.month - 1]
    fecha_formateada = f"{asistencia.fecha.day:02d}{mes_abreviado}" # Resultado: "05Mar"
    
    nombres_juntos = pasante.nombres.replace(" ", "")
    apellidos_juntos = pasante.apellidos.replace(" ", "")
    
    nombre_archivo = f"ReporteDiario_{nombres_juntos}{apellidos_juntos}_{fecha_formateada}.pdf"
    
    return StreamingResponse(
        pdf_buffer, 
        media_type="application/pdf", 
        headers={'Content-Disposition': f'attachment; filename="{nombre_archivo}"'}
    )

@router.get("/ver/{asistencia_id}")
def ver_reporte_asistencia(
    asistencia_id: int, 
    db: Session = Depends(get_db),
    # Solo el pasante necesita leer su reporte aquí
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    # Buscamos si ya existe un reporte para esta asistencia
    reporte = db.query(Reporte).filter(Reporte.asistencia_id == asistencia_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="No hay reporte aún.")
    
    return reporte