import pandas as pd
import matplotlib.pyplot as plt
import os


INPUT_FILE = "data/processed/books_clean.csv"
CHARTS_DIR = "charts"


def load_data(file_path):
    """Load the cleaned book dataset."""

    return pd.read_csv(file_path)


def create_rating_chart(df):
    """Create a chart showing book ratings."""

    rating_counts = df["rating"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))

    plt.bar(
        rating_counts.index.astype(str),
        rating_counts.values
    )

    plt.title("Book Rating Distribution")
    plt.xlabel("Rating")
    plt.ylabel("Number of Books")

    plt.tight_layout()

    plt.savefig(
        f"{CHARTS_DIR}/rating_distribution.png",
        dpi=300
    )

    plt.close()


def create_price_chart(df):
    """Create a price distribution chart."""

    plt.figure(figsize=(8, 5))

    plt.hist(
        df["price"],
        bins=10
    )

    plt.title("Book Price Distribution")
    plt.xlabel("Price (£)")
    plt.ylabel("Number of Books")

    plt.tight_layout()

    plt.savefig(
        f"{CHARTS_DIR}/price_distribution.png",
        dpi=300
    )

    plt.close()


def create_top_expensive_chart(df):
    """Create a chart showing the most expensive books."""

    top_books = (
        df.sort_values(
            "price",
            ascending=False
        )
        .head(10)
        .sort_values("price")
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_books["title"],
        top_books["price"]
    )

    plt.title("Top 10 Most Expensive Books")
    plt.xlabel("Price (£)")
    plt.ylabel("Book")

    plt.tight_layout()

    plt.savefig(
        f"{CHARTS_DIR}/top_10_expensive_books.png",
        dpi=300
    )

    plt.close()


def create_availability_chart(df):
    """Create an availability chart."""

    availability_counts = (
        df["availability"]
        .value_counts()
    )

    plt.figure(figsize=(8, 5))

    plt.bar(
        availability_counts.index,
        availability_counts.values
    )

    plt.title("Book Availability")
    plt.xlabel("Availability")
    plt.ylabel("Number of Books")

    plt.tight_layout()

    plt.savefig(
        f"{CHARTS_DIR}/availability.png",
        dpi=300
    )

    plt.close()


def main():

    os.makedirs(CHARTS_DIR, exist_ok=True)

    print("Loading cleaned data...")

    df = load_data(INPUT_FILE)

    print(f"Books loaded: {len(df)}")

    print("\nCreating visualizations...")

    create_rating_chart(df)
    create_price_chart(df)
    create_top_expensive_chart(df)
    create_availability_chart(df)

    print("\n" + "=" * 45)
    print("VISUALIZATION COMPLETE")
    print("=" * 45)

    print("\nCharts saved to:")
    print("charts/")


if __name__ == "__main__":
    main()