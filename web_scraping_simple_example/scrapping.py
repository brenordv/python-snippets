"""Web scraper for Azure resource naming conventions.

Scrapes the Azure Cloud Adoption Framework naming page, merges with
locally cached data, and generates a Markdown cheatsheet (table + list).

Target page:
https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming
"""

import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Tag
from tabulate import tabulate


def fetch_content(
    url: str,
    element: str = "div",
    element_id: str = "main-column",
) -> Tag:
    """Fetch a page and return the BeautifulSoup element matching *element_id*."""
    response = requests.get(url, timeout=30)

    if not response.ok:
        raise RuntimeError(f"Error fetching content. Status: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser", from_encoding="utf-8")
    content = soup.find(element, {"id": element_id})

    if not content:
        raise RuntimeError(
            f"Element <{element} id='{element_id}'> not found in the page."
        )

    return content


def get_all_tables_from_content(content: Tag) -> list[Tag]:
    """Return all <table> elements found inside *content*."""
    tables = content.find_all("table")
    if not tables:
        raise RuntimeError("No tables found in the fetched content.")
    return tables


def filter_tables_by_columns(
    tables: list[Tag],
    expected_columns: list[str],
) -> list[Tag]:
    """Keep only tables whose header columns are a subset of *expected_columns*."""
    filtered: list[Tag] = []
    for table in tables:
        columns = [col.text.strip() for col in table.find_all("th")]
        if all(col in expected_columns for col in columns):
            filtered.append(table)
    return filtered


def extract_table_data(table: Tag) -> dict[str, dict]:
    """Parse rows from a naming-convention table into a dict keyed by asset type."""
    rows = table.find("tbody").find_all("tr")
    data: dict[str, dict] = {}

    for row in rows:
        cells = row.find_all("td")
        asset_type = cells[0].text.strip()
        scope = cells[1].text.strip()
        name_format = (
            cells[2]
            .find("em")
            .text.replace("\u00a0", " ")
            .replace("\u00c2", "")
            .strip()
        )
        examples = [code.text.strip() for code in cells[2].find_all("code")]

        data[asset_type] = {
            "scope": scope,
            "name_format": name_format,
            "examples": examples,
        }

    return data


def persist_data(data: dict, filename: str = "new_resources.json") -> None:
    """Write *data* to a JSON file."""
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True, ensure_ascii=True)


def load_json_file(filename: str) -> dict:
    """Load and return JSON data from *filename*, or an empty dict if missing."""
    try:
        with open(filename, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def scrape_data(url: str) -> dict:
    """Scrape the naming-convention tables from *url* and persist the result."""
    content = fetch_content(url)
    tables = get_all_tables_from_content(content)

    required_columns = ["Asset type", "Scope", "Format and examples"]
    filtered_tables = filter_tables_by_columns(tables, required_columns)

    if not filtered_tables:
        raise RuntimeError("No tables matched the expected columns.")

    data: dict = {}
    for table in filtered_tables:
        data.update(extract_table_data(table))

    persist_data(data)
    return data


def generate_markdown_cheatsheet_table(data: dict) -> str:
    """Return a Markdown pipe-table summarising each resource."""
    table_rows = [("Resource", "Pattern", "Examples")]
    for resource, info in data.items():
        table_rows.append((resource, info["name_format"], ", ".join(info["examples"])))
    return tabulate(table_rows, headers="firstrow", tablefmt="pipe")


def generate_markdown_cheatsheet_list(data: dict) -> str:
    """Return a numbered Markdown list with detailed resource info."""
    lines: list[str] = []
    for i, (resource, info) in enumerate(data.items(), start=1):
        lines.append(f"{i}. **{resource}**")
        lines.append(f"    - Naming convention: {info['Naming convention']}")
        lines.append(f"    - Format: {info['name_format']}")
        lines.append(f"    - Length: {info['Length']}")
        lines.append(f"    - Examples: {', '.join(info['examples'])}")
        lines.append(f"    - Scope: {info['scope']}")
        lines.append("")
    return "\n".join(lines)


def sanitize(text: str) -> str:
    """Escape angle brackets so Markdown renders correctly on GitHub."""
    return text.replace("<", "&lt;").replace(">", "&gt;")


def persist_final_markdown(
    url: str,
    markdown_table: str,
    markdown_list: str,
) -> None:
    """Write the final cheatsheet Markdown file."""
    markdown_table = sanitize(markdown_table)
    markdown_list = sanitize(markdown_list)

    with open("README.md", "w", encoding="utf-8") as fh:
        fh.write(f"# Azure Resource Naming Convention\n\n")
        fh.write(f"## Cheatsheet\n\n")
        fh.write(f"{markdown_table}\n\n")
        fh.write(f"## List\n\n")
        fh.write(f"{markdown_list}\n\n")
        fh.write(f"> Reference: {url}\n")


def get_corresponding_item(old_data: dict, resource_name: str) -> dict | None:
    """Find a matching entry in *old_data* by case-/space-insensitive name."""
    target = resource_name.replace(" ", "").lower()
    for key, value in old_data.items():
        if key.replace(" ", "").lower() == target:
            return value
    return None


def merge_data(old_data: dict, new_data: dict) -> dict:
    """Merge old (AI-generated) data with freshly scraped data."""
    merged: dict = {}
    orphans: dict = {}

    for resource, resource_data in new_data.items():
        old_item = get_corresponding_item(old_data, resource)
        if old_item is None:
            orphans[resource] = resource_data
            continue
        resource_data.update(old_item)
        merged[resource] = resource_data

    if orphans:
        print(f"Found {len(orphans)} orphan resources (no match in old data).")
        print(orphans)

    return merged


def main(refresh: bool = False) -> None:
    """Scrape (or load cached) data, merge, and generate the Markdown cheatsheet."""
    url = (
        "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/"
        "ready/azure-best-practices/resource-naming"
    )

    if refresh:
        data = scrape_data(url)
    else:
        data = load_json_file("new_resources.json")

    old_data = load_json_file("old_resources.json")
    data = merge_data(old_data, data)
    data = dict(sorted(data.items()))

    markdown_table = generate_markdown_cheatsheet_table(data)
    markdown_list = generate_markdown_cheatsheet_list(data)
    persist_final_markdown(url, markdown_table, markdown_list)


if __name__ == "__main__":
    main(refresh=not Path("new_resources.json").exists())
