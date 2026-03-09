from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.reporte_schema import ReporteCreate, ReporteResponse, ReporteEvaluar
from app.crud import crud_reporte
from app.models.usuario import Usuario
from app.models.asistencia import Reporte
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.utils.generador_pdf import generar_comprobante_pdf

router = APIRouter()


# ──────────────────────────────────────────────────────────────────────────────
# POST /subir  —  solo el PASANTE puede subir o actualizar su reporte
# ──────────────────────────────────────────────────────────────────────────────
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
        return crud_reporte.crear_reporte(db=db, reporte=reporte)


# ──────────────────────────────────────────────────────────────────────────────
# GET /listar
# ADMINISTRADOR → ve todos los reportes
# ENCARGADO     → ve solo los reportes de pasantes de su carrera
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/listar")
def listar_reportes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol = getattr(usuario_actual.rol, "nombre", "")
    es_encargado = (nombre_rol == "ENCARGADO")

    # El ENCARGADO filtra por su carrera; el ADMINISTRADOR ve todo
    filtro_carrera = usuario_actual.carrera_id if es_encargado else None

    reportes_db = crud_reporte.obtener_reportes(db=db, carrera_id=filtro_carrera)

    reportes_con_nombres = []
    for rep in reportes_db:
        rep_dict = rep.__dict__.copy()
        
        # Validar si existe la asistencia asociada para extraer datos
        if rep.asistencia:
            if rep.asistencia.pasante:
                p = rep.asistencia.pasante
                rep_dict["nombre_pasante"] = f"{p.nombres} {p.apellidos}"
            else:
                rep_dict["nombre_pasante"] = "Pasante sin registro"
            
            # Extraer y asignar las horas trabajadas al diccionario de respuesta
            rep_dict["horas_trabajadas"] = rep.asistencia.horas_trabajadas
        else:
            rep_dict["nombre_pasante"] = "Pasante sin registro"
            rep_dict["horas_trabajadas"] = None
            
        reportes_con_nombres.append(rep_dict)

    return reportes_con_nombres


# ──────────────────────────────────────────────────────────────────────────────
# PUT /evaluar/{reporte_id}  —  ADMINISTRADOR y ENCARGADO evalúan reportes
# ──────────────────────────────────────────────────────────────────────────────
@router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
def evaluar_reporte(
    reporte_id: int,
    evaluacion: ReporteEvaluar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
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


# ──────────────────────────────────────────────────────────────────────────────
# GET /descargar/{reporte_id}  —  descarga el comprobante PDF
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/descargar/{reporte_id}")
def descargar_reporte_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        rol_requerido(["PASANTE", "ADMINISTRADOR", "ENCARGADO"])
    )
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
        "actividades": reporte.actividades_realizadas,
    }

    pdf_buffer = generar_comprobante_pdf(datos_reporte=datos_pdf)

    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    mes_abreviado = meses[asistencia.fecha.month - 1]
    fecha_formateada = f"{asistencia.fecha.day:02d}{mes_abreviado}"

    nombres_juntos = pasante.nombres.replace(" ", "")
    apellidos_juntos = pasante.apellidos.replace(" ", "")
    nombre_archivo = f"ReporteDiario_{nombres_juntos}{apellidos_juntos}_{fecha_formateada}.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'},
    )


# ──────────────────────────────────────────────────────────────────────────────
# GET /ver/{asistencia_id}  —  el PASANTE consulta su reporte del día
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/ver/{asistencia_id}")
def ver_reporte_asistencia(
    asistencia_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    reporte = db.query(Reporte).filter(Reporte.asistencia_id == asistencia_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="No hay reporte aún.")
    return reporte