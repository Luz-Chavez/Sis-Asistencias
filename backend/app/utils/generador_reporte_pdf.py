import io
from datetime import date, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

W, H = A4   # 595 x 842 pt

# ── Paleta institucional exacta de la imagen ──────────────────────────────────
AZUL_OSCURO = colors.HexColor("#1e3a5f") # El de la cabecera
AZUL_TABLA  = colors.HexColor("#2563eb") # El del encabezado de tabla
GRIS_FONDOS = colors.HexColor("#f8fafc") # Fondo suave para datos pasante
GRIS_BORDE  = colors.HexColor("#e2e8f0")
BLANCO      = colors.white

# Colores para los Badges de Estado
VERDE    = colors.HexColor("#16a34a")
ROJO     = colors.HexColor("#dc2626")
AMARILLO = colors.HexColor("#d97706")
GRIS_EST = colors.HexColor("#64748b")

MARGIN = 1.5 * cm
W_UTIL = W - 2 * MARGIN

def _estado_color(estado: str):
    e = (estado or "").upper()
    if e == "APROBADO": return VERDE
    if e == "RECHAZADO": return ROJO
    if e in ["SIN ASISTENCIA", "SIN REPORTE"]: return GRIS_EST
    return AMARILLO

def _fmt_hora(dt) -> str:
    if dt is None: return "—"
    if isinstance(dt, str): return dt[:5]
    return dt.strftime("%H:%M")

def _fmt_fecha(d) -> str:
    if d is None: return "—"
    if isinstance(d, str): d = date.fromisoformat(d)
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return f"{dias[d.weekday()]} {d.day:02d}/{d.month:02d}"

def _draw_bloque(c: canvas.Canvas, pasante: dict, filas: list, titulo: str, y_top: float, variant="default"):
    x = MARGIN
    
    # 1. Cabecera Azul Marino
    cab_h = 2.0 * cm
    c.setFillColor(AZUL_OSCURO)
    c.rect(x, y_top - cab_h, W_UTIL, cab_h, fill=1, stroke=0)
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 0.5*cm, y_top - 0.7*cm, "FACULTAD DE CIENCIAS SOCIALES · UMSA")
    c.setFont("Helvetica", 8)
    c.drawString(x + 0.5*cm, y_top - 1.2*cm, "Sistema de Control de Asistencia de Pasantes")
    
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(x + W_UTIL - 0.5*cm, y_top - 0.7*cm, titulo)
    c.setFont("Helvetica", 7)
    c.drawRightString(x + W_UTIL - 0.5*cm, y_top - 1.2*cm, f"Generado: {date.today().strftime('%d/%m/%Y')}")

    # 2. Banda Datos del Pasante (Gris suave)
    info_h = 1.8 * cm
    info_top = y_top - cab_h
    c.setFillColor(GRIS_FONDOS)
    c.rect(x, info_top - info_h, W_UTIL, info_h, fill=1, stroke=1)
    
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 0.5*cm, info_top - 0.5*cm, f"Pasante: {pasante.get('nombres', '')} {pasante.get('apellidos', '')}")
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, info_top - 1.0*cm, f"C.I.: {pasante.get('ci', '—')}   ·   Carrera: {pasante.get('carrera', '—')}")
    
    if pasante.get('proyecto'):
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(x + 0.5*cm, info_top - 1.45*cm, f"Proyecto: {pasante.get('proyecto')}")

    # 3. Tabla de Asistencias
    tabla_top = info_top - info_h - 0.2*cm
    header_h = 0.8 * cm
    fila_h = 0.7 * cm
    
    # Encabezado Tabla Azul
    c.setFillColor(AZUL_TABLA)
    c.rect(x, tabla_top - header_h, W_UTIL, header_h, fill=1, stroke=0)
    
    headers = ["Fecha", "Entrada", "Salida", "Horas", "Acumuladas", "Detalle/Estado"] if variant=="week" else ["Fecha", "Entrada", "Salida", "Horas", "Actividades realizadas", "Estado"]
    col_widths = [2.5*cm, 2.0*cm, 2.0*cm, 1.5*cm, 2.5*cm, 7.3*cm] if variant=="week" else [2.5*cm, 2.0*cm, 2.0*cm, 1.5*cm, 7.5*cm, 2.3*cm]
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 8)
    cur_x = x
    for i, h_txt in enumerate(headers):
        c.drawString(cur_x + 0.2*cm, tabla_top - 0.5*cm, h_txt)
        cur_x += col_widths[i]

    # Filas
    cur_y = tabla_top - header_h
    for i, fila in enumerate(filas):
        # Fondo cebra
        if i % 2 == 0:
            c.setFillColor(BLANCO)
        else:
            c.setFillColor(colors.HexColor("#f1f5f9"))
        c.rect(x, cur_y - fila_h, W_UTIL, fila_h, fill=1, stroke=0)
        
        # Borde inferior fila
        c.setStrokeColor(GRIS_BORDE)
        c.line(x, cur_y - fila_h, x + W_UTIL, cur_y - fila_h)
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)
        
        # Datos
        c.drawString(x + 0.2*cm, cur_y - 0.45*cm, _fmt_fecha(fila.get('fecha')))
        c.drawString(x + col_widths[0] + 0.2*cm, cur_y - 0.45*cm, _fmt_hora(fila.get('hora_entrada')))
        c.drawString(x + sum(col_widths[:2]) + 0.2*cm, cur_y - 0.45*cm, _fmt_hora(fila.get('hora_salida')))
        
        horas = fila.get('horas_trabajadas')
        c.drawString(x + sum(col_widths[:3]) + 0.2*cm, cur_y - 0.45*cm, f"{horas}h" if horas else "—")
        
        if variant == "week":
            acum = fila.get('horas_acumuladas', 0)
            c.drawString(x + sum(col_widths[:4]) + 0.2*cm, cur_y - 0.45*cm, f"{acum}h")
            c.drawString(x + sum(col_widths[:5]) + 0.2*cm, cur_y - 0.45*cm, fila.get('detalle', ''))
        else:
            # Texto actividades (truncado si es muy largo)
            act = fila.get('actividades', 'Sin reporte')[:55] + "..." if len(fila.get('actividades', '')) > 55 else fila.get('actividades', 'Sin reporte')
            c.drawString(x + sum(col_widths[:4]) + 0.2*cm, cur_y - 0.45*cm, act)
            
            # Badge de Estado
            estado = (fila.get('estado') or 'PENDIENTE').upper()
            badge_w, badge_h = 2.0*cm, 0.45*cm
            bx = x + sum(col_widths[:5]) + (col_widths[5]-badge_w)/2
            by = cur_y - 0.55*cm
            c.setFillColor(_estado_color(estado))
            c.roundRect(bx, by, badge_w, badge_h, 4, fill=1, stroke=0)
            c.setFillColor(BLANCO)
            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(bx + badge_w/2, by + 0.12*cm, estado)
            
        cur_y -= fila_h

    # 4. Línea de Totales (azul claro)
    total_y = cur_y
    c.setFillColor(colors.HexColor("#e0f2fe"))
    c.rect(x, total_y - 0.8*cm, W_UTIL, 0.8*cm, fill=1, stroke=0)
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 8)
    
    sum_horas = sum(float(f.get('horas_trabajadas') or 0) for f in filas)
    txt_total = f"Total: {len(filas)} días  ·  {sum_horas:.1f} horas acumuladas  ·  {sum(1 for f in filas if f.get('actividades'))} reportes enviados"
    c.drawString(x + 0.4*cm, total_y - 0.5*cm, txt_total)

    # 5. Firmas (4 líneas)
    f_y = total_y - 2.5*cm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    
    # Líneas de firma
    fw = 4.5*cm
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y) # Pasante
    c.line(x + W_UTIL - fw - 0.5*cm, f_y, x + W_UTIL - 0.5*cm, f_y) # Tutor
    
    f_y2 = f_y - 1.5*cm
    c.line(x + 0.5*cm, f_y2, x + 0.5*cm + fw, f_y2) # Coordinador
    c.line(x + W_UTIL - fw - 0.5*cm, f_y2, x + W_UTIL - 0.5*cm, f_y2) # Docente

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + 0.5*cm + fw/2, f_y - 0.4*cm, "Pasante")
    c.drawCentredString(x + W_UTIL - fw/2 - 0.5*cm, f_y - 0.4*cm, "Tutor Institucional")
    c.drawCentredString(x + 0.5*cm + fw/2, f_y2 - 0.4*cm, "Coordinador")
    c.drawCentredString(x + W_UTIL - fw/2 - 0.5*cm, f_y2 - 0.4*cm, "Docente de la UMSA")

# API PÚBLICA (Funciones llamadas desde las rutas)

def generar_reporte_semanal(pasante: dict, filas: list, titulo: str) -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, variant="week")
    c.save()
    buf.seek(0)
    return buf

def generar_reporte_mensual(pasante: dict, filas: list, titulo: str) -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    # Si hay muchas filas, aquí se podría implementar paginación, por ahora una hoja:
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, variant="default")
    c.save()
    buf.seek(0)
    return buf