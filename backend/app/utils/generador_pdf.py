import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generar_comprobante_pdf(datos_reporte: dict) -> io.BytesIO:
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()

    estilo_titulo = styles['Heading1']
    estilo_titulo.alignment = 1 

    estilo_subtitulo = styles['Heading3']
    estilo_subtitulo.alignment = 1
    
    story.append(Paragraph("Comprobante de Asistencia y Reporte Diario", estilo_titulo))
    story.append(Paragraph("Facultad de Ciencias Sociales - UMSA", estilo_subtitulo))
    story.append(Spacer(1, 20)) 

    datos_pasante = [
        ["Pasante:", datos_reporte.get("pasante_nombre", "")],
        ["Carrera:", datos_reporte.get("carrera_nombre", "No asignada")],
        ["Fecha del Reporte:", str(datos_reporte.get("fecha", ""))]
    ]
    
    tabla_pasante = Table(datos_pasante, colWidths=[120, 350])
    tabla_pasante.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(tabla_pasante)
    story.append(Spacer(1, 20))

    datos_tiempos = [
        ["Hora de Entrada", "Hora de Salida", "Total Horas"],
        [
            str(datos_reporte.get("hora_entrada", "")),
            str(datos_reporte.get("hora_salida", "Sin marcar")),
            str(datos_reporte.get("horas_trabajadas", 0)) + " hrs"
        ]
    ]
    
    tabla_tiempos = Table(datos_tiempos, colWidths=[150, 150, 150])
    tabla_tiempos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")), # Azul oscuro
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8)
    ]))
    story.append(tabla_tiempos)
    story.append(Spacer(1, 25))

    story.append(Paragraph("Actividades Realizadas:", styles['Heading4']))
    estilo_texto = styles['Normal']
    estilo_texto.leading = 14 
    
    texto_actividades = datos_reporte.get("actividades", "No se registraron actividades.")
    story.append(Paragraph(texto_actividades, estilo_texto))
    
    story.append(Spacer(1, 60))

    estilo_firma = styles['Normal']
    estilo_firma.alignment = 1
    story.append(Paragraph("___________________________________", estilo_firma))
    story.append(Paragraph("Firma / Sello de Revisión", estilo_firma))

    doc.build(story)
    buffer.seek(0)
    
    return buffer