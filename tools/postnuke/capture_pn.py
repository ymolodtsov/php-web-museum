#!/usr/bin/env python3
"""tools/capture.py with a cookie jar (the shared tool is left untouched).

PostNuke and PNphpBB2 keep a session per visitor; without cookies every request starts a new guest session
(inflating "Who's Online") and PNphpBB2 appends ?sid=<session> to its links, so links between captured
forum pages could not be matched.
"""
import http.cookiejar
import importlib.util
import os
import sys
import urllib.request

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("capture", os.path.join(here, "..", "capture.py"))
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
UA = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with opener.open(req, timeout=60) as r:
        return r.read(), r.headers.get_content_charset()


capture.fetch = fetch
base = sys.argv[sys.argv.index("--base") + 1]
fetch(base + "/index.php")  # obtain the PostNuke session cookie first
fetch(base + "/index.php?name=PNphpBB2&file=index")  # and PNphpBB2's
capture.main()
