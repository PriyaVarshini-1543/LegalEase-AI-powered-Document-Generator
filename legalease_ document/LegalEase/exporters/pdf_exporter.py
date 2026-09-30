from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from exporters.common import stream


def export_pdf(title: str, content: str):
    output = BytesIO()

    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
        title=title,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "LegalEaseTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    body_style = ParagraphStyle(
        "LegalEaseBody",
        parent=styles["BodyText"],
        leading=15,
        spaceAfter=9,
    )

    story = [Paragraph(escape(title), title_style)]

    for block in content.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        safe = escape(block).replace("\n", "<br/>")
        story.append(Paragraph(safe, body_style))
        story.append(Spacer(1, 3))

    doc.build(story)
    return stream(output.getvalue())
