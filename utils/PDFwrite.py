from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import re
import io

def write_content_to_area(x, y, width, height, content, pdf_address, result_address, display_assist=False):
    
    """
    Writes the given content into the designated area of the PDF template and saves the result to result_address.

    Parameters:
    - x (float): The x-coordinate of the lower-left corner of the area.
    - y (float): The y-coordinate of the lower-left corner of the area.
    - width (float): The width of the area.
    - height (float): The height of the area.
    - content (str): The text content to write.
    - pdf_address (str): The path to the template PDF file.
    - result_address (str): The path to the output PDF file.
    """
    
    # Create a PDF in memory with the content
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=LETTER)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='Bold',
        parent=styles['CustomNormal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceAfter=14
    ))
    styles.add(ParagraphStyle(
        name='Section',
        parent=styles['Bold'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        spaceAfter=16
    ))
    styles.add(ParagraphStyle(
        name='CustomBullet',
        parent=styles['CustomNormal'],
        leftIndent=20,
        firstLineIndent=-10,
        fontSize=11,
        leading=14,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Section'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        spaceAfter=20
    ))
    
    if display_assist:
        # Draw a black border around the area
        c.setStrokeColor(colors.black)
        c.rect(x, y, width, height, stroke=1, fill=0)

        # Draw a red dot at (x, y)
        c.setFillColor(colors.red)
        c.circle(x, y, 5, fill=1)  # radius 5, filled
        c.setFillColor(colors.black)  # Reset color to black for text

    # Starting position (top-left of the area)
    current_y = y + height
    max_width = width

    def process_inline_bold(text):
        # Then process any remaining text for bold formatting
        parts = []
        last_end = 0
        for match in re.finditer(r'\*([^*]+)\*', text):
            
            # Add the text before the bold section
            if match.start() > last_end:
                parts.append(text[last_end:match.start()].replace('*', ''))
            
            # Add the bold text without asterisks
            parts.append(f"<b>{match.group(1)}</b>")
            
            last_end = match.end()
            
        # Add any remaining text
        if last_end < len(text):
            parts.append(text[last_end:].replace('*', ''))
            
        return ''.join(parts)
    
    
    def process_inline_link(text):
        
        # Then process any remaining text for bold formatting
        parts = []
        last_end = 0
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
            
            # Add the text before the bold section
            if match.start() > last_end:
                parts.append(text[last_end:match.start()].replace('[', '').replace(']', '').replace('(', '').replace(')', ''))
            
            # Add the bold text without asterisks
            parts.append(f"<a href='{match.group(2)}'>{match.group(1)}</a>")
            
            last_end = match.end()
            
        # Add any remaining text
        if last_end < len(text):
            parts.append(text[last_end:].replace('[', '').replace(']', '').replace('(', '').replace(')', ''))
            
        return ''.join(parts)
    
    def draw_line(canvas, x, y, width, line_type='normal'):
        """Draw a horizontal line at the specified position"""
        if line_type == 'bold':
            canvas.setLineWidth(2)
        else:
            canvas.setLineWidth(1)
        canvas.line(x, y, x + width, y)
        canvas.setLineWidth(1)  # Reset line width
    
    for line in content.split('\n'):
        add_space = False
        line = line.strip()
        if not line:
            current_y -= 6  # Add space between paragraphs
            continue
            
        # Handle different line types
        if line.startswith('***') and line.endswith('***'):
            # Title
            text = line[3:-3]
            p = Paragraph(text, styles['CustomTitle'])
            add_space = True
        elif line.startswith('**') and line.endswith('**'):
            # Section header
            text = line[2:-2]
            p = Paragraph(text, styles['Section'])
            add_space = True
        elif line.startswith('*') and line.endswith('*'):
            # Bullet point
            text = process_inline_bold(line[1:-1])
            p = Paragraph(text, styles['Bold'])
            add_space = True
        elif line.startswith('* '):
            # Bullet point
            text = '• ' + process_inline_bold(line[2:])
            
            # Process inline links
            text = process_inline_link(text)
            
            p = Paragraph(text, styles['CustomBullet'])
        elif line.startswith('---'):
            # Draw a normal horizontal line
            draw_line(c, x, current_y - 2, width)
            current_y -= 10  # Add some space after the line
            continue
        elif line.startswith('==='):
            # Draw a bold horizontal line
            draw_line(c, x, current_y - 2, width, 'bold')
            current_y -= 10  # Add some space after the line
            continue
        else:
            # Normal text with potential inline bold
            text = process_inline_bold(line)
            
            # Process inline links
            text = process_inline_link(text)
            
            p = Paragraph(text, styles['CustomNormal'])

        w, h = p.wrap(max_width, current_y - y)
        if current_y - h < y:
            break  # No more space in the area
        
        p.drawOn(c, x, current_y - h)
        current_y -= (h)
    
        if add_space:
            current_y -= 6

    c.save()
    packet.seek(0)

    # Read the template PDF
    template_reader = PdfReader(pdf_address)
    template_page = template_reader.pages[0]

    # Read the overlay PDF
    overlay_reader = PdfReader(packet)
    overlay_page = overlay_reader.pages[0]

    # Merge the overlay onto the template
    template_page.merge_page(overlay_page)

    # Write the result to a new PDF
    writer = PdfWriter()
    writer.add_page(template_page)
    with open(result_address, 'wb') as f:
        writer.write(f) 
        
