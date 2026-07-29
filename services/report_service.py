import os
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

from services.ai_service import generate_ai_insights


# ==============================
# FOOTER
# ==============================

def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9
    )

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
    # PDF GENERATOR
    # ==============================

def generate_pdf(
        df,
        uploaded_filename
):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        os.makedirs(
            "reports/charts",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        report_path = os.path.join(
            "reports",
            f"analytics_report_{timestamp}.pdf"
        )

        doc = SimpleDocTemplate(
            report_path
        )

        styles = getSampleStyleSheet()

        title_style = styles["Title"]

        subtitle_style = styles[
            "Heading2"
        ]

        heading_style = styles[
            "Heading3"
        ]

        normal_style = styles[
            "BodyText"
        ]

        elements = []

        # ==============================
        # COVER PAGE
        # ==============================

        logo_path = "static/images/logo.png"

        if os.path.exists(logo_path):
            elements.append(
                Image(
                    logo_path,
                    width=90,
                    height=90
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        elements.append(
            Paragraph(
                """
                <font size='28' color='#0A4A92'>
                <b>UNIVERSAL DATA</b><br/>
                <b>ANALYTICS</b>
                </font>
                """,
                title_style
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        elements.append(
            Paragraph(
                "AI Powered Data Analytics Platform",
                subtitle_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        elements.append(
            Paragraph(
                f"<b>Dataset:</b> {uploaded_filename}",
                normal_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>Generated On:</b> "
                f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                normal_style
            )
        )

        elements.append(
            Spacer(1, 40)
        )

        elements.append(
            Paragraph(
                "Prepared using Python, Flask, Machine Learning and Artificial Intelligence",
                normal_style
            )
        )

        elements.append(
            Spacer(1, 50)
        )

        elements.append(
            PageBreak()
        )

        # ==============================
        # EXECUTIVE SUMMARY
        # ==============================

        elements.append(
            Paragraph(
                "EXECUTIVE SUMMARY",
                subtitle_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        summary = f"""
        This report provides an analytical overview of the uploaded dataset.
        The dataset contains <b>{len(df)}</b> records and
        <b>{len(df.columns)}</b> attributes.

        The report includes:

        • Dataset Summary<br/>
        • Dataset Preview<br/>
        • Statistical Analysis<br/>
        • Pie Chart Analysis<br/>
        • Histogram Analysis<br/>
        • Correlation Heatmap<br/>
        • AI Generated Insights

        This report has been automatically generated using
        Universal Data Analytics.
        """

        elements.append(
            Paragraph(
                summary,
                normal_style
            )
        )

        elements.append(
            Spacer(1, 40)
        )



        # ==============================
        # DATASET SUMMARY
        # ==============================

        elements.append(
            Paragraph(
                "DATASET SUMMARY",
                subtitle_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        summary_data = [

            ["Dataset Name", uploaded_filename],

            ["Total Rows", str(len(df))],

            ["Total Columns", str(len(df.columns))],

            ["Missing Values", str(df.isnull().sum().sum())],

            ["Generated By", "Universal Data Analytics"],

        ]

        summary_table = Table(
            summary_data,
            colWidths=[180, 300]
        )

        summary_table.setStyle(
            TableStyle([

                ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),

                ('GRID', (0, 0), (-1, -1), 1, colors.black),

                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),

                ('FONTSIZE', (0, 0), (-1, -1), 10),

                ('ROWHEIGHT', (0, 0), (-1, -1), 25),

            ])
        )

        elements.append(
            summary_table
        )

        elements.append(
            Spacer(1, 40)
        )


        # ==============================
        # DATASET PREVIEW
        # ==============================

        elements.append(
            Paragraph(
                "DATASET PREVIEW",
                subtitle_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        preview_df = df.head(5)

        preview_data = [
            preview_df.columns.tolist()
        ]

        for row in preview_df.values:
            preview_data.append(
                list(map(str, row))
            )

        preview_table = Table(
            preview_data,
            repeatRows=1,
            colWidths=[65] * len(preview_df.columns)
        )

        preview_table.setStyle(
            TableStyle([

                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A4A92")),

                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

                ('GRID', (0, 0), (-1, -1), 1, colors.black),

                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

                ('FONTSIZE', (0, 0), (-1, -1), 7),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

                ('ROWHEIGHT', (0, 0), (-1, -1), 20),

            ])
        )

        elements.append(
            preview_table
        )

        elements.append(
            Spacer(1, 40)
        )

        elements.append(
            PageBreak()
        )

        # ==============================
        # STATISTICAL ANALYSIS
        # ==============================

        elements.append(
            Paragraph(
                "STATISTICAL ANALYSIS",
                subtitle_style
            )
        )

        elements.append(
            Spacer(1, 15)
        )

        stats_df = (
            df.describe(include="all")
            .fillna("-")
            .round(2)
        )

        stats_data = [
            ["Metric"] + stats_df.columns.tolist()
        ]

        for index, row in stats_df.iterrows():
            stats_data.append(
                [str(index)] + list(map(str, row.values))
            )

        stats_table = Table(
            stats_data,
            repeatRows=1
        )

        stats_table.setStyle(
            TableStyle([

                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0A4A92")),

                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

                ('GRID', (0, 0), (-1, -1), 1, colors.black),

                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

                ('FONTSIZE', (0, 0), (-1, -1), 6),

                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

            ])
        )

        elements.append(
            stats_table
        )

        elements.append(
            Spacer(1, 40)
        )


        # ==============================
        # PIE CHART
        # ==============================

        elements.append(
            Paragraph(
                "PIE CHART ANALYSIS",
                subtitle_style
            )
        )

        categorical_cols = df.select_dtypes(
            include="object"
        ).columns

        pie_column = None

        for col in categorical_cols:

            if (
                    "id" not in col.lower()
                    and "date" not in col.lower()
            ):
                pie_column = col
                break

        print("Pie Column =", pie_column)

        if pie_column is not None:
            top_values = (
                df[pie_column]
                .value_counts()
                .head(5)
            )

            plt.figure(figsize=(5, 5))

            plt.pie(
                top_values.values,
                labels=top_values.index,
                autopct="%1.1f%%"
            )

            plt.title(
                f"{pie_column} Distribution"
            )

            pie_path = os.path.join(
                "reports/charts",
                "pie_chart.png"
            )

            plt.savefig(
                pie_path,
                bbox_inches="tight"
            )

            plt.close()

            print("Adding Pie Chart")

            elements.append(
                Image(
                    pie_path,
                    width=350,
                    height=250
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        elements.append(
            PageBreak()
        )

        # ==============================
        # BAR CHART ANALYSIS
        # ==============================

        elements.append(
            Paragraph(
                "BAR CHART ANALYSIS",
                subtitle_style
            )
        )

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        numeric_cols = [
            col
            for col in numeric_cols
            if "id" not in col.lower()
        ]

        if len(numeric_cols) > 0:
            plt.figure(figsize=(6, 4))

            df[numeric_cols].mean().head(5).plot(
                kind="bar"
            )

            plt.title(
                "Average Numerical Values"
            )

            plt.xlabel(
                "Columns"
            )

            plt.ylabel(
                "Average Value"
            )

            plt.tight_layout()

            bar_chart_path = os.path.join(
                "reports/charts",
                "bar_chart.png"
            )

            plt.savefig(
                bar_chart_path,
                bbox_inches="tight"
            )

            plt.close()

            print("Adding Bar Chart")

            elements.append(
                Image(
                    bar_chart_path,
                    width=420,
                    height=250
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        # ==============================
        # HISTOGRAM ANALYSIS
        # ==============================

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns

        numeric_cols = [
            col
            for col in numeric_cols
            if "id" not in col.lower()
        ]

        if len(numeric_cols) > 0:

            plt.figure(figsize=(6, 4))

            df[numeric_cols[0]].hist(
                bins=20
            )

            plt.title(
                f"{numeric_cols[0]} Distribution"
            )

            plt.xlabel(
                numeric_cols[0]
            )

            plt.ylabel(
                "Frequency"
            )

            histogram_path = os.path.join(
                "reports/charts",
                "histogram.png"
            )

            plt.savefig(
                histogram_path,
                bbox_inches="tight"
            )

            plt.close()

            elements.append(
                Paragraph(
                    "HISTOGRAM ANALYSIS",
                    subtitle_style
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            elements.append(
                Image(
                    histogram_path,
                    width=420,
                    height=250
                )
            )

            elements.append(
                Spacer(1, 20)
            )

        else:

            print(
                "Histogram Skipped"
            )

        elements.append(
            PageBreak()
        )

        # ==============================
        # CORRELATION HEATMAP
        # ==============================

        elements.append(
            Paragraph(
                "CORRELATION HEATMAP",
                subtitle_style
            )
        )

        if len(numeric_cols) > 1:
            plt.figure(figsize=(6, 4))

            sns.heatmap(
                df[numeric_cols].corr(),
                annot=True,
                cmap="Blues"
            )

            plt.title(
                "Correlation Heatmap"
            )

            heatmap_path = os.path.join(
                "reports/charts",
                "heatmap.png"
            )

            plt.savefig(
                heatmap_path,
                bbox_inches="tight"
            )

            plt.close()

            print("Adding Heatmap")

            elements.append(
                Image(
                    heatmap_path,
                    width=420,
                    height=250
                )
            )


            # ==============================
            # AI INSIGHTS
            # ==============================

            elements.append(
                Paragraph(
                    "AI INSIGHTS",
                    subtitle_style
                )
            )

            elements.append(
                Spacer(1, 15)
            )

            try:

                ai_text = generate_ai_insights(
                    str(df.describe())
                )

            except Exception:

                ai_text = (
                    "AI Insights could not be generated "
                    "at this time."
                )

            elements.append(
                Paragraph(
                    ai_text,
                    normal_style
                )
            )

            elements.append(
                Spacer(1, 30)
            )

            # ==============================
            # THANK YOU PAGE
            # ==============================

            elements.append(
                PageBreak()
            )

            elements.append(
                Spacer(1, 100)
            )

            elements.append(
                Paragraph(
                    """
                    <font size='30' color='#0A4A92'>
                    <b>THANK YOU</b>
                    </font>
                    """,
                    title_style
                )
            )

            elements.append(
                Spacer(1, 20)
            )

            elements.append(
                Paragraph(
                    "Universal Data Analytics v1.0",
                    subtitle_style
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            elements.append(
                Paragraph(
                    "Developed by Vineeth Kumar D",
                    normal_style
                )
            )

            elements.append(
                Spacer(1, 10)
            )

            elements.append(
                Paragraph(
                    "Powered by Python, Flask and AI",
                    normal_style
                )
            )

            doc.build(
                elements,
                onFirstPage=add_page_number,
                onLaterPages=add_page_number
            )

            return report_path