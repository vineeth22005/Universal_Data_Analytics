import pandas as pd


def recommend_chart(df):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # ID columns remove
    ignore_words = ["id", "code", "number", "no"]

    numeric_cols = [
        c for c in numeric_cols
        if not any(word in c.lower() for word in ignore_words)
    ]

    categorical_cols = [
        c for c in categorical_cols
        if not any(word in c.lower() for word in ignore_words)
    ]

    # Date column detect
    date_cols = []

    for col in df.columns:

        try:

            pd.to_datetime(df[col])

            date_cols.append(col)

        except:

            pass

    # Date + Numeric
    if len(date_cols) > 0 and len(numeric_cols) > 0:

        return {
            "chart": "line",
            "x": date_cols[0],
            "y": numeric_cols[0]
        }

    # Category + Numeric
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:

        return {
            "chart": "bar",
            "x": categorical_cols[0],
            "y": numeric_cols[0]
        }

    # Numeric + Numeric
    if len(numeric_cols) >= 2:

        return {
            "chart": "scatter",
            "x": numeric_cols[0],
            "y": numeric_cols[1]
        }

    # Category only
    if len(categorical_cols) > 0:

        return {
            "chart": "pie",
            "x": categorical_cols[0],
            "y": None
        }

    # Numeric only
    if len(numeric_cols) > 0:

        return {
            "chart": "histogram",
            "x": numeric_cols[0],
            "y": None
        }

    return {
        "chart": "bar",
        "x": df.columns[0],
        "y": None
    }