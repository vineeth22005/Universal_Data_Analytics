from flask import Blueprint, session, redirect, url_for, send_file
import pandas as pd
import os

export_bp = Blueprint("export", __name__)


@export_bp.route("/export")
def export():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    filepath = session["uploaded_file"]

    try:

        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Fill missing values
        for col in df.columns:

            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna("Unknown")

        export_folder = "exports"
        os.makedirs(export_folder, exist_ok=True)

        output_path = os.path.join(
            export_folder,
            "cleaned_dataset.csv"
        )

        df.to_csv(output_path, index=False)

        return send_file(
            output_path,
            as_attachment=True
        )

    except Exception as e:
        return f"Export Error: {e}"