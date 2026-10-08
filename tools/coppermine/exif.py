#!/usr/bin/env python3
"""Write 2004-2005 camera EXIF into the prepared photos (lossless APP1 splice).

usage: exif.py photos.json SRC_DIR OUT_DIR
photos.json: list of {folder, file, camera, taken, edited?, exposure, fnumber, focal, iso?, flash?}
"""
import json, os, struct, sys
from fractions import Fraction
from PIL import Image, TiffImagePlugin

CAMERAS = {
    "a75":  ("Canon", "Canon PowerShot A75", None),
    "300d": ("Canon", "Canon EOS 300D DIGITAL", None),
    "d70":  ("NIKON CORPORATION", "NIKON D70", "Ver.2.00 "),
}

def R(v):
    f = Fraction(v).limit_denominator(1000)
    return TiffImagePlugin.IFDRational(f.numerator, f.denominator)

def build(p, w, h):
    make, model, fw = CAMERAS[p["camera"]]
    e = Image.Exif()
    e[0x010F] = make
    e[0x0110] = model
    e[0x0112] = 1
    e[0x011A] = R(180 if make == "Canon" else 300)
    e[0x011B] = R(180 if make == "Canon" else 300)
    e[0x0128] = 2
    if p.get("edited"):
        e[0x0131] = p.get("software") or "Adobe Photoshop Elements 3.0"
        e[0x0132] = p["edited"]
    else:
        if fw:
            e[0x0131] = fw
        e[0x0132] = p["taken"]
    e[0x0213] = 1 if make == "Canon" else 2
    x = e.get_ifd(0x8769)
    num, den = p["exposure"].split("/") if "/" in p["exposure"] else (p["exposure"], "1")
    x[0x829A] = TiffImagePlugin.IFDRational(int(num), int(den))
    x[0x829D] = R(p["fnumber"])
    if p.get("iso"):
        x[0x8827] = int(p["iso"])
    x[0x9000] = b"0220" if make != "NIKON CORPORATION" else b"0221"
    x[0x9003] = p["taken"]
    x[0x9004] = p["taken"]
    x[0x9101] = b"\x01\x02\x03\x00"
    x[0x9204] = R(0)
    x[0x9207] = 5
    x[0x9209] = int(p.get("flash", 16))
    x[0x920A] = R(p["focal"])
    x[0xA000] = b"0100"
    x[0xA001] = 1 if not p.get("edited") else 0xFFFF
    x[0xA002] = w
    x[0xA003] = h
    return e.tobytes()

def splice(jpeg, exif):
    assert jpeg[:2] == b"\xff\xd8"
    i = 2
    # drop any existing APP0..APP15 / COM segments
    while jpeg[i] == 0xFF and (0xE0 <= jpeg[i + 1] <= 0xEF or jpeg[i + 1] == 0xFE):
        i += 2 + struct.unpack(">H", jpeg[i + 2:i + 4])[0]
    if not exif.startswith(b"Exif\x00\x00"):
        exif = b"Exif\x00\x00" + exif
    return b"\xff\xd8" + b"\xff\xe1" + struct.pack(">H", len(exif) + 2) + exif + jpeg[i:]

def main():
    plan, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
    for p in plan:
        s = os.path.join(src, p["folder"], p["file"])
        d = os.path.join(out, p["folder"], p["file"])
        os.makedirs(os.path.dirname(d), exist_ok=True)
        w, h = Image.open(s).size
        data = splice(open(s, "rb").read(), build(p, w, h))
        open(d, "wb").write(data)
        Image.open(d).load()
        # file mtime = time taken (cameras/cards preserved it through FTP)
        import time, calendar
        t = calendar.timegm(time.strptime(p["taken"], "%Y:%m:%d %H:%M:%S"))
        os.utime(d, (t, t))
        print(d, w, h, p["camera"], p["taken"])

if __name__ == "__main__":
    main()
