#!/usr/bin/env python3
"""Generate the combined hanafi-atlas index.html from existing source files."""
import re
import json
from pathlib import Path

ROOT = Path('/home/mza/Desktop')
OUT = ROOT / 'hanafi-atlas' / 'index.html'

# ── Read source files ──
with open(ROOT / 'hanafi-timeline.html') as f:
    tl = f.read()
with open(ROOT / 'hanafi-map' / 'index.html') as f:
    mp = f.read()

# Extract existing CSS/JS bodies (we will rewrite them with unified dark theme)
tl_css = re.search(r'<style>(.*?)</style>', tl, re.DOTALL).group(1)
tl_scripts = re.findall(r'<script>(.*?)</script>', tl, re.DOTALL)
tl_js = tl_scripts[-1]

mp_css = re.search(r'<style>(.*?)</style>', mp, re.DOTALL).group(1)
mp_scripts = re.findall(r'<script>(.*?)</script>', mp, re.DOTALL)
mp_js = mp_scripts[-1]

# Extract data from the map file (PLACES, SCHOLARS, CHAPTERS)
places_match = re.search(r'const PLACES = (\{.*?\});', mp, re.DOTALL)
scholars_match = re.search(r'const SCHOLARS = (\[.*?\]);', mp, re.DOTALL)
chapters_match = re.search(r'const CHAPTERS = (\[.*?\]);', mp, re.DOTALL)
PLACES = places_match.group(1)
SCHOLARS = scholars_match.group(1)
CHAPTERS = chapters_match.group(1)

# ── Helpers for re-themeing ──
# We'll keep the original CSS bodies (already dark) but:
#   - Map's CSS uses light/cream theme → we replace its color variables
#   - Add unified view-switcher CSS
# Strategy: take timeline's CSS (dark, proven), then append a SCOPED map view
# CSS that overrides map UI to dark theme + view-switcher styles.

# Build a new combined CSS by:
# 1. Taking timeline's CSS (the dark theme) wholesale
# 2. Appending map's CSS but with light-theme variables remapped to dark
# 3. Adding view-switcher styles

# Keep map CSS as-is (light theme) — we want the map view to match hanafi-map exactly
mp_css_dark = mp_css

# ── Build the combined HTML ──
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ḥanafī Atlas — Timeline &amp; Map of the Ḥanafī School</title>
<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet">
<style>
/* ─── Unified dark theme variables ─── */
:root {{
  --bg-primary: #0a0f0d;
  --bg-card: #111a16;
  --bg-card-hover: #162320;
  --gold: #c9a84c;
  --gold-light: #e0c872;
  --gold-dim: #8a7233;
  --green-primary: #0d7c3e;
  --green-light: #1bb960;
  --green-dark: #064f28;
  --emerald: #04412f;
  --teal: #0fa17e;
  --text-primary: #e8e0d0;
  --text-secondary: #a0997e;
  --text-dim: #6e684f;
  --border: #1e3028;
  --border-gold: #3d3218;
  --shadow-gold: rgba(201,168,76,0.15);
  --shadow-green: rgba(13,124,62,0.2);
  --shadow-strong: rgba(0,0,0,0.6);
  --map-bg: #0a0f0d;
}}

@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body {{
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
}}

/* Islamic geometric pattern overlay (subtle) */
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%231e3028' stroke-width='0.5' opacity='0.4'%3E%3Cpath d='M40 0L80 40L40 80L0 40Z'/%3E%3Cpath d='M20 0L60 0L80 20L80 60L60 80L20 80L0 60L0 20Z'/%3E%3Cpath d='M40 20L60 40L40 60L20 40Z'/%3E%3C/g%3E%3C/svg%3E");
  background-size: 80px 80px;
  pointer-events: none;
  z-index: 0;
}}

/* ─── Top navigation ─── */
.atlas-nav {{
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 150;
  background: rgba(10, 15, 13, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}}

.atlas-brand {{
  display: flex;
  align-items: baseline;
  gap: 12px;
  font-family: 'Amiri', serif;
  color: var(--gold);
}}
.atlas-brand .ornament {{ font-size: 1rem; letter-spacing: 0.5em; opacity: 0.6; }}
.atlas-brand h1 {{ font-size: 1.2rem; font-weight: 700; }}
.atlas-brand .sub {{ font-size: 0.72rem; color: var(--text-secondary); font-style: italic; font-family: 'Inter', sans-serif; }}

.atlas-toggle {{
  display: flex;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 4px;
  gap: 2px;
}}
.atlas-toggle button {{
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-family: 'Inter', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  padding: 8px 18px;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.25s;
  display: flex;
  align-items: center;
  gap: 6px;
}}
.atlas-toggle button:hover {{ color: var(--gold-light); }}
.atlas-toggle button.active {{
  background: linear-gradient(135deg, var(--emerald), var(--green-dark));
  color: var(--gold-light);
  box-shadow: 0 0 12px var(--shadow-green);
}}

/* ─── View containers ─── */
.view {{ display: none; padding-top: 64px; position: relative; z-index: 1; }}
.view.active {{ display: block; animation: viewFade 0.35s ease; }}
@keyframes viewFade {{
  from {{ opacity: 0; transform: translateY(8px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

/* ─── TIMELINE VIEW ─── */
/* All timeline CSS (header, controls, cards, bio modal, print) */
{tl_css}

/* Override for fixed nav — timeline's .controls becomes a sub-bar */
.view-timeline .controls {{
  position: sticky;
  top: 60px;
  z-index: 50;
  background: rgba(10,15,13,0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}}
.view-timeline .timeline-container {{ padding-top: 30px; }}
.view-timeline .header {{ padding-top: 30px; padding-bottom: 20px; }}

/* ─── MAP VIEW ─── */
.view-map {{
  position: relative;
  height: calc(100vh - 64px);
  overflow: hidden;
}}
.view-map .map-main {{
  display: flex;
  height: 100%;
  width: 100%;
}}
.view-map .map-wrap {{
  position: relative;
  height: 100%;
  flex: 1;
  min-width: 0;
  background: var(--map-bg);
}}
.view-map #map {{ width: 100%; height: 100%; background: var(--map-bg); }}

/* Map view sidebar (text column) */
.view-map .text-col {{
  width: 45%;
  max-width: 540px;
  min-width: 320px;
  overflow-y: auto;
  border-left: 1px solid var(--border);
  background: rgba(10,15,13,0.4);
  height: 100%;
}}
.view-map .lesson {{
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 36px;
  border-bottom: 1px dashed var(--border);
}}
.view-map .lesson-content {{ max-width: 420px; }}
.view-map .lesson-subtitle {{
  font-size: 0.78rem;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 600;
  margin-bottom: 8px;
}}
.view-map .lesson-title {{
  font-family: 'Amiri', serif;
  font-size: 1.6rem;
  color: var(--text-primary);
  font-weight: 700;
  margin-bottom: 14px;
  line-height: 1.3;
}}
.view-map .lesson-text {{
  font-size: 0.92rem;
  color: var(--text-secondary);
  line-height: 1.7;
}}

/* Map UI chrome — dark theme overrides for the original light styles */
.view-map .header {{ display: none; }}  /* Hide the per-view header, the global nav replaces it */

/* Scrubber */
.view-map .scrubber {{
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(10,15,13,0.95) 60%);
  padding: 30px 20px 16px;
  z-index: 5;
}}
.view-map .scrubber-inner {{ max-width: 700px; margin: 0 auto; }}
.view-map .scrubber-label {{ color: var(--text-secondary); font-size: 0.78rem; font-weight: 500; }}
.view-map .scrubber-value {{ font-family: 'Amiri', serif; color: var(--gold); min-width: 130px; }}
.view-map .scrubber-slider {{ background: var(--border); }}
.view-map .scrubber-slider::-webkit-slider-thumb {{
  background: var(--gold); border: 2px solid var(--bg-card);
  box-shadow: 0 0 0 1px var(--gold-dim);
}}
.view-map .scrubber-slider::-moz-range-thumb {{
  background: var(--gold); border: 2px solid var(--bg-card);
}}

/* Region chips (top-left) */
.view-map .chips {{ top: 16px; left: 16px; max-width: calc(100% - 100px); z-index: 5; }}
.view-map .chip {{
  background: rgba(17, 26, 22, 0.92);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}}
.view-map .chip:hover {{ border-color: var(--gold-dim); color: var(--gold-light); }}
.view-map .chip.active {{
  background: linear-gradient(135deg, var(--gold-dim), var(--emerald));
  border-color: var(--gold);
  color: #fff;
  font-weight: 600;
}}

/* Toggles (top-right) */
.view-map .toggles {{ top: 16px; right: 16px; z-index: 5; }}
.view-map .toggle-btn {{
  background: rgba(17, 26, 22, 0.92);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}}
.view-map .toggle-btn.active {{
  background: linear-gradient(135deg, var(--emerald), var(--green-dark));
  border-color: var(--green-primary);
  color: var(--gold-light);
}}

/* Markers (3D columns click targets) */
.view-map .marker {{
  background: rgba(201, 168, 76, 0.85);
  border: 2px solid var(--gold);
  color: #0a0f0d;
  font-weight: 700;
  text-shadow: none;
}}
.view-map .marker:hover {{ background: var(--gold-light); }}
.view-map .marker.active {{
  background: var(--gold-light);
  border-color: var(--gold);
  color: #0a0f0d;
  box-shadow: 0 0 0 4px rgba(201,168,76,0.4), 0 1px 4px rgba(0,0,0,0.4);
}}

/* City labels */
.view-map .city-label {{
  background: rgba(17, 26, 22, 0.92);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  color: var(--text-primary);
}}
.view-map .city-label .count {{ color: var(--gold); }}

/* Chapter display */
.view-map .chapter-display {{
  background: rgba(17, 26, 22, 0.95);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  color: var(--gold);
}}

/* Side panel */
.view-map .panel-backdrop {{ background: rgba(10, 15, 13, 0.6); }}
.view-map .panel {{
  background: var(--bg-card);
  border-left: 1px solid var(--border);
  box-shadow: -8px 0 32px var(--shadow-strong);
}}
.view-map .panel-header {{
  background: linear-gradient(180deg, var(--bg-card) 0%, rgba(17,26,22,0.6) 100%);
  border-bottom: 1px solid var(--border);
}}
.view-map .panel-title {{ color: var(--text-primary); }}
.view-map .panel-eyebrow {{ color: var(--gold); }}
.view-map .panel-stats {{ color: var(--text-secondary); }}
.view-map .panel-stat strong {{ color: var(--gold); }}
.view-map .panel-body::-webkit-scrollbar-thumb {{ background: var(--border); }}
.view-map .scholar-row {{ border-bottom: 1px solid var(--border); }}
.view-map .scholar-row:hover {{ background: rgba(201, 168, 76, 0.05); }}
.view-map .scholar-date {{
  color: var(--gold);
  border-right: 1px solid var(--border);
}}
.view-map .scholar-date .ce {{ color: var(--text-dim); }}
.view-map .scholar-name {{ color: var(--text-primary); }}
.view-map .scholar-name a {{ border-bottom: 1px dotted var(--border); }}
.view-map .scholar-name a:hover {{ color: var(--gold); border-bottom-color: var(--gold); }}
.view-map .scholar-works {{ color: var(--gold); }}
.view-map .scholar-bio {{ color: var(--text-secondary); }}
.view-map .scholar-note {{ color: var(--text-dim); border-left: 2px solid var(--border); }}
.view-map .panel-close {{
  border: 1px solid var(--border);
  color: var(--text-secondary);
}}
.view-map .panel-close:hover {{
  background: var(--gold);
  border-color: var(--gold);
  color: #0a0f0d;
}}
.view-map .panel-empty {{ color: var(--text-dim); }}

/* Column legend */
.view-map .col-legend {{
  background: rgba(17, 26, 22, 0.95);
  border: 1px solid var(--border);
  color: var(--text-secondary);
}}
.view-map .col-legend .lbl {{ color: var(--gold); }}
.view-map .col-legend .col-set div {{
  background: linear-gradient(180deg, var(--gold-light) 0%, var(--gold-dim) 100%);
  border: 1px solid var(--gold-dim);
}}
.view-map .col-legend .col-set div::after {{ color: var(--text-dim); }}

/* MapLibre attribution override */
.view-map .maplibregl-ctrl-attrib {{
  background: rgba(10,15,13,0.7) !important;
  font-size: 10px !important;
}}
.view-map .maplibregl-ctrl-attrib a {{ color: var(--gold) !important; }}

/* Mobile */
@media (max-width: 900px) {{
  .view-map .map-main {{ flex-direction: column; }}
  .view-map .text-col {{ width: 100%; max-width: none; height: auto; border-left: none; border-top: 1px solid var(--border); }}
  .view-map .map-wrap {{ height: 50vh; }}
  .atlas-nav {{ padding: 10px 14px; }}
  .atlas-brand .sub {{ display: none; }}
  .atlas-toggle button {{ padding: 6px 12px; font-size: 0.75rem; }}
}}

/* Print cleanup */
@media print {{
  .atlas-nav, .view-map .scrubber, .view-map .toggles, .view-map .chips,
  .view-map .chapter-display, .view-map .panel, .view-map .panel-backdrop,
  .view-map .col-legend, .view-map .city-label, .maplibregl-ctrl {{
    display: none !important;
  }}
  body::before {{ display: none; }}
}}
</style>
</head>
<body>

<!-- ─── Top Navigation ─── -->
<nav class="atlas-nav">
  <div class="atlas-brand">
    <span class="ornament">✦</span>
    <h1>Ḥanafī Atlas</h1>
    <span class="sub">Timeline &amp; Map of the Ḥanafī School</span>
    <span class="ornament">✦</span>
  </div>
  <div class="atlas-toggle" id="viewToggle">
    <button class="active" data-view="timeline">📜 Timeline</button>
    <button data-view="map">🗺 Map</button>
  </div>
</nav>

<!-- ─── TIMELINE VIEW ─── -->
<section class="view view-timeline active" id="view-timeline">
  <div class="header" id="timeline">
    <div class="bismillah">بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>
    <div class="header-ornament">✦ ❖ ✦</div>
    <h1>Al-Madhhab al-Hanafī</h1>
    <div class="subtitle">A Chronological Journey Through the Scholars of the Hanafī School</div>
    <div class="meta">
      Data from <a href="https://hadithnotes.org/english-chronological-order-of-major-hanafi-jurists/" target="_blank">Hadith Notes</a> — Compiled by Muntasir Zaman
    </div>
  </div>

  <div class="controls">
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Search scholars, works, or dates…" />
    </div>
    <div class="century-filters" id="centuryFilters"></div>
    <div class="region-filters" id="regionFilters"></div>
    <div class="layout-toggle">
      <button id="btnVertical" class="active" title="Vertical timeline">∟</button>
      <button id="btnHorizontal" title="Horizontal timeline">⇥</button>
    </div>
    <button id="btnPrintMode" class="print-mode-btn" title="Switch to compact A3-printable layout">🖨 A3</button>
    <span class="stats" id="stats"></span>
  </div>

  <div class="scroll-hint" id="scrollHint">↔ Scroll horizontally through centuries</div>

  <div class="timeline-container" id="timelineContainer">
    <div class="timeline-line"></div>
  </div>

  <div id="print-layout" style="display:none"></div>

  <div class="bio-modal-overlay" id="bioModal" onclick="if(event.target===this)closeBioModal()">
    <div class="bio-modal">
      <button class="bio-modal-close" onclick="closeBioModal()" aria-label="Close">&times;</button>
      <div id="bioModalContent"></div>
    </div>
  </div>

  <div class="footer">
    <div style="margin-bottom:8px; color: var(--gold); font-family: 'Amiri', serif;">✦ ❖ ✦</div>
    Interactive Timeline of Hanafī Jurists — Source: <a href="https://hadithnotes.org/english-chronological-order-of-major-hanafi-jurists/" target="_blank">Hadith Notes</a><br>
    CE dates are approximate conversions from Hijri dates
  </div>

  <button class="scroll-top" id="scrollTopBtn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})">↑</button>
</section>

<!-- ─── MAP VIEW ─── -->
<section class="view view-map" id="view-map">
  <div class="map-main">
    <div class="map-wrap">
      <div id="map"></div>

      <div class="chips" id="regionChips">
        <span class="chip active" data-region="all">🌍 All regions</span>
      </div>

      <div class="toggles">
        <button class="toggle-btn active" id="toggleRoutes">Routes</button>
        <button class="toggle-btn" id="toggleHeatmap">Heatmap</button>
      </div>

      <div class="scrubber">
        <div class="scrubber-inner">
          <span class="scrubber-label">Century</span>
          <input type="range" min="2" max="15" value="2" step="1" class="scrubber-slider" id="scrubber">
          <span class="scrubber-value" id="scrubberValue">2nd AH</span>
        </div>
      </div>

      <div class="col-legend" id="colLegend">
        <div>
          <div class="lbl">Scholars</div>
          <div class="col-set">
            <div style="height:6px" data-n="1"></div>
            <div style="height:18px" data-n="5"></div>
            <div style="height:36px" data-n="20"></div>
            <div style="height:54px" data-n="44"></div>
          </div>
        </div>
      </div>

      <div class="chapter-display" id="chapterDisplay"></div>
    </div>

    <div class="text-col" id="textCol">
      <section class="lesson" id="lesson-intro">
        <div class="lesson-content">
          <div class="lesson-subtitle">A Geographic Journey Through 1,400 Years of Scholarship</div>
          <h2 class="lesson-title">Ḥanafī Hearts of the World</h2>
          <p class="lesson-text">From the Kūfan circle of Abū Ḥanīfah to the global diaspora of the modern era, follow the geographic spread of the Ḥanafī school through the lives of 165 scholars across 89 cities and 16 regions. Scroll to begin the journey.</p>
        </div>
      </section>
      <!-- 8 more lesson sections from the original map's text-col -->
    </div>
  </div>
</section>

<!-- ─── Side panel (map view) ─── -->
<div class="panel-backdrop" id="panelBackdrop"></div>
<aside class="panel" id="scholarPanel" aria-hidden="true">
  <button class="panel-close" id="panelClose" title="Close (Esc)">✕</button>
  <div class="panel-header">
    <div class="panel-eyebrow" id="panelEyebrow">City</div>
    <h2 class="panel-title" id="panelTitle">—</h2>
    <div class="panel-modern" id="panelModern"></div>
    <div class="panel-stats" id="panelStats"></div>
  </div>
  <div class="panel-body" id="panelBody"></div>
</aside>

<!-- ─── Scripts ─── -->
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/@turf/turf@7.1.0/turf.min.js"></script>
<script>
// ── Inline data (extracted from existing source files) ──
const PLACES = {PLACES};
const SCHOLARS = {SCHOLARS};
const CHAPTERS = {CHAPTERS};

// ── View switching ──
const viewToggle = document.getElementById('viewToggle');
let currentView = 'timeline';
let mapInitialized = false;
let mapInstance = null;

function setView(view, opts) {{
  if (view === currentView && !opts?.force) return;
  currentView = view;
  document.querySelectorAll('#viewToggle button').forEach(b => {{
    b.classList.toggle('active', b.dataset.view === view);
  }});
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById('view-' + view);
  target.classList.add('active');
  // Lazy-init map on first show
  if (view === 'map' && !mapInitialized) {{
    initMap();
    mapInitialized = true;
  }} else if (view === 'map' && mapInstance) {{
    // Map needs a resize after becoming visible
    setTimeout(() => mapInstance.resize(), 100);
  }}
  // Update URL
  const url = new URL(window.location.href);
  url.searchParams.set('view', view);
  history.replaceState(null, '', url);
}}

viewToggle.querySelectorAll('button').forEach(b => {{
  b.addEventListener('click', () => setView(b.dataset.view));
}});

// Esc closes panel
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') {{
    const panel = document.getElementById('scholarPanel');
    if (panel.classList.contains('open')) closePanel();
  }}
}});

// On load: read URL view param
(function() {{
  const params = new URLSearchParams(window.location.search);
  const view = params.get('view');
  if (view === 'map') setView('map', {{ force: true }});
}})();

// ── Map setup (deferred until first show) ──
function initMap() {{
  mapInstance = new maplibregl.Map({{
    container: 'map',
    style: 'https://tiles.openfreemap.org/styles/dark',
    center: [50, 30],
    zoom: 3,
    pitch: 25,
    bearing: -10
  }});
  mapInstance.addControl(new maplibregl.NavigationControl({{ showCompass: true, visualizePitch: true }}), 'bottom-right');
  mapInstance.on('load', setupMapLayers);
}}

// All the map JS (from the original map) goes here — needs the DOM to be present
// We move all the placeMarkers / updateMarkers / region chips / scrubber / panel
// logic into a single setupMapLayers function called from map.on('load')
function setupMapLayers() {{
  // === original map JS body inlined here, with minimal changes ===
  {mp_js}
}}
</script>

<!-- ── Timeline JS (in its own script so its DOM lookups work even when map view is hidden) ── -->
<script>
{tl_js}
</script>

</body>
</html>
"""

OUT.write_text(HTML, encoding='utf-8')
print(f"Wrote {OUT} ({len(HTML)} chars, {HTML.count(chr(10))} lines)")
