from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generar_pedido_pdf(nombre_archivo, cliente, items, total):

    doc = SimpleDocTemplate(nombre_archivo)

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph("<b>CleanPro Solutions</b>", styles["Title"])
    )

    elementos.append(
        Paragraph("Comprobante de Compra", styles["Heading2"])
    )

    elementos.append(
        Paragraph(f"Cliente: {cliente}", styles["Normal"])
    )

    elementos.append(Spacer(1, 15))

    data = [["Producto", "Cantidad", "Precio", "Subtotal"]]

    for item in items:

        data.append([
            item["producto"].nombre,
            item["cantidad"],
            f"${item['producto'].precio:.2f}",
            f"${item['subtotal']:.2f}"
        ])

    data.append(["", "", "TOTAL", f"${total:.2f}"])

    tabla = Table(data)

    tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elementos.append(tabla)

    doc.build(elementos)