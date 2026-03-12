from __future__ import annotations

from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.asistencia import Asistencia
from app.models.carrera import Rol
from app.models.notificacion_pasantia import NotificacionPasantia
from app.models.usuario import Usuario
from app.utils.emailer import send_email


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


def horas_validadas_pasante(db: Session, pasante_id: int) -> Decimal:
    from sqlalchemy import case
    from app.models.asistencia import Reporte

    total = (
        db.query(
            func.coalesce(
                func.sum(
                    case(
                        (func.upper(Reporte.estado) == "APROBADO", Asistencia.horas_trabajadas),
                        else_=0,
                    )
                ),
                0,
            )
        )
        .outerjoin(Reporte, Reporte.asistencia_id == Asistencia.id)
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
        .outerjoin(Rol, Usuario.rol_id == Rol.id)
        .filter(Usuario.carrera_id == carrera_id)
        .filter(Usuario.estado.is_(True))
        .filter(or_(Usuario.rol_id == 2, func.upper(Rol.nombre) == "ENCARGADO"))
        .all()
    )


def check_and_notify_completion(db: Session, pasante_id: int) -> Tuple[Decimal, bool, bool]:
    """Returns: (total_horas, cumplio, notificado_ahora)."""
    pasante = db.query(Usuario).filter(Usuario.id == pasante_id).first()
    if not pasante:
        return Decimal("0"), False, False

    meta_raw = getattr(pasante, "meta_horas_pasantia", None) or Decimal("240")
    try:
        meta = Decimal(str(meta_raw))
    except Exception:
        meta = Decimal("240")

    total = total_horas_pasante(db, pasante_id)
    validadas = horas_validadas_pasante(db, pasante_id)

    cumplio = total >= meta
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

    carrera_nombre = getattr(getattr(pasante, "carrera", None), "nombre", None)
    if pasante.carrera_id is None:
        carrera_linea = "?"
    elif carrera_nombre:
        carrera_linea = f"{pasante.carrera_id} - {carrera_nombre}"
    else:
        carrera_linea = str(pasante.carrera_id)

    programa_nombre = getattr(getattr(pasante, "programa", None), "nombre", None)
    programa_linea = programa_nombre or "No asignado"

    subject_encargado = "Pasantia completada: meta de horas cumplida"
    body_encargado = f"""Estimado/a Encargado/a:

Se informa que el/la pasante ha cumplido su meta de horas de pasantia registrada en el sistema.

Datos del pasante
- Nombre: {pasante.nombres} {pasante.apellidos}
- Usuario: {pasante.username}
- CI: {pasante.carnet_identidad}
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta}
- Horas acumuladas: {total}
- Horas validadas (APROBADO): {validadas}

Quedamos atentos a cualquier verificacion o tramite correspondiente.

Atentamente,
Sistema de Control de Asistencia
"""

    subject_pasante = "Felicitaciones: cumpliste tu meta de horas de pasantia"
    body_pasante = f"""Estimado/a {pasante.nombres}:

Felicitaciones. Te confirmamos que has cumplido tu meta de horas de pasantia registrada en el sistema.

Detalle
- Carrera: {carrera_linea}
- Programa: {programa_linea}
- Meta horas: {meta}
- Horas acumuladas: {total}
- Horas validadas (APROBADO): {validadas}

Tu Encargado/a fue notificado/a.

Atentamente,
Sistema de Control de Asistencia
"""

    sent_to: List[str] = []
    failed_to: List[str] = []

    for correo_encargado in emails_encargados:
        try:
            enviado = send_email(subject=subject_encargado, body=body_encargado, to=[correo_encargado])
            if enviado:
                sent_to.append(correo_encargado)
            else:
                failed_to.append(correo_encargado)
        except Exception as e:
            print(f"[pasantia_completion] Error enviando al encargado {correo_encargado}: {e}")
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

    pasante_ok = (email_pasante is None) or (email_pasante in sent_to)
    encargado_ok = (not emails_encargados) or any(c in sent_to for c in emails_encargados)

    if not (pasante_ok and encargado_ok):
        detalle = ", ".join(failed_to) if failed_to else "sin detalle"
        print(
            "[pasantia_completion] No se pudo enviar la notificaci?n a todos los destinatarios. "
            f"Fallidos: {detalle}"
        )
        return total, True, False

    notif = NotificacionPasantia(
        pasante_id=pasante_id,
        carrera_id=pasante.carrera_id,
        total_horas=total,
        enviado_a=", ".join(sent_to) if sent_to else None,
    )
    db.add(notif)
    db.commit()

    return total, True, True
