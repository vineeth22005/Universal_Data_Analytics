from flask import Blueprint, session, redirect, url_for, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import os
from services.report_service import generate_pdf

report_bp = Blueprint("report", __name__)


@report_bp.route("/download-report")
def download_report():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    pdf_path = generate_pdf(df)

    return send_file(pdf_path, as_attachment=True)

    