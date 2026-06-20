#!/usr/bin/env python3
"""Re-embed all data after adding Nadwi."""

import json, re, os

BASE_DIR = "/home/mza/Desktop/hanafi-atlas"

with open(os.path.join(BASE_DIR, "data-scholars.json")) as f:
    scholars = json.load(f)
with open(os.path.join(BASE_DIR, "data-graph.json")) as f:
    graph = json.load(f)
with open(os.path.join(BASE_DIR, "data-places.json")) as f:
    places = json.load(f)

def replace_inline(filepath, new_data):
    with open(filepath) as f:
        html = f.read()
    new_json = json.dumps(new_data, indent=None, ensure_ascii=False)
    replacement = f'<script id="inlineData" type="application/json">{new_json}</script>'
    html_new = re.sub(
        r'<script id="inlineData" type="application/json">.*?</script>',
        replacement, html, count=1, flags=re.DOTALL
    )
    with open(filepath, 'w') as f:
        f.write(html_new)
    return html_new != html

replace_inline(os.path.join(BASE_DIR, "network.html"), graph)
print("✅ network.html")

replace_inline(os.path.join(BASE_DIR, "index.html"), {"SCHOLARS": scholars})
print("✅ index.html")

with open(os.path.join(BASE_DIR, "map.html")) as f:
    html = f.read()
match = re.search(r'<script id="inlineData" type="application/json">(.*?)</script>', html, re.DOTALL)
chapters = json.loads(match.group(1)).get("CHAPTERS", []) if match else []
replace_inline(os.path.join(BASE_DIR, "map.html"), {"SCHOLARS": scholars, "PLACES": places, "CHAPTERS": chapters})
print("✅ map.html")

import subprocess, os as os2
os2.chdir(BASE_DIR)
for s in ['add_nadwi.py']:
    p = os2.path.join(BASE_DIR, s)
    if os2.path.exists(p): os2.remove(p)

subprocess.run(['git', 'add', '-A'], capture_output=True)
subprocess.run(['git', 'commit', '-m', 'Add Abul Hasan Ali Nadwi (Abū al-Ḥasan al-Nadwī) - 20th c. Hanafi scholar, chancellor of Nadwat al-Ulama, author of Islam and the World'], capture_output=True)
r = subprocess.run(['git', 'push'], capture_output=True, text=True)
print(r.stdout + r.stderr)
print("✅ All done!")
