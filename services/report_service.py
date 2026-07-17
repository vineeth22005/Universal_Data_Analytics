import os
print("REPORT SERVICE LOADED")
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle, Image
)

from services.ai_service import generate_ai_insights

def generate_pdf(df):
    print("GENERATE PDF FUNCTION CALLED")



# ==============================
# Footer (Page Number)
# ==============================
def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    page = canvas.getPageNumber()

    canvas.drawString(
        30,
        20,
        f"Page {page}"
    )

    canvas.drawRightString(
        560,
        20,
        "Universal Data Analytics | Developed by Vineeth Kumar D"
    )

    canvas.restoreState()


# ==============================
# PDF Generator
# ==============================
def generate_pdf(df):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = os.path.join(
        "reports",
        f"analytics_report_{timestamp}.pdf"
    )

    doc = SimpleDocTemplate(report_path)

    styles = getSampleStyleSheet()

    elements = []

    logo_path = "static/images/logo.png"

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=80,
            height=80
        )

        elements.append(logo)

    # ==============================
    # Title
    # ==============================

    elements.append(
        Paragraph(
            "<font color='#0A4A92'><b>UNIVERSAL DATA ANALYTICS</b></font>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Professional Analytics Report</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Prepared For :</b> Vineeth Kumar D",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            datetime.now().strftime(
                "Generated on : %d-%m-%Y %H:%M:%S"
            ),
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Dataset Name :</b> Uploaded Dataset",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"<b>Dataset Size :</b> {round(df.memory_usage(deep=True).sum() / 1024, 2)} KB",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "<b>Status :</b> Ready for Analysis",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "___________________________________________",
            styles["Normal"]
        )
    )

    # ==============================
    # Dataset Summary
    # ==============================

    elements.append(
        Paragraph(
            "<b>Dataset Summary</b>",
            styles["Heading2"]
        )
    )

    summary = [
        ["Metric", "Value"],
        ["Total Rows", str(df.shape[0])],
        ["Total Columns", str(df.shape[1])],
        ["Missing Values", str(df.isnull().sum().sum())],
        ["Duplicate Rows", str(df.duplicated().sum())],
    ]

    table = Table(summary)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0A4A92")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F4F8FC")),

        ("GRID", (0, 0), (-1, -1), 1, colors.grey),

        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),

        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(
        Paragraph(
            "<font color='#0A4A92'><b>DATASET OVERVIEW</b></font>",
            styles["Heading2"]
        )
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    # ==============================
    # Dataset Preview
    # ==============================

    elements.append(
        Paragraph(
            "<font color='#0A4A92'><b>DATASET PREVIEW</b></font>",
            styles["Heading2"]
        )
    )

    preview_df = df.head(5)

    preview_data = [preview_df.columns.tolist()]

    for row in preview_df.values.tolist():
        preview_data.append(
            [str(value) for value in row]
        )

    preview_table = Table(preview_data)

    preview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))

    elements.append(preview_table)

    elements.append(Spacer(1, 20))

    # ==============================
    # Columns
    # ==============================

    elements.append(
        Paragraph("<b>Columns</b>", styles["Heading2"])
    )

    for col in df.columns:
        elements.append(
            Paragraph(f"• {col}", styles["BodyText"])
        )

    elements.append(Spacer(1, 20))

    # ==============================
    # Data Types
    # ==============================

    elements.append(
        Paragraph("<b>Data Types</b>", styles["Heading2"])
    )

    for col, dtype in df.dtypes.items():
        elements.append(
            Paragraph(f"{col} : {dtype}", styles["BodyText"])
        )

    elements.append(Spacer(1, 20))

    # ==============================
    # Quick Insights
    # ==============================

    elements.append(
        Paragraph("<font color='#0A4A92'><b>QUICK INSIGHTS</b></font>", styles["Heading2"])
    )

    if df.isnull().sum().sum() == 0:
        elements.append(
            Paragraph("✓ Dataset contains no missing values.", styles["BodyText"])
        )
    else:
        elements.append(
            Paragraph("⚠ Dataset contains missing values.", styles["BodyText"])
        )

    if df.duplicated().sum() == 0:
        elements.append(
            Paragraph("✓ No duplicate rows found.", styles["BodyText"])
        )
    else:
        elements.append(
            Paragraph("⚠ Duplicate rows detected.", styles["BodyText"])
        )

    elements.append(
        Paragraph("✓ Dataset is ready for analysis.", styles["BodyText"])
    )

    elements.append(Spacer(1, 20))

    # ==============================
    # Statistics
    # ==============================

    elements.append(
        Paragraph("<b>Statistics (Numerical Columns)</b>", styles["Heading2"])
    )

    try:

        stats = df.describe().round(2)

        data = [["Metric"] + list(stats.columns)]

        for row in stats.index:

            values = [row]

            for col in stats.columns:
                values.append(str(stats.loc[row, col]))

            data.append(values)

        stat_table = Table(data)

        stat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ]))

        elements.append(stat_table)

    except Exception as e:

        elements.append(
            Paragraph(
                f"Statistics could not be generated: {str(e)}",
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1, 20))

    # ==============================
    # AI Analysis
    # ==============================

    elements.append(
        Paragraph("<font color='#0A4A92'><b>AI DATASET ANALYSIS</b></font>", styles["Heading2"])
    )

    try:

        summary = f"""
   Dataset Summary

   Rows : {df.shape[0]}
   Columns : {df.shape[1]}
   Missing Values : {df.isnull().sum().sum()}
   Duplicate Rows : {df.duplicated().sum()}

   Columns:
   {list(df.columns)}

   Data Types:
   {df.dtypes.to_string()}

   Statistics:
   {df.describe(include='all').to_string()}
   """

        ai_report = generate_ai_insights(summary)

        for line in ai_report.split("\n"):

            if line.strip():
                elements.append(
                    Paragraph(line, styles["BodyText"])
                )

    except Exception as e:

        elements.append(
            Paragraph(
                f"AI Analysis Error: {str(e)}",
                styles["BodyText"]
            )
        )

    elements.append(Spacer(1, 20))

    # ==============================
    # Footer Text
    # ==============================

    elements.append(
        Paragraph(
            "<font color='#0A4A92'><b>Universal Data Analytics v1.0</b></font>",
            styles["Heading3"]
        )
    )

    elements.append(
        Paragraph(
            "Powered by Flask + Python + Machine Learning + Artificial Intelligence",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            "© 2026 Universal Data Analytics. All Rights Reserved.",
            styles["BodyText"]
        )
    )

    # ==============================
    # Build PDF
    # ==============================

    doc.build(
        elements,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return report_path