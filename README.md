# Ḥanafī Atlas

**Timeline · Map · Network of the Ḥanafī School**

A triple-view web app tracing 1,400 years of Ḥanafī scholarship across 184 scholars, 100 cities, and 15 regions — from the Kūfan circle of Abū Ḥanīfah to the modern global diaspora.

## Views

### 📜 Timeline (`index.html`)
Dark-themed chronological scrollytelling. Browse scholars by century, filter by region, search by name/works. Each scholar card shows dates, key works, biography, and notable highlights.

<img width="1898" height="908" alt="image" src="https://github.com/user-attachments/assets/49641b10-ed53-4751-966d-25fc06e33d95" />

### 🗺 Map (`map.html`)
Light parchment-themed interactive map (MapLibre GL). Click city markers to fly between chapters, filter by region and century, and open the side panel to read scholar bios for each city.

<img width="1899" height="909" alt="image" src="https://github.com/user-attachments/assets/87ecc099-79c7-48e5-b556-eb208cfefd96" />

### 🔗 Network (`network.html`)
Interactive force-directed graph showing teacher↔student chains and peer connections across all 184 scholars. Colour-coded by century, with hover tooltips showing scholarly relationships. Filter by century, search by name (Unicode-aware), and toggle teacher/peer/external edge types.
<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/d157b3ec-def5-409e-84fa-781a48c87491" />


- **181 teacher→student links** (gold arrows) tracing isnād chains
- **28 peer connections** (dashed green lines) showing contemporary colleagues
- **131 external links** (dotted gold) connecting to scholars outside the 184-scholar dataset
- Drag nodes, zoom/pan, and click century buttons to isolate eras

## Data

| File | Contents |
|---|---|
| `data-scholars.json` | 184 scholars with name, dates (AH), century, region, place, bio, works, note |
| `data-places.json` | 100 cities with coordinates (lng/lat), modern name, region |
| `data-chapters.json` | 10 map chapter definitions (center, zoom, pitch, bearing, text) |
| `data-graph.json` | 184 nodes + 340 edges for the network graph (century, place, region, relations) |

All pages have data embedded inline (works offline, no server needed). The JSON files are the source of truth — run the embed script to update HTML after edits.

## Tech Stack

- **MapLibre GL JS v4** — interactive map with flyTo animations
- **D3.js v7** — force-directed network graph with zoom/pan/drag
- **Vanilla JS** — no frameworks, no build step
- **Amiri + Inter** — Arabic + Latin typography
- **OpenFreeMap (Positron tiles)** — no API key needed

## Local Development

Just open the HTML files in a browser. No server required — all data is embedded inline.

```bash
# Clone
git clone https://github.com/ziyadasghar-GIT/hanafi-atlas.git
cd hanafi-atlas

# Open
open index.html    # Timeline
open map.html      # Map
open network.html  # Network
```

## Editing Data

1. Edit the JSON files (`data-scholars.json`, `data-places.json`, `data-chapters.json`, `data-graph.json`)
2. Re-embed into HTML:
   ```bash
   python3 embed_data.py
   ```
   This updates the `<script id="inlineData">` tags in `index.html`, `map.html`, and `network.html`.
3. For the network graph, also edit `fill_relations.py` if adding new teacher/student/peer data, then:
   ```bash
   python3 fill_relations.py   # regenerates scholars-teachers-peers.md AND data-graph.json
   python3 embed_data.py        # re-embeds into HTML
   ```

## Credits

- Scholar data compiled by **Muntasir Zaman** via [Hadith Notes](https://hadithnotes.org/english-chronological-order-of-major-hanafi-jurists/)
- Cross-referenced with [attahawi.com](https://attahawi.com)
- Map reference: [Bukhari Project](https://bukhariproject.netlify.app)

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to share and remix with attribution. Scholar data credited to Muntasir Zaman / Hadith Notes.
