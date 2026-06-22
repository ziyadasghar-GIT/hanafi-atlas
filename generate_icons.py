#!/usr/bin/env python3
"""Generate PWA icons for Hanafi Atlas — gold geometric star on dark green."""

import math
from PIL import Image, ImageDraw

SIZES = [48, 72, 96, 144, 192, 512]
BG = (10, 15, 13)        # #0a0f0d — dark green-black
GOLD = (201, 168, 76)    # #c9a84c
GOLD_DIM = (138, 114, 51) # #8a7233


def rounded_rectangle_mask(size, radius_frac=0.18):
    """Create a rounded-rectangle mask (squircle-style)."""
    w, h = size, size
    r = int(size * radius_frac)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    # Main body
    draw.rectangle([r, 0, w - r, h], fill=255)
    draw.rectangle([0, r, w, h - r], fill=255)
    # Corner circles
    draw.pieslice([0, 0, r * 2, r * 2], 180, 270, fill=255)
    draw.pieslice([w - r * 2, 0, w, r * 2], 270, 360, fill=255)
    draw.pieslice([0, h - r * 2, r * 2, h], 90, 180, fill=255)
    draw.pieslice([w - r * 2, h - r * 2, w, h], 0, 90, fill=255)
    return mask


def draw_8point_star(draw, cx, cy, outer_r, inner_r, color, width=3):
    """Draw an 8-pointed Islamic geometric star."""
    points = []
    for i in range(16):
        angle = -math.pi / 2 + (i * math.pi / 8)
        r = outer_r if i % 2 == 0 else inner_r
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    for i in range(16):
        j = (i + 1) % 16
        draw.line([points[i], points[j]], fill=color, width=width)

    # Connect opposite outer points through center (geometric lines)
    for i in range(0, 16, 4):
        draw.line([points[i], points[(i + 8) % 16]], fill=color, width=width)


def draw_compass_rose(draw, cx, cy, size, color, width=2):
    """Draw a small compass rose at center."""
    # N-S
    draw.line([(cx, cy - size), (cx, cy + size)], fill=color, width=width)
    # E-W
    draw.line([(cx - size, cy), (cx + size, cy)], fill=color, width=width)
    # NE-SW
    d = size * 0.6
    draw.line([(cx - d, cy - d), (cx + d, cy + d)], fill=GOLD_DIM, width=width)
    # NW-SE
    draw.line([(cx + d, cy - d), (cx - d, cy + d)], fill=GOLD_DIM, width=width)
    # N arrowhead
    draw.polygon([(cx, cy - size - 4), (cx - 4, cy - size + 3), (cx + 4, cy - size + 3)],
                 fill=color)


def draw_outer_ring(draw, cx, cy, r, color, width=2):
    """Draw a thin outer circle border."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)


def draw_geometric_corners(draw, cx, cy, r, color, width=2):
    """Draw small geometric corner ornaments (star-petal tips)."""
    # Small diamonds at 45° intervals
    for i in range(8):
        angle = -math.pi / 2 + (i * math.pi / 4)
        # Skip cardinal/diagonal if they clash with compass
        px = cx + (r + 8) * math.cos(angle)
        py = cy + (r + 8) * math.sin(angle)
        # Tiny diamond
        d_size = 5
        diamond = [
            (px, py - d_size),
            (px + d_size // 2, py),
            (px, py + d_size),
            (px - d_size // 2, py),
        ]
        draw.polygon(diamond, fill=color)


def generate_icon(size):
    """Generate a single icon at given size."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    margin = size * 0.12
    cx = size / 2
    cy = size / 2
    usable = size - 2 * margin
    outer_r = usable / 2
    inner_r = outer_r * 0.45

    # Scale line widths with size
    lw_star = max(1, int(size * 0.008))
    lw_ring = max(1, int(size * 0.005))
    lw_compass = max(1, int(size * 0.004))

    # Outer ring
    draw_outer_ring(draw, cx, cy, outer_r, GOLD, width=lw_ring)

    # 8-pointed star
    draw_8point_star(draw, cx, cy, outer_r * 0.92, inner_r, GOLD, width=lw_star)

    # Second smaller star (offset)
    draw_8point_star(draw, cx, cy, outer_r * 0.62, inner_r * 0.55, GOLD_DIM, width=lw_star)

    # Compass rose at center
    compass_size = outer_r * 0.22
    draw_compass_rose(draw, cx, cy, compass_size, GOLD, width=lw_compass)

    # Apply rounded rectangle mask (Android adaptive icon style)
    mask = rounded_rectangle_mask(size, radius_frac=0.18)
    img.putalpha(mask)

    # Composite onto solid background
    bg = Image.new("RGBA", (size, size), (*BG, 255))
    bg.paste(img, (0, 0), img)

    return bg


# Generate all sizes
for size in SIZES:
    icon = generate_icon(size)
    filename = f"/home/mza/Desktop/hanafi-atlas/icon-{size}x{size}.png"
    icon.save(filename, "PNG")
    print(f"✅ {filename} ({size}×{size})")

# Also save a 512x512 as 'icon.png' for general use
import shutil
shutil.copy(
    f"/home/mza/Desktop/hanafi-atlas/icon-512x512.png",
    f"/home/mza/Desktop/hanafi-atlas/icon.png"
)
print("✅ icon.png (512×512)")

print("\nAll icons generated!")
