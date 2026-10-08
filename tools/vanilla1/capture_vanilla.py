#!/usr/bin/env python3
"""tools/capture.py with two Vanilla 1 specific link mappings (the shared tool is left untouched):

- every page's "Sign In" link is people.php?ReturnUrl=<that page's URL>; map them all to the one
  captured sign-in page;
- discussion links carry &page=1 (and the last page of a one-page discussion is page 1); map
  comments.php?DiscussionID=N&page=1 to the captured comments.php?DiscussionID=N.
"""
import importlib.util
import os
import urllib.parse

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("capture", os.path.join(here, "..", "capture.py"))
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)

_norm = capture.Capture.norm


def norm(self, url):
    p = urllib.parse.urlsplit(url)
    q = urllib.parse.parse_qsl(p.query, keep_blank_values=True)
    if p.path.endswith("/people.php"):
        q = [(k, v) for k, v in q if k != "ReturnUrl"]
    elif p.path.endswith("/comments.php"):
        q = [(k, v) for k, v in q if not (k == "page" and v == "1")]
    return _norm(self, urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, urllib.parse.urlencode(q), p.fragment)))


capture.Capture.norm = norm
capture.main()
