from flask import Blueprint, render_template, request, redirect, session, flash, url_for
import pandas as pd
import os

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = ""

    total_rows = 0
    total_columns = 0
    missing_values = 0
    duplicate_rows = 0
    total_numeric_columns = 0
    average_values = {}
    preview_data = []
    columns = []

    data_types = {}
    unique_values = {}
    memory_usage = 0

    dataset_size = "0 KB"

    if "uploaded_file" in session:

        filepath = session["uploaded_file"]

        try:

            if filepath.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)

            total_rows = df.shape[0]
            total_columns = df.shape[1]
            missing_values = int(df.isnull().sum().sum())
            duplicate_rows = int(df.duplicated().sum())

            numeric_df = df.select_dtypes(include="number")
            total_numeric_columns = len(numeric_df.columns)

            if not numeric_df.empty:
                average_values = (
                    numeric_df.mean()
                    .round(2)
                    .to_dict()
                )

                data_types = df.dtypes.astype(str).to_dict()

                unique_values = {}

                for col in df.columns:
                    unique_values[col] = int(df[col].nunique())

                memory_usage = round(
                    df.memory_usage(deep=True).sum() / 1024,
                    2
                )

            search = request.args.get("search", "")

            if search:
                df = df[
                    df.astype(str)
                    .apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
                ]

            preview_data = df.head(10).to_dict(orient="records")
            columns = df.columns.tolist()

            if os.path.exists(filepath):
                dataset_size = f"{round(os.path.getsize(filepath)/1024,2)} KB"

        except Exception as e:
            print(e)

    return render_template(
        "dashboard.html",
        name=session["user_name"],

        total_rows=total_rows,
        total_columns=total_columns,
        missing_values=missing_values,
        duplicate_rows=duplicate_rows,

        total_numeric_columns=total_numeric_columns,
        average_values=average_values,
        preview_data=preview_data,

        dataset_size=dataset_size,

        rows=total_rows,
        columns_count=total_columns,
        missing=missing_values,
        duplicates=duplicate_rows,
        columns=columns,
        data_types=data_types,
        unique_values=unique_values,
        memory_usage=memory_usage,
        search=search,
        upload_history=session.get("upload_history", [])
    )

@dashboard_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("file")

        if file:
            upload_folder = "uploads"

            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(
                upload_folder,
                file.filename
            )

            file.save(file_path)

            # Save in Session
            session["uploaded_file"] = file_path

            flash(
                "Dataset uploaded successfully!",
                "success"
            )

            return redirect(
                url_for("dashboard.dashboard")
            )

    return render_template("upload.html")