import streamlit as st
import pandas as pd

from analyzer import (
    total_expenses,
    average_expense,
    transaction_count,
    category_expenses,
    monthly_expenses
)

from data_cleaner import clean_expenses

from insights import generate_insights


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Expense Analyzer",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💰 Personal Expense Analyzer")

st.write(
    "Analyze your spending patterns, categories, "
    "transactions, and monthly expenses."
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your expense CSV",
    type=["csv"]
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)
        df = clean_expenses(df)

        st.success(
            f"Successfully loaded {len(df)} transactions."
        )

    except Exception as error:

        st.error(
            f"Error loading file: {error}"
        )

        st.stop()

else:

    st.info(
        "No file uploaded. Using sample expense data."
    )

    df = pd.read_csv(
        "data/sample_expenses.csv"
    )

    df = clean_expenses(df)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")


# Category filter

categories = sorted(
    df["category"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories
)


# Payment method filter

payment_methods = sorted(
    df["payment_method"].unique()
)

selected_payment_methods = st.sidebar.multiselect(
    "Payment Method",
    payment_methods,
    default=payment_methods
)


# Apply filters

filtered_df = df[
    df["category"].isin(selected_categories)
    &
    df["payment_method"].isin(
        selected_payment_methods
    )
]


# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Expense Overview")

total = total_expenses(filtered_df)

average = average_expense(filtered_df)

transactions = transaction_count(filtered_df)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "💰 Total Spending",
        f"₹{total:,.2f}"
    )


with col2:

    st.metric(
        "🧾 Transactions",
        transactions
    )


with col3:

    st.metric(
        "📌 Average Expense",
        f"₹{average:,.2f}"
    )


# --------------------------------------------------
# INSIGHTS
# --------------------------------------------------

st.subheader("💡 Spending Insights")

if not filtered_df.empty:

    insights = generate_insights(
        filtered_df
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"🏆 Highest spending category: "
            f"**{insights['highest_category']}**"
        )

    with col2:

        st.info(
            f"💸 Amount spent in this category: "
            f"**₹{insights['highest_category_amount']:,.2f}**"
        )

else:

    st.warning(
        "No transactions match the selected filters."
    )


# --------------------------------------------------
# TRANSACTIONS
# --------------------------------------------------

st.subheader("📋 Transactions")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

st.subheader("📊 Spending by Category")

if not filtered_df.empty:

    category_data = category_expenses(
        filtered_df
    )

    st.bar_chart(
        category_data
    )


# --------------------------------------------------
# MONTHLY ANALYSIS
# --------------------------------------------------

st.subheader("📅 Monthly Spending")

if not filtered_df.empty:

    monthly_data = monthly_expenses(
        filtered_df
    )

    monthly_data.index = (
        monthly_data.index.astype(str)
    )

    st.line_chart(
        monthly_data
    )


# --------------------------------------------------
# EXPORT
# --------------------------------------------------

st.subheader("📥 Export Data")

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv_data,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Personal Expense Analyzer • "
    "Built with Python, Pandas, and Streamlit"
)