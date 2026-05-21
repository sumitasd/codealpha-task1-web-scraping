"""Web Scraping Dataset Builder (BeautifulSoup + requests)

Scrapes public data from https://books.toscrape.com/
and saves it as a CSV dataset.

Run:
    py dataset_scraper.py

Output:
    books_dataset.csv (in the same folder)
"""

from __future__ import annotations

import datetime
import re
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT_CSV = Path(__file__).with_name("books_dataset.csv")

# Limit pages for faster runs. Set to None to fetch until site ends.
MAX_PAGES: int | None = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def build_page_url(page_index: int) -> str:
    """books.toscrape uses page-2.html, page-3.html ...; first page is just /"""
    if page_index == 1:
        return BASE_URL
    return f"{BASE_URL}catalogue/page-{page_index}.html"


def parse_books_from_page(html: str) -> list[dict]:
    """Extracts rows for all books present on a single catalog page."""
    soup = BeautifulSoup(html, "html.parser")
    books = soup.select("article.product_pod")

    rows: list[dict] = []
    for book in books:
        # Title
        title_tag = book.select_one("h3 a")
        title = title_tag.get("title", "").strip() if title_tag else ""

        # Price
        price_tag = book.select_one("p.price_color")
        price = price_tag.get_text(strip=True) if price_tag else ""

        # Availability
        avail_tag = book.select_one("p.instock.availability")
        availability = avail_tag.get_text(" ", strip=True) if avail_tag else ""

        # Extract numeric stock if present (e.g. 'In stock (20 available)')
        stock = ""
        m = re.search(r"(\d+)", availability)
        if m:
            stock = int(m.group(1))

        # Rating is encoded as a class on the star element, e.g. 'One'/'Two'...
        rating = ""
        rating_tag = book.select_one("p.star-rating")
        if rating_tag and rating_tag.has_attr("class"):
            classes = [c for c in rating_tag.get("class", []) if c.lower() != "star-rating"]
            rating = classes[0] if classes else ""

        rows.append(
            {
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Stock": stock,
                "Rating": rating,
            }
        )

    return rows


def scrape_books() -> pd.DataFrame:
    data: list[dict] = []
    page = 1

    start_time = time.time()
    print("Starting scrape...")

    while True:
        if isinstance(MAX_PAGES, int) and page > MAX_PAGES:
            print(f"Reached MAX_PAGES={MAX_PAGES}. Stopping.")
            break

        url = build_page_url(page)
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
        except requests.RequestException as exc:
            print(f"Request failed on page {page}: {exc}")
            break

        # Last page returns 404 on the next page; treat it as done.
        if resp.status_code == 404:
            print("Reached end of site (404). Stopping.")
            break

        resp.raise_for_status()
        resp.encoding = "utf-8"

        page_rows = parse_books_from_page(resp.text)
        if not page_rows:
            print("No books found on page. Stopping.")
            break

        data.extend(page_rows)
        print(f"Processed page {page} | total rows: {len(data)}")
        page += 1

        # Be polite
        time.sleep(0.5)

    df = pd.DataFrame(data)
    return df


def generate_html_report(df: pd.DataFrame, output_path: Path) -> None:
    """Generate a professional HTML report from the dataset."""
    html_path = output_path.with_suffix(".html")
    
    avg_price = df["Price"].str.replace("£", "").astype(float).mean() if "Price" in df.columns else 0
    rating_counts = df["Rating"].value_counts().to_dict() if "Rating" in df.columns else {}
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Books Dataset Report</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 40px 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 30px; text-align: center; }}
            .header h1 {{ color: #667eea; font-size: 2.5em; margin-bottom: 10px; }}
            .header p {{ color: #666; font-size: 1.1em; }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .stat-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); text-align: center; }}
            .stat-value {{ font-size: 2em; color: #667eea; font-weight: bold; }}
            .stat-label {{ color: #999; margin-top: 10px; font-size: 0.9em; }}
            .table-container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; text-align: left; font-weight: 600; }}
            td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
            tr:hover {{ background: #f5f5f5; }}
            .rating {{ display: inline-block; padding: 5px 10px; background: #f0f0f0; border-radius: 5px; font-weight: bold; color: #667eea; }}
            .price {{ color: #27ae60; font-weight: bold; }}
            .available {{ color: #27ae60; }}
            .footer {{ text-align: center; color: white; margin-top: 30px; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Books Dataset Report</h1>
                <p>Professional Web Scraping Analysis - books.toscrape.com</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">{len(df)}</div>
                    <div class="stat-label">Total Books</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">£{avg_price:.2f}</div>
                    <div class="stat-label">Avg Price</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{len(rating_counts)}</div>
                    <div class="stat-label">Rating Types</div>
                </div>
            </div>
            
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Price</th>
                            <th>Availability</th>
                            <th>Stock</th>
                            <th>Rating</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for _, row in df.iterrows():
        html_content += f"""
                        <tr>
                            <td>{row.get('Title', 'N/A')}</td>
                            <td class="price">{row.get('Price', 'N/A')}</td>
                            <td class="available">{row.get('Availability', 'N/A')}</td>
                            <td>{row.get('Stock', 'N/A')}</td>
                            <td><span class="rating">★ {row.get('Rating', 'N/A')}</span></td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            <div class="footer">
                <p>Generated automatically • Data sourced from books.toscrape.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return html_path


def main() -> None:
    start_time = time.time()
    df = scrape_books()
    df.to_csv(OUTPUT_CSV, index=False)
    
    # Generate professional HTML report
    html_report = generate_html_report(df, OUTPUT_CSV)

    duration = time.time() - start_time

    print("\n" + "="*60)
    print("🎯 SCRAPE SUMMARY - PROFESSIONAL REPORT GENERATED")
    print("="*60)
    print(f"✅ Total Books Collected: {len(df)}")
    print(f"📊 CSV File: {OUTPUT_CSV}")
    print(f"🌐 HTML Report: {html_report}")
    print(f"⏱️  Duration: {duration:.2f}s")
    print("="*60)

    # Quick preview
    if len(df) > 0:
        print("\n📋 TOP 5 BOOKS PREVIEW:")
        print("-" * 60)
        preview_df = df.head(5)[["Title", "Price", "Rating"]].copy()
        for idx, row in preview_df.iterrows():
            print(f"{idx+1}. {row['Title'][:50]:<50} | {row['Price']:>8} | ⭐ {row['Rating']}")
        print("-" * 60)
        print(f"\n✨ Open the HTML file in browser for full professional view!")


if __name__ == "__main__":
    main()
