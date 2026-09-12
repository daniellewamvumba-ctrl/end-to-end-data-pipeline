import pandas as pd


INPUT_FILE = "data/raw/books_raw.csv"
OUTPUT_FILE = "data/processed/books_clean.csv"


def load_data(file_path):
    """Load raw scraped data."""

    return pd.read_csv(file_path)


def clean_title(df):
    """Clean book titles."""

    df = df.copy()

    df["title"] = (
        df["title"]
        .astype("string")
        .str.strip()
    )

    return df


def clean_price(df):
    """Convert scraped price values into numeric values."""

    df = df.copy()

    df["price"] = (
        df["price"]
        .astype("string")
        .str.replace(r"[^\d.]", "", regex=True)
        .str.strip()
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    return df
def clean_rating(df):
    """Convert rating words into numeric values."""

    df = df.copy()

    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["rating"].map(
        rating_map
    )

    return df


def clean_availability(df):
    """Clean availability information."""

    df = df.copy()

    df["availability"] = (
        df["availability"]
        .astype("string")
        .str.strip()
        .str.replace(
            "\n",
            " ",
            regex=False
        )
    )

    df["availability"] = (
        df["availability"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )

    return df


def remove_duplicates(df):
    """Remove duplicate records."""

    df = df.copy()

    return df.drop_duplicates(
        subset=["product_url"]
    )


def validate_data(df):
    """Validate the cleaned dataset."""

    errors = []

    if df["title"].isnull().any():
        errors.append("Missing titles found.")

    if df["price"].isnull().any():
        errors.append("Invalid prices found.")

    if df["rating"].isnull().any():
        errors.append("Invalid ratings found.")

    if df["product_url"].duplicated().any():
        errors.append(
            "Duplicate product URLs found."
        )

    if (df["price"] < 0).any():
        errors.append(
            "Negative prices found."
        )

    if errors:

        print("\nVALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        return False

    print("\nVALIDATION PASSED")

    return True


def clean_dataset(df):
    """Run the complete cleaning pipeline."""

    df = clean_title(df)

    df = clean_price(df)

    df = clean_rating(df)

    df = clean_availability(df)

    df = remove_duplicates(df)

    return df


def save_data(df, output_file):
    """Save cleaned data."""

    df.to_csv(
        output_file,
        index=False
    )


def main():

    print("Loading raw data...")

    df = load_data(INPUT_FILE)

    print(f"Raw rows: {len(df)}")

    print("\nCleaning data...")

    cleaned_df = clean_dataset(df)

    print(
        f"Cleaned rows: {len(cleaned_df)}"
    )

    validate_data(cleaned_df)

    save_data(
        cleaned_df,
        OUTPUT_FILE
    )

    print("\n" + "=" * 45)
    print("CLEANING COMPLETE")
    print("=" * 45)

    print(
        f"\nClean data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()