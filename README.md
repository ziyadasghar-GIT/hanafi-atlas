# Ḥanafī Atlas

**Timeline & Interactive Map of the Ḥanafī School**

A dual-view web app tracing 1,400 years of Ḥanafī scholarship across 165 scholars, 89 cities, and 16 regions — from the Kūfan circle of Abū Ḥanīfah to the modern global diaspora.

## Views

### 📜 Timeline (`index.html`)
Dark-themed chronological scrollytelling. Browse scholars by century, filter by region, search by name/works. Each scholar card shows dates, key works, biography, and notable highlights.

### 🗺 Map (`map.html`)
Light parchment-themed interactive map (MapLibre GL). Click city markers to fly between chapters, filter by region and century, and open the side panel to read scholar bios for each city.

## Data

| File | Contents |
|---|---|
| `data-scholars.json` | 165 scholars with name, dates (AH), century, place, bio, works, note |
| `data-places.json` | 89 cities with coordinates (lng/lat), modern name, region |
| `data-chapters.json` | 10 map chapter definitions (center, zoom, pitch, bearing, text) |

Both pages load data from these JSON files at runtime.

## Tech Stack

- **MapLibre GL JS v4** — interactive map with flyTo animations
- **Vanilla JS** — no frameworks, no build step
- **Amiri + Inter** — Arabic + Latin typography
- **OpenFreeMap (Positron tiles)** — no API key needed

## Local Development

Just open the HTML files in a browser. No server required — all data is loaded from local JSON via `fetch()`.

```bash
# Clone
git clone https://github.com/ziyadasghar-GIT/hanafi-atlas.git
cd hanafi-atlas

# Open
open index.html    # Timeline
open map.html      # Map
```

> **Note:** `fetch()` requires a local server for some browsers. If data doesn't load, run:
> ```bash
> python3 -m http.server 8000
> # Then visit http://localhost:8000
> ```

## Credits

- Scholar data compiled by **Muntasir Zaman** via [Hadith Notes](https://hadithnotes.org/english-chronological-order-of-major-hanafi-jurists/)
- Map reference: [Bukhari Project](https://bukhariproject.netlify.app)

## License

MIT