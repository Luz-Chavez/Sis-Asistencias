import io
from datetime import date, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit

W, H = A4   # 595 x 842 pt

# ── Paleta institucional ──────────────────────────────────────────────────────
AZUL_OSCURO = colors.HexColor("#1e3a5f")
AZUL_TABLA  = colors.HexColor("#2563eb")
GRIS_FONDOS = colors.HexColor("#f8fafc")
GRIS_BORDE  = colors.HexColor("#e2e8f0")
BLANCO      = colors.white

MARGIN = 1.5 * cm
W_UTIL = W - 2 * MARGIN

def _fmt_hora(dt) -> str:
    if dt is None: return "—"
    if isinstance(dt, str): return dt[:5]
    return dt.strftime("%H:%M")

def _fmt_fecha(d) -> str:
    if d is None: return "—"
    if isinstance(d, str): d = date.fromisoformat(d)
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return f"{dias[d.weekday()]} {d.day:02d}/{d.month:02d}"

# ── DIBUJO DEL BLOQUE UNIFICADO ──────────────────────────────────────────────
def _draw_bloque(c: canvas.Canvas, pasante: dict, filas: list, titulo: str, y_top: float, texto_reporte: str = ""):
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

    # 2. Banda Datos del Pasante
    info_h = 2.0 * cm
    info_top = y_top - cab_h
    c.setFillColor(GRIS_FONDOS)
    c.rect(x, info_top - info_h, W_UTIL, info_h, fill=1, stroke=1)
    
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 0.5*cm, info_top - 0.5*cm, f"Pasante: {pasante.get('nombres', '')} {pasante.get('apellidos', '')}")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, info_top - 0.95*cm, f"C.I.: {pasante.get('ci', '—')}   ·   RU: {pasante.get('ru', '—')}")
    
    mitad_x = x + (W_UTIL / 2) - 1.5 * cm
    c.drawString(mitad_x, info_top - 0.5*cm, f"Carrera: {pasante.get('carrera', '—')}")
    c.drawString(mitad_x, info_top - 0.95*cm, f"Unidad Asignada: {pasante.get('unidad_asignada', '—')}")
    
    if pasante.get('proyecto'):
        c.setFont("Helvetica-Oblique", 7.5)
        c.drawString(x + 0.5*cm, info_top - 1.45*cm, f"Proyecto: {pasante.get('proyecto')}")

    # 3. Tabla de Asistencias (UNIFICADA)
    tabla_top = info_top - info_h - 0.2*cm
    header_h = 0.8 * cm
    
    # Truco: Si hay muchos días (mensual), hacemos las filas más angostas para que entre todo en 1 hoja
    fila_h = 0.55 * cm if len(filas) > 10 else 0.7 * cm
    
    c.setFillColor(AZUL_TABLA)
    c.rect(x, tabla_top - header_h, W_UTIL, header_h, fill=1, stroke=0)
    
    headers = ["Fecha", "Entrada", "Salida", "Horas", "Acumuladas", "Detalle/Estado"]
    col_widths = [2.5*cm, 2.0*cm, 2.0*cm, 1.5*cm, 2.5*cm, 7.3*cm]
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 8)
    cur_x = x
    for i, h_txt in enumerate(headers):
        c.drawString(cur_x + 0.2*cm, tabla_top - 0.5*cm, h_txt)
        cur_x += col_widths[i]

    cur_y = tabla_top - header_h
    for i, fila in enumerate(filas):
        if i % 2 == 0:
            c.setFillColor(BLANCO)
        else:
            c.setFillColor(colors.HexColor("#f1f5f9"))
        c.rect(x, cur_y - fila_h, W_UTIL, fila_h, fill=1, stroke=0)
        
        c.setStrokeColor(GRIS_BORDE)
        c.line(x, cur_y - fila_h, x + W_UTIL, cur_y - fila_h)
        
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 8)
        
        c.drawString(x + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_fecha(fila.get('fecha')))
        c.drawString(x + col_widths[0] + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_hora(fila.get('hora_entrada')))
        c.drawString(x + sum(col_widths[:2]) + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_hora(fila.get('hora_salida')))
        
        horas = fila.get('horas_trabajadas')
        c.drawString(x + sum(col_widths[:3]) + 0.2*cm, cur_y - (fila_h * 0.65), f"{horas}h" if horas else "—")
        
        acum = fila.get('horas_acumuladas', 0)
        c.drawString(x + sum(col_widths[:4]) + 0.2*cm, cur_y - (fila_h * 0.65), f"{acum}h")
        c.drawString(x + sum(col_widths[:5]) + 0.2*cm, cur_y - (fila_h * 0.65), fila.get('detalle', ''))
            
        cur_y -= fila_h

    # Bloque de Texto del Reporte (AHORA PARA AMBOS)
    if texto_reporte:
        cur_y -= 0.5 * cm 
        
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(AZUL_OSCURO)
        c.drawString(x, cur_y, "Resumen de Actividades / Reporte:")
        cur_y -= 0.2 * cm
        
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.black)
        lineas = simpleSplit(texto_reporte, "Helvetica", 8, W_UTIL - 1 * cm)
        
        alto_linea = 0.4 * cm
        alto_caja = (len(lineas) * alto_linea) + 0.6 * cm
        
        c.setFillColor(GRIS_FONDOS)
        c.setStrokeColor(GRIS_BORDE)
        cur_y -= alto_caja
        c.rect(x, cur_y, W_UTIL, alto_caja, fill=1, stroke=1)
        
        c.setFillColor(colors.black)
        texto_y = cur_y + alto_caja - 0.5 * cm
        for linea in lineas:
            c.drawString(x + 0.5 * cm, texto_y, linea)
            texto_y -= alto_linea
            
        cur_y -= 0.3 * cm 

    # 4. Línea de Totales
    total_y = cur_y
    c.setFillColor(colors.HexColor("#e0f2fe"))
    c.rect(x, total_y - 0.8*cm, W_UTIL, 0.8*cm, fill=1, stroke=0)
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 8)
    
    dias_asistidos = sum(1 for f in filas if f.get('hora_entrada') is not None)
    sum_horas = sum(float(f.get('horas_trabajadas') or 0) for f in filas)
    txt_total = f"Días asistidos: {dias_asistidos}   ·   {sum_horas:.2f} horas acumuladas"
    
    c.drawString(x + 0.4*cm, total_y - 0.5*cm, txt_total)

    # 5. Firmas
    f_y = total_y - 2.5*cm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    
    fw = 4.5*cm
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y) 
    c.line(x + W_UTIL - fw - 0.5*cm, f_y, x + W_UTIL - 0.5*cm, f_y) 
    
    f_y2 = f_y - 1.5*cm
    c.line(x + 0.5*cm, f_y2, x + 0.5*cm + fw, f_y2) 
    c.line(x + W_UTIL - fw - 0.5*cm, f_y2, x + W_UTIL - 0.5*cm, f_y2) 

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + 0.5*cm + fw/2, f_y - 0.4*cm, "Pasante")
    c.drawCentredString(x + W_UTIL - fw/2 - 0.5*cm, f_y - 0.4*cm, "Tutor Institucional")
    c.drawCentredString(x + 0.5*cm + fw/2, f_y2 - 0.4*cm, "Coordinador")
    c.drawCentredString(x + W_UTIL - fw/2 - 0.5*cm, f_y2 - 0.4*cm, "Docente de la UMSA")

# ── API PÚBLICA ───────────────────────────────────────────────────────────────

def generar_reporte_semanal(pasante: dict, filas: list, titulo: str, texto_reporte: str = "") -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, texto_reporte=texto_reporte)
    c.save()
    buf.seek(0)
    return buf

def generar_reporte_mensual(pasante: dict, filas: list, titulo: str, texto_reporte: str = "") -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, texto_reporte=texto_reporte)
    c.save()
    buf.seek(0)
    return buf