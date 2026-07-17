from flask import Blueprint, render_template, session
import pandas as pd

recommendation_bp = Blueprint(
    "recommendation",
    __name__
)


@recommendation_bp.route("/recommendation")
def recommendation():

    if "uploaded_file" not in session:
        return render_template(
            "recommendation.html",
            recommendations=[]
        )

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    recommendations = []

    # Missing Values
    missing = df.isnull().sum()

    for col, value in missing.items():
        if value > 0:
            recommendations.append(
                f"Fill missing values in '{col}' ({value} missing)."
            )

    # Duplicate Rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        recommendations.append(
            f"Remove {duplicates} duplicate rows."
        )

    # Datetime Suggestions
    for col in df.columns:
        if "date" in col.lower():
            recommendations.append(
                f"Convert '{col}' to datetime format."
            )

    # Numeric Charts
    numeric = df.select_dtypes(include="number").columns

    if len(numeric) > 0:
        recommendations.append(
            "Create histograms and boxplots for numerical columns."
        )

    # Categorical Charts
    categorical = df.select_dtypes(include="object").columns

    if len(categorical) > 0:
        recommendations.append(
            "Create bar charts for categorical columns."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Dataset looks clean. Ready for analysis."
        )

    return render_template(
        "recommendation.html",
        recommendations=recommendations
    )