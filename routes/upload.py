from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        if "file" not in request.files:
            flash("No file selected!", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("Please choose a file.", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filepath = os.path.join(UPLOAD_FOLDER, filename)

            file.save(filepath)

            # Save file details in session
            session["uploaded_file"] = filepath
            session["uploaded_filename"] = filename

            print("UPLOAD SUCCESS")
            print("FILE:", filepath)
            print("NAME:", filename)
            print("SESSION:", session)
            print("FILE =", session.get("uploaded_file"))
            print("FILENAME =", session.get("uploaded_filename"))


            history = session.get("upload_history", [])

            history.append({
                "filename": file.filename,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })

            # Last 10 uploads mattum save pannuvom
            session["upload_history"] = history[-10:]

            # Read dataset
            if filename.lower().endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)

            # Dataset Preview
            preview = df.head(10).to_html(
                classes="table table-striped table-bordered",
                index=False
            )

            # Dataset Statistics
            rows = df.shape[0]
            columns = df.shape[1]

            column_names = df.columns.tolist()
            data_types = df.dtypes.astype(str).to_dict()
            missing_values = df.isnull().sum().to_dict()
            duplicate_rows = int(df.duplicated().sum())

            # Dashboard KPI Values
            session["rows"] = rows
            session["columns"] = columns
            session["missing"] = int(df.isnull().sum().sum())
            session["duplicates"] = duplicate_rows

            return render_template(
                "preview.html",
                filename=filename,
                rows=rows,
                columns=columns,
                preview=preview,
                column_names=column_names,
                data_types=data_types,
                missing_values=missing_values,
                duplicate_rows=duplicate_rows
            )

        flash("Only CSV, XLSX and XLS files are allowed.", "danger")
        return redirect(request.url)

    return render_template("upload.html")