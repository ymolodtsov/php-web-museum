#!/usr/bin/env python3
"""Run tools/capture.py with an e107 login cookie, so the snapshot shows the site as a
logged-in member sees it (e107 0.617 only shows the member list and profiles to members).

usage: capture_as.py COOKIE_VALUE <capture.py arguments...>
The cookie is e107's own: "<user_id>.<md5(user_password)>" under the name e107cookie.
"""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import capture  # noqa: E402

COOKIE = "e107cookie=" + sys.argv.pop(1)


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0",
        "Cookie": COOKIE})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read(), r.headers.get_content_charset()


capture.fetch = fetch
capture.main()
