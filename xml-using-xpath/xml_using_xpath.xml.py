# -*- coding: utf-8 -*-
"""
Demo of how to extract XML data using XPATH.

Part of a post from <https://raccoon.ninja>

If you a question about the script, feel free to contact me. If you want to know more about the XML, it's contents or
how it was structured, then contact it's author.
This XML Sample is part of an article and was slightly modified. Original can be found here:
<https://www.service-architecture.com/articles/object-oriented-databases/xml_file_for_complex_data.html>
"""


from xml.etree import ElementTree as ET_xml
from lxml import etree as ET_lxml


def get_root(xml_filename, engine):
    """Returns the root element of a XML file."""
    try:
        if engine == "xml":
            return ET_xml.parse(xml_filename).getroot()
        elif engine == "lxml":
            return ET_lxml.parse(xml_filename).getroot()
        else:
            raise ValueError("Wrong type of engine. Expecting: xml or lxml. Got: {}".format(engine))

    except FileNotFoundError as fnf_err:
        print("FATAL ERROR: XML file not found! (Filename: {})".format(xml_filename))
        print(fnf_err)
        return None

    except Exception as why:
        print("EVEN MORE FATAL ERROR! Wasn't expecting that...")
        print(why)
        return None


def example_01(root, cur_engine_name):
    """
    Simple search to get the VALUE of an ATTRIBUTE.
    :return: None
    """
    try:
        print("Looking for the GENDER for each CATALOG_ITEM inside the CATALOG...")
        for i, item in enumerate(root.findall("product/catalog_item")):
            print("\t{}: {}".format(i, item.attrib["gender"]))

        print("--| Success! [Engine: {}]".format(cur_engine_name))
    except:
        print("--| Failed! [Engine: {}]".format(cur_engine_name))


def example_02(root, cur_engine_name):
    """
    Simple search to get the TEXT (content) of an ELEMENT
    :return: None
    """
    try:
        print("Looking for the ITEM NUMBER for each CATALOG_ITEM inside the CATALOG...")
        for i, item in enumerate(root.findall("product/catalog_item/item_number")):
            print("\t{}: {}".format(i, item.text))

        print("--| Success! [Engine: {}]".format(cur_engine_name))
    except:
        print("--| Failed! [Engine: {}]".format(cur_engine_name))


def example_03(root, cur_engine_name):
    """
    Simple search to get the TEXT (content) of an ELEMENT
    :return: None
    """
    try:
        print("Looking for all COLOR_SWATCHES for MEDIUM products...")
        for i, item in enumerate(root.findall("product/catalog_item/size[@description='Medium']")):
            swatches = [s.text for s in item.findall("color_swatch")]
            print("\t{} Color swatches form MEDIUM: {}".format(i, ", ".join(swatches)))

        print("--| Success! [Engine: {}]".format(cur_engine_name))
    except:
        print("--| Failed! [Engine: {}]".format(cur_engine_name))


def example_03b(root, cur_engine_name):
    """
    Simple search to get the TEXT (content) of an ELEMENT
    :return: None
    """
    try:
        print("Looking for all COLOR_SWATCHES for MEDIUM products...")
        for i, item in enumerate(root.findall("product/catalog_item/size[@description='Medium']/color_swatch")):
            print("\t{} Color: {}".format(i, item.text))

        print("--| Success! [Engine: {}]".format(cur_engine_name))
    except:
        print("--| Failed! [Engine: {}]".format(cur_engine_name))


def example_04(root, cur_engine_name):
    """
    Will search for all COLOR_SWATCHES that have the text BLACK and that belongs only to LARGE and EXTRA LARGE products
    :return: None
    """
    try:
        print("Looking for black  COLOR_SWATCHES of LARGE and EXTRA LARGE products.")
        xpath_pattern = "product/catalog_item/size[contains(@description, 'Large')]/color_swatch[text()='Black']"
        for i, item in enumerate(root.xpath(xpath_pattern)):
            print("\t{}: Image: {}, Tag: {}, Text: {}".format(i, item.attrib["image"], item.tag, item.text))

        print("--| Success! [Engine: {}]".format(cur_engine_name))
    except:
        print("--| Failed! [Engine: {}]".format(cur_engine_name))


if __name__ == '__main__':
    engines = ["xml", "lxml"]
    xml_file = ".\\samples\\prod_catalog.xml"
    results = dict()

    for eng in engines:
        print("=======================================================================")
        print("TESTING ENGINE: {}".format(eng))
        root = get_root(xml_filename=xml_file, engine=eng)
        if root is None:
            print("Skipping tests with {}. Could not read XML with it...".format(eng))
            continue

        example_01(root=root, cur_engine_name=eng)
        print("-----------------------------------------------------------------------")
        example_02(root=root, cur_engine_name=eng)
        print("-----------------------------------------------------------------------")
        example_03(root=root, cur_engine_name=eng)
        print("-----------------------------------------------------------------------")
        example_03b(root=root, cur_engine_name=eng)
        print("-----------------------------------------------------------------------")
        example_04(root=root, cur_engine_name=eng)
        print("\n")

    print("All done!")
