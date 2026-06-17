#!/usr/bin/env python3
"""Embed JSON data files into index.html and map.html as inline <script> tags.

Usage: python3 embed_data.py

This reads data-scholars.json, data-places.json, data-chapters.json
and replaces the <script id="inlineData"> blocks in both HTML files.
"""

import json
import re

BASE = "/home/mza/Desktop/hanafi-atlas"


def load_json(filename):
    with open(f"{BASE}/{filename}", "r") as f:
        return json.load(f)


def build_inline_script(data):
    """Create the <script id="inlineData"> tag with embedded JSON."""
    json_str = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
    # Escape </script> inside JSON (unlikely but safe)
    json_str = json_str.replace("</script>", "<\\/script>")
    return f'<script id="inlineData" type="application/json">{json_str}</script>'


def embed_in_file(html_file, inline_script):
    """Replace the inlineData script tag in an HTML file."""
    with open(f"{BASE}/{html_file}", "r") as f:
        content = f.read()

    pattern = r'<script id="inlineData" type="application/json">.*?</script>'
    new_content = re.sub(pattern, inline_script, content, flags=re.DOTALL)

    if new_content == content:
        print(f"  ⚠️  No inlineData tag found in {html_file}")
        return False

    with open(f"{BASE}/{html_file}", "w") as f:
        f.write(new_content)
    return True


def main():
    print("Loading JSON data files...")
    scholars = load_json("data-scholars.json")
    places = load_json("data-places.json")
    chapters = load_json("data-chapters.json")
    print(f"  {len(scholars)} scholars, {len(places)} places, {len(chapters)} chapters")

    data = {"SCHOLARS": scholars, "PLACES": places, "CHAPTERS": chapters}
    inline_script = build_inline_script(data)
    print(f"  Inline data: {len(inline_script):,} chars")

    for html_file in ["index.html", "map.html"]:
        if embed_in_file(html_file, inline_script):
            print(f"  ✅ {html_file} updated")
        else:
            print(f"  ❌ {html_file} — no inlineData tag found")

    print("Done!")


if __name__ == "__main__":
    main()