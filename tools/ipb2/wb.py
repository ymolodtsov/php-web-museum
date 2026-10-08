#!/usr/bin/env python3
"""Polite Wayback Machine fetcher (serial, retries with backoff).

usage: wb.py cdx '<query string>'            -> prints CDX rows
       wb.py get <timestamp> <url> <outfile>  -> raw original bytes (id_ mode)
"""
import sys
import time
import urllib.parse
import urllib.request

UA = "php-museum-research/1.0 (personal archive study)"


def fetch(url, tries=6):
    delay = 10
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read(), r.geturl()
        except urllib.error.HTTPError as e:
            if e.code in (404, 403):
                raise
            print("  retry", e, file=sys.stderr)
        except Exception as e:  # timeouts, resets
            print("  retry", e, file=sys.stderr)
        time.sleep(delay)
        delay = min(delay * 2, 120)
    raise SystemExit("giving up on " + url)


def main():
    if sys.argv[1] == "cdx":
        data, _ = fetch("https://web.archive.org/cdx/search/cdx?" + sys.argv[2])
        sys.stdout.write(data.decode("utf-8", "replace"))
    elif sys.argv[1] == "get":
        ts, url, out = sys.argv[2:5]
        data, final = fetch("https://web.archive.org/web/%sid_/%s" % (ts, url))
        with open(out, "wb") as fh:
            fh.write(data)
        print(len(data), final)


if __name__ == "__main__":
    main()
