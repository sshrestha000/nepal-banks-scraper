# nepal-banks-scraper
Python web scraper that extracts bank data from Wikipedia and exports to CSV


# Nepal Banks Web Scraper

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Source](https://img.shields.io/badge/source-Wikipedia-lightgrey)

**Author:** Sushmita Shrestha  
**Tools:** Python · BeautifulSoup · Requests · Pandas  
**Source:** [Wikipedia — List of Banks in Nepal](https://en.wikipedia.org/wiki/List_of_banks_in_Nepal)

---

## Overview
End-to-end data extraction pipeline that scrapes Nepal's banking registry from Wikipedia across three bank classes (Commercial, Development, Finance), normalizes raw HTML tables into structured schemas, and exports clean CSV output for downstream analysis.

Built as part of a data engineering portfolio — demonstrating HTTP request handling, HTML parsing, schema normalization, and reusable pipeline design.

---

## Output

Three CSV files, one per bank class licensed by Nepal Rastra Bank:

| File | Class | Description |
|------|-------|-------------|
| `ClassA_Commercial_Banks.csv` | A | Full-service commercial banks |
| `ClassB_Development_Banks.csv` | B | Development banks |
| `ClassC_Finance_Companies.csv` | C | Finance companies |

### Sample Data — Class A Commercial Banks

| Bank Name | Headquarters | Total Assets (Arab NPR) | Branches |
|-----------|-------------|------------------------|----------|
| Global IME Bank | Kathmandu | 674.84 | 439 |
| Nabil Bank | Kathmandu | 651.15 | 293 |
| Nepal Investment Mega Bank | Kathmandu | 606.21 | 339 |
| NIC Asia Bank | Kathmandu | 380.14 | 474 |
| Standard Chartered Bank | Kathmandu | 156.12 | 18 |

### Key Insights

1. **Global IME Bank** leads by total assets (रु 674.84 Arab) — largest balance sheet in the sector
2. **NIC Asia Bank** has the widest branch network (474) despite ranking 4th by assets — high retail reach relative to size
3. **Standard Chartered** runs a low-volume, high-value model: only 18 branches, premium international positioning

---

## Pipeline Design

```
fetch page → parse HTML tables → normalize schema → validate rows → export CSV
```

A single reusable `parse_table()` function handles all three bank classes — one fix applies everywhere rather than maintaining three separate code blocks.

---

## Project Structure

```
nepal-banks-scraper/
│
├── README.md
├── nepal_banks_scraper.py    ← main scraper script
└── ClassA_Commercial_Banks.csv    ← sample output
```

---

## How to Run

```bash
git clone https://github.com/sshrestha000/nepal-banks-scraper
cd nepal-banks-scraper
pip install requests beautifulsoup4 pandas
python nepal_banks_scraper.py
```

CSVs will be saved to `data/` — the folder is created automatically if it doesn't exist.

---

## Engineering Notes

- `raise_for_status()` surfaces HTTP failures immediately rather than silently parsing error pages
- Row-length validation (`len(row_data) == len(headers)`) filters malformed rows from inconsistent Wikipedia table formatting
- List-first DataFrame construction — rows collected into a list, DataFrame built once — avoids slow row-by-row `loc` appending
- `get_text(strip=True)` handles nested tags more cleanly than `.text.strip()`
- Relative output paths (`data/`) work on any machine — no hardcoded local paths
- `encoding='utf-8-sig'` ensures Nepali characters (रु) render correctly in Excel

---

## Next Steps

- [ ] Parse numeric columns — extract floats from `रु X Arab` format
- [ ] Add Pandas analysis notebook: asset rankings, branch-to-capital ratio, HQ distribution
- [ ] Schedule monthly runs to track registry changes over time
