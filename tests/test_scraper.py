import csv
import tempfile
import unittest
from pathlib import Path

from scraper import load_html, parse_quotes, write_csv


SAMPLE_HTML = """
<html><body>
<div class=\"quote\">
  <span class=\"text\">“Example quote one.”</span>
  <span>by <small class=\"author\">Author One</small></span>
  <div class=\"tags\"><a class=\"tag\">life</a><a class=\"tag\">inspire</a></div>
</div>
<div class=\"quote\">
  <span class=\"text\">“Example quote two.”</span>
  <span>by <small class=\"author\">Author Two</small></span>
  <div class=\"tags\"><a class=\"tag\">humor</a></div>
</div>
</body></html>
"""


class ScraperTests(unittest.TestCase):
    def test_parse_quotes_extracts_expected_fields(self):
        rows = parse_quotes(SAMPLE_HTML)
        self.assertEqual(2, len(rows))
        self.assertEqual("Author One", rows[0]["author"])
        self.assertEqual("life, inspire", rows[0]["tags"])

    def test_load_html_and_write_csv_integration(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "sample.html"
            csv_path = Path(tmpdir) / "output.csv"

            html_path.write_text(SAMPLE_HTML, encoding="utf-8")
            html = load_html(url=None, input_file=str(html_path))
            rows = parse_quotes(html)
            write_csv(rows, str(csv_path))

            with csv_path.open(newline="", encoding="utf-8") as file:
                csv_rows = list(csv.DictReader(file))

            self.assertEqual(2, len(csv_rows))
            self.assertEqual("Author Two", csv_rows[1]["author"])

    def test_load_html_requires_source(self):
        with self.assertRaises(ValueError):
            load_html(url=None, input_file=None)


if __name__ == "__main__":
    unittest.main()
