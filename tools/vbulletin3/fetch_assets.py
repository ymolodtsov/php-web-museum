#!/usr/bin/env python3
"""Download every image/script the built exhibit references, from the Wayback Machine.

Each file is looked up (raw "id_" mode, nearest capture to 2007-02-12):
  images:  images.vbulletin.com/images_tmp/ (gradients), images.vbulletin.com/images_vb3/,
           www.vbulletin.com/forum/images/, www.vbulletin.org/forum/images/
           -- Jelsoft's own copies of the stock image set.
           The source board's image host is not used: it put its own art (logo,
           phone-shaped forum icons) under the stock file names.
  scripts: www.cdmaforums.com/forums/ (the source board), forum.doom9.org/
Files land in raw/assets/<path> (kept, so rebuilding is offline) and are copied
into the exhibit. raw/assets.tsv records the archived URL of every file.

usage: python3 fetch_assets.py
"""
import glob
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "exhibits", "vbulletin"))
STORE = os.path.join(HERE, "raw", "assets")
LOG = os.path.join(HERE, "raw", "assets.tsv")
UA = "php-museum-research/1.0 (personal archive study)"
WHEN = "20070212000000"


def candidates(path):
    if path.startswith("images/"):
        # Jelsoft's own copy of the stock vBulletin 3 image set (vbulletin.com, 2006-2007).
        # The source board's own image host is NOT used: it replaced stock files
        # (logo, forum icons) with its own art under the stock file names.
        sub = path[len("images/"):]
        if sub.startswith("gradients/"):
            yield "http://images.vbulletin.com/images_tmp/" + sub
        yield "http://images.vbulletin.com/images_vb3/" + sub
        yield "http://www.vbulletin.com/forum/images/" + sub
        # vbulletin.org kept the stock set too (its reputation_pos.gif is byte-identical)
        yield "http://www.vbulletin.org/forum/images/" + sub
    else:
        yield "http://www.cdmaforums.com/forums/" + path + "?v=364"
        yield "http://forum.doom9.org/" + path + "?v=364"


def get(url):
    """Return (bytes, final archived url) or None on 404; retry other errors with backoff."""
    delay = 10
    for _ in range(6):
        try:
            req = urllib.request.Request("https://web.archive.org/web/%sid_/%s" % (WHEN, url), headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
                ctype = r.headers.get("Content-Type", "")
                if "text/html" in ctype and not url.endswith((".js", ".css")):
                    return None  # archive error page / soft 404
                return data, r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return None
            print("  retry", url, e, file=sys.stderr)
        except Exception as e:
            print("  retry", url, e, file=sys.stderr)
        time.sleep(delay)
        delay = min(delay * 2, 120)
    return None


def referenced():
    refs = set()
    for page in glob.glob(os.path.join(OUT, "*.html")):
        html = open(page, encoding="latin-1").read()
        refs.update(re.findall(r'\b(?:src|background)="((?:images|clientscript)/[^"?#]+)', html))
        refs.update(re.findall(r"url\((images/[^)]+)\)", html))
    return sorted(refs)


def main():
    log = {}
    if os.path.exists(LOG):
        for line in open(LOG):
            p, u = line.rstrip("\n").split("\t")
            log[p] = u
    missing = []
    for path in referenced():
        dest = os.path.join(STORE, path)
        if not os.path.exists(dest):
            for url in candidates(path):
                got = get(url)
                time.sleep(1.5)
                if got:
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    with open(dest, "wb") as fh:
                        fh.write(got[0])
                    log[path] = got[1]
                    print("got", path, "<-", got[1])
                    break
            else:
                missing.append(path)
                continue
        out = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(dest, out)
    with open(LOG, "w") as fh:
        for p in sorted(log):
            fh.write("%s\t%s\n" % (p, log[p]))
    if missing:
        print("MISSING:", *missing, sep="\n  ")


if __name__ == "__main__":
    main()
