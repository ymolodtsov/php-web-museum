#!/usr/bin/env python3
"""Run PNphpBB2 1.2g's own installer through PostNuke's Modules admin, as an admin would:
log in, regenerate the module list, Initialise PNphpBB2, then press each installer screen's
default button until the installer hands back to the module list."""
import html, http.cookiejar, re, sys, urllib.parse, urllib.request

base, user, pw = sys.argv[1:4]
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

def get(url, data=None):
    if data is not None:
        data = urllib.parse.urlencode(data).encode()
    with op.open(urllib.parse.urljoin(base + "/", url), data, timeout=120) as r:
        return r.read().decode("latin-1")

def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s)))

get("user.php")
get("user.php", {"module": "NS-User", "op": "login", "uname": user, "pass": pw, "url": "index.php"})
page = get("index.php?module=Modules&type=admin")
authid = re.search(r"func=regenerate&amp;authid=([0-9a-f]+)", page).group(1)
get("index.php?module=Modules&type=admin&func=regenerate&authid=" + authid)
page = get("index.php?module=Modules&type=admin&func=list")
rows = re.split(r"<tr", page)
url = next(html.unescape(re.search(r'href="([^"]*func=initialise[^"]*)"', r).group(1)) for r in rows
           if "PNphpBB2" in r and "func=initialise" in r)
page = get(url)
for step in range(20):
    f = re.search(r'<form action="([^"]*)" name="install" method="post">(.*?)</form>', page, re.S | re.I)
    print("--", step, text(page)[text(page).find("PNphpBB2 Installation"):][:600])
    if not f:
        break
    fields = {}
    for inp in re.findall(r"<input[^>]*>", f.group(2), re.I):
        n = re.search(r'name="([^"]*)"', inp)
        v = re.search(r'value="([^"]*)"', inp)
        t = re.search(r'type="([^"]*)"', inp, re.I)
        if n and (not t or t.group(1).lower() not in ("checkbox", "radio") or "checked" in inp.lower()):
            fields[n.group(1)] = html.unescape(v.group(1)) if v else ""
    page = get(html.unescape(f.group(1)), fields)
