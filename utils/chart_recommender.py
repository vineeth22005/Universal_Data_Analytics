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

    def get_best_numeric_column(cols):

        priority = [
            "sales",
            "profit",
            "revenue",
            "amount",
            "price",
            "quantity"
        ]

        for word in priority:

            for col in cols:

                if word in col.lower():
                    return col

        return cols[0] if cols else None

    categorical_cols = [
        c for c in categorical_cols
        if not any(word in c.lower() for word in ignore_words)
    ]

    # Date column detect
    date_cols = []

    date_cols = []

    for col in df.columns:

        if (
                "date" in col.lower()
                or "time" in col.lower()
                or "year" in col.lower()
        ):
            date_cols.append(col)

    # Date + Numeric
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        return {
            "chart": "line",
            "x": date_cols[0],
            "y": get_best_numeric_column(numeric_cols)
        }

    # Category + Numeric
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        return {
            "chart": "bar",
            "x": categorical_cols[0],
            "y": get_best_numeric_column(numeric_cols)
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