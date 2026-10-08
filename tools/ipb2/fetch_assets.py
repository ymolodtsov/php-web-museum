#!/usr/bin/env python3
"""Download every stylesheet, script and image the built pages reference, as
archived from the source boards (raw original bytes, Wayback id_ mode).

Run after a first `build.py`, then run `build.py` again to copy assets in.
Each asset is tried on forum.imgburn.com first (the main source board), then on
forums.invisionpower.com (same IPB 2.1.5 default skin, style_images/1).
"""
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "exhibits", "ipb"))
ASSETS = os.path.join(HERE, "raw", "assets")
LOG = os.path.join(HERE, "raw", "assets.log")
HOSTS = [("http://forum.imgburn.com/", "20060512"), ("http://forums.invisionpower.com/", "20060503")]
UA = "php-museum-research/1.0"
REF = re.compile(r"""(?:src|href)\s*=\s*['"]((?:style_images|jscripts|style_emoticons)/[^'"#?]+)['"]""")
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")
JS_IMG = re.compile(r"""([\w/.-]*?[\w-]+\.(?:gif|png|jpg))\b""")


def get(url):
    delay = 10
    for _ in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None, None
            print("  retry", e, file=sys.stderr)
        except Exception as e:
            print("  retry", e, file=sys.stderr)
        time.sleep(delay)
        delay = min(delay * 2, 120)
    return None, None


def fetch(path, log):
    dest = os.path.join(ASSETS, path)
    if os.path.exists(dest):
        return dest
    for host, ts in HOSTS:
        data, final = get("https://web.archive.org/web/%sid_/%s%s" % (ts, host, path))
        time.sleep(1)
        if data and not data.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(data)
            log.write("%s\t%s\n" % (path, final))
            print("ok  ", path, final)
            return dest
    print("MISS", path)
    log.write("%s\tMISSING\n" % path)
    return None


def main():
    todo = set()
    for f in os.listdir(OUT):
        if f.endswith(".html"):
            todo |= set(REF.findall(open(os.path.join(OUT, f), encoding="latin-1").read()))
    todo.add("style_images/css_3.css")
    done = set()
    with open(LOG, "a") as log:
        while todo:
            path = todo.pop()
            if path in done:
                continue
            done.add(path)
            dest = fetch(path, log)
            if not dest:
                continue
            if path.endswith(".css"):
                css = open(dest, encoding="latin-1").read()
                for u in CSS_URL.findall(css):
                    todo.add(os.path.normpath(os.path.join(os.path.dirname(path), u)))
            elif path.endswith(".js"):
                js = open(dest, encoding="latin-1").read()
                for u in JS_IMG.findall(js):
                    u = u.lstrip("/")
                    if "/" not in u:   # bare names are relative to style_images/1
                        u = "style_images/1/" + u
                    if u.startswith("style_images/"):
                        todo.add(u)


if __name__ == "__main__":
    main()
