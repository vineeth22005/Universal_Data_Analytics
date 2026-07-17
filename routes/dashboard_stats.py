from flask import Blueprint, jsonify, session
import pandas as pd

dashboard_stats_bp = Blueprint("dashboard_stats", __name__)


@dashboard_stats_bp.route("/dashboard-stats")
def dashboard_stats():

    if "uploaded_file" not in session:
        return jsonify({})

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    numeric = df.select_dtypes(include="number")

    return jsonify({
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "numeric_columns": list(numeric.columns)
    })