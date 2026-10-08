#!/usr/bin/env python3
"""Generate the museum favicons from one pixel grid: a white lowercase m on black."""
import os

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

M = [
    "##.#.",
    "#.#.#",
    "#.#.#",
    "#.#.#",
    "#.#.#",
]


def raster(size, cell, ox, oy):
    im = Image.new("RGB", (size, size), (0, 0, 0))
    px = im.load()
    for y, row in enumerate(M):
        for x, ch in enumerate(row):
            if ch == "#":
                for dy in range(cell):
                    for dx in range(cell):
                        px[ox + x * cell + dx, oy + y * cell + dy] = (255, 255, 255)
    return im


def centered(size, cell):
    span = 5 * cell
    off = (size - span) // 2
    # sit the glyph a hair low, like a lowercase letter on a baseline
    return raster(size, cell, off, off + (cell // 2 if size >= 32 else 0))


def main():
    sizes = {16: 2, 32: 4, 48: 6}
    icons = [centered(s, c) for s, c in sizes.items()]
    icons[-1].save(os.path.join(ROOT, "favicon.ico"), format="ICO", sizes=[(s, s) for s in sizes], append_images=icons[:-1])
    centered(180, 22).save(os.path.join(ROOT, "apple-touch-icon.png"))
    centered(512, 64).save(os.path.join(ROOT, "icon-512.png"))

    rects = "".join(
        f'<rect x="{x + 1}" y="{y + 1}" width="1" height="1"/>'
        for y, row in enumerate(M) for x, ch in enumerate(row) if ch == "#"
    )
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 7 7" shape-rendering="crispEdges">'
           f'<rect width="7" height="7" fill="#000"/><g fill="#fff">{rects}</g></svg>\n')
    open(os.path.join(ROOT, "icon.svg"), "w").write(svg)
    print("wrote favicon.ico, icon.svg, apple-touch-icon.png, icon-512.png")


if __name__ == "__main__":
    main()
