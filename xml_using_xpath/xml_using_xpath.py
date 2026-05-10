"""Demo of extracting XML data using XPath with both stdlib xml.etree and lxml.

Runs the same set of queries against a product catalog XML file using both
engines side by side, showing where stdlib falls short (e.g. contains(), text()).

Based on a post from https://raccoon.ninja
Sample XML source: https://www.service-architecture.com/articles/object-oriented-databases/xml_file_for_complex_data.html
"""

from pathlib import Path
from xml.etree import ElementTree as ET_xml

from lxml import etree as ET_lxml


def get_root(xml_filename: str, engine: str):
    """Parse an XML file and return the root element.

    Args:
        xml_filename: Path to the XML file.
        engine: Either "xml" (stdlib) or "lxml".

    Returns:
        The root element, or None on failure.
    """
    try:
        if engine == "xml":
            return ET_xml.parse(xml_filename).getroot()
        elif engine == "lxml":
            return ET_lxml.parse(xml_filename).getroot()
        else:
            raise ValueError(f"Unknown engine '{engine}'. Expected: xml or lxml.")
    except FileNotFoundError:
        print(f"FATAL ERROR: XML file not found! (Filename: {xml_filename})")
        return None
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return None


def example_01(root, engine_name: str) -> None:
    """Get the GENDER attribute from each catalog_item."""
    try:
        print("Looking for the GENDER for each CATALOG_ITEM inside the CATALOG...")
        for i, item in enumerate(root.findall("product/catalog_item")):
            print(f"\t{i}: {item.attrib['gender']}")
        print(f"--| Success! [Engine: {engine_name}]")
    except Exception:
        print(f"--| Failed! [Engine: {engine_name}]")


def example_02(root, engine_name: str) -> None:
    """Get the text content of item_number elements."""
    try:
        print("Looking for the ITEM NUMBER for each CATALOG_ITEM inside the CATALOG...")
        for i, item in enumerate(root.findall("product/catalog_item/item_number")):
            print(f"\t{i}: {item.text}")
        print(f"--| Success! [Engine: {engine_name}]")
    except Exception:
        print(f"--| Failed! [Engine: {engine_name}]")


def example_03(root, engine_name: str) -> None:
    """Get color swatches for Medium products (grouped by catalog_item)."""
    try:
        print("Looking for all COLOR_SWATCHES for MEDIUM products...")
        for i, item in enumerate(
            root.findall("product/catalog_item/size[@description='Medium']")
        ):
            swatches = [s.text for s in item.findall("color_swatch")]
            print(f"\t{i} Color swatches for MEDIUM: {', '.join(swatches)}")
        print(f"--| Success! [Engine: {engine_name}]")
    except Exception:
        print(f"--| Failed! [Engine: {engine_name}]")


def example_03b(root, engine_name: str) -> None:
    """Get color swatches for Medium products (flat list)."""
    try:
        print("Looking for all COLOR_SWATCHES for MEDIUM products...")
        for i, item in enumerate(
            root.findall(
                "product/catalog_item/size[@description='Medium']/color_swatch"
            )
        ):
            print(f"\t{i} Color: {item.text}")
        print(f"--| Success! [Engine: {engine_name}]")
    except Exception:
        print(f"--| Failed! [Engine: {engine_name}]")


def example_04(root, engine_name: str) -> None:
    """Find Black color swatches for Large and Extra Large products (lxml only).

    Uses contains() and text() XPath functions which are not supported by
    the stdlib xml.etree module.
    """
    try:
        print("Looking for black COLOR_SWATCHES of LARGE and EXTRA LARGE products.")
        xpath = (
            "product/catalog_item"
            "/size[contains(@description, 'Large')]"
            "/color_swatch[text()='Black']"
        )
        for i, item in enumerate(root.xpath(xpath)):
            print(
                f"\t{i}: Image: {item.attrib['image']}, "
                f"Tag: {item.tag}, Text: {item.text}"
            )
        print(f"--| Success! [Engine: {engine_name}]")
    except Exception:
        print(f"--| Failed! [Engine: {engine_name}]")


if __name__ == "__main__":
    engines = ["xml", "lxml"]
    xml_file = str(Path(__file__).parent / "samples" / "prod_catalog.xml")

    for eng in engines:
        print("=" * 71)
        print(f"TESTING ENGINE: {eng}")
        root = get_root(xml_filename=xml_file, engine=eng)
        if root is None:
            print(f"Skipping tests with {eng}. Could not read XML.")
            continue

        example_01(root=root, engine_name=eng)
        print("-" * 71)
        example_02(root=root, engine_name=eng)
        print("-" * 71)
        example_03(root=root, engine_name=eng)
        print("-" * 71)
        example_03b(root=root, engine_name=eng)
        print("-" * 71)
        example_04(root=root, engine_name=eng)
        print()

    print("All done!")
