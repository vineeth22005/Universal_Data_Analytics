import pandas as pd


def generate_recommendations(df):

    recommendations = []

    # Missing values
    missing = df.isnull().sum().sum()

    if missing > 0:
        recommendations.append(
            f"⚠ Dataset contains {missing} missing values. Clean the data before analysis."
        )
    else:
        recommendations.append(
            "✅ Dataset is clean. No missing values found."
        )

    # Duplicate rows
    duplicate = df.duplicated().sum()

    if duplicate > 0:
        recommendations.append(
            f"⚠ Found {duplicate} duplicate rows. Consider removing them."
        )
    else:
        recommendations.append(
            "✅ No duplicate records found."
        )

    # Numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:

        col = numeric_cols[0]

        avg = df[col].mean()

        recommendations.append(
            f"📊 Average {col}: {round(avg, 2)}"
        )

        recommendations.append(
            f"📈 Maximum {col}: {df[col].max()}"
        )

    # Categorical columns
    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if categorical_cols:

        col = categorical_cols[0]

        top = df[col].mode()[0]

        recommendations.append(
            f"🏆 Most frequent {col}: {top}"
        )

    recommendations.append(
        "💡 Recommendation: Focus on high-performing categories and monitor low-performing segments."
    )

    return recommendations