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
    if isinstance(d, str):
        # Intentar formato ISO primero, luego DD/MM/YYYY
        try:
            d = date.fromisoformat(d)
        except ValueError:
            # Formato DD/MM/YYYY
            if '/' in d:
                parts = d.split('/')
                if len(parts) == 3:
                    d = date(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                return d  # Devolver string si no se puede parsear
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    return f"{dias[d.weekday()]} {d.day:02d}/{d.month:02d}"

# ── DIBUJO DEL BLOQUE UNIFICADO ──────────────────────────────────────────────
def _draw_bloque(c: canvas.Canvas, pasante: dict, filas: list, titulo: str, y_top: float, texto_reporte: str = "", anio: int = None, semana: int = None):
    """"Dibuja el bloque principal del reporte PDF."""
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
    
    # Agregar rango de fechas de la semana si es reporte semanal
    if anio is not None and semana is not None and "Semanal" in titulo:
        # Calcular rango de fechas (lunes a viernes de esa semana)
        from datetime import datetime, timedelta
        try:
            # Calcular lunes de la semana
            fecha_lunes = datetime.strptime(f"{anio}-01-01", "%Y-%m-%d")
            if semana > 1:
                fecha_lunes += timedelta(weeks=semana-1)
            
            # Ajustar al lunes de esa semana
            dias_lunes = fecha_lunes.weekday()
            if dias_lunes != 0:
                fecha_lunes -= timedelta(days=dias_lunes)
            
            # Calcular viernes
            fecha_viernes = fecha_lunes + timedelta(days=4)
            
            # Mostrar rango
            rango_texto = f"Semana {semana}: {fecha_lunes.strftime('%d/%m/%Y')} al {fecha_viernes.strftime('%d/%m/%Y')} (Lun-Vie)"
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColor(colors.HexColor("#6b7280"))
            c.drawString(x + 0.5*cm, y_top - 1.5*cm, rango_texto)
        except Exception as e:
            print(f"[pdf] Error calculando rango de fechas: {e}")
            pass  # Si hay error, no mostrar rango

    # 2. Banda Datos del Pasante
    info_h = 2.5 * cm
    info_top = y_top - cab_h
    c.setFillColor(GRIS_FONDOS)
    c.rect(x, info_top - info_h, W_UTIL, info_h, fill=1, stroke=1)
    
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 0.5*cm, info_top - 0.5*cm, f"Pasante: {pasante.get('nombres', '')} {pasante.get('apellidos', '')}")
    
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, info_top - 0.95*cm, f"C.I.: {pasante.get('carnet_identidad', '—')}")
    c.drawString(x + 0.5*cm, info_top - 1.15*cm, f"RU: {pasante.get('ru', '—')}")
    
    mitad_x = x + (W_UTIL / 2) - 1.5 * cm
    c.drawString(mitad_x, info_top - 0.5*cm, f"Carrera: {pasante.get('carrera', '—')}")
    c.drawString(mitad_x, info_top - 0.95*cm, f"Proyecto: {pasante.get('proyecto', '—')}")
    
    # 3. Tabla de Asistencias (UNIFICADA)
    tabla_top = info_top - info_h - 0.2*cm
    header_h = 0.8 * cm
    
    # Truco: Si hay muchos días (mensual), hacemos las filas más angostas para que entre todo en 1 hoja
    fila_h = 0.55 * cm if len(filas) > 10 else 0.7 * cm
    
    c.setFillColor(AZUL_TABLA)
    c.rect(x, tabla_top - header_h, W_UTIL, header_h, fill=1, stroke=0)
    
    headers = ["Fecha", "Entrada", "Salida", "Horas", "Estado Admin", "Estado Encargado", "Comentarios"]
    col_widths = [2.2*cm, 1.5*cm, 1.5*cm, 1.2*cm, 1.8*cm, 1.8*cm, 6.0*cm]
    
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
        c.setFont("Helvetica", 7)  # Reducir fuente para que quepa todo
        
        # Fecha
        c.drawString(x + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_fecha(fila.get('fecha')))
        
        # Entrada y Salida
        c.drawString(x + col_widths[0] + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_hora(fila.get('hora_entrada')))
        c.drawString(x + sum(col_widths[:2]) + 0.2*cm, cur_y - (fila_h * 0.65), _fmt_hora(fila.get('hora_salida')))
        
        # Horas
        horas = fila.get('horas_trabajadas')
        c.drawString(x + sum(col_widths[:3]) + 0.2*cm, cur_y - (fila_h * 0.65), f"{horas}h" if horas != "—" else "—")
        
        # Estado con color (mostrar estado combinado)
        estado = fila.get('estado_admin') or fila.get('estado_encargado') or 'SIN REGISTRO'
        if estado == 'APROBADO' or estado == 'VERIFICADO':
            c.setFillColor(colors.HexColor("#16a34a"))
        elif estado == 'RECHAZADO':
            c.setFillColor(colors.HexColor("#dc2626"))
        elif estado == 'RECTIFICADO':
            c.setFillColor(colors.HexColor("#f59e0b"))
        else:
            c.setFillColor(colors.HexColor("#6b7280"))
        c.drawString(x + sum(col_widths[:4]) + 0.2*cm, cur_y - (fila_h * 0.65), estado)
        
        # Estado Admin
        c.setFillColor(colors.black)
        estado_admin = fila.get('estado_admin', 'SIN REGISTRO')
        c.drawString(x + sum(col_widths[:5]) + 0.2*cm, cur_y - (fila_h * 0.65), estado_admin)
        
        # Estado Encargado
        estado_encargado = fila.get('estado_encargado', 'SIN REGISTRO')
        c.drawString(x + sum(col_widths[:6]) + 0.2*cm, cur_y - (fila_h * 0.65), estado_encargado)
        
        # Comentarios (con truncamiento si es muy largo)
        c.setFillColor(colors.black)
        comentario = fila.get('comentarios_director') or fila.get('actividades') or ''
        if comentario and len(comentario) > 40:
            comentario = comentario[:37] + "..."
        c.drawString(x + sum(col_widths[:7]) + 0.2*cm, cur_y - (fila_h * 0.65), comentario)
            
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
            
        cur_y -= alto_caja + 0.5*cm 

    
    # Buscar último estado del encargado
    ultimo_estado_encargado = 'SIN REGISTRO'
    for fila in filas:
        estado_enc = fila.get('estado_encargado', '')
        if estado_enc in ['VERIFICADO', 'RECTIFICADO', 'PENDIENTE']:
            ultimo_estado_encargado = estado_enc
    
    # Buscar último estado del admin
    ultimo_estado_admin = 'SIN REGISTRO'
    for fila in filas:
        estado_adm = fila.get('estado_admin', '')
        if estado_adm in ['APROBADO', 'RECHAZADO', 'PENDIENTE']:
            ultimo_estado_admin = estado_adm
    
    # Mostrar los últimos estados
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.4*cm, cur_y - 1.5*cm, f"Último Estado Encargado: {ultimo_estado_encargado}")
    c.drawString(x + 0.4*cm, cur_y - 1.8*cm, f"Último Estado Administrador: {ultimo_estado_admin}")
    
    # Nota final
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.gray)
    nota_final = "Los estados reflejan la última actualización realizada por los responsables."
    lineas_nota = simpleSplit(nota_final, "Helvetica-Oblique", 7, W_UTIL - 1.0*cm)
    for i, linea in enumerate(lineas_nota):
        c.drawString(x + 0.4*cm, cur_y - 2.3*cm + i*0.3*cm, linea)

    # 5. FIRMAS PROFESIONALES
    f_y = cur_y - 2.5*cm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    
    # Título de firmas
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, f_y, "FIRMAS DE VALIDACIÓN")
    f_y -= 0.8*cm
    
    # Línea horizontal superior
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.line(x + 0.5*cm, f_y, x + W_UTIL - 0.5*cm, f_y)
    f_y -= 0.3*cm
    
    # Primera firma - Pasante
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, f_y, f"Firma del Pasante: {pasante.get('nombres', '')} {pasante.get('apellidos', '')}")
    f_y -= 0.5*cm
    
    # Línea de firma
    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)
    fw = 7.0*cm
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y)
    f_y -= 0.4*cm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.gray)
    c.drawString(x + 0.5*cm, f_y, f"Fecha: _______________________")
    f_y -= 0.8*cm
    
    # Segunda firma - Administrador
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, f_y, "Firma del Administrador:")
    f_y -= 0.5*cm
    
    # Línea de firma
    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y)
    f_y -= 0.4*cm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.gray)
    c.drawString(x + 0.5*cm, f_y, f"Fecha: _______________________")
    f_y -= 0.8*cm
    
    # Tercera firma - Encargado
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    c.drawString(x + 0.5*cm, f_y, "Firma del Encargado:")
    f_y -= 0.5*cm
    
    # Línea de firma
    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y)
    f_y -= 0.4*cm
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.gray)
    c.drawString(x + 0.5*cm, f_y, f"Fecha: _______________________")
    f_y -= 0.8*cm
    
    # Nota final
    c.setFont("Helvetica-Oblique", 7)
    c.setFillColor(colors.gray)
    nota_final = "Las firmas certifican la veracidad y aprobación de la información contenida en este reporte."
    lineas_nota = simpleSplit(nota_final, "Helvetica-Oblique", 7, W_UTIL - 1.0*cm)
    for i, linea in enumerate(lineas_nota):
        c.drawString(x + 0.5*cm, f_y + i*0.3*cm, linea)
    
    # Marco final de firmas
    c.setStrokeColor(colors.black)
    c.setLineWidth(1.0)
    c.rect(x + 0.3*cm, total_y - 2.5*cm, W_UTIL - 0.6*cm, f_y - total_y + 2.5*cm + 0.3*cm, fill=0, stroke=1)

# ── API PÚBLICA ───────────────────────────────────────────────────────────────

def generar_reporte_diario(pasante: dict, filas: list, titulo: str, texto_reporte: str = "") -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, texto_reporte=texto_reporte)
    c.save()
    buf.seek(0)
    return buf

def generar_reporte_semanal(pasante: dict, filas: list, titulo: str, texto_reporte: str = "", anio: int = None, semana: int = None) -> io.BytesIO:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    _draw_bloque(c, pasante, filas, titulo, H - MARGIN, texto_reporte=texto_reporte, anio=anio, semana=semana)
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

def generar_reporte_historial_completo(pasante: dict, filas: list, titulo: str) -> io.BytesIO:
    """Genera un PDF con el historial completo de asistencias de un pasante."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    
    # Usar la misma función de dibujo base pero adaptada para historial completo
    _draw_bloque_historial_completo(c, pasante, filas, titulo, H - MARGIN)
    
    c.save()
    buf.seek(0)
    return buf

def _draw_bloque_historial_completo(c: canvas.Canvas, pasante: dict, filas: list, titulo: str, y_top: float):
    """Dibuja el bloque específico para historial completo."""
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
    
    # 2. Datos del Pasante
    y = y_top - cab_h - 1.0*cm
    c.setFillColor(AZUL_TABLA)
    c.rect(x, y - 1.2*cm, W_UTIL, 1.2*cm, fill=1, stroke=0)
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 0.4*cm, y - 0.4*cm, f"{pasante['nombres']} {pasante['apellidos']}")
    c.setFont("Helvetica", 7)
    c.drawString(x + 0.4*cm, y - 0.8*cm, f"CI: {pasante['ci']} · Usuario: {pasante['username']} · Carrera: {pasante['carrera']}")
    c.drawRightString(x + W_UTIL - 0.4*cm, y - 0.4*cm, f"Total Registros: {pasante['total_asistencias']}")
    
    # 3. Tabla de Historial
    y -= 2.5*cm
    
    # Encabezados de tabla
    headers = [
        ("Fecha", 2.5*cm),
        ("Entrada", 1.5*cm),
        ("Salida", 1.5*cm),
        ("Horas", 1.5*cm),
        ("Estado", 2.0*cm),
        ("Actividades", 4.0*cm),
        ("Comentarios", 3.0*cm)
    ]
    
    # Dibujar encabezados
    c.setFillColor(GRIS_FONDOS)
    c.rect(x, y - 0.8*cm, W_UTIL, 0.8*cm, fill=1, stroke=1)
    c.setFillColor(AZUL_OSCURO)
    c.setFont("Helvetica-Bold", 7)
    
    x_cur = x
    for header, width in headers:
        c.drawString(x_cur + 0.2*cm, y - 0.5*cm, header)
        x_cur += width
    
    # Datos de la tabla
    y -= 0.8*cm
    row_h = 0.6*cm
    
    for i, fila in enumerate(filas):
        if y - row_h < MARGIN + 2*cm:  # Espacio para firmas
            # Nueva página
            c.showPage()
            y = H - MARGIN - cab_h - 1.0*cm
            
            # Redibujar encabezados en nueva página
            c.setFillColor(GRIS_FONDOS)
            c.rect(x, y - 0.8*cm, W_UTIL, 0.8*cm, fill=1, stroke=1)
            c.setFillColor(AZUL_OSCURO)
            c.setFont("Helvetica-Bold", 7)
            x_cur = x
            for header, width in headers:
                c.drawString(x_cur + 0.2*cm, y - 0.5*cm, header)
                x_cur += width
            y -= 0.8*cm
        
        # Fila de datos
        if i % 2 == 0:
            c.setFillColor(GRIS_FONDOS)
            c.rect(x, y - row_h, W_UTIL, row_h, fill=1, stroke=0)
        else:
            c.setFillColor(BLANCO)
            c.rect(x, y - row_h, W_UTIL, row_h, fill=1, stroke=1)
        
        # Datos de la fila
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 6)
        
        x_cur = x
        datos = [
            _fmt_fecha(fila.get('fecha')),
            _fmt_hora(fila.get('hora_entrada')),
            _fmt_hora(fila.get('hora_salida')),
            f"{fila.get('horas_trabajadas', 0):.1f}h" if fila.get('horas_trabajadas') else "—",
            fila.get('estado_admin') or fila.get('estado_encargado') or 'PENDIENTE',
            (fila.get('actividades') or "—")[:40],  # Limitar texto
            (fila.get('comentarios_director') or "—")[:30]  # Limitar texto
        ]
        
        for j, (dato, width) in enumerate(zip(datos, [w for _, w in headers])):
            if j == 4:  # Estado con color
                estado = (fila.get('estado_admin') or fila.get('estado_encargado') or 'PENDIENTE').upper()
                if estado == 'APROBADO' or estado == 'VERIFICADO':
                    c.setFillColor(colors.HexColor("#16a34a"))
                elif estado == 'RECHAZADO':
                    c.setFillColor(colors.HexColor("#dc2626"))
                elif estado == 'RECTIFICADO':
                    c.setFillColor(colors.HexColor("#f59e0b"))
                else:
                    c.setFillColor(colors.HexColor("#6b7280"))
            else:
                c.setFillColor(colors.black)
            
            # Texto con truncamiento
            texto = simpleSplit(dato, "Helvetica", 6, width - 0.4*cm)
            if texto:
                c.drawString(x_cur + 0.2*cm, y - 0.4*cm, texto[0])
            x_cur += width
        
        y -= row_h
    
    # 4. Resumen
    if y - 2*cm < MARGIN + 2*cm:
        c.showPage()
        y = H - MARGIN - cab_h - 1.0*cm
    
    y -= 1.0*cm
    c.setFillColor(AZUL_TABLA)
    c.rect(x, y - 1.0*cm, W_UTIL, 1.0*cm, fill=1, stroke=0)
    
    c.setFillColor(BLANCO)
    c.setFont("Helvetica-Bold", 8)
    
    dias_asistidos = sum(1 for f in filas if f.get('hora_entrada') is not None)
    sum_horas = sum(float(f.get('horas_trabajadas') or 0) for f in filas)
    aprobados = sum(1 for f in filas if f.get('estado_admin') == 'APROBADO')
    verificados = sum(1 for f in filas if f.get('estado_encargado') == 'VERIFICADO')
    
    resumen_texto = (f"Días asistidos: {dias_asistidos} | Horas totales: {sum_horas:.1f}h | "
                     f"Aprobados: {aprobados} | Verificados: {verificados}")
    
    c.drawString(x + 0.4*cm, y - 0.5*cm, resumen_texto)
    
    # 5. Firmas
    f_y = y - 2.5*cm
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    
    fw = 4.5*cm
    c.line(x + 0.5*cm, f_y, x + 0.5*cm + fw, f_y)
    c.line(x + W_UTIL - fw - 0.5*cm, f_y, x + W_UTIL - 0.5*cm, f_y)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x + 0.5*cm + fw/2, f_y - 0.4*cm, "Pasante")
    c.drawCentredString(x + W_UTIL - fw/2 - 0.5*cm, f_y - 0.4*cm, "Encargado de Carrera")
    
    # Nota al pie
    c.setFont("Helvetica-Oblique", 6)
    c.setFillColor(colors.gray)
    nota_texto = f"Documento generado el {pasante['fecha_generacion']} · Historial completo de asistencias"
    c.drawCentredString(W/2, MARGIN + 0.5*cm, nota_texto)