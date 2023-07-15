# -*- coding: utf-8 -*-
import json
from pathlib import Path
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup

"""
Quick example of how to scrap a website using BeautifulSoup.

Here we are scrapping this page:
https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming

The idea is to get the data from every table in that page, create a markdown file with:
    - Table with Resource name, Naming pattern, example
    - Alphabetical list of all the resources with the same information + extra data from another 
    file (old_resources.json)

For context, I tried using AI to generate this list for me, but it started hallucinating and I had to stop it.
So I saved the data it generated, and I'm using it here, but not the full thing, just the "naming convention" and
"length".
"""


def fetch_content(url, element="div", element_id="main-column"):
    # Fetch the content of the page
    response = requests.get(url)

    if not response.ok:
        raise Exception(f"Error fetching content. Error: {response.status_code}")

    # Parse the content
    soup = BeautifulSoup(response.text, "html.parser", from_encoding="utf-8")

    # Find the element with id element_id
    content = soup.find(element, {"id": element_id})

    # Check if content is valid
    if not content:
        raise Exception(f"Error fetching content. Element: {element} with id: {element_id} not found.")

    return content


def get_all_tables_from_content(content):
    # Find all tables in the content
    tables = content.find_all("table")

    # Check if tables are valid
    if not tables:
        raise Exception(f"Error fetching content. Tables not found.")

    return tables


def filter_tables_by_columns(tables, expected_columns):
    # Filter tables by expected columns
    filtered_tables = []
    for table in tables:
        columns = [column.text.strip() for column in table.find_all("th")]
        if not all(table_column in expected_columns for table_column in columns):
            continue

        filtered_tables.append(table)

    return filtered_tables


def extract_table_data(table):
    # Find all tr elements inside tbody
    rows = table.find("tbody").find_all("tr")

    # Extract data from each row
    data = {}

    # I know from visiting the page which columns are which, so I'm hard-coding it here
    for row in rows:
        td_elements = row.find_all("td")
        asset_type = td_elements[0].text.strip()
        scope = td_elements[1].text.strip()
        name_format = td_elements[2].find("em").text.replace(" ", " ").replace("\u00c2", "").strip()
        examples = [example.text.strip() for example in td_elements[2].find_all("code")]

        data[asset_type] = {
            "scope": scope,
            "name_format": name_format,
            "examples": examples
        }

    return data


def persist_data(data):
    # Persist data
    with open("new_resources.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=True)


def load_new_data():
    # Load new data
    try:
        with open("new_resources.json", "r") as f:
            data = json.load(f)

    except FileNotFoundError:
        data = {}

    return data


def load_old_data():
    # Load old data
    try:
        with open("old_resources.json", "r") as f:
            old_data = json.load(f)

    except FileNotFoundError:
        old_data = {}

    return old_data


def scrape_data(url):
    # Fetch content
    content = fetch_content(url)

    # Get all tables from content
    tables = get_all_tables_from_content(content)

    # Filter tables by expected columns
    required_columns = ["Asset type", "Scope", "Format and examples"]
    filtered_tables = filter_tables_by_columns(tables, required_columns)

    if len(filtered_tables) == 0:
        raise Exception(f"In the content fetched, no tables have the expected columns.")

    # Extract data from each table
    data = {}
    for table in filtered_tables:
        table_data = extract_table_data(table)
        data.update(table_data)

    # Save data
    persist_data(data)

    return data


def generate_markdown_cheatsheet_table(data):
    table_rows = [("Resource", "Pattern", "Examples")]
    for resource, resource_data in data.items():
        table_rows.append((resource, resource_data["name_format"], ", ".join(resource_data["examples"])))

    return tabulate(table_rows, headers='firstrow', tablefmt='pipe')


def generate_markdown_cheatsheet_list(data):
    lines = []

    # This method has a flaw: I'm assuming that old_data contains all the resources that can be found in data.
    for i, (resource, resource_data) in enumerate(data.items()):
        lines.append(f"{i+1}. **{resource}**")
        lines.append(f"    - Naming convention: {resource_data['Naming convention']}")
        lines.append(f"    - Format: {resource_data['name_format']}")
        lines.append(f"    - Length: {resource_data['Length']}")
        lines.append(f"    - Examples: {', '.join(resource_data['examples'])}")
        lines.append(f"    - Scope: {resource_data['scope']}")
        lines.append("")

    return "\n".join(lines)


def persist_final_markdown(url, markdown_table, markdown_list):
    with open("README.md", "w") as f:
        f.write(f"# Azure Resource Naming Convention\n\n")
        f.write(f"## Cheatsheet\n\n")
        f.write(f"{markdown_table}\n\n")
        f.write(f"## List\n\n")
        f.write(f"{markdown_list}\n\n")
        f.write(f"> Reference: {url}\n")


def get_corresponding_item(old_data, n_resource):
    target_name = n_resource.replace(" ", "").lower()
    for o_resource, o_resource_data in old_data.items():
        if o_resource.replace(" ", "").lower() != target_name:
            continue
        return o_resource_data

    return None


def merge_data(old_data, new_data):
    merged = {}
    orphans = {}

    for n_resource, n_resource_data in new_data.items():
        old_item = get_corresponding_item(old_data, n_resource)
        if old_item is None:
            orphans[n_resource] = n_resource_data
            continue

        n_resource_data.update(old_item)

        merged[n_resource] = n_resource_data

    if len(orphans) > 0:
        print(f"Found {len(orphans)} orphan resources. :/")
        print(orphans)

    return merged


def main(refresh=False):
    # Target URL
    url = "https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming"

    if refresh:
        # Fetch data from the page and save it
        data = scrape_data(url)
    else:
        # Load previously scrapped data from file
        data = load_new_data()

    # Load old data
    old_data = load_old_data()

    # Merge old and new data
    data = merge_data(old_data, data)

    # Sort data by key
    data = dict(sorted(data.items()))

    # Generate Markdown table
    markdown_table = generate_markdown_cheatsheet_table(data)

    # Generate Markdown detailed list
    markdown_list = generate_markdown_cheatsheet_list(data)

    # Create final Markdown file
    persist_final_markdown(url, markdown_table, markdown_list)


if __name__ == '__main__':
    main(refresh=not Path("new_resources.json").exists())
