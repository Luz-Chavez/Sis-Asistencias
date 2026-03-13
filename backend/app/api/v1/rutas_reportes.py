from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import case
from typing import List
from datetime import datetime, date, timedelta
import calendar

from app.db.database import get_db
from app.schemas.reporte_schema import ReporteCreate, ReporteResponse, ReporteEvaluar, ReporteHistorialItem
from app.crud import crud_reporte
from app.models.usuario import Usuario
from app.models.asistencia import Reporte, Asistencia, Asistencia as AsistenciaModel
from app.models.reporte_historial import ReporteEstadoHistorial
from app.api.dependencias import obtener_usuario_actual, rol_requerido
from app.utils.generador_pdf import generar_comprobante_pdf
from app.utils.pasantia_completion import check_and_notify_completion
from app.utils.generador_reporte_pdf import generar_reporte_semanal, generar_reporte_mensual

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────
# POST /subir  —  solo el PASANTE puede subir o actualizar su reporte
# ─────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────
# POST /publico/crear — Sin token — el pasante crea su reporte
# ─────────────────────────────────────────────────────────────────────────
@router.post("/publico/crear", response_model=ReporteResponse, status_code=status.HTTP_201_CREATED)
def crear_reporte_publico(
    reporte: ReporteCreate,
    db: Session = Depends(get_db)
):
    asistencia = db.query(Asistencia).filter(Asistencia.id == reporte.asistencia_id).first()
    if not asistencia:
        raise HTTPException(404, detail="Asistencia no encontrada.")

    if not asistencia.hora_salida:
        raise HTTPException(400, detail="No puedes crear el reporte antes de registrar tu salida.")

    existente = db.query(Reporte).filter(Reporte.asistencia_id == reporte.asistencia_id).first()
    if existente:
        existente.actividades_realizadas = reporte.actividades_realizadas
        db.commit()
        db.refresh(existente)
        return existente

    return crud_reporte.crear_reporte(db=db, reporte=reporte)

# ─────────────────────────────────────────────────────────────────────────
# GET /listar — ADMINISTRADOR y ENCARGADO
# ─────────────────────────────────────────────────────────────────────────
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

    pasante_ids = []
    for r in reportes_db:
        try:
            if r.asistencia and r.asistencia.pasante_id:
                pasante_ids.append(int(r.asistencia.pasante_id))
        except Exception:
            pass

    horas_por_pasante = {}
    horas_verificadas_por_pasante = {}
    horas_validadas_por_pasante = {}

    if pasante_ids:
        pasante_ids = list(set(pasante_ids))
        q = (
            db.query(
                Asistencia.pasante_id.label("pasante_id"),
                func.coalesce(func.sum(Asistencia.horas_trabajadas), 0).label("horas_total"),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                func.upper(Reporte.estado).in_(["VERIFICADO", "APROBADO"]),
                                Asistencia.horas_trabajadas,
                            ),
                            else_=0,
                        )
                    ),
                    0,
                ).label("horas_verificadas"),
                func.coalesce(
                    func.sum(
                        case(
                            (func.upper(Reporte.estado) == "APROBADO", Asistencia.horas_trabajadas),
                            else_=0,
                        )
                    ),
                    0,
                ).label("horas_validadas"),
            )
            .outerjoin(Reporte, Reporte.asistencia_id == Asistencia.id)
            .filter(Asistencia.pasante_id.in_(pasante_ids))
            .group_by(Asistencia.pasante_id)
        )

        for row in q.all():
            pid = int(row.pasante_id)
            horas_por_pasante[pid] = float(row.horas_total or 0)
            horas_verificadas_por_pasante[pid] = float(row.horas_verificadas or 0)
            horas_validadas_por_pasante[pid] = float(row.horas_validadas or 0)

    resultado = []
    for r in reportes_db:
        pasante = db.query(Usuario).filter(
            Usuario.id == r.asistencia.pasante_id
        ).first() if r.asistencia else None
        pid = int(r.asistencia.pasante_id) if r.asistencia and r.asistencia.pasante_id else None
        total_horas_pasante = horas_por_pasante.get(pid, 0.0) if pid is not None else 0.0
        total_horas_verificadas = horas_verificadas_por_pasante.get(pid, 0.0) if pid is not None else 0.0
        total_horas_validadas = horas_validadas_por_pasante.get(pid, 0.0) if pid is not None else 0.0

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
            "horas_verificadas":      round(total_horas_verificadas, 2),
            "horas_validadas":        round(total_horas_validadas, 2),
            "estado":                 r.estado,
            "comentarios_director":   r.comentarios_director,
            "creado_en":              r.creado_en,
            "nombre_pasante":         f"{pasante.nombres} {pasante.apellidos}" if pasante else None,
            "proyecto_nombre":        getattr(pasante, "proyecto_nombre", None) if pasante else None,
        })
    return resultado

# ─────────────────────────────────────────────────────────────────────────
# PUT /evaluar/{reporte_id} — ENCARGADO y ADMINISTRADOR
# ─────────────────────────────────────────────────────────────────────────
@router.put("/evaluar/{reporte_id}", response_model=ReporteResponse)
def evaluar_reporte(
    reporte_id: int,
    evaluacion: ReporteEvaluar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ENCARGADO", "ADMINISTRADOR"]))
):
    rol_nombre = (getattr(getattr(usuario_actual, "rol", None), "nombre", "") or "").upper()
    estado_req = (evaluacion.estado or "").strip().upper()
    comentarios = (evaluacion.comentarios_director or "").strip()
    rep = None

    if not comentarios:
        raise HTTPException(status_code=400, detail="Debes dejar un comentario obligatoriamente.")

    # Flujo de 2 niveles:
    if rol_nombre == "ENCARGADO":
        if estado_req not in ("VERIFICADO", "RECHAZADO"):
            raise HTTPException(400, detail="Estado inválido para ENCARGADO. Usa: VERIFICADO o RECHAZADO.")
    else:
        if estado_req not in ("APROBADO", "RECHAZADO"):
            raise HTTPException(400, detail="Estado inválido para ADMINISTRADOR. Usa: APROBADO o RECHAZADO.")

        if estado_req == "APROBADO":
            rep = db.query(Reporte).filter(Reporte.id == reporte_id).first()
            if not rep:
                raise HTTPException(404, detail="Reporte no encontrado.")
            if (rep.estado or "").upper() != "VERIFICADO":
                raise HTTPException(409, detail="Para aprobar, el reporte debe estar VERIFICADO por un encargado.")

    reporte_actualizado = crud_reporte.evaluar_reporte(
        db=db,
        reporte_id=reporte_id,
        estado=estado_req,
        comentarios=comentarios,
        revisado_por=usuario_actual.id
    )
    if not reporte_actualizado:
        raise HTTPException(404, detail="Reporte no encontrado.")

    if rol_nombre != "ENCARGADO" and estado_req == "APROBADO":
        try:
            if rep and rep.asistencia and rep.asistencia.pasante_id:
                check_and_notify_completion(db, int(rep.asistencia.pasante_id))
        except Exception as e:
            print(f"[reportes] Error en notificacion de pasantia completada: {e}")
            
    return reporte_actualizado

# ─────────────────────────────────────────────────────────────────────────
# GET /historial/{reporte_id} — Historial y Auditoría
# ─────────────────────────────────────────────────────────────────────────
@router.get("/historial/{reporte_id}", response_model=List[ReporteHistorialItem])
def historial_reporte(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["ADMINISTRADOR", "ENCARGADO"])),
):
    return crud_reporte.obtener_historial_reporte(db=db, reporte_id=reporte_id)

# ─────────────────────────────────────────────────────────────────────────
# GET /descargar/{reporte_id} — PASANTE, ENCARGADO, ADMINISTRADOR
# ─────────────────────────────────────────────────────────────────────────
@router.get("/descargar/{reporte_id}")
def descargar_reporte_pdf(
    reporte_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE", "ENCARGADO", "ADMINISTRADOR"]))
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

# ─────────────────────────────────────────────────────────────────────────
# GET /ver/{asistencia_id} — PASANTE
# ─────────────────────────────────────────────────────────────────────────
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

# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/semanal — PASANTE
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/semanal")
def descargar_pdf_semanal(
    anio: int,
    semana: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
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

    carrera_nombre = "—"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "—"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(usuario_actual, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    acumulado = 0.0
    cur = primer_dia
    while cur <= ultimo_dia:
        a = asistencias_por_fecha.get(cur)
        if not a:
            filas.append({
                "fecha": cur,
                "hora_entrada": None,
                "hora_salida": None,
                "horas_trabajadas": None,
                "horas_acumuladas": round(acumulado, 2),
                "detalle": "Sin asistencia",
            })
            cur = cur + timedelta(days=1)
            continue

        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        horas_dia = float(a.horas_trabajadas) if a.horas_trabajadas else 0.0
        acumulado = acumulado + horas_dia
        filas.append({
            "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
            "hora_entrada": a.hora_entrada,
            "hora_salida": a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "horas_acumuladas": round(acumulado, 2) if a.horas_trabajadas else round(acumulado, 2),
            "detalle": "Con reporte" if reporte else "Sin reporte",
        })
        cur = cur + timedelta(days=1)

    titulo = f"Reporte semanal · Semana {semana}: {primer_dia.strftime('%d/%m')} al {ultimo_dia.strftime('%d/%m/%Y')}"
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

# ─────────────────────────────────────────────────────────────────────────
# GET /pdf/mensual — PASANTE
# ─────────────────────────────────────────────────────────────────────────
@router.get("/pdf/mensual")
def descargar_pdf_mensual(
    anio: int,
    mes: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(rol_requerido(["PASANTE"]))
):
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

    carrera_nombre = "—"
    if hasattr(usuario_actual, "carrera") and usuario_actual.carrera:
        carrera_nombre = usuario_actual.carrera.nombre

    pasante = {
        "nombres":  usuario_actual.nombres,
        "apellidos": usuario_actual.apellidos,
        "ci":       getattr(usuario_actual, "carnet_identidad", "—"),
        "username": usuario_actual.username,
        "carrera":  carrera_nombre,
        "proyecto": getattr(usuario_actual, "proyecto_nombre", None),
    }

    asistencias_por_fecha = {}
    for a in asistencias:
        f = a.fecha.date() if hasattr(a.fecha, "date") else a.fecha
        asistencias_por_fecha[f] = a

    filas = []
    cur = primer_dia
    while cur <= ultimo_dia:
        a = asistencias_por_fecha.get(cur)
        if not a:
            filas.append({
                "fecha": cur,
                "hora_entrada": None,
                "hora_salida": None,
                "horas_trabajadas": None,
                "actividades": "Sin asistencia",
                "estado": "SIN ASISTENCIA",
            })
            cur = cur + timedelta(days=1)
            continue

        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        filas.append({
            "fecha": a.fecha.date() if hasattr(a.fecha, "date") else a.fecha,
            "hora_entrada": a.hora_entrada,
            "hora_salida": a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "actividades": reporte.actividades_realizadas if reporte else "",
            "estado": reporte.estado if reporte else "SIN REPORTE",
        })
        cur = cur + timedelta(days=1)

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