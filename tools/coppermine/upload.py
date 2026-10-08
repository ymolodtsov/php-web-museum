#!/usr/bin/env python3
"""Batch-add the FTP'd photos through Coppermine's own "Batch add files" screens.

usage: upload.py http://127.0.0.1:8911 USER PASS folder=aid [folder=aid ...]
For each folder under albums/: GET searchnew.php?startdir=<folder> (the file list
form), POST it with every file assigned to the album, then request each
addpic.php image the result page embeds, as a browser would. addpic.php runs
Coppermine's add_picture(), which makes the thumb_ and normal_ files with GD.
"""
import base64
import http.cookiejar
import re
import sys
import urllib.parse
import urllib.request

base, user, pw = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def req(path, data=None):
    body = urllib.parse.urlencode(data, doseq=True).encode() if data is not None else None
    with op.open(base + path, body, timeout=300) as r:
        return r.read()


req("/login.php", {"username": user, "password": pw, "submitted": "Login"})
for spec in sys.argv[4:]:
    folder, aid = spec.split("=")
    form = req("/searchnew.php?startdir=" + urllib.parse.quote(folder)).decode("latin-1")
    ids = re.findall(r'name="pics\[\]"[^>]*value="([^"]+)"', form)
    data = {"insert": "1", "pics[]": ids}
    order = []
    for pid in ids:
        lb = re.search(r'name="album_lb_id_%s" type="hidden" value="([^"]+)"' % re.escape(pid), form).group(1)
        pf = re.search(r'name="picfile_%s" type="hidden" value="([^"]+)"' % re.escape(pid), form).group(1)
        data["album_lb_id_" + pid] = lb
        data[lb] = aid
        data["picfile_" + pid] = pf
        order.append(pf)
    result = req("/searchnew.php", data).decode("latin-1")
    srcs = re.findall(r'<img src="(addpic\.php\?[^"]+)"', result)
    # add in file-name order so picture ids follow the album's shooting order
    srcs.sort(key=lambda s: base64.b64decode(urllib.parse.parse_qs(urllib.parse.urlsplit(s.replace("&amp;", "&")).query)["pic_file"][0]))
    for s in srcs:
        r = req("/" + s.replace("&amp;", "&"))
        ok = r[:3] == b"GIF" and len(r) > 0
        print(folder, urllib.parse.unquote(s)[:90], "ok" if ok else r[:200])
