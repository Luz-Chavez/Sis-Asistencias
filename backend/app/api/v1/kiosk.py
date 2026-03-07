from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db.database import get_db
from app.models.usuario import Usuario
from app.models.asistencia import Asistencia
from pydantic import BaseModel
import math

router = APIRouter(prefix="/kiosk", tags=["kiosk"])


class KioskEntradaRequest(BaseModel):
    carnet_identidad: str
    latitud_entrada: float
    longitud_entrada: float

class KioskSalidaRequest(BaseModel):
    carnet_identidad: str
    latitud_salida: float
    longitud_salida: float


def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


@router.post("/entrada")
def kiosk_entrada(datos: KioskEntradaRequest, db: Session = Depends(get_db)):
    pasante = db.query(Usuario).filter(
        Usuario.carnet_identidad == datos.carnet_identidad,
        Usuario.estado == True
    ).first()

    if not pasante:
        raise HTTPException(status_code=404, detail="No se encontró ningún pasante activo con ese carnet.")

    hoy = datetime.now(timezone.utc).date()
    ya_entro = db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante.id,
        Asistencia.fecha == hoy
    ).first()

    if ya_entro:
        raise HTTPException(status_code=400, detail="Ya tienes una entrada registrada para hoy.")

    LAT_FACULTAD = -16.500276
    LON_FACULTAD = -68.119293
    distancia = calcular_distancia(datos.latitud_entrada, datos.longitud_entrada, LAT_FACULTAD, LON_FACULTAD)
    esta_en_facultad = distancia <= 100
    mensaje = "Entrada registrada correctamente." if esta_en_facultad else f"Entrada registrada, pero estás a {round(distancia)}m de la facultad."

    nueva = Asistencia(
        pasante_id=pasante.id,
        fecha=hoy,
        hora_entrada=datetime.now(timezone.utc),
        latitud_entrada=datos.latitud_entrada,
        longitud_entrada=datos.longitud_entrada
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return {
        "id": nueva.id,
        "nombre_completo": f"{pasante.nombres} {pasante.apellidos}",
        "hora_entrada": nueva.hora_entrada,
        "esta_en_facultad": esta_en_facultad,
        "mensaje": mensaje
    }


@router.post("/salida")
def kiosk_salida(datos: KioskSalidaRequest, db: Session = Depends(get_db)):
    pasante = db.query(Usuario).filter(
        Usuario.carnet_identidad == datos.carnet_identidad,
        Usuario.estado == True
    ).first()

    if not pasante:
        raise HTTPException(status_code=404, detail="No se encontró ningún pasante activo con ese carnet.")

    hoy = datetime.now(timezone.utc).date()
    asistencia = db.query(Asistencia).filter(
        Asistencia.pasante_id == pasante.id,
        Asistencia.fecha == hoy,
        Asistencia.hora_salida == None
    ).first()

    if not asistencia:
        raise HTTPException(status_code=400, detail="No tienes una entrada activa para hoy. Primero registra tu entrada.")

    hora_actual = datetime.now(timezone.utc)
    asistencia.hora_salida = hora_actual
    asistencia.latitud_salida = datos.latitud_salida
    asistencia.longitud_salida = datos.longitud_salida
    diferencia = hora_actual - asistencia.hora_entrada
    asistencia.horas_trabajadas = round(diferencia.total_seconds() / 3600, 2)

    db.commit()
    db.refresh(asistencia)

    return {
        "id": asistencia.id,
        "nombre_completo": f"{pasante.nombres} {pasante.apellidos}",
        "hora_entrada": asistencia.hora_entrada,
        "hora_salida": asistencia.hora_salida,
        "horas_trabajadas": float(asistencia.horas_trabajadas)
    }