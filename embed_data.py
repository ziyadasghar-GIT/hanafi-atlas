#!/usr/bin/env python3
"""Re-embed JSON data files into inline <script> tags in all three HTML files.

Reads data-scholars.json, data-places.json, data-chapters.json, and data-graph.json
and updates the <script id="inlineData" type="application/json"> blocks in:
  - index.html  → SCHOLARS only
  - map.html    → SCHOLARS + PLACES + CHAPTERS
  - network.html → nodes + edges (from data-graph.json)
"""

import json
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT)

def read_json(filename):
    with open(filename) as f:
        return json.load(f)

def embed_in_html(html_path, data_dict):
    """Replace inlineData script tag in HTML with new JSON data."""
    with open(html_path) as f:
        html = f.read()

    json_str = json.dumps(data_dict, ensure_ascii=False, separators=(',', ':'))

    # Match the existing inlineData script tag
    pattern = r'<script id="inlineData" type="application/json">.*?</script>'
    replacement = f'<script id="inlineData" type="application/json">{json_str}</script>'

    new_html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

    if new_html == html:
        print(f"  ⚠️  {html_path}: data unchanged (already up to date)")
        return True

    with open(html_path, 'w') as f:
        f.write(new_html)

    # Verify the data is parseable
    match = re.search(pattern, new_html, re.DOTALL)
    if match:
        inner = re.sub(r'<script[^>]*>|</script>', '', match.group())
        try:
            parsed = json.loads(inner)
            keys = list(parsed.keys())
            print(f"  ✅ {html_path}: keys={keys} len={len(json_str)}")
            return True
        except json.JSONDecodeError as e:
            print(f"  ❌ {html_path}: invalid JSON — {e}")
            return False
    return False

# ── Load data ──
scholars = read_json('data-scholars.json')
places = read_json('data-places.json')
chapters = read_json('data-chapters.json')
graph = read_json('data-graph.json')

print(f"Loaded: {len(scholars)} scholars, {len(places)} places, {len(chapters)} chapters, {len(graph['nodes'])} graph nodes, {len(graph['edges'])} graph edges")
print()

# ── Embed ──
print("Embedding:")
embed_in_html('index.html', {'SCHOLARS': scholars})
embed_in_html('map.html', {
    'SCHOLARS': scholars,
    'PLACES': places,
    'CHAPTERS': chapters
})
embed_in_html('network.html', {
    'nodes': graph['nodes'],
    'edges': graph['edges']
})

print("\n✅ Done — all three HTML files updated with inline data")
