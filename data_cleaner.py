import pandas as pd


def clean_expenses(df):
    """
    Clean and standardize expense data.
    """

    df = df.copy()

    # Convert date column
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert amount column to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove rows with invalid required data
    df = df.dropna(
        subset=[
            "date",
            "category",
            "amount"
        ]
    )

    # Remove zero or negative expenses
    df = df[df["amount"] > 0]

    # Clean description
    df["description"] = (
        df["description"]
        .astype(str)
        .str.strip()
    )

    # Clean category
    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
    )

    # Clean payment method
    df["payment_method"] = (
        df["payment_method"]
        .astype(str)
        .str.strip()
    )

    # Sort by date
    df = df.sort_values(
        by="date"
    )

    # Reset index
    df = df.reset_index(drop=True)

    return df