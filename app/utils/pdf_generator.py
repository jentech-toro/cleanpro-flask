from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_order_pdf(file_name, customer, items, total):

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph("<b>CleanPro Solutions</b>", styles["Title"])
    )

    elements.append(
        Paragraph("Purchase Receipt", styles["Heading2"])
    )

    elements.append(
        Paragraph(f"Customer: {customer}", styles["Normal"])
    )

    elements.append(Spacer(1, 15))

    data = [["Product", "Quantity", "Price", "Subtotal"]]

    for item in items:

        data.append([
            item["producto"].nombre,
            item["cantidad"],
            f"${item['producto'].precio:.2f}",
            f"${item['subtotal']:.2f}"
        ])

    data.append(["", "", "TOTAL", f"${total:.2f}"])

    table = Table(data)

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(table)

    doc.build(elements)