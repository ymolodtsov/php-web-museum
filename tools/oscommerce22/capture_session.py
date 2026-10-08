#!/usr/bin/env python3
"""Run tools/capture.py as one osCommerce visitor with items in the shopping cart.

- A cookie jar keeps the osCsid session between requests (so the Shopping Cart box and
  shopping_cart.php show the same cart on every captured page, and no osCsid leaks into links).
- Before capturing, the visitor puts products in the cart through the store's own
  "Add to Cart" form (product_info.php?action=add_product), like a shopper would.
- osCommerce links one product with different extra parameters depending on where the link
  appears (cPath=..., manufacturers_id=..., sort=...). Product pages are matched on
  products_id/reviews_id only, so every variant points to the one captured file.

usage: capture_session.py --cart 28 --cart 42 <capture.py arguments>
"""
import http.cookiejar
import os
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
urllib.request.install_opener(urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())))

import capture  # noqa: E402

PRODUCT_PAGES = ("/product_info.php", "/product_reviews.php", "/product_reviews_info.php")
_norm = capture.Capture.norm


def norm(self, url):
    p = urllib.parse.urlsplit(url)
    pairs = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if k != "osCsid"]
    if p.path in PRODUCT_PAGES and not any(k == "action" for k, _ in pairs):
        pairs = [(k, v) for k, v in pairs if k in ("products_id", "reviews_id")]
    return _norm(self, urllib.parse.urlunsplit(("", "", p.path, urllib.parse.urlencode(pairs), "")))


capture.Capture.norm = norm

args = sys.argv[1:]
cart = []
while "--cart" in args:
    i = args.index("--cart")
    cart.append(args[i + 1])
    del args[i:i + 2]
base = args[args.index("--base") + 1].rstrip("/")

capture.fetch(base + "/")
for pid in cart:
    data = urllib.parse.urlencode({"products_id": pid}).encode()
    req = urllib.request.Request(base + "/product_info.php?products_id=%s&action=add_product" % pid, data=data,
                                 headers={"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.3) Gecko/20040910"})
    urllib.request.urlopen(req, timeout=60).read()

sys.argv = [sys.argv[0]] + args
capture.main()
