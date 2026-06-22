#!/usr/bin/env python3
"""Render icon.svg to PNG at all required PWA sizes using cairosvg."""

import cairosvg
from PIL import Image

SIZES = [48, 72, 96, 144, 192, 512]
SVG_PATH = "/home/mza/Desktop/hanafi-atlas/icon.svg"

for size in SIZES:
    out = f"/home/mza/Desktop/hanafi-atlas/icon-{size}x{size}.png"
    cairosvg.svg2png(
        url=SVG_PATH,
        write_to=out,
        output_width=size,
        output_height=size,
    )
    # Verify
    img = Image.open(out)
    w, h = img.size
    assert w == size and h == size, f"Expected {size}x{size}, got {w}x{h}"
    print(f"✅ icon-{size}x{size}.png ({w}×{h}) {img.mode}")

# Also copy 512 as icon.png
import shutil
shutil.copy(
    "/home/mza/Desktop/hanafi-atlas/icon-512x512.png",
    "/home/mza/Desktop/hanafi-atlas/icon.png"
)
print("✅ icon.png (512×512)")
print("\nAll icons rendered from SVG!")
