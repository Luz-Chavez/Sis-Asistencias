from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.asistencia_schema import (
    AsistenciaCreate, AsistenciaResponse, AsistenciaUpdate,
    FichajePublicoEntrada, FichajePublicoSalida,
)
from app.crud import crud_asistencia
from app.utils.geofencing import validar_ubicacion
from app.api.dependencias import obtener_usuario_actual
from app.models.usuario import Usuario
from app.utils.pasantia_completion import check_and_notify_completion

router = APIRouter()

LAT_FACULTAD = -16.5048
LON_FACULTAD = -68.1299
RADIO_METROS = 500


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /publico/entrada  â€”  sin token, solo username
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/publico/entrada")
def fichaje_publico_entrada(datos: FichajePublicoEntrada, db: Session = Depends(get_db)):
    pasante = db.query(Usuario).filter(
        Usuario.username == datos.username.strip().lower()
    ).first()

    if not pasante:
        raise HTTPException(404, detail="Username no encontrado. Verifica tus datos.")

    nombre_rol = getattr(pasante.rol, "nombre", "")
    if nombre_rol != "PASANTE":
        raise HTTPException(
            403,
            detail=f"Esta pantalla es solo para Pasantes. Tu rol es: {nombre_rol}."
        )

    if not pasante.estado:
        raise HTTPException(403, detail="Tu cuenta estÃ¡ desactivada. Contacta al encargado.")

    nuevo = crud_asistencia.crear_entrada_por_pasante_id(db=db, pasante_id=pasante.id)
    if not nuevo:
        raise HTTPException(400, detail="Ya tienes registrada una entrada para el dÃ­a de hoy.")

    return {
        "mensaje":       f"Â¡Buen dÃ­a, {pasante.nombres}! Entrada registrada.",
        "nombre":        pasante.nombres,
        "hora_entrada":  nuevo.hora_entrada.strftime("%H:%M:%S"),
        "fecha":         str(nuevo.fecha),
        "asistencia_id": nuevo.id,
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /publico/salida  â€”  sin token, solo username
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/publico/salida")
def fichaje_publico_salida(datos: FichajePublicoSalida, db: Session = Depends(get_db)):
    pasante = db.query(Usuario).filter(
        Usuario.username == datos.username.strip().lower()
    ).first()

    if not pasante:
        raise HTTPException(404, detail="Username no encontrado. Verifica tus datos.")

    nombre_rol = getattr(pasante.rol, "nombre", "")
    if nombre_rol != "PASANTE":
        raise HTTPException(
            403,
            detail=f"Esta pantalla es solo para Pasantes. Tu rol es: {nombre_rol}."
        )

    if not pasante.estado:
        raise HTTPException(403, detail="Tu cuenta estÃ¡ desactivada. Contacta al encargado.")

    registro, estado = crud_asistencia.registrar_salida_por_pasante_id(
        db=db, pasante_id=pasante.id
    )

    if estado == "no_entrada":
        raise HTTPException(400, detail="No tienes entrada registrada hoy. Ficha tu entrada primero.")
    if estado == "ya_salio":
        raise HTTPException(400, detail="Ya registraste tu salida de hoy.")

    # Notificar al encargado si el pasante completó 240h
    total_horas, cumplio, _notificado = check_and_notify_completion(db, pasante.id)


    return {
        "mensaje":          f"Â¡Hasta luego, {pasante.nombres}! Salida registrada.",
        "nombre":           pasante.nombres,
        "hora_entrada":     registro.hora_entrada.strftime("%H:%M:%S"),
        "hora_salida":      registro.hora_salida.strftime("%H:%M:%S"),
        "horas_trabajadas": float(registro.horas_trabajadas),
        "asistencia_id":    registro.id,
        "total_horas_acumuladas": float(total_horas),
        "cumplio_pasantia": bool(cumplio),
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# POST /entrada  â€”  pasante logueado, con GPS opcional
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.post("/entrada", response_model=AsistenciaResponse, status_code=status.HTTP_201_CREATED)
def marcar_entrada(
    asistencia: AsistenciaCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    esta_en_facultad = False
    if asistencia.latitud_entrada and asistencia.longitud_entrada:
        esta_en_facultad = validar_ubicacion(
            lat_pasante=asistencia.latitud_entrada,
            lon_pasante=asistencia.longitud_entrada,
            lat_facultad=LAT_FACULTAD,
            lon_facultad=LON_FACULTAD,
            radio_permitido=RADIO_METROS
        )

    nuevo = crud_asistencia.crear_entrada(db=db, asistencia_data=asistencia)
    if not nuevo:
        raise HTTPException(400, detail="El pasante ya tiene un registro de entrada para el dÃ­a de hoy.")

    mensaje = (
        "Asistencia registrada correctamente dentro de la Facultad."
        if esta_en_facultad
        else " Asistencia registrada, pero tu GPS indica que NO estabas en la Facultad."
    )

    return {
        "id": nuevo.id, "pasante_id": nuevo.pasante_id,
        "fecha": nuevo.fecha, "hora_entrada": nuevo.hora_entrada,
        "hora_salida": nuevo.hora_salida, "horas_trabajadas": nuevo.horas_trabajadas,
        "esta_en_facultad": esta_en_facultad, "mensaje_alerta": mensaje,
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# PUT /salida/{asistencia_id}  â€”  pasante logueado
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
@router.put("/salida/{asistencia_id}", response_model=AsistenciaResponse)
def marcar_salida(
    asistencia_id: int,
    datos_salida: AsistenciaUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    registro = crud_asistencia.registrar_salida(
        db=db, asistencia_id=asistencia_id, datos_salida=datos_salida
    )
    if not registro:
        raise HTTPException(404, detail="Registro no encontrado o salida ya marcada.")
    # Notificar al encargado si el pasante completó 240h
    check_and_notify_completion(db, registro.pasante_id)

    return registro


# AÃ‘ADIDOâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# GET /mis-asistencias  â€”  historial del pasante con reporte incluido
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from typing import Optional

@router.get("/mis-asistencias")
def mis_asistencias(
    pasante_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Devuelve el historial de asistencias.

    - Si el usuario es pasante retorna sus propias asistencias.
    - Si se proporciona *pasante_id* y el usuario tiene rol de encargado/admin
      permite ver el historial de aquel pasante.
    """
    from app.models.asistencia import Reporte

    # si solicitan otro id, sÃ³lo lo permitimos para roles 1 (admin) o 2 (encargado)
    if pasante_id is not None and usuario_actual.rol_id not in (1, 2):
        raise HTTPException(403, detail="No autorizado para ver ese historial.")
    # Si es ENCARGADO, solo puede ver asistencias de PASANTES de su misma carrera
    if pasante_id is not None and usuario_actual.rol_id == 2:
        objetivo = db.query(Usuario).filter(Usuario.id == pasante_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Pasante no encontrado.")
        rol_objetivo = getattr(objetivo.rol, "nombre", "")
        if rol_objetivo != "PASANTE" or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes ver asistencias de pasantes de tu carrera.")


    target_id = pasante_id or usuario_actual.id
    asistencias = crud_asistencia.obtener_asistencias_por_pasante(
        db=db, pasante_id=target_id
    )
    resultado = []
    for a in asistencias:
        reporte = db.query(Reporte).filter(Reporte.asistencia_id == a.id).first()
        resultado.append({
            "id":               a.id,
            "pasante_id":       a.pasante_id,
            "fecha":            a.fecha,
            "hora_entrada":     a.hora_entrada,
            "hora_salida":      a.hora_salida,
            "horas_trabajadas": float(a.horas_trabajadas) if a.horas_trabajadas else None,
            "reporte": {
                "id":                     reporte.id,
                "actividades_realizadas": reporte.actividades_realizadas,
                "estado":                 reporte.estado,
                "comentarios_director":   reporte.comentarios_director,
                "creado_en":              reporte.creado_en,
            } if reporte else None,
        })
    return resultado
# GET /reporte-pdf — descarga PDF por día/semana/mes
@router.get("/reporte-pdf")
def descargar_reporte_periodo_pdf(
    tipo: str,
    fecha: str,
    pasante_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Descarga un PDF de asistencias+reportes por día/semana/mes.

    Query params:
      - tipo: dia | semana | mes
      - fecha: YYYY-MM-DD (para mes también sirve, toma el mes de esa fecha)
      - pasante_id (opcional): solo ADMIN/ENCARGADO
    """
    from datetime import date, timedelta
    from fastapi.responses import StreamingResponse
    from sqlalchemy.orm import joinedload

    from app.models.asistencia import Asistencia
    from app.utils.generador_reporte_pdf import (
        generar_reporte_diario,
        generar_reporte_semanal,
        generar_reporte_mensual,
    )

    tipo = (tipo or '').strip().lower()
    if tipo not in ('dia', 'semana', 'mes'):
        raise HTTPException(400, detail="tipo inválido. Usa: dia, semana, mes")

    try:
        base_date = date.fromisoformat(str(fecha))
    except Exception:
        raise HTTPException(400, detail="fecha inválida. Usa formato YYYY-MM-DD")

    # Resolver objetivo según rol
    if pasante_id is not None and usuario_actual.rol_id not in (1, 2):
        raise HTTPException(403, detail="No autorizado para descargar ese reporte.")

    target_id = pasante_id or usuario_actual.id

    # Validación ENCARGADO: solo pasantes de su carrera
    if pasante_id is not None and usuario_actual.rol_id == 2:
        objetivo = db.query(Usuario).filter(Usuario.id == pasante_id).first()
        if not objetivo:
            raise HTTPException(404, detail="Pasante no encontrado.")
        rol_objetivo = getattr(objetivo.rol, 'nombre', '')
        if rol_objetivo != 'PASANTE' or objetivo.carrera_id != usuario_actual.carrera_id:
            raise HTTPException(403, detail="Solo puedes descargar reportes de pasantes de tu carrera.")

    pasante = db.query(Usuario).filter(Usuario.id == target_id).first()
    if not pasante:
        raise HTTPException(404, detail="Pasante no encontrado.")

    # Rango y título
    if tipo == 'dia':
        start = base_date
        end = base_date
        titulo = f"Reporte diario · {base_date.strftime('%d/%m/%Y')}"
        filename = f"reporte_diario_{pasante.username}_{base_date.isoformat()}.pdf"
    elif tipo == 'semana':
        start = base_date - timedelta(days=base_date.weekday())
        end = start + timedelta(days=6)
        titulo = f"Reporte semanal · {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}"
        filename = f"reporte_semanal_{pasante.username}_{start.isoformat()}.pdf"
    else:
        start = date(base_date.year, base_date.month, 1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
        titulo = f"Reporte mensual · {start.strftime('%m/%Y')}"
        filename = f"reporte_mensual_{pasante.username}_{start.strftime('%Y-%m')}.pdf"

    asistencias = (
        db.query(Asistencia)
        .options(joinedload(Asistencia.reporte))
        .filter(Asistencia.pasante_id == pasante.id)
        .filter(Asistencia.fecha >= start)
        .filter(Asistencia.fecha <= end)
        .order_by(Asistencia.fecha.asc())
        .all()
    )

    # PASANTE: solo puede descargar si TODO el periodo est? APROBADO
    # (si falta reporte o est? PENDIENTE/RECHAZADO, se bloquea).
    if usuario_actual.rol_id == 3:
        for a in asistencias:
            rep = getattr(a, 'reporte', None)
            if not rep or (rep.estado or '').upper() != 'APROBADO':
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    detail='Solo puedes descargar el PDF cuando todos los reportes del periodo est?n APROBADOS.',
                )


    filas = []
    for a in asistencias:
        rep = getattr(a, 'reporte', None)
        filas.append({
            'fecha': a.fecha,
            'hora_entrada': a.hora_entrada,
            'hora_salida': a.hora_salida,
            'horas_trabajadas': float(a.horas_trabajadas) if a.horas_trabajadas is not None else None,
            'actividades': rep.actividades_realizadas if rep else None,
            'estado': rep.estado if rep else 'PENDIENTE',
        })

    carrera_nombre = getattr(getattr(pasante, 'carrera', None), 'nombre', None)
    pasante_info = {
        'nombres': pasante.nombres,
        'apellidos': pasante.apellidos,
        'ci': pasante.carnet_identidad,
        'carrera': carrera_nombre or (str(pasante.carrera_id) if pasante.carrera_id is not None else '—'),
    }

    if tipo == 'mes':
        buf = generar_reporte_mensual(pasante_info, filas, titulo)
    elif tipo == 'dia':
        buf = generar_reporte_diario(pasante_info, filas, titulo)
    else:
        buf = generar_reporte_semanal(pasante_info, filas, titulo)

    return StreamingResponse(
        buf,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={filename}'},
    )


# GET /resumen-horas ? resumen de horas por pasante (Encargado/Admin)
@router.get("/resumen-horas")
def resumen_horas_pasantes(
    tipo: str = "semana",
    fecha: Optional[str] = None,
    carrera_id: Optional[int] = None,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    """Resumen de horas trabajadas por pasante.

    - ENCARGADO: solo su carrera (usa su carrera_id)
    - ADMIN: puede enviar carrera_id (opcional). Si no env?a, devuelve todas.
    - PASANTE: solo su propio resumen (ignora carrera_id)

    Query params:
      - tipo: dia | semana | mes | total
      - fecha: YYYY-MM-DD (opcional; si no se manda usa hoy)
      - carrera_id: solo ADMIN (opcional)
    """
    from datetime import date, datetime, time, timedelta

    from sqlalchemy import case, func

    from app.models.asistencia import Asistencia

    tipo = (tipo or "").strip().lower()
    if tipo not in ("dia", "semana", "mes", "total"):
        raise HTTPException(400, detail="tipo inv?lido. Usa: dia, semana, mes, total")

    base_date = date.today()
    if fecha:
        try:
            base_date = date.fromisoformat(str(fecha))
        except Exception:
            raise HTTPException(400, detail="fecha inv?lida. Usa formato YYYY-MM-DD")

    # Permisos / alcance
    if usuario_actual.rol_id == 2:
        if usuario_actual.carrera_id is None:
            raise HTTPException(400, detail="Tu usuario no tiene carrera asignada. Contacta al administrador.")
        carrera_filtro = usuario_actual.carrera_id
        pasante_unico = None
    elif usuario_actual.rol_id == 1:
        carrera_filtro = carrera_id
        pasante_unico = None
    elif usuario_actual.rol_id == 3:
        carrera_filtro = None
        pasante_unico = usuario_actual.id
    else:
        raise HTTPException(403, detail="No autorizado.")

    # Rango
    start_dt = None
    end_dt = None
    if tipo == "dia":
        start = base_date
        end = base_date
    elif tipo == "semana":
        start = base_date - timedelta(days=base_date.weekday())
        end = start + timedelta(days=6)
    elif tipo == "mes":
        start = date(base_date.year, base_date.month, 1)
        next_month = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        end = next_month - timedelta(days=1)
    else:
        start = None
        end = None

    if start is not None and end is not None:
        start_dt = datetime.combine(start, time.min)
        end_dt = datetime.combine(end + timedelta(days=1), time.min)

    # Query agregada
    q = (
        db.query(
            Usuario.id.label("pasante_id"),
            Usuario.nombres.label("nombres"),
            Usuario.apellidos.label("apellidos"),
            Usuario.username.label("username"),
            func.count(Asistencia.id).label("registros"),
            func.coalesce(func.sum(Asistencia.horas_trabajadas), 0).label("horas"),
            func.coalesce(
                func.sum(case((Asistencia.horas_trabajadas.is_(None), 1), else_=0)),
                0,
            ).label("sin_salida"),
        )
        .join(Asistencia, Asistencia.pasante_id == Usuario.id)
        .filter(Usuario.rol_id == 3)
    )

    if carrera_filtro is not None:
        q = q.filter(Usuario.carrera_id == carrera_filtro)

    if pasante_unico is not None:
        q = q.filter(Usuario.id == pasante_unico)

    if start_dt is not None and end_dt is not None:
        q = q.filter(Asistencia.fecha >= start_dt).filter(Asistencia.fecha < end_dt)

    q = q.group_by(Usuario.id, Usuario.nombres, Usuario.apellidos, Usuario.username)
    q = q.order_by(func.coalesce(func.sum(Asistencia.horas_trabajadas), 0).desc())

    items = []
    for row in q.all():
        horas = float(row.horas or 0)
        items.append(
            {
                "pasante_id": int(row.pasante_id),
                "nombres": row.nombres,
                "apellidos": row.apellidos,
                "username": row.username,
                "registros": int(row.registros or 0),
                "horas": horas,
                "sin_salida": int(row.sin_salida or 0),
            }
        )

    periodo = {"tipo": tipo}
    if start_dt is not None and end_dt is not None:
        periodo.update({"inicio": start.isoformat(), "fin": end.isoformat()})

    return {"periodo": periodo, "items": items}

