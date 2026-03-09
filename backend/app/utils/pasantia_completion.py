from __future__ import annotations

from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.asistencia import Asistencia
from app.models.usuario import Usuario
from app.models.carrera import Rol
from app.models.notificacion_pasantia import NotificacionPasantia
from app.utils.emailer import send_email


META_HORAS_PASANTIA = Decimal("240")


def total_horas_pasante(db: Session, pasante_id: int) -> Decimal:
    total = (
        db.query(func.coalesce(func.sum(Asistencia.horas_trabajadas), 0))
        .filter(Asistencia.pasante_id == pasante_id)
        .scalar()
    )
    try:
        return Decimal(str(total))
    except Exception:
        return Decimal("0")


def _encargados_de_carrera(db: Session, carrera_id: Optional[int]) -> List[Usuario]:
    if carrera_id is None:
        return []
    return (
        db.query(Usuario)
        .join(Rol, Usuario.rol_id == Rol.id)
        .filter(Rol.nombre == "ENCARGADO")
        .filter(Usuario.carrera_id == carrera_id)
        .filter(Usuario.estado == True)
        .all()
    )


def check_and_notify_completion(db: Session, pasante_id: int) -> Tuple[Decimal, bool, bool]:
    """Returns: (total_horas, cumplio, notificado_ahora)."""
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        return Decimal("0"), False, False

    total = total_horas_pasante(db, pasante_id)
    cumplio = total >= META_HORAS_PASANTIA
    if not cumplio:
        return total, False, False

    ya = (
        db.query(NotificacionPasantia)
        .filter(NotificacionPasantia.pasante_id == pasante_id)
        .first()
    )
    if ya:
        return total, True, False

    encargados = _encargados_de_carrera(db, pasante.carrera_id)
    emails_encargados = [e.email for e in encargados if e.email]
    email_pasante = pasante.email if pasante.email else None

    # Si no hay destinatarios, igual registramos el hito para no reintentar indefinidamente.
    if not emails_encargados and not email_pasante:
        notif = NotificacionPasantia(
            pasante_id=pasante_id,
            carrera_id=pasante.carrera_id,
            total_horas=total,
            enviado_a=None,
        )
        db.add(notif)
        db.commit()
        return total, True, True

    # Correos
    carrera_nombre = getattr(getattr(pasante, "carrera", None), "nombre", None)
    if pasante.carrera_id is None:
        carrera_linea = "-"
    elif carrera_nombre:
        carrera_linea = f"{pasante.carrera_id} - {carrera_nombre}"
    else:
        carrera_linea = str(pasante.carrera_id)

    subject_encargado = "Notificacion de cumplimiento de horas de pasantia"
    body_encargado = (
        "Estimado/a encargado/a:\n\n"
        "Se informa que el/la estudiante ha completado satisfactoriamente el total de horas "
        "establecidas para su pasantia.\n\n"
        f"Estudiante: {pasante.nombres} {pasante.apellidos}\n"
        f"Usuario: {pasante.username}\n"
        f"CI: {pasante.carnet_identidad}\n"
        f"Carrera: {carrera_linea}\n"
        f"Horas requeridas: {META_HORAS_PASANTIA}\n"
        f"Horas acumuladas: {total}\n\n"
        "Atentamente,\n"
        "Sistema de Control de Asistencia\n"
    )

    subject_pasante = "Felicitaciones! Has completado tu pasantia"
    body_pasante = (
        f"Felicitaciones, {pasante.nombres}!\n\n"
        "Te informamos que has completado satisfactoriamente el total de horas requeridas para tu pasantia.\n"
        f"Carrera: {carrera_linea}\n"
        f"Horas requeridas: {META_HORAS_PASANTIA}\n"
        f"Horas acumuladas: {total}\n\n"
        "Tu encargado/a ya fue notificado/a.\n\n"
        "Atentamente,\n"
        "Sistema de Control de Asistencia\n"
    )

    sent_to: List[str] = []
    failed_to: List[str] = []

    # Intentar notificar de forma aislada por destinatario para que un fallo
    # no bloquee los demas envios.
    for correo_encargado in emails_encargados:
        try:
            enviado = send_email(
                subject=subject_encargado,
                body=body_encargado,
                to=[correo_encargado],
            )
            if enviado:
                sent_to.append(correo_encargado)
            else:
                failed_to.append(correo_encargado)
        except Exception as e:
            print(
                f"[pasantia_completion] Error enviando al encargado {correo_encargado}: {e}"
            )
            failed_to.append(correo_encargado)

    if email_pasante:
        try:
            enviado = send_email(subject=subject_pasante, body=body_pasante, to=[email_pasante])
            if enviado:
                sent_to.append(email_pasante)
            else:
                failed_to.append(email_pasante)
        except Exception as e:
            print(f"[pasantia_completion] Error enviando al pasante {email_pasante}: {e}")
            failed_to.append(email_pasante)

    if not sent_to:
        print(
            "[pasantia_completion] No se pudo enviar ningun correo. "
            f"Fallidos: {', '.join(failed_to) if failed_to else 'sin detalle'}"
        )
        return total, True, False

    notif = NotificacionPasantia(
        pasante_id=pasante_id,
        carrera_id=pasante.carrera_id,
        total_horas=total,
        enviado_a=", ".join(sent_to),
    )
    db.add(notif)
    db.commit()

    return total, True, True
