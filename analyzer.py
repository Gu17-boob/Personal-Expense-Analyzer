import pandas as pd


def load_expenses(file_path):
    """Load expense data from a CSV file."""
    df = pd.read_csv(file_path)

    required_columns = [
        "date",
        "description",
        "category",
        "amount",
        "payment_method"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {', '.join(missing_columns)}"
        )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date", "category", "amount"]
    )

    return df


def total_expenses(df):
    """Calculate total spending."""
    return df["amount"].sum()


def average_expense(df):
    """Calculate average transaction amount."""
    return df["amount"].mean()


def transaction_count(df):
    """Return number of transactions."""
    return len(df)


def category_expenses(df):
    """Calculate spending by category."""
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def monthly_expenses(df):
    """Calculate spending by month."""
    df = df.copy()

    df["month"] = df["date"].dt.to_period("M")

    return (
        df.groupby("month")["amount"]
        .sum()
        .sort_index()
    )