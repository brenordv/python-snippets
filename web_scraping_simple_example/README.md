# Web Scraping Simple Example

Scrapes the Azure Cloud Adoption Framework resource-naming page, extracts naming conventions from HTML tables, merges them with locally cached data, and generates a Markdown cheatsheet with a summary table and a detailed list.

## Usage

```bash
# First run (scrapes live page and caches to new_resources.json)
python scrapping.py

# Subsequent runs use the cached file; delete new_resources.json to re-scrape
```
