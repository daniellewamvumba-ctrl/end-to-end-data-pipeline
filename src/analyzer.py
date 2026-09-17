import pandas as pd


INPUT_FILE = "data/processed/books_clean.csv"
OUTPUT_FILE = "outputs/analysis_summary.txt"


def load_data(file_path):
    """Load the cleaned dataset."""

    return pd.read_csv(file_path)


def calculate_summary(df):
    """Calculate overall dataset metrics."""

    summary = {
        "total_books": len(df),
        "average_price": df["price"].mean(),
        "minimum_price": df["price"].min(),
        "maximum_price": df["price"].max(),
        "average_rating": df["rating"].mean(),
    }

    return summary


def analyze_ratings(df):
    """Count books by rating."""

    return (
        df.groupby("rating")
        .size()
        .sort_index()
    )


def analyze_availability(df):
    """Analyze books by availability."""

    return (
        df.groupby("availability")
        .size()
        .sort_values(ascending=False)
    )


def find_price_extremes(df):
    """Find the cheapest and most expensive books."""

    cheapest = df.loc[df["price"].idxmin()]
    most_expensive = df.loc[df["price"].idxmax()]

    return cheapest, most_expensive


def generate_summary(
    df,
    summary,
    ratings,
    availability,
    cheapest,
    most_expensive
):
    """Generate a human-readable analysis report."""

    report = f"""
END-TO-END BOOK DATA ANALYSIS
=============================

DATASET SUMMARY

Total books: {summary['total_books']}
Average price: £{summary['average_price']:.2f}
Minimum price: £{summary['minimum_price']:.2f}
Maximum price: £{summary['maximum_price']:.2f}
Average rating: {summary['average_rating']:.2f}


RATING DISTRIBUTION

{ratings.to_string()}


AVAILABILITY

{availability.to_string()}


CHEAPEST BOOK

Title: {cheapest['title']}
Price: £{cheapest['price']:.2f}


MOST EXPENSIVE BOOK

Title: {most_expensive['title']}
Price: £{most_expensive['price']:.2f}
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(report)


def main():

    print("Loading cleaned data...")

    df = load_data(INPUT_FILE)

    print(f"Books loaded: {len(df)}")

    print("\nAnalyzing data...")

    summary = calculate_summary(df)

    ratings = analyze_ratings(df)

    availability = analyze_availability(df)

    cheapest, most_expensive = find_price_extremes(df)

    generate_summary(
        df,
        summary,
        ratings,
        availability,
        cheapest,
        most_expensive
    )

    print("\n" + "=" * 45)
    print("ANALYSIS COMPLETE")
    print("=" * 45)

    print(f"\nAnalysis saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()