#!/usr/bin/env python3
"""Run tools/capture.py as a single browser session (keeps cookies between requests).

Mambo creates a new guest session row for every cookieless request, so without this the
Who's Online count would climb by one on each captured page.
"""
import http.cookiejar
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
urllib.request.install_opener(urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())))

import capture  # noqa: E402

capture.main()
