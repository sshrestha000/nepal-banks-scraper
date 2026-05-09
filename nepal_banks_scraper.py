from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# ── Config ────────────────────────────────────────────────────────────────────
URL = 'https://en.wikipedia.org/wiki/List_of_banks_in_Nepal'
HEADERS = {
    'User-Agent': 'mydataanalysisbot/1.1 Learning web scraping'
}
OUTPUT_DIR = 'data'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Fetch page ────────────────────────────────────────────────────────────────
response = requests.get(URL, headers=HEADERS)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', class_='wikitable')
print(f"Found {len(tables)} tables on page")


# ── Helper: parse one wikitable into a DataFrame ─────────────────────────────
def parse_table(table, skip_rows=1):
    # Headers
    raw_headers = table.find_all('th')
    headers = [th.get_text(strip=True) for th in raw_headers]
    # Remove duplicates while preserving order
    seen = {}
    clean_headers = []
    for h in headers:
        if h in seen:
            seen[h] += 1
            clean_headers.append(f"{h}_{seen[h]}")
        else:
            seen[h] = 0
            clean_headers.append(h)

    # Rows
    rows = []
    for row in table.find_all('tr')[skip_rows:]:
        cols = row.find_all('td')
        if not cols:
            continue
        row_data = [col.get_text(strip=True) for col in cols]
        # Only keep rows that match header length
        if len(row_data) == len(clean_headers):
            rows.append(row_data)

    return pd.DataFrame(rows, columns=clean_headers)


# ── Scrape each class ─────────────────────────────────────────────────────────
class_configs = [
    {'index': 0, 'name': 'ClassA_Commercial_Banks', 'skip_rows': 1},
    {'index': 1, 'name': 'ClassB_Development_Banks', 'skip_rows': 2},
    {'index': 2, 'name': 'ClassC_Finance_Companies', 'skip_rows': 2},
]

for config in class_configs:
    idx = config['index']
    if idx >= len(tables):
        print(f"Table {idx} not found — skipping {config['name']}")
        continue

    df = parse_table(tables[idx], skip_rows=config['skip_rows'])
    out_path = os.path.join(OUTPUT_DIR, f"{config['name']}.csv")
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f" {config['name']}: {len(df)} rows → {out_path}")

print("\n All files saved to /data/")
print(f"Saving to: {os.path.abspath(OUTPUT_DIR)}")