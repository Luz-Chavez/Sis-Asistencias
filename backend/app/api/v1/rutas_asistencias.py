from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.asistencia_schema import AsistenciaCreate, AsistenciaResponse, AsistenciaUpdate
from app.crud import crud_asistencia
from app.utils.geofencing import validar_ubicacion

from app.api.dependencias import obtener_usuario_actual
from app.models.usuario import Usuario

router = APIRouter()

LAT_FACULTAD = -16.5048
LON_FACULTAD = -68.1299
RADIO_METROS = 50

@router.post("/entrada", response_model=AsistenciaResponse, status_code=status.HTTP_201_CREATED)
def marcar_entrada(
    asistencia: AsistenciaCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual) # <-- Seguridad activada
):
    
    esta_en_facultad = validar_ubicacion(
        lat_pasante=asistencia.latitud_entrada,
        lon_pasante=asistencia.longitud_entrada,
        lat_facultad=LAT_FACULTAD,
        lon_facultad=LON_FACULTAD,
        radio_permitido=RADIO_METROS
    )

    nuevo_registro = crud_asistencia.crear_entrada(db=db, asistencia_data=asistencia)
    
    if not nuevo_registro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pasante ya tiene un registro de entrada para el día de hoy."
        )

    if esta_en_facultad:
        mensaje = "Asistencia registrada correctamente dentro de la Facultad."
    else:
        mensaje = "⚠️ Asistencia registrada, pero tu GPS indica que NO estabas en la Facultad."

    return {
        "id": nuevo_registro.id,
        "pasante_id": nuevo_registro.pasante_id,
        "fecha": nuevo_registro.fecha,
        "hora_entrada": nuevo_registro.hora_entrada,
        "hora_salida": nuevo_registro.hora_salida,
        "horas_trabajadas": nuevo_registro.horas_trabajadas,
        "esta_en_facultad": esta_en_facultad,
        "mensaje_alerta": mensaje
    }

@router.put("/salida/{asistencia_id}", response_model=AsistenciaResponse)
def marcar_salida(
    asistencia_id: int, 
    datos_salida: AsistenciaUpdate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual) # <-- Añadimos seguridad también a la salida
):
    
    registro_actualizado = crud_asistencia.registrar_salida(db=db, asistencia_id=asistencia_id, datos_salida=datos_salida)
    
    if not registro_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de asistencia no encontrado o la salida ya fue marcada."
        )
        
    return registro_actualizado