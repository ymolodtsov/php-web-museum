#!/usr/bin/env python3
"""Post-capture fixes for the Coppermine exhibit.

The intermediate photo opens the full-size view through a JavaScript popup
(MM_openBrWindow('displayimage.php?pid=N&fullsize=1', ...)). capture.py only
rewrites HTML attributes, so point that popup at the captured full-N.html page.
"""
import os
import re
import sys

out = sys.argv[1]
for name in sorted(os.listdir(out)):
    if not name.endswith(".html"):
        continue
    path = os.path.join(out, name)
    html = open(path, encoding="latin-1").read()
    orig = html

    def popup(m):
        target = "full-%s.html" % m.group(1)
        return "MM_openBrWindow('%s'" % (target if os.path.exists(os.path.join(out, target)) else "#")

    html = re.sub(r"MM_openBrWindow\('displayimage\.php\?pid=(\d+)&(?:amp;)?fullsize=1'", popup, html)
    if html != orig:
        open(path, "w", encoding="latin-1").write(html)
