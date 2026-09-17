import streamlit as st
import pandas as pd


DATA_FILE = "data/processed/books_clean.csv"


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Z.lewadevs Book Data Dashboard",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Load data
# -----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    return df


df = load_data()


# -----------------------------
# Title
# -----------------------------

st.title("📚 Z.lewadevs Book Data Dashboard")

st.write(
    "An end-to-end data pipeline demonstrating "
    "web scraping, cleaning, analysis, and visualization."
)


# -----------------------------
# Key metrics
# -----------------------------

total_books = len(df)
average_price = df["price"].mean()
average_rating = df["rating"].mean()
in_stock = (df["availability"] == "In stock").sum()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Books",
    total_books
)

col2.metric(
    "Average Price",
    f"£{average_price:.2f}"
)

col3.metric(
    "Average Rating",
    f"{average_rating:.2f} / 5"
)

col4.metric(
    "In Stock",
    in_stock
)


st.divider()


# -----------------------------
# Rating distribution
# -----------------------------

st.subheader("⭐ Rating Distribution")

rating_counts = (
    df["rating"]
    .value_counts()
    .sort_index()
)

st.bar_chart(rating_counts)


# -----------------------------
# Price distribution
# -----------------------------

st.subheader("💷 Price Distribution")

price_data = df[["price"]].copy()

st.line_chart(
    price_data.reset_index(drop=True)
)


# -----------------------------
# Most expensive books
# -----------------------------

st.subheader("💰 Top 10 Most Expensive Books")

top_expensive = (
    df[
        ["title", "price", "rating", "availability"]
    ]
    .sort_values(
        "price",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_expensive,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# Availability
# -----------------------------

st.subheader("📦 Availability")

availability = (
    df["availability"]
    .value_counts()
)

st.bar_chart(availability)


# -----------------------------
# Dataset explorer
# -----------------------------

st.subheader("🔎 Dataset Explorer")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# Business insights
# -----------------------------

st.subheader("💡 Business Insights")

most_expensive = df.loc[
    df["price"].idxmax()
]

cheapest = df.loc[
    df["price"].idxmin()
]

highest_rating = df["rating"].max()

st.write(
    f"• The dataset contains **{total_books} books**."
)

st.write(
    f"• The average book price is "
    f"**£{average_price:.2f}**."
)

st.write(
    f"• The most expensive book is "
    f"**{most_expensive['title']}**, "
    f"priced at **£{most_expensive['price']:.2f}**."
)

st.write(
    f"• The cheapest book is "
    f"**{cheapest['title']}**, "
    f"priced at **£{cheapest['price']:.2f}**."
)

st.write(
    f"• The highest rating in the dataset is "
    f"**{highest_rating} / 5**."
)

st.write(
    f"• **{in_stock} of {total_books} books** "
    f"are currently listed as in stock."
)


st.divider()

st.caption(
    "Built with Python, Pandas, Matplotlib and Streamlit | Z.lewadevs"
)