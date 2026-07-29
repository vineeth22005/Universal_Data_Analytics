import pandas as pd


def generate_ai_insights(df):

    insights = []

    # Dataset size
    insights.append(f"📊 Total Rows : {len(df)}")
    insights.append(f"📋 Total Columns : {len(df.columns)}")

    # Missing values
    missing = df.isnull().sum().sum()

    insights.append(f"⚠ Missing Values : {missing}")

    # Duplicate rows
    duplicate = df.duplicated().sum()

    insights.append(f"📑 Duplicate Rows : {duplicate}")

    # Numeric columns
    ignore_words = [
        "id",
        "code",
        "number",
        "no",
        "index"
    ]

    numeric = [
        col for col in df.select_dtypes(include="number").columns
        if not any(word in col.lower() for word in ignore_words)
    ]

    if len(numeric) > 0:

        col = numeric[0]

        insights.append(f"📈 Highest {col} : {df[col].max()}")

        insights.append(f"📉 Lowest {col} : {df[col].min()}")

        insights.append(f"📊 Average {col} : {round(df[col].mean(),2)}")

    # Categorical columns
    categorical = [
        col
        for col in df.select_dtypes(
            include=["object", "category"]
        ).columns
        if (
                "date" not in col.lower()
                and "id" not in col.lower()
        )
    ]

    if len(categorical) > 0:

        col = categorical[0]

        top = df[col].mode()[0]

        insights.append(f"🏆 Most Frequent {col} : {top}")

    # AI Recommendation
    if missing > 0:

        insights.append(
            "💡 Recommendation : Fill missing values before analysis."
        )

    elif duplicate > 0:

        insights.append(
            "💡 Recommendation : Remove duplicate records."
        )

    else:

        insights.append(
            "💡 Recommendation : Dataset is clean and ready for advanced analytics."
        )

    return insights