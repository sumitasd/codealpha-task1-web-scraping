import argparse
import csv
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

DEFAULT_URL = "https://quotes.toscrape.com/"
DEFAULT_OUTPUT = "scraped_quotes.csv"


def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def parse_quotes(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: List[Dict[str, str]] = []

    for quote in soup.select("div.quote"):
        text = quote.select_one("span.text")
        author = quote.select_one("small.author")
        tags = [tag.get_text(strip=True) for tag in quote.select("div.tags a.tag")]

        if text and author:
            rows.append(
                {
                    "quote": text.get_text(strip=True),
                    "author": author.get_text(strip=True),
                    "tags": ", ".join(tags),
                }
            )

    return rows


def write_csv(rows: List[Dict[str, str]], output_file: str) -> None:
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author", "tags"])
        writer.writeheader()
        writer.writerows(rows)


def load_html(url: str, input_file: str | None) -> str:
    if input_file:
        with open(input_file, "r", encoding="utf-8") as file:
            return file.read()
    return fetch_page(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape quote data and save it to CSV.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Website URL to scrape")
    parser.add_argument(
        "--input-file",
        default=None,
        help="Optional local HTML file path. If set, URL fetching is skipped.",
    )
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT, help="CSV file path to write scraped data"
    )
    args = parser.parse_args()

    html = load_html(args.url, args.input_file)
    rows = parse_quotes(html)
    write_csv(rows, args.output)
    print(f"Saved {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
