#!/usr/bin/env python3
"""Run tools/capture.py for MyBB 1.2 with two adjustments.

1. Every request carries the cookies of a guest who last visited the night before
   (mybb[lastvisit] / mybb[lastactive]), as a returning browser would. MyBB then marks
   forums and threads with posts since that visit as new, the same on every page.
   Usage: capture_session.py <lastvisit-unix-time> <capture.py args...>
2. MyBB 1.2 serves its theme stylesheet from css.php?theme=N. A static server can't serve
   CSS from a .php path, so that one asset is saved as css/theme_N.css (its url()s are
   rewritten relative to that location as usual).
"""
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import capture  # noqa: E402

lastvisit = int(sys.argv.pop(1))
opener = urllib.request.build_opener()
opener.addheaders = [("Cookie", f"mybb[lastvisit]={lastvisit}; mybb[lastactive]={lastvisit}")]
urllib.request.install_opener(opener)

_orig_asset_path = capture.Capture.asset_path
_orig_attr_html = capture.Capture.rewrite_html


def asset_path(self, absurl):
    p = urllib.parse.urlsplit(absurl)
    if p.path.endswith("/css.php"):
        theme = urllib.parse.parse_qs(p.query).get("theme", ["1"])[0]
        return f"css/theme_{int(theme)}.css"
    return _orig_asset_path(self, absurl)


def rewrite_html(self, html, page_url):
    # treat the stylesheet link like any other asset
    def css(m):
        absurl = urllib.parse.urljoin(page_url, m.group(2).replace("&amp;", "&"))
        return m.group(1) + self.save_asset(absurl) + m.group(3)
    html = re.sub(r'(<link\b[^>]*\bhref=")([^"]*css\.php\?[^"]*)(")', css, html, flags=re.I)
    return _orig_attr_html(self, html, page_url)


_orig_fetch = capture.fetch


def fetch(url):
    """Follow MyBB's own "you will now be taken to..." redirect pages (search.php?action=finduser)."""
    data, charset = _orig_fetch(url)
    m = re.search(rb'<meta http-equiv="refresh" content="\d+;\s*URL=([^"]+)"', data, re.I)
    if m and b"search.php?action=results" in m.group(1):
        return _orig_fetch(urllib.parse.urljoin(url, m.group(1).decode().replace("&amp;", "&")))
    return data, charset


capture.fetch = fetch
capture.Capture.asset_path = asset_path
capture.Capture.rewrite_html = rewrite_html
capture.main()
