#!/usr/bin/env python3
"""Generates PWA icon PNGs for ATIS Board. Run once; outputs land in icons/."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "icons")
os.makedirs(OUT, exist_ok=True)

BG = (10, 13, 18, 255)        # --bg
BOX = (45, 212, 191, 255)     # --accent teal
TEXT = (6, 16, 15, 255)       # dark text on teal

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def draw_icon(size, maskable=False, out_name=None):
    img = Image.new("RGBA", (size, size), BG)
    draw = ImageDraw.Draw(img)

    if maskable:
        # keep content inside the ~80% safe-zone circle for adaptive icon masks
        margin = int(size * 0.22)
    else:
        margin = int(size * 0.12)
        # rounded outer corners for the non-maskable (any-purpose) icon
        radius = int(size * 0.22)
        mask = Image.new("L", (size, size), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
        bg_layer = Image.new("RGBA", (size, size), BG)
        img = Image.composite(bg_layer, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
        draw = ImageDraw.Draw(img)

    box_rect = [margin, margin, size - margin, size - margin]
    box_radius = int((size - 2 * margin) * 0.18)
    draw.rounded_rectangle(box_rect, radius=box_radius, fill=BOX)

    letter = "A"
    font_size = int((size - 2 * margin) * 0.62)
    font = ImageFont.truetype(FONT_PATH, font_size)
    bbox = draw.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx, cy = size / 2, size / 2
    draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), letter, font=font, fill=TEXT)

    name = out_name or f"icon-{size}.png"
    img.save(os.path.join(OUT, name))
    print("wrote", name)


draw_icon(512, maskable=False, out_name="icon-512.png")
draw_icon(192, maskable=False, out_name="icon-192.png")
draw_icon(512, maskable=True, out_name="icon-512-maskable.png")
draw_icon(192, maskable=True, out_name="icon-192-maskable.png")
draw_icon(180, maskable=False, out_name="apple-touch-icon.png")
draw_icon(32, maskable=False, out_name="favicon-32.png")
