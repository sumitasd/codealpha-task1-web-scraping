# Task 1 — Web Scraping Dataset (BeautifulSoup + requests)

## What this does
Scrapes the public website **https://books.toscrape.com/** and builds a CSV dataset with book-level fields.

Output CSV (created in the same folder):
- `books_dataset.csv`

Columns:
- `Title`
- `Price`
- `Availability`
- `Stock` (numeric extracted from availability)
- `Rating` (e.g., One/Two/Three… encoded as CSS classes)

## How it works (HTML structure)
This scraper relies on the catalog card structure on the page:
- Each book card: `article.product_pod`
- Title: `h3 a` (attribute `title`)
- Price: `p.price_color`
- Availability: `p.instock.availability` (contains text like `In stock (20 available)`)
- Rating: `p.star-rating` where the rating is stored as a CSS class such as:
  - `star-rating One`
  - `star-rating Two`

We parse those elements with **BeautifulSoup** selectors.

## Run
1. Install dependencies (if not already installed):
   ```bash
   py -m pip install requests beautifulsoup4 pandas
   ```
2. Run the scraper:
   ```bash
   py dataset_scraper.py
   ```

## Configuration
In `dataset_scraper.py`:
- `MAX_PAGES = 10`
  - Set to `None` to fetch until the site ends.

## Notes / Best practices
- Uses a browser-like `User-Agent` header.
- Adds `time.sleep(0.5)` between requests to be polite.
- Stops when:
  - `MAX_PAGES` is reached, or
  - a next-page request returns **404**, or
  - a page returns no book cards.

