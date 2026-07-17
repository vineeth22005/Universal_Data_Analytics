from flask import Blueprint, render_template, session, redirect, url_for, flash
import pandas as pd
import os
from flask import send_file

cleaning_bp = Blueprint("cleaning", __name__)


def load_dataset():

    filepath = session["uploaded_file"]

    if filepath.endswith(".csv"):
        return pd.read_csv(filepath), filepath

    return pd.read_excel(filepath), filepath

def save_cleaned_dataset(df, filepath):

    os.makedirs("cleaned", exist_ok=True)

    filename = os.path.basename(filepath)

    cleaned_path = os.path.join(
        "cleaned",
        f"cleaned_{filename}"
    )

    if filepath.endswith(".csv"):
        df.to_csv(cleaned_path, index=False)
    else:
        df.to_excel(cleaned_path, index=False)

    session["cleaned_file"] = cleaned_path

    return cleaned_path


@cleaning_bp.route("/cleaning")
def cleaning():

    if "uploaded_file" not in session:
        return redirect(url_for("upload.upload"))

    df, filepath = load_dataset()

    info = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }

    return render_template(
        "cleaning.html",
        info=info
    )


@cleaning_bp.route("/remove-duplicates")
def remove_duplicates():

    df, filepath = load_dataset()

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    save_cleaned_dataset(df, filepath)

    flash(f"{removed} duplicate rows removed successfully.", "success")

    return redirect(url_for("cleaning.cleaning"))


@cleaning_bp.route("/drop-missing")
def drop_missing():

    df, filepath = load_dataset()

    before = len(df)

    df = df.dropna()

    removed = before - len(df)

    save_cleaned_dataset(df, filepath)

    flash(f"{removed} rows with missing values removed.", "success")

    return redirect(url_for("cleaning.cleaning"))


@cleaning_bp.route("/fill-missing")
def fill_missing():

    df, filepath = load_dataset()

    for col in df.columns:

        # Numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(df[col].mean())

        # All non-numeric columns
        else:

            mode = df[col].mode()

            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])

    save_cleaned_dataset(df, filepath)

    flash("Missing values filled successfully.", "success")

    return redirect(url_for("cleaning.cleaning"))

@cleaning_bp.route("/download-cleaned")
def download_cleaned():

    if "cleaned_file" not in session:

        flash(
            "Please clean the dataset first.",
            "warning"
        )

        return redirect(
            url_for("cleaning.cleaning")
        )

    return send_file(
        session["cleaned_file"],
        as_attachment=True
    )