# Ḥanafī Atlas

**Timeline & Interactive Map of the Ḥanafī School**

A dual-view web app tracing 1,400 years of Ḥanafī scholarship across 164 scholars, 89 cities, and 16 regions — from the Kūfan circle of Abū Ḥanīfah to the modern global diaspora.

## Views

### 📜 Timeline (`index.html`)
Dark-themed chronological scrollytelling. Browse scholars by century, filter by region, search by name/works. Each scholar card shows dates, key works, biography, and notable highlights.

### 🗺 Map (`map.html`)
Light parchment-themed interactive map (MapLibre GL). Click city markers to fly between chapters, filter by region and century, and open the side panel to read scholar bios for each city.

## Data

| File | Contents |
|---|---|
| `data-scholars.json` | 164 scholars with name, dates (AH), century, place, bio, works, note |
| `data-places.json` | 89 cities with coordinates (lng/lat), modern name, region |
| `data-chapters.json` | 10 map chapter definitions (center, zoom, pitch, bearing, text) |

Both pages have all data embedded inline (works offline, no server needed). The JSON files in the repo are the source of truth for editing — run the embed script to update the HTML after edits.

## Tech Stack

- **MapLibre GL JS v4** — interactive map with flyTo animations
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
```

## Editing Data

1. Edit the JSON files (`data-scholars.json`, `data-places.json`, `data-chapters.json`)
2. Re-embed into HTML:
   ```bash
   python3 embed_data.py
   ```
   This updates the `<script id="inlineData">` tags in both `index.html` and `map.html`.

## Credits

- Scholar data compiled by **Muntasir Zaman** via [Hadith Notes](https://hadithnotes.org/english-chronological-order-of-major-hanafi-jurists/)
- Cross-referenced with [attahawi.com](https://attahawi.com)
- Map reference: [Bukhari Project](https://bukhariproject.netlify.app)

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to share and remix with attribution. Scholar data credited to Muntasir Zaman / Hadith Notes.