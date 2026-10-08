#!/usr/bin/env python3
"""Apply the shared museum navigation, footer and exhibit breadcrumbs to every museum page.

Exhibit reconstructions under exhibits/<name>/ keep their own software's markup;
only exhibits/index.html (the Exhibits listing) is a museum page.
"""
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKIP = {"tools", ".git", ".claude", "node_modules", "api"}

NAV = [
    ("Home", "index.html"),
    ("Exhibits", "exhibits/index.html"),
    ("Timeline", "timeline/index.html"),
    ("About", "about/index.html"),
    ("Links", "links/index.html"),
    ("Guestbook", "guestbook/index.html"),
]

FOOTER = """<div id="footer">
<p>PHP Web Museum &copy; 2026</p>
<p>Best viewed at 1024&times;768</p>
<p class="debug">[ Page generated in 0.0003 seconds ] [ 0 Queries ] [ GZIP : On ]</p>
<p><span class="badge80 xhtml"><span class="l">W3C</span><span class="r">XHTML 1.0</span></span><span class="badge80 css"><span class="l">W3C</span><span class="r">CSS</span></span></p>
</div>"""

SECTIONS = {"cms": ("CMS", "cms"), "forums": ("Forums", "forums"), "other": ("Other", "other")}

SITE = "https://museum.molodtsov.me/"
DESCRIPTION = ("The web of the 2000s, rebuilt from the original software: phpBB, vBulletin, "
               "PHP-Nuke, Joomla, WordPress and more.")
HEAD_START, HEAD_END = "<!-- museum:head -->", "<!-- /museum:head -->"


def head_block(rel, html, depth):
    up = "../" * depth
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    title = m.group(1).strip() if m else "PHP Web Museum"
    path = rel.replace(os.sep, "/")
    path = "" if path == "index.html" else path[: -len("index.html")] if path.endswith("index.html") else path
    return "\n".join([
        HEAD_START,
        f'<meta name="description" content="{DESCRIPTION}">',
        f'<link rel="icon" href="{up}favicon.ico" sizes="any">',
        f'<link rel="icon" href="{up}icon.svg" type="image/svg+xml">',
        f'<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="PHP Web Museum">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{DESCRIPTION}">',
        f'<meta property="og:url" content="{SITE}{path}">',
        f'<meta property="og:image" content="{SITE}og.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        HEAD_END,
    ])


def set_head(rel, html, depth):
    html = re.sub(re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END) + r"\n?", "", html, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*">\n?', "", html)
    return html.replace("</head>", head_block(rel, html, depth) + "\n</head>", 1)


def museum_pages():
    for dirpath, dirs, files in os.walk(ROOT):
        rel_dir = os.path.relpath(dirpath, ROOT)
        top = rel_dir.split(os.sep)[0]
        dirs[:] = [d for d in dirs if d not in SKIP and not (rel_dir == "exhibits")]
        for name in files:
            if not name.endswith(".html"):
                continue
            rel = os.path.normpath(os.path.join(rel_dir, name))
            if top == "exhibits" and rel != os.path.join("exhibits", "index.html"):
                continue
            yield rel


def nav_html(depth):
    up = "../" * depth
    items = "\n".join(f'<li><a href="{up}{href}">{label}</a></li>' for label, href in NAV)
    return f'<div id="navbar">\n<ul>\n{items}\n</ul>\n</div>'


def breadcrumb(rel, html):
    parts = rel.split(os.sep)
    if len(parts) != 3 or parts[0] not in SECTIONS:
        return html
    m = re.search(r'<div id="breadcrumb">(.*?)</div>', html, re.S)
    if not m:
        return html
    name = m.group(1).split("&gt;")[-1].strip()
    label, anchor = SECTIONS[parts[0]]
    crumb = (f'<div id="breadcrumb">\n<a href="../../index.html">PHP Web Museum</a> &gt; '
             f'<a href="../../exhibits/index.html">Exhibits</a> &gt; '
             f'<a href="../../exhibits/index.html#{anchor}">{label}</a> &gt; {name}\n</div>')
    return html[: m.start()] + crumb + html[m.end():]


def main():
    changed = 0
    for rel in museum_pages():
        path = os.path.join(ROOT, rel)
        html = open(path, encoding="utf-8").read()
        depth = rel.count(os.sep)
        new = re.sub(r'<div id="navbar">.*?</div>', nav_html(depth), html, count=1, flags=re.S)
        new = re.sub(r'<div id="footer">.*?</div>', FOOTER, new, count=1, flags=re.S)
        new = breadcrumb(rel, new)
        new = set_head(rel, new, depth)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print(changed, "pages updated")


if __name__ == "__main__":
    main()
