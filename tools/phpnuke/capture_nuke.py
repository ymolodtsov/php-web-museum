#!/usr/bin/env python3
"""tools/capture.py with two PHP-Nuke specific adjustments (the shared tool is left untouched):

- keep cookies between requests, as a browser would; otherwise the bundled phpBB appends a fresh
  ?sid=<session> to every forum link and links between captured forum pages cannot be matched;
- the login block's security-code image is a PHP script (modules.php?...op=gfx); store that one
  response as a .jpg instead of as a file called modules.php.
"""
import http.cookiejar
import importlib.util
import os
import sys
import urllib.parse
import urllib.request

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("capture", os.path.join(here, "..", "capture.py"))
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
UA = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=60) as r:
        return r.read(), r.headers.get_content_charset()


capture.fetch = fetch
_asset_path = capture.Capture.asset_path


def asset_path(self, absurl):
    if "op=gfx" in urllib.parse.urlsplit(absurl).query:
        return "modules/Your_Account/images/security-code.jpg"
    return _asset_path(self, absurl)


capture.Capture.asset_path = asset_path

base = sys.argv[sys.argv.index("--base") + 1]
fetch(base + "/modules.php?name=Forums")  # obtain the phpBB session cookie first
capture.main()
