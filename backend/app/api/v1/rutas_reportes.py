from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from datetime import datetime, date

from app.db.database import get_db
from app.schemas.reporte_schema import ReporteCreate, ReporteResponse, ReporteEvaluar
from app.crud import crud_reporte
from app.models.usuario import Usuario
#from app.models.asistencia import Reporte
from app.models.asistencia import Reporte, Asistencia
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.utils.generador_pdf import generar_comprobante_pdf

router = APIRouter()


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /subir  â€”  solo el PASANTE puede subir o actualizar su reporte
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
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


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /listar
# ADMINISTRADOR â†’ ve todos los reportes
# ENCARGADO     â†’ ve solo los reportes de pasantes de su carrera
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# @router.get("/listar")
# def listar_reportes(
#     db: Session = Depends(get_db),
#     usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
# ):
#     nombre_rol = getattr(usuario_actual.rol, "nombre", "")
#     es_encargado = (nombre_rol == "ENCARGADO")

#     # El ENCARGADO filtra por su carrera; el ADMINISTRADOR ve todo
#     filtro_carrera = usuario_actual.carrera_id if es_encargado else None

#     reportes_db = crud_reporte.obtener_reportes(db=db, carrera_id=filtro_carrera)

#     reportes_con_nombres = []
#     for rep in reportes_db:
#         rep_dict = rep.__dict__.copy()
#         if rep.asistencia and rep.asistencia.pasante:
#             p = rep.asistencia.pasante
#             rep_dict["nombre_pasante"] = f"{p.nombres} {p.apellidos}"
#         else:
#             rep_dict["nombre_pasante"] = "Pasante sin registro"
#         reportes_con_nombres.append(rep_dict)

#     return reportes_con_nombres


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PUT /evaluar/{reporte_id}  â€”  el ENCARGADO evalÃºa un reporte
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# @router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
# def evaluar_reporte(
#     reporte_id: int,
#     evaluacion: ReporteEvaluar,
#     db: Session = Depends(get_db),
#     usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
# ):
#     reporte_actualizado = crud_reporte.evaluar_reporte(
#         db=db,
#         reporte_id=reporte_id,
#         evaluacion=evaluacion,
#         revisado_por_id=usuario_actual.id
#     )

#     if not reporte_actualizado:
#         raise HTTPException(status_code=404, detail="Reporte no encontrado")

#     return reporte_actualizado


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /descargar/{reporte_id}  â€”  descarga el comprobante PDF
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# @router.get("/descargar/{reporte_id}")
# def descargar_reporte_pdf(
#     reporte_id: int,
#     db: Session = Depends(get_db),
#     usuario_actual: Usuario = Depends(
#         rol_requerido(["PASANTE", "ADMINISTRADOR", "ENCARGADO"])
#     )
# ):
#     reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
#     if not reporte:
#         raise HTTPException(status_code=404, detail="Reporte no encontrado")

#     asistencia = reporte.asistencia
#     pasante = asistencia.pasante
#     carrera = pasante.carrera

#     datos_pdf = {
#         "pasante_nombre": f"{pasante.nombres} {pasante.apellidos}",
#         "carrera_nombre": carrera.nombre if carrera else "No asignada",
#         "fecha": asistencia.fecha.strftime("%d/%m/%Y"),
#         "hora_entrada": asistencia.hora_entrada.strftime("%H:%M") if asistencia.hora_entrada else "",
#         "hora_salida": asistencia.hora_salida.strftime("%H:%M") if asistencia.hora_salida else "Pendiente",
#         "horas_trabajadas": asistencia.horas_trabajadas or 0,
#         "actividades": reporte.actividades_realizadas,
#     }

#     pdf_buffer = generar_comprobante_pdf(datos_reporte=datos_pdf)

#     meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
#     mes_abreviado = meses[asistencia.fecha.month - 1]
#     fecha_formateada = f"{asistencia.fecha.day:02d}{mes_abreviado}"

#     nombres_juntos = pasante.nombres.replace(" ", "")
#     apellidos_juntos = pasante.apellidos.replace(" ", "")
#     nombre_archivo = f"ReporteDiario_{nombres_juntos}{apellidos_juntos}_{fecha_formateada}.pdf"

#     return StreamingResponse(
#         pdf_buffer,
#         media_type="application/pdf",
#         headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'},
#     )


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /ver/{asistencia_id}  â€”  el PASANTE consulta su reporte del dÃ­a
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.get("/ver/{asistencia_id}")
def ver_reporte_asistencia(
    asistencia_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    reporte = db.query(Reporte).filter(Reporte.asistencia_id == asistencia_id).first()
    if not reporte:
        raise HTTPException(status_code=404, detail="No hay reporte aÃºn.")
    return reporte


# AÃ‘ADIDOâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /publico/crear
# Sin token â€” el pasante crea su reporte justo despuÃ©s de fichar salida
# desde la pantalla pÃºblica. Solo necesita asistencia_id y actividades.
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/publico/crear", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
def crear_reporte_publico(
    reporte: ReporteCreate,
    db: Session = Depends(get_db)
):
    # Verificar que la asistencia existe
    asistencia = db.query(Asistencia).filter(Asistencia.id == reporte.asistencia_id).first()
    if not asistencia:
        raise HTTPException(404, detail="Asistencia no encontrada.")

    # Verificar que ya tiene salida registrada
    if not asistencia.hora_salida:
        raise HTTPException(400, detail="No puedes crear el reporte antes de registrar tu salida.")

    # Si ya existe un reporte para esta asistencia, lo actualizamos
    existente = db.query(Reporte).filter(Reporte.asistencia_id == reporte.asistencia_id).first()
    if existente:
        existente.actividades_realizadas = reporte.actividades_realizadas
        db.commit()
        db.refresh(existente)
        return existente

    return crud_reporte.crear_reporte(db=db, reporte=reporte)


# MODIFICADO â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /listar â€” ADMINISTRADOR y ENCARGADO
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.get("/listar")
def listar_reportes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"]))
):
    nombre_rol = getattr(usuario_actual.rol, "nombre", "")
    filtro_carrera = usuario_actual.carrera_id if nombre_rol == "ENCARGADO" else None

    if nombre_rol == "ENCARGADO" and not filtro_carrera:
        raise HTTPException(400, detail="Tu usuario no tiene carrera asignada. Contacta al administrador.")

    reportes_db = crud_reporte.obtener_reportes(db=db, carrera_id=filtro_carrera)

    resultado = []
    for r in reportes_db:
        pasante = db.query(Usuario).filter(
            Usuario.id == r.asistencia.pasante_id
        ).first() if r.asistencia else None
        total_horas_pasante = float((
            db.query(func.coalesce(func.sum(Asistencia.horas_trabajadas), 0))
            .filter(Asistencia.pasante_id == r.asistencia.pasante_id)
            .scalar()
        ) or 0)


        horas = 0.0
        if r.asistencia:
            valor_bd = float(r.asistencia.horas_trabajadas) if r.asistencia.horas_trabajadas is not None else None
            if valor_bd is not None and valor_bd > 0:
                horas = valor_bd
            elif r.asistencia.hora_entrada and r.asistencia.hora_salida:
                dt_entrada = r.asistencia.hora_entrada
                dt_salida = r.asistencia.hora_salida
                horas_calc = round(max((dt_salida - dt_entrada).total_seconds() / 3600, 0), 2)
                horas = horas_calc if horas_calc > 0 else 0.01

        resultado.append({
            "id":                     r.id,
            "asistencia_id":          r.asistencia_id,
            "actividades_realizadas": r.actividades_realizadas,
            "horas_trabajadas":       horas,
            "horas_totales":          round(total_horas_pasante, 2),
            "estado":                 r.estado,
            "comentarios_director":   r.comentarios_director,
            "creado_en":              r.creado_en,
            "nombre_pasante":         f"{pasante.nombres} {pasante.apellidos}" if pasante else None,
        })
    return resultado

# MODIFICADOâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PUT /evaluar/{reporte_id} — ENCARGADO y ADMINISTRADOR
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
def evaluar_reporte(
    reporte_id: int,
    evaluacion: ReporteEvaluar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
):
    reporte_actualizado = crud_reporte.evaluar_reporte(
        db=db,
        reporte_id=reporte_id,
        estado=evaluacion.estado,
        comentarios=evaluacion.comentarios_director,
        revisado_por=usuario_actual.id
    )
    if not reporte_actualizado:
        raise HTTPException(404, detail="Reporte no encontrado.")
    return reporte_actualizado

# MODIFICADOâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /descargar/{reporte_id} â€” PASANTE, ENCARGADO, ADMINISTRADOR
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.get("/descargar/{reporte_id}")
def descargar_reporte_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(
        rol_requerido(["PASANTE", "ENCARGADO", "ADMINISTRADOR"])
    )
):
    reporte = db.query(Reporte).filter(Reporte.id == reporte_id).first()
    if not reporte:
        raise HTTPException(404, detail="Reporte no encontrado.")

    asistencia = reporte.asistencia
    pasante = asistencia.pasante if asistencia else None
    carrera = pasante.carrera if pasante else None

    datos_pdf = {
        "pasante_nombre": f"{pasante.nombres} {pasante.apellidos}" if pasante else "Pasante",
        "carrera_nombre": carrera.nombre if carrera else "No asignada",
        "fecha": asistencia.fecha.strftime("%d/%m/%Y") if asistencia and asistencia.fecha else "",
        "hora_entrada": asistencia.hora_entrada.strftime("%H:%M") if asistencia and asistencia.hora_entrada else "",
        "hora_salida": asistencia.hora_salida.strftime("%H:%M") if asistencia and asistencia.hora_salida else "Pendiente",
        "horas_trabajadas": float(asistencia.horas_trabajadas) if asistencia and asistencia.horas_trabajadas is not None else 0,
        "actividades": reporte.actividades_realizadas,
    }

    pdf_buffer = generar_comprobante_pdf(datos_pdf)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=reporte_{reporte_id}.pdf"}
    )
# GET /ver/{asistencia_id} â€” PASANTE
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.get("/ver/{asistencia_id}")
def ver_reporte_por_asistencia(
    asistencia_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    reporte = db.query(Reporte).filter(Reporte.asistencia_id == asistencia_id).first()
    if not reporte:
        raise HTTPException(404, detail="No hay reporte para esta asistencia.")
    return reporte


# AÃ‘ADIDOSâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /pdf/semanal?anio=2026&semana=10
# GET /pdf/mensual?anio=2026&mes=3
# Descarga PDF de reporte del PASANTE logueado
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from datetime import date, timedelta
from app.utils.generador_reporte_pdf import generar_reporte_semanal, generar_reporte_mensual
from app.models.asistencia import Asistencia as AsistenciaModel

@router.get("/pdf/semanal")
def descargar_pdf_semanal(
    anio: int,
    semana: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    # Calcular rango de fechas de la semana ISO
    primer_dia = date.fromisocalendar(anio, semana, 1)   # lunes
    ultimo_dia = primer_dia + timedelta(days=6)           # domingo

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == usuario_actual.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    if not asistencias:
        raise HTTPException(404, detail="No hay asistencias registradas para esa semana.")

    # Obtener carrera del pasante
    carrera_nombre = "â€”"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "â€”"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
    }

    filas = []
    for a in asistencias:
        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        filas.append({
            "fecha":           a.fecha,
            "hora_entrada":    a.hora_entrada,
            "hora_salida":     a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "actividades":     reporte.actividades_realizadas if reporte else "",
            "estado":          reporte.estado if reporte else "SIN REPORTE",
        })

    titulo = f"Semana {semana} â€” {primer_dia.strftime('%d/%m')} al {ultimo_dia.strftime('%d/%m/%Y')}"
    buf = generar_reporte_semanal(pasante, filas, titulo)

    nombre_archivo = (
        f"Reporte_Semanal_Sem{semana}_{anio}_"
        f"{usuario_actual.nombres.split()[0]}{usuario_actual.apellidos.split()[0]}.pdf"
    )
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )


@router.get("/pdf/mensual")
def descargar_pdf_mensual(
    anio: int,
    mes: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
    import calendar
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, calendar.monthrange(anio, mes)[1])

    asistencias = (
        db.query(AsistenciaModel)
        .filter(
            AsistenciaModel.pasante_id == usuario_actual.id,
            AsistenciaModel.fecha >= primer_dia,
            AsistenciaModel.fecha <= ultimo_dia,
        )
        .order_by(AsistenciaModel.fecha)
        .all()
    )

    if not asistencias:
        raise HTTPException(404, detail="No hay asistencias registradas para ese mes.")

    carrera_nombre = "â€”"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "â€”"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
    }

    filas = []
    for a in asistencias:
        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        filas.append({
            "fecha":           a.fecha,
            "hora_entrada":    a.hora_entrada,
            "hora_salida":     a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "actividades":     reporte.actividades_realizadas if reporte else "",
            "estado":          reporte.estado if reporte else "SIN REPORTE",
        })

    meses_es = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    titulo = f"{meses_es[mes]} {anio}"
    buf = generar_reporte_mensual(pasante, filas, titulo)

    nombre_archivo = (
        f"Reporte_Mensual_{meses_es[mes]}{anio}_"
        f"{usuario_actual.nombres.split()[0]}{usuario_actual.apellidos.split()[0]}.pdf"
    )
    return StreamingResponse(
        buf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{nombre_archivo}"'}
    )

