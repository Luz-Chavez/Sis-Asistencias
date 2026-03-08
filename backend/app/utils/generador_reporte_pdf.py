"""
generador_reporte_pdf.py
Genera reportes de asistencia en PDF para el pasante.

- Semanal : ocupa media hoja A4 (puede caber 2 semanas por hoja)
- Mensual : ocupa una hoja A4 completa
"""

import io
from datetime import date, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

W, H = A4   # 595 x 842 pt

# ── Paleta institucional ──────────────────────────────────────────────────────
AZUL_OSCURO = colors.HexColor("#1e3a5f")
AZUL_MEDIO  = colors.HexColor("#2563eb")
GRIS_CLARO  = colors.HexColor("#f1f5f9")
GRIS_BORDE  = colors.HexColor("#cbd5e1")
VERDE       = colors.HexColor("#16a34a")
AMARILLO    = colors.HexColor("#d97706")
ROJO        = colors.HexColor("#dc2626")
BLANCO      = colors.white

MARGIN = 1.8 * cm
W_UTIL = W - 2 * MARGIN

# Ancho de columnas tabla (suma = W_UTIL ≈ 19 cm)
COL_W = [2.6*cm, 2.0*cm, 2.0*cm, 1.6*cm, 8.2*cm, 2.5*cm]
COL_HEADERS = ["Fecha", "Entrada", "Salida", "Horas", "Actividades Realizadas", "Estado"]

FILA_H   = 0.68 * cm   # altura de cada fila de dato
HEADER_H = 0.78 * cm   # altura del encabezado de columnas
CAB_H    = 2.2  * cm   # altura franja azul superior
INFO_H   = 1.4  * cm   # altura banda datos del pasante
TOTAL_H  = 0.85 * cm   # altura banda de totales
SEP_H    = 0.5  * cm   # separación entre bloques


def _estado_color(estado: str):
    m = {"APROBADO": VERDE, "RECHAZADO": ROJO}
    return m.get(estado, AMARILLO)


def _fmt_hora(dt) -> str:
    if dt is None:
        return "—"
    if isinstance(dt, str):
        return dt[:5]
    return dt.strftime("%H:%M")


def _fmt_fecha(d, con_dia=True) -> str:
    """Devuelve 'Lun 03/03' o '03/03/2026'."""
    if d is None:
        return "—"
    if isinstance(d, str):
        d = date.fromisoformat(d)
    if isinstance(d, datetime):
        d = d.date()
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    if con_dia:
        return f"{dias[d.weekday()]} {d.day:02d}/{d.month:02d}"
    return d.strftime("%d/%m/%Y")


def _alto_bloque(n_filas: int) -> float:
    """Calcula la altura total del bloque dado el número de filas."""
    return CAB_H + INFO_H + HEADER_H + FILA_H * n_filas + TOTAL_H + SEP_H * 2


def _draw_bloque(c: canvas.Canvas, pasante: dict, filas: list,
                 titulo: str, y_top: float):
    """
    Dibuja un bloque completo dentro del canvas.
    y_top: coordenada Y de la parte SUPERIOR del bloque.
    """
    x = MARGIN

    # ── 1. Franja de cabecera ─────────────────────────────────────────────────
    c.setFillColor(AZUL_OSCURO)
    c.rect(x, y_top - CAB_H, W_UTIL, CAB_H, fill=1, stroke=0)

    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 0.4*cm, y_top - 0.75*cm,
                 "FACULTAD DE CIENCIAS SOCIALES · UMSA")
    c.setFont("Helvetica", 8)
    c.drawString(x + 0.4*cm, y_top - 1.3*cm,
                 "Sistema de Control de Asistencia de Pasantes")

    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(x + W_UTIL - 0.4*cm, y_top - 0.75*cm, titulo)

    fecha_gen = date.today().strftime("%d/%m/%Y")
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.HexColor("#93c5fd"))
    c.drawRightString(x + W_UTIL - 0.4*cm, y_top - 1.3*cm,
                      f"Generado: {fecha_gen}")

    # ── 2. Banda datos del pasante ────────────────────────────────────────────
    info_top = y_top - CAB_H
    c.setFillColor(GRIS_CLARO)
    c.rect(x, info_top - INFO_H, W_UTIL, INFO_H, fill=1, stroke=0)
    c.setStrokeColor(GRIS_BORDE)
    c.setLineWidth(0.4)
    c.rect(x, info_top - INFO_H, W_UTIL, INFO_H, fill=0, stroke=1)

    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 8.5)
    nombre_completo = f"{pasante.get('nombres', '')} {pasante.get('apellidos', '')}".strip()
    c.drawString(x + 0.4*cm, info_top - 0.52*cm,
                 f"Pasante: {nombre_completo}")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawString(x + 0.4*cm, info_top - 1.02*cm,
                 f"C.I.: {pasante.get('ci', '—')}   ·   "
                 f"Carrera: {pasante.get('carrera', '—')}")

    # ── 3. Encabezado columnas ────────────────────────────────────────────────
    tabla_top = info_top - INFO_H
    c.setFillColor(AZUL_MEDIO)
    c.rect(x, tabla_top - HEADER_H, W_UTIL, HEADER_H, fill=1, stroke=0)
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 7.5)
    col_x = x
    for txt, cw in zip(COL_HEADERS, COL_W):
        c.drawString(col_x + 0.2*cm, tabla_top - HEADER_H + 0.24*cm, txt)
        col_x += cw

    # ── 4. Filas de datos ─────────────────────────────────────────────────────
    cur_y = tabla_top - HEADER_H
    for idx, fila in enumerate(filas):
        bg = GRIS_CLARO if idx % 2 == 0 else BLANCO
        c.setFillColor(bg)
        c.rect(x, cur_y - FILA_H, W_UTIL, FILA_H, fill=1, stroke=0)
        c.setStrokeColor(GRIS_BORDE)
        c.setLineWidth(0.25)
        c.line(x, cur_y - FILA_H, x + W_UTIL, cur_y - FILA_H)

        c.setFillColor(colors.HexColor("#1e293b"))
        c.setFont("Helvetica", 7.5)
        col_x = x

        fecha_txt = _fmt_fecha(fila.get("fecha"), con_dia=True)
        entrada_txt = _fmt_hora(fila.get("hora_entrada"))
        salida_txt  = _fmt_hora(fila.get("hora_salida"))
        horas_val   = fila.get("horas_trabajadas")
        horas_txt   = f"{float(horas_val):.1f}h" if horas_val else "—"
        act = fila.get("actividades", "Sin reporte")
        if len(act) > 62:
            act = act[:59] + "..."

        valores = [fecha_txt, entrada_txt, salida_txt, horas_txt, act]
        for val, cw in zip(valores, COL_W[:-1]):
            c.drawString(col_x + 0.2*cm, cur_y - FILA_H + 0.2*cm, val)
            col_x += cw

        # Badge de estado
        estado = fila.get("estado", "PENDIENTE")
        badge_x = col_x + 0.12*cm
        badge_y = cur_y - FILA_H + 0.13*cm
        c.setFillColor(_estado_color(estado))
        c.roundRect(badge_x, badge_y, 2.1*cm, 0.42*cm, 0.12*cm, fill=1, stroke=0)
        c.setFillColor(BLANCO)
        c.setFont("Helvetica-Bold", 6.5)
        c.drawCentredString(badge_x + 1.05*cm, badge_y + 0.14*cm, estado)

        cur_y -= FILA_H

    # Borde exterior tabla
    tabla_total_h = HEADER_H + FILA_H * len(filas)
    c.setStrokeColor(GRIS_BORDE)
    c.setLineWidth(0.5)
    c.rect(x, tabla_top - tabla_total_h, W_UTIL, tabla_total_h, fill=0, stroke=1)

    # ── 5. Banda de totales ───────────────────────────────────────────────────
    total_top = cur_y
    c.setFillColor(colors.HexColor("#e0f2fe"))
    c.rect(x, total_top - TOTAL_H, W_UTIL, TOTAL_H, fill=1, stroke=0)
    c.setStrokeColor(colors.HexColor("#7dd3fc"))
    c.setLineWidth(0.5)
    c.rect(x, total_top - TOTAL_H, W_UTIL, TOTAL_H, fill=0, stroke=1)

    total_horas = sum(
        float(f.get("horas_trabajadas") or 0) for f in filas
    )
    dias_reporte = sum(1 for f in filas if f.get("actividades"))
    aprobados    = sum(1 for f in filas if f.get("estado") == "APROBADO")

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(AZUL_OSCURO)
    c.drawString(x + 0.4*cm, total_top - TOTAL_H + 0.28*cm,
                 f"Total: {len(filas)} días  ·  {total_horas:.1f} horas acumuladas  ·  "
                 f"{dias_reporte} reportes enviados  ·  {aprobados} aprobados")

    # ── 6. Línea separadora inferior ─────────────────────────────────────────
    sep_y = total_top - TOTAL_H - 0.25*cm
    c.setStrokeColor(GRIS_BORDE)
    c.setLineWidth(0.8)
    c.line(x, sep_y, x + W_UTIL, sep_y)


# ── API pública ───────────────────────────────────────────────────────────────

def generar_reporte_semanal(pasante: dict, filas: list, titulo_semana: str) -> io.BytesIO:
    """
    Genera un PDF con el reporte semanal ocupando la mitad superior de la hoja.
    pasante: dict con keys nombre, ci, username, carrera
    filas:   lista de dicts con keys fecha, hora_entrada, hora_salida,
             horas_trabajadas, actividades, estado
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # El bloque ocupa desde H-MARGIN hasta la mitad de la hoja
    y_top = H - MARGIN
    _draw_bloque(c, pasante, filas, titulo_semana, y_top)

    c.save()
    buf.seek(0)
    return buf


def generar_reporte_mensual(pasante: dict, filas: list, titulo_mes: str) -> io.BytesIO:
    """
    Genera un PDF con el reporte mensual ocupando una hoja A4 completa.
    Si hay muchos días se divide en páginas automáticamente.
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    # Cuántas filas caben en una página completa
    y_disponible = H - 2 * MARGIN
    overhead      = CAB_H + INFO_H + HEADER_H + TOTAL_H + SEP_H * 2
    filas_por_pag = int((y_disponible - overhead) / FILA_H)

    # Dividir en páginas
    paginas = [filas[i:i + filas_por_pag] for i in range(0, max(len(filas), 1), filas_por_pag)]

    for n_pag, lote in enumerate(paginas):
        if n_pag > 0:
            c.showPage()
        sufijo = f"  (pág. {n_pag + 1}/{len(paginas)})" if len(paginas) > 1 else ""
        _draw_bloque(c, pasante, lote, titulo_mes + sufijo, H - MARGIN)

    c.save()
    buf.seek(0)
    return buf