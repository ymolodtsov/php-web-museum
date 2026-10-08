#!/usr/bin/env python3
"""Snapshot pages from a locally running original app into a static exhibit.

usage: capture.py --base http://127.0.0.1:8901 --out exhibits/wordpress \
                  --page '/=index.html' --page '/?p=5=post.html' [--alias '/?cat=1=index.html']

Pages are saved at the exhibit root. Same-origin assets keep their URL path.
Links to captured pages become relative; other same-origin links become '#'.
Forms submit nowhere (static servers cannot answer POST).
"""
import argparse
import os
import re
import sys
import urllib.parse
import urllib.request

ATTR = re.compile(r'(\b(?:href|src|background|action)\s*=\s*)(["\'])(.*?)\2', re.I | re.S)
CSS_URL = re.compile(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)', re.I)
CSS_IMPORT = re.compile(r'@import\s+(["\'])([^"\']+)\1', re.I)
ASSET_EXT = re.compile(r"\.(css|js|gif|jpe?g|png|ico|bmp|swf|htc|cur|woff2?|ttf|eot|svg)$", re.I)

BAR = ('<div style="background:#23466C;color:#FFFFFF;font:11px Verdana,Arial,sans-serif;'
       'padding:4px 10px;text-align:left;">&larr; <a href="../../index.html" target="_top" '
       'style="color:#FFFFFF;">Return to PHP Web Museum</a></div>')


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get_content_charset()


class Capture:
    def __init__(self, base, out, pages, aliases, bar_bottom=False):
        self.bar_bottom = bar_bottom
        self.base = base.rstrip("/")
        self.host = urllib.parse.urlsplit(self.base).netloc
        self.out = out
        self.pages = pages  # normalized key -> filename
        self.pages.update(aliases)
        self.assets = {}

    def norm(self, url):
        p = urllib.parse.urlsplit(url)
        path = p.path or "/"
        if path.endswith("/index.php"):
            path = path[: -len("index.php")]
        q = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(p.query, keep_blank_values=True)))
        return path + ("?" + q if q else "")

    def local(self, absurl):
        p = urllib.parse.urlsplit(absurl)
        return p.netloc in ("", self.host)

    def asset_path(self, absurl):
        return urllib.parse.unquote(urllib.parse.urlsplit(absurl).path).lstrip("/")

    def save_asset(self, absurl):
        rel = self.asset_path(absurl)
        if not rel or rel in self.assets:
            return rel
        self.assets[rel] = True
        try:
            data, _ = fetch(absurl)
        except Exception as e:  # missing assets are reported, not fatal
            print("  missing asset", absurl, e, file=sys.stderr)
            return rel
        dest = os.path.join(self.out, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if rel.lower().endswith(".css"):
            data = self.rewrite_css(data.decode("latin-1"), absurl).encode("latin-1")
        with open(dest, "wb") as fh:
            fh.write(data)
        return rel

    def rel_from(self, from_rel_dir, target_rel):
        return os.path.relpath(target_rel, from_rel_dir or ".").replace(os.sep, "/")

    def rewrite_css(self, css, css_url):
        css_dir = os.path.dirname(self.asset_path(css_url))

        def fix(m, quote, ref):
            if ref.startswith("data:"):
                return m.group(0)
            absurl = urllib.parse.urljoin(css_url, ref.strip())
            if not self.local(absurl):
                return m.group(0)
            rel = self.save_asset(absurl)
            return self.rel_from(css_dir, rel)

        css = CSS_IMPORT.sub(lambda m: "@import " + m.group(1) + fix(m, m.group(1), m.group(2)) + m.group(1), css)
        return CSS_URL.sub(lambda m: "url(" + m.group(1) + fix(m, m.group(1), m.group(2)) + m.group(1) + ")", css)

    def rewrite_html(self, html, page_url):
        def attr(m):
            prefix, q, val = m.group(1), m.group(2), m.group(3)
            name = prefix.strip().rstrip("=").strip().lower()
            raw = val.replace("&amp;", "&")
            if raw.startswith(("#", "javascript:", "mailto:", "data:")):
                return m.group(0)
            absurl = urllib.parse.urljoin(page_url, raw)
            if not self.local(absurl):
                # outbound links would leave the reconstruction for today's web
                return prefix + q + "#" + q if name in ("href", "action") else m.group(0)
            frag = urllib.parse.urlsplit(absurl).fragment
            if name == "action":
                return prefix + q + "#" + q
            path = urllib.parse.urlsplit(absurl).path
            if name in ("src", "background") or ASSET_EXT.search(path):
                return prefix + q + self.save_asset(absurl) + q
            target = self.pages.get(self.norm(absurl))
            if target:
                return prefix + q + target + ("#" + frag if frag else "") + q
            return prefix + q + "#" + q

        html = ATTR.sub(attr, html)
        html = re.sub(r"(<style[^>]*>)(.*?)(</style>)",
                      lambda m: m.group(1) + self.rewrite_css(m.group(2), page_url) + m.group(3), html, flags=re.S | re.I)
        html = re.sub(r'(style\s*=\s*")([^"]*url\([^"]*)(")',
                      lambda m: m.group(1) + self.rewrite_css(m.group(2), page_url) + m.group(3), html, flags=re.I)
        html = re.sub(r'(<form\b[^>]*?)\bmethod\s*=\s*(["\']?)post\2', r'\1method="get"', html, flags=re.I)
        html = re.sub(r'(<input\b[^>]*type=["\']?password["\']?[^>]*?)\sname=(["\'])[^"\']*\2', r"\1", html, flags=re.I)
        html = html.replace("http://" + self.host + "/", "").replace("http://" + self.host, "")
        if self.bar_bottom:  # for skins that absolutely position elements at the top of the page
            return re.sub(r"(</body>)", lambda m: BAR + "\n" + m.group(1), html, count=1, flags=re.I)
        return re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + "\n" + BAR, html, count=1, flags=re.I)

    def run(self, order):
        os.makedirs(self.out, exist_ok=True)
        for key, fname in order:
            url = self.base + key
            data, charset = fetch(url)
            html = data.decode(charset or "latin-1", errors="replace")
            html = self.rewrite_html(html, url)
            with open(os.path.join(self.out, fname), "w", encoding=charset or "latin-1", errors="xmlcharrefreplace") as fh:
                fh.write(html)
            print("page", key, "->", fname)
        print(len(self.assets), "assets")


def parse_map(items, cap):
    out = []
    for it in items:
        url, fname = it.rsplit("=", 1)
        out.append((url, fname))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--page", action="append", default=[], help="URLPATH=FILENAME to capture")
    ap.add_argument("--alias", action="append", default=[], help="URLPATH=FILENAME to link to without capturing")
    ap.add_argument("--bar-bottom", action="store_true", help="put the museum return bar at the end of the page")
    a = ap.parse_args()
    cap = Capture(a.base, a.out, {}, {}, bar_bottom=a.bar_bottom)
    order = parse_map(a.page, cap)
    cap.pages = {cap.norm(u): f for u, f in order}
    cap.pages.update({cap.norm(u): f for u, f in parse_map(a.alias, cap)})
    cap.run(order)


if __name__ == "__main__":
    main()
