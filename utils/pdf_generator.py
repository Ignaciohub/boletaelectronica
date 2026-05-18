"""Generador de PDFs para boletas electrónicas"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
from models.boleta import Boleta


class PDFGenerator:
    """Genera PDFs de boletas electrónicas"""
    
    def __init__(self):
        """Inicializa el generador de PDFs"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        # Estilo para el título
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        ))
    
    def generar_boleta_pdf(self, boleta: Boleta, filepath: str, 
                          nombre_negocio: str = "Negocio de Informática",
                          rut_negocio: str = "12.345.678-9",
                          direccion_negocio: str = "Av. Principal 123",
                          telefono_negocio: str = "+56 9 1234 5678"):
        """
        Genera un PDF de la boleta
        
        Args:
            boleta: Objeto Boleta a imprimir
            filepath: Ruta donde guardar el PDF
            nombre_negocio: Nombre del negocio
            rut_negocio: RUT del negocio
            direccion_negocio: Dirección del negocio
            telefono_negocio: Teléfono del negocio
        """
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Encabezado del negocio
        title = Paragraph(nombre_negocio, self.styles['CustomTitle'])
        story.append(title)
        
        negocio_info = f"""
        <para align=center>
        RUT: {rut_negocio}<br/>
        {direccion_negocio}<br/>
        Tel: {telefono_negocio}
        </para>
        """
        story.append(Paragraph(negocio_info, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Título de boleta
        boleta_title = Paragraph(
            f"<para align=center><b>BOLETA ELECTRÓNICA N° {boleta.numero}</b></para>",
            self.styles['CustomHeading']
        )
        story.append(boleta_title)
        story.append(Spacer(1, 0.2*inch))
        
        # Información de la boleta y cliente
        fecha_formateada = boleta.fecha.strftime("%d/%m/%Y %H:%M")
        
        info_data = [
            ['Fecha:', fecha_formateada, 'Cliente:', boleta.cliente_nombre],
            ['', '', 'RUT:', boleta.cliente_rut]
        ]
        
        info_table = Table(info_data, colWidths=[1*inch, 2*inch, 1*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Tabla de items
        items_data = [['Descripción', 'Cant.', 'Precio Unit.', 'Subtotal']]
        
        for item in boleta.items:
            items_data.append([
                item.descripcion,
                str(item.cantidad),
                f"${item.precio_unitario:,.0f}",
                f"${item.subtotal:,.0f}"
            ])
        
        items_table = Table(items_data, colWidths=[3.5*inch, 0.7*inch, 1.2*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a90e2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Contenido
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            
            # Bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternancia de colores en filas
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Totales
        totales_data = [
            ['', '', 'Subtotal:', f"${boleta.subtotal:,.0f}"],
            ['', '', 'IVA (19%):', f"${boleta.iva:,.0f}"],
            ['', '', 'TOTAL:', f"${boleta.total:,.0f}"]
        ]
        
        totales_table = Table(totales_data, colWidths=[3.5*inch, 0.7*inch, 1.2*inch, 1.2*inch])
        totales_table.setStyle(TableStyle([
            ('FONTNAME', (2, 0), (2, 1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 0), (-1, -1), 11),
            ('FONTSIZE', (2, 2), (-1, 2), 13),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('LINEABOVE', (2, 2), (-1, 2), 2, colors.black),
            ('TEXTCOLOR', (2, 2), (-1, 2), colors.HexColor('#1a1a1a')),
        ]))
        story.append(totales_table)
        
        # Observaciones
        if boleta.observaciones:
            story.append(Spacer(1, 0.3*inch))
            obs_title = Paragraph('<b>Observaciones:</b>', self.styles['Normal'])
            story.append(obs_title)
            observaciones = Paragraph(boleta.observaciones, self.styles['Normal'])
            story.append(observaciones)
        
        # Pie de página
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            '<para align=center><i>Gracias por su compra</i></para>',
            self.styles['Normal']
        )
        story.append(footer)
        
        # Generar el PDF
        doc.build(story)
        return filepath
