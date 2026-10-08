#!/usr/bin/env python3
"""Crawl the running Joomla 1.5 site and print capture.py --page/--alias arguments.

Each distinct page (front page, section, category, article, article print view,
contact, poll results) is captured once; other URLs that reach the same page are
passed as aliases so links between captured pages stay live.
usage: pages.py http://127.0.0.1:8906  ->  one argument per line on stdout
"""
import html
import re
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip("/")
HREF = re.compile(r'(?:href="|location\.href=\')([^"\']+)["\'][^>]*>(?:\s*<(?!a\b)[^>]+>)*\s*([^<]*)')


def classify(url):
    p = urllib.parse.urlsplit(url)
    if p.netloc not in ("", urllib.parse.urlsplit(BASE).netloc):
        return None
    if p.path not in ("/", "/index.php"):
        return None
    q = dict(urllib.parse.parse_qsl(p.query, keep_blank_values=True))
    if not q:
        return ("front",), "index.html"
    if q.get("format") or q.get("task") or q.get("limitstart") or q.get("layout") == "form":
        return None
    opt, view = q.get("option", "com_content"), q.get("view")
    num = lambda v: v.split(":")[0]
    slug = lambda v, d: v.split(":", 1)[1] if ":" in v else d
    if opt == "com_content" and view == "frontpage":
        return ("front",), "index.html"
    if opt == "com_content" and view == "article" and "id" in q:
        if q.get("print") == "1":
            return ("print", num(q["id"])), "print-%s.html" % slug(q["id"], "article-" + num(q["id"]))
        return ("article", num(q["id"])), slug(q["id"], "article-" + num(q["id"])) + ".html"
    if opt == "com_content" and view == "section" and "id" in q:
        return ("section", num(q["id"])), None
    if opt == "com_content" and view == "category" and "id" in q:
        return ("category", num(q["id"])), None
    if opt == "com_contact" and view == "contact":
        return ("contact", num(q.get("id", "0"))), "contact-us.html"
    if opt == "com_poll" and "id" in q:
        return ("poll", num(q["id"])), "poll-results.html"
    return None


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def main():
    seen, order, names = {("front",): ["/"]}, [("front",)], {("front",): "index.html"}
    queue = ["/"]
    visited = set()
    while queue:
        rel = queue.pop(0)
        if rel in visited:
            continue
        visited.add(rel)
        body = fetch(BASE + rel)
        for raw, text in HREF.findall(body):
            href = html.unescape(raw)
            absu = urllib.parse.urljoin(BASE + rel, href)
            c = classify(absu)
            if not c:
                continue
            key, fname = c
            p = urllib.parse.urlsplit(absu)
            path = p.path + ("?" + p.query if p.query else "")
            if key not in seen:
                seen[key] = [path]
                order.append(key)
                queue.append(path)
            elif path not in seen[key]:
                seen[key].append(path)
            generic = lambda n: n is None or re.match(r"(print-)?article-\d+\.html$", n)
            if fname and (generic(names.get(key)) or not generic(fname)):
                names[key] = fname
            if (key not in names or (generic(names[key]) and key[0] == "article")) and text.strip():
                names[key] = re.sub(r"[^a-z0-9]+", "-", html.unescape(text).lower()).strip("-") + ".html"
    for key in order:
        if key not in names:
            body = fetch(BASE + seen[key][0])
            m = re.search(r'<title>(.*?)</title>', body, re.S)
            t = re.sub(r"[^a-z0-9]+", "-", html.unescape(m.group(1)).lower()).strip("-") if m else "-".join(key)
            names[key] = t + ".html"
    rank = {"front": 0, "section": 1, "category": 2, "contact": 3, "poll": 4, "article": 5, "print": 6}
    order.sort(key=lambda k: rank[k[0]])
    used = {}
    for key in order:
        n = names[key]
        if n in used.values() and used.get(key) != n:
            n = n[:-5] + "-" + key[-1] + ".html"
        used[key] = n
        urls = seen[key]
        print("--page=%s=%s" % (urls[0], n))
        for u in urls[1:]:
            print("--alias=%s=%s" % (u, n))


if __name__ == "__main__":
    main()
