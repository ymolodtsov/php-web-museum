#!/usr/bin/env python3
"""Discover the Coppermine pages to capture and print capture.py arguments.

usage: pages.py http://127.0.0.1:8911  > pages.args
Walks the guest view: home, categories, albums, meta albums, and every
displayimage link they contain. Photo pages are named photo-<pid>.html.
"""
import re
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/")


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=60) as r:
        return r.read().decode("latin-1")


def links(html, pat):
    out = []
    for m in re.finditer(r'href="([^"]*)"', html):
        u = m.group(1).replace("&amp;", "&")
        if re.match(pat, u) and u not in out:
            out.append(u)
    return out


def pid_of(html):
    m = re.search(r"displayimage\.php\?pid=(\d+)&(?:amp;)?fullsize=1", html) or re.search(r"addfav\.php\?pid=(\d+)", html)
    return int(m.group(1))


pages, aliases = [], []
seen = set()


def page(url, fname):
    if url not in seen:
        seen.add(url)
        pages.append((url, fname))


page("/", "index.html")
aliases.append(("/index.php?cat=0", "index.html"))
home = get("/")
cats = [int(c) for c in re.findall(r'href="index\.php\?cat=(\d+)"', home)]
for c in sorted(set(cats)):
    if c:
        page("/index.php?cat=%d" % c, "cat-%d.html" % c)

album_ids = sorted({int(a) for a in re.findall(r'thumbnails\.php\?album=(\d+)"', home)})
for a in album_ids:
    page("/thumbnails.php?album=%d" % a, "album-%d.html" % a)
    aliases.append(("/thumbnails.php?album=%d&page=1" % a, "album-%d.html" % a))

META = [("lastup", "lastup"), ("lastcom", "lastcom"), ("topn", "mostviewed"), ("toprated", "toprated")]
for key, name in META:
    page("/thumbnails.php?album=%s&cat=0" % key, name + ".html")
    aliases.append(("/thumbnails.php?album=%s&cat=0&page=1" % key, name + ".html"))
page("/thumbnails.php?album=favpics", "favorites.html")
page("/search.php", "search.html")
page("/login.php?referer=%2Findex.php", "login.html")

# photo pages in album context
pids = {}
for a in album_ids:
    html = get("/thumbnails.php?album=%d" % a)
    for u in links(html, r"displayimage\.php\?album=\d+&pos=\d+$"):
        p = pid_of(get("/" + u))
        pids[p] = True
        page("/" + u, "photo-%d.html" % p)
        page("/displayimage.php?pid=%d&fullsize=1" % p, "full-%d.html" % p)
        aliases.append(("/displayimage.php?pos=-%d" % p, "photo-%d.html" % p))

# photo pages reached from meta albums and the home page rows
for key, name in META:
    html = get("/thumbnails.php?album=%s&cat=0" % key)
    for u in links(html, r"displayimage\.php\?album=%s&cat=0&pos=\d+$" % key):
        pos = re.search(r"pos=(\d+)", u).group(1)
        page("/" + u, "%s-%s.html" % (name, pos))
for u in links(home, r"displayimage\.php\?album=lastup&cat=0&pos=\d+$"):
    pos = re.search(r"pos=(\d+)", u).group(1)
    page("/" + u, "lastup-%s.html" % pos)

args = []
for u, f in pages:
    args += ["--page", "%s=%s" % (u, f)]
for u, f in aliases:
    args += ["--alias", "%s=%s" % (u, f)]
print("\n".join(args))
