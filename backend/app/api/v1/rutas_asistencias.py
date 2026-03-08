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

router = APIRouter()

LAT_FACULTAD = -16.5048
LON_FACULTAD = -68.1299
RADIO_METROS = 500


# ──────────────────────────────────────────────────────────────────────────────
# POST /publico/entrada  —  sin token, solo username
# ──────────────────────────────────────────────────────────────────────────────
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
        raise HTTPException(403, detail="Tu cuenta está desactivada. Contacta al encargado.")

    nuevo = crud_asistencia.crear_entrada_por_pasante_id(db=db, pasante_id=pasante.id)
    if not nuevo:
        raise HTTPException(400, detail="Ya tienes registrada una entrada para el día de hoy.")

    return {
        "mensaje":       f"¡Buen día, {pasante.nombres}! Entrada registrada.",
        "nombre":        pasante.nombres,
        "hora_entrada":  nuevo.hora_entrada.strftime("%H:%M:%S"),
        "fecha":         str(nuevo.fecha),
        "asistencia_id": nuevo.id,
    }


# ──────────────────────────────────────────────────────────────────────────────
# POST /publico/salida  —  sin token, solo username
# ──────────────────────────────────────────────────────────────────────────────
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
        raise HTTPException(403, detail="Tu cuenta está desactivada. Contacta al encargado.")

    registro, estado = crud_asistencia.registrar_salida_por_pasante_id(
        db=db, pasante_id=pasante.id
    )

    if estado == "no_entrada":
        raise HTTPException(400, detail="No tienes entrada registrada hoy. Ficha tu entrada primero.")
    if estado == "ya_salio":
        raise HTTPException(400, detail="Ya registraste tu salida de hoy.")

    return {
        "mensaje":          f"¡Hasta luego, {pasante.nombres}! Salida registrada.",
        "nombre":           pasante.nombres,
        "hora_entrada":     registro.hora_entrada.strftime("%H:%M:%S"),
        "hora_salida":      registro.hora_salida.strftime("%H:%M:%S"),
        "horas_trabajadas": float(registro.horas_trabajadas),
        "asistencia_id":    registro.id,
    }


# ──────────────────────────────────────────────────────────────────────────────
# POST /entrada  —  pasante logueado, con GPS opcional
# ──────────────────────────────────────────────────────────────────────────────
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
        raise HTTPException(400, detail="El pasante ya tiene un registro de entrada para el día de hoy.")

    mensaje = (
        "Asistencia registrada correctamente dentro de la Facultad."
        if esta_en_facultad
        else "⚠️ Asistencia registrada, pero tu GPS indica que NO estabas en la Facultad."
    )

    return {
        "id": nuevo.id, "pasante_id": nuevo.pasante_id,
        "fecha": nuevo.fecha, "hora_entrada": nuevo.hora_entrada,
        "hora_salida": nuevo.hora_salida, "horas_trabajadas": nuevo.horas_trabajadas,
        "esta_en_facultad": esta_en_facultad, "mensaje_alerta": mensaje,
    }


# ──────────────────────────────────────────────────────────────────────────────
# PUT /salida/{asistencia_id}  —  pasante logueado
# ──────────────────────────────────────────────────────────────────────────────
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
    return registro


# AÑADIDO──────────────────────────────────────────────────────────────────────────────
# GET /mis-asistencias  —  historial del pasante con reporte incluido
# ──────────────────────────────────────────────────────────────────────────────
@router.get("/mis-asistencias")
def mis_asistencias(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    from app.models.asistencia import Reporte
    asistencias = crud_asistencia.obtener_asistencias_por_pasante(
        db=db, pasante_id=usuario_actual.id
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
