#!/usr/bin/env python3
"""Apply the standard museum footer to every museum page (exhibits keep their own)."""
import os
import re

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKIP = {"exhibits", "tools", ".git", ".claude"}

FOOTER = """<div id="footer">
<p>PHP Web Museum &copy; 2026</p>
<p>Best viewed at 1024&times;768</p>
<p><span class="badge80 xhtml"><span class="l">W3C</span><span class="r">XHTML 1.0</span></span><span class="badge80 css"><span class="l">W3C</span><span class="r">CSS</span></span></p>
</div>"""

changed = 0
for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for name in files:
        if not name.endswith(".html"):
            continue
        path = os.path.join(dirpath, name)
        html = open(path, encoding="utf-8").read()
        new = re.sub(r'<div id="footer">.*?</div>', FOOTER, html, count=1, flags=re.S)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
print(changed, "pages updated")
