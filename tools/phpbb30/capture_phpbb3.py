#!/usr/bin/env python3
"""Capture the Pixel Arena phpBB 3.0.2 board with tools/capture.py, as one guest visitor.

- A cookie jar keeps the guest's phpBB session, so phpBB does not append ?sid= to every link
  (it only does that for visitors whose session cookie it has not seen yet). The cookies'
  2009 expiry dates are dropped, since the capturing machine's clock is years past them.
- Links are matched without the sid and without the forum id on topic links (phpBB 3 links
  one topic as viewtopic.php?f=4&t=1 or ?t=1, and global announcements with any f).
- Uploaded avatars are served by download/file.php?avatar=<name>; each one is saved under
  download/file/<name> so they don't all land on one path.
- prosilver's stylesheet is served by style.php from the database (prosilver's theme.cfg sets
  parse_css_file); it is saved as style.css.
- Right before capturing, online.php (tools/phpbb30) records who is online.

usage: WWW=<board dir> capture_phpbb3.py http://127.0.0.1:8916   (run from the museum root; reads the board's DB)
"""
import http.cookiejar
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))


class SessionCookies(urllib.request.HTTPCookieProcessor):
    """The board's faked clock sets cookies that expire in 2009, which is long past for the
    real clock of the capturing machine; keep them as session cookies instead."""

    def http_response(self, request, response):
        values = response.headers.get_all("Set-Cookie") or []
        del response.headers["Set-Cookie"]
        for v in values:
            response.headers["Set-Cookie"] = re.sub(r";\s*expires=[^;]*", "", v, flags=re.I)
        return super().http_response(request, response)


urllib.request.install_opener(urllib.request.build_opener(SessionCookies(http.cookiejar.CookieJar())))
import capture  # noqa: E402

_norm = capture.Capture.norm
_asset_path = capture.Capture.asset_path


def norm(self, url):
    p = urllib.parse.urlsplit(url)
    pairs = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if k != "sid"]
    if p.path.endswith("/viewtopic.php") and any(k in ("t", "p") for k, _ in pairs):
        pairs = [(k, v) for k, v in pairs if k in ("t", "p", "start") and not (k == "start" and v == "0")]
    return _norm(self, urllib.parse.urlunsplit(("", "", p.path, urllib.parse.urlencode(pairs), "")))


def asset_path(self, absurl):
    p = urllib.parse.urlsplit(absurl)
    if p.path.endswith("/download/file.php"):
        q = dict(urllib.parse.parse_qsl(p.query))
        if "avatar" in q:
            return "download/file/" + os.path.basename(q["avatar"])
    if p.path.endswith("/style.php"):
        return "style.css"
    return _asset_path(self, absurl)


capture.ASSET_EXT = re.compile(capture.ASSET_EXT.pattern.replace(")$", ")$|/style\\.php$"), re.I)
capture.Capture.norm = norm
capture.Capture.asset_path = asset_path


def sql(query):
    out = subprocess.run(["docker", "exec", "museum-db", "mysql", "-N", "-uroot", "-pmuseum", "phpbb3", "-e", query],
                         check=True, capture_output=True, text=True).stdout
    return [line.split("\t") for line in out.splitlines() if line]


base = sys.argv[1].rstrip("/")
pages = [("/", "index.html"), ("/faq.php", "faq.html"), ("/search.php", "search.html"),
         ("/search.php?search_id=active_topics", "search-active.html"),
         ("/memberlist.php", "memberlist.html"), ("/memberlist.php?mode=leaders", "team.html"),
         ("/ucp.php?mode=login", "login.html"), ("/ucp.php?mode=register", "register.html")]
aliases = []
for (fid,) in sql("SELECT forum_id FROM phpbb_forums ORDER BY left_id"):
    pages.append(("/viewforum.php?f=%s" % fid, "forum-%s.html" % fid))
per_page = 10
for tid, replies in sql("SELECT topic_id, topic_replies FROM phpbb_topics WHERE topic_first_post_id IN "
                        "(SELECT post_id FROM phpbb_posts) ORDER BY topic_id"):
    npages = int(replies) // per_page + 1
    for n in range(npages):
        url = "/viewtopic.php?t=%s" % tid + ("&start=%d" % (n * per_page) if n else "")
        pages.append((url, "topic-%s%s.html" % (tid, "-%d" % (n + 1) if n else "")))
    for i, (pid,) in enumerate(sql("SELECT post_id FROM phpbb_posts WHERE topic_id = %s ORDER BY post_time, post_id" % tid)):
        n = i // per_page
        aliases.append(("/viewtopic.php?p=%s" % pid, "topic-%s%s.html" % (tid, "-%d" % (n + 1) if n else "")))
for (uid,) in sql("SELECT DISTINCT poster_id FROM phpbb_posts UNION SELECT user_id FROM phpbb_user_group WHERE group_id IN (4, 5) "
                  "UNION SELECT user_id FROM phpbb_moderator_cache"):
    pages.append(("/memberlist.php?mode=viewprofile&u=%s" % uid, "member-%s.html" % uid))

# who is online, then a first visit so the guest session cookie is set before the capture
for f in ("online.php", "museum_content.php"):
    assert os.path.exists(os.path.join(os.environ["WWW"], f)), f
capture.fetch(base + "/online.php")
capture.fetch(base + "/")

args = ["capture.py", "--base", base, "--out", "exhibits/phpbb3"]
for u, f in pages:
    args += ["--page", "%s=%s" % (u, f)]
for u, f in aliases:
    args += ["--alias", "%s=%s" % (u, f)]
sys.argv = args
capture.main()
