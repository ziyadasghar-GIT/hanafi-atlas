#!/usr/bin/env python3
"""Add attribution header to all Hanafi Atlas pages + commit + push."""

import re
import os
import subprocess

BASE_DIR = "/home/mza/Desktop/hanafi-atlas"

HEADER_HTML = '''<div id="attribution-footer">
  <div class="attribution-inner">
    Created by Ziyad Asghar for the benefit of all students around the world, please remember me in your duas
  </div>
</div>'''

FOOTER_CSS = '''
#attribution-footer {
  width: 100%;
  text-align: center;
  padding: 14px 20px;
  background: rgba(10,15,13,0.95);
  border-top: 1px solid rgba(201,168,76,0.08);
  font-size: 12px;
  font-family: 'Inter', system-ui, sans-serif;
  letter-spacing: 0.02em;
}
.attribution-inner {
  max-width: 700px;
  margin: 0 auto;
  color: rgba(160,153,126,0.65);
  line-height: 1.5;
}

/* Dark theme adjustments for map.html */
.map-footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
}
.map-footer .attribution-inner {
  color: var(--text-dim);
}'''

def add_attribution_to_html(filepath, css_class=""):
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Don't add twice
    if 'attribution-footer' in html:
        print(f"  ⏭️ {os.path.basename(filepath)} already has footer")
        return False
    
    # Add CSS before </style>
    css_class_style = f".{css_class} {{ }}" if css_class else ""
    html = html.replace('</style>', f'{FOOTER_CSS}\n</style>')
    
    # Add footer HTML before </body>
    footer = HEADER_HTML
    if css_class:
        footer = footer.replace('attribution-footer', f'attribution-footer {css_class}')
    
    html = html.replace('</body>', f'{footer}\n</body>')
    
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"  ✅ {os.path.basename(filepath)} footer added")
    return True

# Add to all three pages
add_attribution_to_html(os.path.join(BASE_DIR, "network.html"))
add_attribution_to_html(os.path.join(BASE_DIR, "index.html"))
add_attribution_to_html(os.path.join(BASE_DIR, "map.html"), css_class="map-footer")

print("\n✅ Attribution header added to all pages.")

# Clean up temp scripts
for script in ['update_data.py', 'embed_data.py', 'embed_map.py', 'add_connections.py']:
    path = os.path.join(BASE_DIR, script)
    if os.path.exists(path):
        os.remove(path)
        print(f"🧹 Cleaned up {script}")

# Commit and push
print("\n--- Git Commit & Push ---")
os.chdir(BASE_DIR)
result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
print(result.stdout + result.stderr)

result = subprocess.run(
    ['git', 'commit', '-m', 'Add Pir Mehr Ali Shah, Anwar Shah Kashmiri, Tahir al-Qadri + verified peer connections + attribution footer'],
    capture_output=True, text=True
)
print(result.stdout + result.stderr)

result = subprocess.run(['git', 'push'], capture_output=True, text=True)
print(result.stdout + result.stderr)

print("\n✅ All done! Pushed to remote.")
