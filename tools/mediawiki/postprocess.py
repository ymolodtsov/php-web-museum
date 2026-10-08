#!/usr/bin/env python3
"""Finish the MediaWiki capture: save the wiki's own site JS/CSS.

MonoBook loads four stylesheet/script URLs that all point at index.php with a
query string (action=raw). capture.py keys assets by path, so they collapse
into one file called "index.php". This fetches each of them from the running
wiki, stores them under raw/, and points the pages at those files.

usage: postprocess.py exhibits/mediawiki http://127.0.0.1:8910
"""
import glob
import os
import re
import sys
import urllib.request

out, base = sys.argv[1], sys.argv[2].rstrip("/")
RAW = [
    ("raw/site.js", "/index.php?title=-&action=raw&gen=js"),
    ("raw/MediaWiki-Common.css", "/index.php?title=MediaWiki:Common.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=18000"),
    ("raw/MediaWiki-Monobook.css", "/index.php?title=MediaWiki:Monobook.css&usemsgcache=yes&action=raw&ctype=text/css&smaxage=18000"),
    ("raw/site.css", "/index.php?title=-&action=raw&gen=css&maxage=18000"),
]
os.makedirs(os.path.join(out, "raw"), exist_ok=True)
for name, url in RAW:
    with urllib.request.urlopen(base + url) as r:
        data = r.read()
    with open(os.path.join(out, name), "wb") as fh:
        fh.write(data)

js = '<script type="text/javascript" src="index.php"><!-- site js --></script>'
css = re.compile(r'@import "index\.php";\n@import "index\.php";\n@import "index\.php";')
for page in glob.glob(os.path.join(out, "*.html")):
    html = open(page, encoding="utf-8").read()
    if js not in html or not css.search(html):
        sys.exit("site js/css block not found in " + page)
    html = html.replace(js, js.replace('"index.php"', '"raw/site.js"'))
    html = css.sub('@import "raw/MediaWiki-Common.css";\n@import "raw/MediaWiki-Monobook.css";\n@import "raw/site.css";', html)
    open(page, "w", encoding="utf-8").write(html)

stray = os.path.join(out, "index.php")
if os.path.exists(stray):
    os.remove(stray)
