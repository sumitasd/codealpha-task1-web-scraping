# codealpha-task1-web-scraping

Python web scraping project using `BeautifulSoup` that extracts website data and stores it in CSV format.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Run scraper

```bash
python scraper.py
```

This scrapes quote data from `https://quotes.toscrape.com/` and saves it to `scraped_quotes.csv`.

Optional arguments:

```bash
python scraper.py --url https://quotes.toscrape.com/ --output my_data.csv
```

For offline/local HTML scraping:

```bash
python scraper.py --input-file /path/to/page.html --output my_data.csv
```
