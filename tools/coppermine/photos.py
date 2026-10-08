#!/usr/bin/env python3
"""Fetch the public-domain / CC0 source photos and turn them into camera-sized JPEGs.

usage: photos.py photos.json OUT_DIR [CACHE_DIR]
Each source is downloaded from Wikimedia Commons (original_url), centre-cropped
to exactly 4:3 or 3:2 and downscaled with Lanczos:
  4:3 -> 1600x1200 (Canon PowerShot A75 "M1" size setting)
  3:2 -> 1536x1024 (EOS 300D / D70 frame resized to half size before upload)
Output has no metadata; exif.py adds the camera EXIF afterwards.
"""
import io
import json
import os
import sys
import time
import urllib.request

from PIL import Image, ImageOps

UA = "PHPWebMuseum/1.0 (local museum reconstruction)"
SIZES = {"4:3": (1600, 1200), "3:2": (1536, 1024)}


def fetch(url, dest):
    if os.path.exists(dest):
        return
    for i in range(10):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            open(dest, "wb").write(data)
            time.sleep(5)
            return
        except Exception as e:  # rate limits: back off and retry
            print("  retry", url, e, file=sys.stderr)
            time.sleep(30 * (i + 1))
    raise SystemExit("could not fetch " + url)


def source_url(p):
    """Large sources come from Commons' standard 1920 (or 3840) px rendition
    (upload.wikimedia.org rate-limits bulk downloads of originals)."""
    url = p["original_url"]
    w, h = p["source_size"]
    if w <= 1920:
        return url
    need = (p.get("size") or SIZES[p["aspect"]])[1]
    step = 1920 if h * 1920 / w >= need else 3840
    if w <= step:
        return url
    head, name = url.rsplit("/", 1)
    head = head.replace("upload.wikimedia.org/wikipedia/commons/", "thumb.wikimedia.org/wikipedia/commons/thumb/", 1)
    return head + "/" + name + "/%dpx-" % step + name


def main():
    plan = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    cache = sys.argv[3] if len(sys.argv) > 3 else os.path.join(out, ".orig")
    os.makedirs(cache, exist_ok=True)
    for p in plan:
        src = os.path.join(cache, p["file"].lower())
        fetch(source_url(p), src)
        im = Image.open(src)
        im = ImageOps.exif_transpose(im).convert("RGB")
        W, H = p.get("size") or SIZES[p["aspect"]]
        im = ImageOps.fit(im, (W, H), Image.LANCZOS, centering=tuple(p.get("centering", (0.5, 0.5))))
        im.info = {}
        dest = os.path.join(out, p["folder"], p["file"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        im.save(dest, "JPEG", quality=88, optimize=False)
        print(dest, W, H)


if __name__ == "__main__":
    main()
