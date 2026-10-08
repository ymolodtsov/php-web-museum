#!/usr/bin/env python3
"""Print the --page/--alias arguments for capture_session.py, reading ids from the mybb database."""
import shlex
import subprocess


def rows(sql):
    out = subprocess.run(["docker", "exec", "museum-db", "mysql", "-N", "-uroot", "-pmuseum", "mybb", "-e", sql],
                         capture_output=True, text=True, check=True).stdout
    return [line.split("\t") for line in out.splitlines() if line]


PPP = 10  # posts per page (MyBB default)
pages = [("/", "index.html"), ("/memberlist.php", "memberlist.html"), ("/search.php", "search.html"),
         ("/calendar.php", "calendar.html"), ("/calendar.php?year=2007&month=4", "calendar-2007-04.html"),
         ("/calendar.php?year=2007&month=2", "calendar-2007-02.html"),
         ("/misc.php?action=help", "help.html"), ("/portal.php", "portal.html"), ("/showteam.php", "showteam.html"),
         ("/stats.php", "stats.html"), ("/online.php", "online.html"), ("/member.php?action=register", "register.html"),
         ("/member.php?action=login", "login.html"), ("/member.php?action=lostpw", "lostpw.html"),
         ("/polls.php?action=showresults&pid=1", "poll-results.html"), ("/archive/index.php", "archive.html")]
aliases = [("/index.php", "index.html"), ("/calendar.php?year=2007&month=3", "calendar.html")]

for (hid,) in rows("SELECT hid FROM mybb_helpdocs ORDER BY hid"):
    pages.append((f"/misc.php?action=help&hid={hid}", f"help-{hid}.html"))
for (fid,) in rows("SELECT fid FROM mybb_forums ORDER BY fid"):
    pages.append((f"/forumdisplay.php?fid={fid}", f"forum-{fid}.html"))
    pages.append((f"/archive/index.php/forum-{fid}.html", f"archive-forum-{fid}.html"))
for tid, fid in rows("SELECT tid, fid FROM mybb_threads ORDER BY tid"):
    pids = [r[0] for r in rows(f"SELECT pid FROM mybb_posts WHERE tid={tid} ORDER BY dateline, pid")]
    npages = (len(pids) - 1) // PPP + 1
    for pg in range(1, npages + 1):
        fname = f"thread-{tid}.html" if pg == 1 else f"thread-{tid}-{pg}.html"
        pages.append((f"/showthread.php?tid={tid}" + ("" if pg == 1 else f"&page={pg}"), fname))
        if pg == 1:
            aliases.append((f"/showthread.php?tid={tid}&page=1", fname))
    last = f"thread-{tid}.html" if npages == 1 else f"thread-{tid}-{npages}.html"
    aliases += [(f"/showthread.php?tid={tid}&action=lastpost", last), (f"/showthread.php?tid={tid}&action=newpost", last),
                (f"/showthread.php?mode=linear&tid={tid}", f"thread-{tid}.html")]
    for i, pid in enumerate(pids):
        fname = f"thread-{tid}.html" if i < PPP else f"thread-{tid}-{i // PPP + 1}.html"
        aliases += [(f"/showthread.php?tid={tid}&pid={pid}", fname), (f"/showthread.php?pid={pid}", fname)]
    pages.append((f"/archive/index.php/thread-{tid}.html", f"archive-thread-{tid}.html"))
for (uid,) in rows("SELECT uid FROM mybb_users ORDER BY uid"):
    pages.append((f"/member.php?action=profile&uid={uid}", f"member-{uid}.html"))
    pages.append((f"/search.php?action=finduser&uid={uid}", f"posts-{uid}.html"))
for (uid,) in rows("SELECT DISTINCT uid FROM mybb_reputation ORDER BY uid"):
    pages.append((f"/reputation.php?uid={uid}", f"reputation-{uid}.html"))
for (eid,) in rows("SELECT eid FROM mybb_events ORDER BY eid"):
    pages.append((f"/calendar.php?action=event&eid={eid}", f"event-{eid}.html"))
# day views for every day with an event or a birthday in the captured months
days = set()
for (d,) in rows("SELECT date FROM mybb_events"):
    days.add(tuple(map(int, d.split("-")[:3])))
for (b,) in rows("SELECT birthday FROM mybb_users WHERE birthday != ''"):
    dd, mm = map(int, b.split("-")[:2])
    if mm in (2, 3, 4):
        days.add((dd, mm, 2007))
for dd, mm, yy in sorted(days, key=lambda x: (x[2], x[1], x[0])):
    pages.append((f"/calendar.php?action=dayview&year={yy}&month={mm}&day={dd}", f"calendar-{yy}-{mm:02d}-{dd:02d}.html"))

print(" ".join(f"--page {shlex.quote(u + '=' + f)}" for u, f in pages) + " " +
      " ".join(f"--alias {shlex.quote(u + '=' + f)}" for u, f in aliases))
