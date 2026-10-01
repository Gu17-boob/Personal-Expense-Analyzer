import pandas as pd


def get_total_expenses(df):
    """Return total spending."""
    return df["amount"].sum()


def get_average_expense(df):
    """Return average transaction amount."""
    return df["amount"].mean()


def get_transaction_count(df):
    """Return number of transactions."""
    return len(df)


def get_highest_category(df):
    """Return the category with the highest spending."""

    category_totals = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return category_totals.index[0], category_totals.iloc[0]


def get_payment_method_summary(df):
    """Return spending by payment method."""

    return (
        df.groupby("payment_method")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


def generate_insights(df):
    """Generate a summary of expense insights."""

    total = get_total_expenses(df)
    average = get_average_expense(df)
    transactions = get_transaction_count(df)

    highest_category, highest_amount = get_highest_category(df)

    return {
        "total_expenses": total,
        "average_expense": average,
        "transaction_count": transactions,
        "highest_category": highest_category,
        "highest_category_amount": highest_amount,
    }