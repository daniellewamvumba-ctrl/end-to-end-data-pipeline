import csv
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
OUTPUT_FILE = "data/raw/books_raw.csv"


def fetch_page(url):
    """Fetch a webpage and return the HTML."""

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.text


def parse_books(html):
    """Extract book information from one page."""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    books = []

    for article in soup.select("article.product_pod"):

        title = article.h3.a["title"]

        price = article.select_one(
            ".price_color"
        ).text.strip()

        rating = article.select_one(
            "p.star-rating"
        )["class"][1]

        availability = article.select_one(
            ".availability"
        ).text.strip()

        relative_url = article.h3.a["href"]

        product_url = (
            "https://books.toscrape.com/catalogue/"
            + relative_url.replace("../", "")
        )

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "product_url": product_url
        })

    return books


def scrape_books(number_of_pages=5):
    """Scrape books from multiple pages."""

    all_books = []

    for page in range(1, number_of_pages + 1):

        url = BASE_URL.format(page)

        print(f"Scraping page {page}...")

        html = fetch_page(url)

        books = parse_books(html)

        all_books.extend(books)

        print(
            f"  Books collected: {len(books)}"
        )

    return all_books


def save_books(books, output_file):
    """Save scraped books to CSV."""

    if not books:
        print("No books were collected.")

        return

    fieldnames = books[0].keys()

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(books)


def main():

    number_of_pages = 5

    books = scrape_books(
        number_of_pages
    )

    save_books(
        books,
        OUTPUT_FILE
    )

    print("\n" + "=" * 45)
    print("SCRAPING COMPLETE")
    print("=" * 45)

    print(
        f"\nTotal books collected: {len(books)}"
    )

    print(
        f"Raw data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()