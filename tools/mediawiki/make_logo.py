#!/usr/bin/env python3
"""Draw the 135x135 Retrocomputing Wiki logo (a beige 8-bit micro and monitor).

The result is kept as tools/mediawiki/logo.png; this script only documents how
it was made (it needs Pillow and the macOS Helvetica font).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

S = 4  # draw at 4x, then downsample for smooth edges
W = H = 135
img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def box(x0, y0, x1, y1, fill, outline=None, r=0, w=1):
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill,
                        outline=outline, width=w * S)


BEIGE, BEIGE_DK, EDGE = (222, 211, 182), (196, 182, 148), (120, 108, 84)
# monitor
box(30, 6, 105, 66, BEIGE, EDGE, r=6)
box(37, 12, 98, 56, (34, 40, 34), (90, 90, 80), r=4)
box(57, 66, 78, 72, BEIGE_DK, EDGE)
box(45, 71, 90, 75, BEIGE, EDGE, r=1)
# text on the screen, pixel style
GREEN = (120, 230, 120)
font_px = [
    "#### #### #### ###  #   #  ",
    "#  # #    #  # #  #  # #   ",
    "#### ###  #### #  #   #    ",
    "# #  #    #  # #  #   #    ",
    "#  # #### #  # ###    #  # ",
]
for row, line in enumerate(font_px):
    for col, ch in enumerate(line):
        if ch == "#":
            box(42 + col * 1.5, 18 + row * 1.5, 42 + col * 1.5 + 1.5, 18 + row * 1.5 + 1.5, GREEN)
box(42, 28, 46, 33, GREEN)  # cursor
# keyboard
d.polygon([(14 * S, 96 * S), (121 * S, 96 * S), (115 * S, 80 * S), (20 * S, 80 * S)],
          fill=BEIGE, outline=EDGE)
d.line([(14 * S, 96 * S), (121 * S, 96 * S)], fill=EDGE, width=S)
for row, (y, x0, x1) in enumerate([(83, 24, 111), (87, 22, 113), (91, 21, 114)]):
    x = x0 + row
    while x + 5 <= x1:
        box(x, y, x + 4.5, y + 2.6, (92, 74, 58))
        x += 6
box(40, 93.2, 95, 95, (92, 74, 58))  # space bar

try:
    f1 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15 * S, index=1)
    f2 = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11 * S)
except OSError:
    sys.exit("needs /System/Library/Fonts/Helvetica.ttc")
for text, font, y, col in [("Retrocomputing", f1, 101, (40, 40, 40)), ("WIKI", f2, 119, (110, 96, 70))]:
    tw = d.textlength(text, font=font)
    d.text(((W * S - tw) / 2, y * S), text, font=font, fill=col)

img.resize((W, H), Image.LANCZOS).save(sys.argv[1] if len(sys.argv) > 1 else "logo.png")
