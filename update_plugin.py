#!/usr/bin/env python3
"""Update a plugin entry in plugins.xml.

Usage: python update_plugin.py <xml_path> <plugin_name> <version> <download_url>

Example:
    python update_plugin.py plugins.xml "Search and Replace" 0.2 \
        https://github.com/ZedeN1/SearchAndReplace/releases/download/v0.2/SearchAndReplace.0.2.zip
"""
import sys
import xml.etree.ElementTree as ET


def strip_whitespace(element):
    """Remove whitespace-only text/tail nodes so ET.indent works cleanly on re-parsed XML."""
    for elem in element.iter():
        if elem.text and not elem.text.strip():
            elem.text = None
        if elem.tail and not elem.tail.strip():
            elem.tail = None


def update_plugin(xml_path, plugin_name, version, download_url):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for plugin in root.findall("pyqgis_plugin"):
        if plugin.get("name") == plugin_name:
            plugin.set("version", version)
            plugin.find("version").text = version
            plugin.find("download_url").text = download_url
            strip_whitespace(root)
            ET.indent(root, space="  ")
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write(ET.tostring(root, encoding="unicode"))
                f.write("\n")
            print(f"Updated '{plugin_name}' to {version}")
            return

    print(f"ERROR: Plugin '{plugin_name}' not found in {xml_path}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            f"Usage: {sys.argv[0]} <xml_path> <plugin_name> <version> <download_url>",
            file=sys.stderr,
        )
        sys.exit(1)
    update_plugin(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
