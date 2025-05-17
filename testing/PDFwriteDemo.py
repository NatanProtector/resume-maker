from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

def write_cv_to_pdf(text, filename):
    """
    Writes the given CV text to a PDF file with proper formatting.

    Parameters:
    - text (str): The CV text to write to the PDF.
    - filename (str): The name of the output PDF file.
    """
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER

    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='Section',
        parent=styles['Bold'],
        fontSize=14,
        spaceAfter=12
    ))
    styles.add(ParagraphStyle(
        name='CustomBullet',
        parent=styles['Normal'],
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=6
    ))

    # Starting position
    x = 50
    y = height - 50
    max_width = width - 100  # Leave margins on both sides

    # Process each line
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            y -= 12  # Add space between paragraphs
            continue

        # Handle different line types
        if line.startswith('**') and line.endswith('**'):
            # Section header
            text = line[2:-2]  # Remove **
            p = Paragraph(text, styles['Section'])
            p.wrapOn(c, max_width, height)
            p.drawOn(c, x, y - p.height)
            y -= p.height + 12
        elif line.startswith('* '):
            # Bullet point
            text = '• ' + line[2:]  # Replace * with bullet
            p = Paragraph(text, styles['CustomBullet'])
            p.wrapOn(c, max_width, height)
            p.drawOn(c, x, y - p.height)
            y -= p.height
        elif line.startswith('**'):
            # Bold text
            text = line[2:]  # Remove **
            p = Paragraph(text, styles['Bold'])
            p.wrapOn(c, max_width, height)
            p.drawOn(c, x, y - p.height)
            y -= p.height
        else:
            # Normal text
            p = Paragraph(line, styles['Normal'])
            p.wrapOn(c, max_width, height)
            p.drawOn(c, x, y - p.height)
            y -= p.height

        # Check if we need a new page
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

def write_content_to_area(x, y, width, height, content, pdf_address):
    """
    Writes the given content into the designated area of the PDF.

    Parameters:
    - x (float): The x-coordinate of the lower-left corner of the area.
    - y (float): The y-coordinate of the lower-left corner of the area.
    - width (float): The width of the area.
    - height (float): The height of the area.
    - content (str): The text content to write.
    - pdf_address (str): The path to the output PDF file.
    """
    c = canvas.Canvas(pdf_address, pagesize=LETTER)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    
     
    # Create a Paragraph for the content
    p = Paragraph(content, style)
    # Wrap the paragraph to fit the width and height
    w, h = p.wrap(width, height)
    # Draw the paragraph at the specified (x, y + height - h) to start from the top-left of the area
    p.drawOn(c, x, y + height - h)
    c.save()

if __name__ == "__main__":
    # Example CV text
    cv_text = """**Jane Doe**
(123) 456-7890 | jane.doe@email.com | linkedin.com/in/janedoe | portfolio.janedoe.com

**Summary**

Highly motivated and creative Front-End Developer with 3+ years of experience building and maintaining responsive, user-friendly websites and applications.  Proficient in HTML, CSS, JavaScript, and React. Passionate about clean code and user-centered design.

**Skills**

HTML, CSS, JavaScript, React, Redux, Git, Responsive Design, Accessibility, Cross-Browser Compatibility, Testing (Jest, Cypress), UI/UX Principles

**Experience**

**Front-End Developer, Company X  |  City, State  |  June 2020 – Present**

* Developed and maintained multiple web applications using React, resulting in a 20% increase in user engagement.
* Implemented responsive design principles, ensuring optimal user experience across all devices.
* Collaborated with designers and back-end developers to deliver high-quality products on time and within budget."""

    write_cv_to_pdf(cv_text, "cv_output.pdf")

    # Example usage: write content to a designated area in 'result.pdf' in the main directory
    content = "This is an example of writing content into a designated area of a PDF using ReportLab."
    x = 50
    y = 500
    width = 400
    height = 200
    pdf_address = "../result.pdf"  # Main directory relative to 'testing/'
    write_content_to_area(x, y, width, height, content, pdf_address)
