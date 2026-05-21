import pandas as pd
from pathlib import Path

# Read CSV
csv_path = Path(__file__).parent / "books_dataset.csv"
df = pd.read_csv(csv_path)

# Calculate stats
avg_price = df["Price"].str.replace("£", "").astype(float).mean()
rating_counts = df["Rating"].value_counts().to_dict()

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

html_path = Path(__file__).parent / "books_dataset.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Professional HTML Report Generated!")
print(f"📊 Total Books: {len(df)}")
print(f"💰 Average Price: £{avg_price:.2f}")
print(f"⭐ Report saved: {html_path}")
