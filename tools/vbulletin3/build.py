#!/usr/bin/env python3
"""Build the vBulletin 3.6.4 exhibit (exhibits/vbulletin) from archived real pages.

vBulletin is closed source, so nothing here runs vBulletin. Every page is the
raw HTML that a real vBulletin 3.6.4 board served (Wayback Machine "id_" mode,
files in ./raw), with the community's content swapped for content.py:

  raw/pages/index.php.html         The CDMA Resource forumhome      (2007-02-03)
  raw/pages/forumdisplay.php.html  The CDMA Resource forumdisplay   (2007-02-08)
  raw/pages/showthread.php.html    The CDMA Resource showthread     (2007-02-05)

The CDMA Resource ran the stock "Default Style" (stock CSS, stock logo). Its own
template edits (ads, shoutbox, arcade, photo gallery link, custom profile fields,
a guest message moved into the header, a forum-description box, an older login
form) are removed, and where that left a hole the stock markup is taken from
other real 3.6.x boards (raw/graft, see SOURCES.txt). Rows that repeat (forums,
threads, posts) are cloned from a real row of the source page.

usage: python3 build.py            (then python3 fetch_assets.py for images/js)
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "exhibits", "vbulletin"))

# tools/capture.py BAR, verbatim
BAR = ('<div style="background:#23466C;color:#FFFFFF;font:11px Verdana,Arial,sans-serif;'
       'padding:4px 10px;text-align:left;">&larr; <a href="../../index.html" target="_top" '
       'style="color:#FFFFFF;">Return to PHP Web Museum</a></div>')

IMGHOST = "http://www.v710.org/forums/images/"
SRC_TITLE = "The CDMA Resource"
LASTVISIT = (21, 14)  # guest cookie: last visit 09:14 PM; later posts count as new

# ids used in the generated vBulletin URLs (mapped to exhibit pages at the end)
CAT_IDS = {"Hardware": 1, "Community": 6}
FORUM_IDS = {"General Hardware Discussion": 2, "CPUs &amp; Motherboards": 3, "Graphics Cards": 4,
             "Overclocking &amp; Cooling": 5, "Off-Topic Lounge": 7}
SUBFORUM_IDS = {"Archived Hardware &amp; Classifieds": 8}
USER_IDS = {"OC_Overlord": 3, "Mobo_Mike": 12, "BIOS_Bob": 57, "SATA_Sam": 1488, "RadeonRaider": 4102,
            "Heatsink_Hank": 9021, "CoolerMaster_Carl": 7710, "Quad_Core_Chris": 11873,
            "ThermalThrottle_Tom": 12290, "VistaVictim": 42188, "PS3_Problems": 39914,
            "WiiWaitList": 41270, "ZuneZealot": 39102, "GTX_Newbie": 42577, "FrostyFSB": 42611}
THREAD_ID0 = 83190
MAIN_T = THREAD_ID0 + 1          # the 8800 GTX thread (index 1 in content.THREADS)
POST_ID0 = 1492840
PER_PAGE = 25                    # posts per page, as on the source board

# reputation strings exactly as vBulletin printed them on the source page
REP = {
    0: ("is an unknown quantity at this point", 1, 0),
    1: ("is on a distinguished road", 1, 0),
    2: ("is a glorious beacon of light", 5, 1),
    3: ("is a glorious beacon of light", 5, 0),
    5: ("has much to be proud of", 5, 3),
}


def read(path):
    with open(os.path.join(RAW, path), encoding="latin-1") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n")


def between(text, start, end, inclusive=True):
    i = text.index(start)
    j = text.index(end, i + len(start))
    return text[i:j + len(end)] if inclusive else text[i + len(start):j]


def grab(pattern, text, flags=re.S):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit("pattern not found: " + pattern[:80])
    return m.group(0)


def is_new(t):
    h, m, _ = re.match(r"(\d\d):(\d\d) ([AP]M)", t).groups()
    h = int(h) % 12 + (12 if t.endswith("PM") else 0)
    return (h, int(m)) > LASTVISIT


def uid(name):
    return USER_IDS[name]


def esc_attr(s):
    return s.replace('"', "&quot;")


# --------------------------------------------------------------------------
# cleanup shared by all source pages
# --------------------------------------------------------------------------

ADSENSE = re.compile(r'<script type="text/javascript"><!--\s*google_ad_client.*?</script>\s*'
                     r'<script type="text/javascript"\s+src="http://pagead2\.googlesyndication\.com/pagead/show_ads\.js">\s*</script>', re.S)

D9_ST = None


def common(html):
    global D9_ST
    if D9_ST is None:
        D9_ST = read("graft/doom9_showthread.html")
    # analytics
    html = re.sub(r'<script src="http://www\.google-analytics\.com/urchin\.js".*?urchinTracker\(\);\s*</script>\n?', "", html, flags=re.S)
    # "Sponsored Links" boxes (forumhome) and centred ad blocks (inner pages)
    html = re.sub(r'<table class="tborder"[^>]*>\s*<tr><td[^>]*class="thead"[^>]*><center>Sponsored Links</center>.*?</table><br>\s*\n<br>\n', "", html, flags=re.S)
    html = re.sub(r'<center>' + ADSENSE.pattern + r'</center><br />\n', "", html, flags=re.S)
    # top-of-page text ad before the logo, ad inside the navbar
    html = ADSENSE.sub("", html)
    # guest welcome message that this board moved into its header template
    html = re.sub(r'\n \n\t<!-- guest welcome message --> \n\t<br />.*?<!-- / guest welcome message -->\n', "\n", html, flags=re.S)
    # stock 3.6.4 login form (doom9, 2007-02-11) instead of this board's older copy
    html = html.replace(between(html, "\t\t<!-- login form -->", "<!-- / login form -->"),
                        between(D9_ST, "\t\t<!-- login form -->", "<!-- / login form -->"))
    # nav buttons added by this board: "Home" and the v3 Arcade
    html = re.sub(r'\t<td class="vbmenu_control"> <a href="http://www\.cdmaforums\.com[^"]*"> Home </a></td>\n'
                  r'<!-- change the text in capitals to your site information -->\n', "", html)
    html = re.sub(r'<!-- v3 Arcade -->.*?<!-- /v3 Arcade -->', "", html, flags=re.S)
    html = re.sub(r'(class="bigusername" href="[^"]*">[^<]*</a>) \n', r"\1\n", html)
    # forum description box this board added under the navbar
    html = re.sub(r'\n\t<table class="tborder"[^>]*>\n\t<tr>\n\t\t<td class="alt1" width="100%"><strong>[^<]*</strong> <span class="smallfont">[^<]*</span></td>\n\t</tr>\n\t</table>\n\t<br />\n', "\n", html)
    # footer: hosting company's line, scheduled-task image
    html = re.sub(r'\n\tCopyright \S+2004 - 200\d AdaptHost Internet Solutions LLC', "", html)
    html = re.sub(r'<img src="http://www\.cdmaforums\.com/forums/cron\.php[^>]*>', "", html)
    html = html.replace('<a href="http://www.cdmaforums.com">CDMAforums.com</a>',
                        '<a href="http://www.overclockhw.com">%s</a>' % C.BBTITLE)
    # board identity
    html = re.sub(r'<meta name="keywords" content="[^"]*" />',
                  '<meta name="keywords" content="vbulletin,forum,bbs,discussion,jelsoft,bulletin board,overclocking,hardware,cpu,graphics cards,cooling" />', html)
    html = re.sub(r'<meta name="description" content="[^"]*" />',
                  '<meta name="description" content="Overclock Hardware Forums: CPUs, motherboards, graphics cards, cooling and overclocking." />', html)
    html = html.replace(SRC_TITLE, C.BBTITLE)
    html = html.replace("The CDMA Resource", C.BBTITLE)
    # session ids
    html = re.sub(r"s=[0-9a-f]{32}(&amp;|&)?", "", html)
    html = html.replace('var SESSIONURL = "";', 'var SESSIONURL = "";')
    html = re.sub(r'<input type="hidden" name="s" value="[0-9a-f]{32}" />', '<input type="hidden" name="s" value="" />', html)
    # images served from the board's sister domain -> local copies
    html = html.replace(IMGHOST, "images/")
    html = html.replace('var IMGDIR_MISC = "http://www.v710.org/forums/images/misc";', 'var IMGDIR_MISC = "images/misc";')
    html = html.replace("images/smiliess/", "images/smilies/")
    # login md5 helper is only needed to submit the form
    html = re.sub(r'\s*<script type="text/javascript" src="clientscript/vbulletin_md5\.js[^"]*"></script>', "", html)
    html = re.sub(r' onsubmit="md5hash\([^"]*\)"', "", html)
    html = html.replace('src="clientscript/vbulletin_global.js?v=364"', 'src="clientscript/vbulletin_global.js"')
    html = html.replace(" (Last Day)", "")
    return html


def time_now(html):
    return re.sub(r'The time now is <span class="time">[^<]*</span>',
                  'The time now is <span class="time">%s</span>' % C.NOW_TIME, html)


def navbits(html, crumbs, final):
    """Rebuild the breadcrumb of an inner page from its own navbits markup."""
    block = between(html, '<td width="100%"><span class="navbar">', "</strong></td>")
    first = re.search(r'<span class="navbar"><a href="index\.php\?" accesskey="1">[^<]*</a></span>', block).group(0)
    item = re.search(r'\n\t<span class="navbar">&gt; <a href="forumdisplay\.php\?f=\d+">[^<]*</a></span>\n', block).group(0)
    tail = block[block.index("\n</td>"):]
    out = '<td width="100%">' + first.replace("index.php?", "index.php") + " "
    for href, label in crumbs:
        out += re.sub(r'<a href="[^"]*">[^<]*</a>', '<a href="%s">%s</a>' % (href, label), item) + "\n"
    tail = re.sub(r'<a href="/forums/[^"]*">', '<a href="%s">' % final[1], tail)
    tail = re.sub(r"<strong>\n\t[^\n]*\n\n</strong>", "<strong>\n\t%s\n\n</strong>" % final[0], tail)
    return html.replace(block, out + tail)


def forum_jump(html, current):
    opts = re.findall(r'(?:\t\t)?<option value="\d+" class="fjdpth\d"[^>]*>[^<]*</option>\n', html)
    if not opts:
        return html
    start = html.index(opts[0])
    end = html.index(opts[-1]) + len(opts[-1])
    cat_tpl, sub_tpl = opts[0], opts[1]
    out = []
    for cat, forums in C.CATEGORIES:
        out.append(re.sub(r'value="\d+"(.*?)> [^<]*<', r'value="%d"\1> %s<' % (CAT_IDS[cat], cat), cat_tpl).lstrip("\t"))
        for f in forums:
            o = re.sub(r'value="\d+"(.*?)>&nbsp; &nbsp;  [^<]*<',
                       r'value="%d"\1>&nbsp; &nbsp;  %s<' % (FORUM_IDS[f["name"]], f["name"]), sub_tpl)
            if f["name"] == current:
                o = o.replace('class="fjdpth1" >', 'class="fjsel" selected="selected">')
            out.append(o)
            for s in f.get("subforums", []):
                out.append(re.sub(r'value="\d+" class="fjdpth1" >&nbsp; &nbsp;  [^<]*<',
                                  'value="%d" class="fjdpth2" >&nbsp; &nbsp; &nbsp; &nbsp;  %s<' % (SUBFORUM_IDS[s], s), sub_tpl))
    return html[:start] + "\t\t" + "".join(out) + html[end:]


# --------------------------------------------------------------------------
# forumhome
# --------------------------------------------------------------------------

def build_index():
    html = common(read("pages/index.php.html"))
    d9 = read("graft/doom9_index.html")
    vbcom = read("graft/vbcom_index.html")
    html = html.replace("<title>%s - Powered by vBulletin</title>" % C.BBTITLE,
                        "<title>%s - Powered by vBulletin</title>" % C.BBTITLE)

    # ---- main forum list ------------------------------------------------
    main = between(html, "<!-- main -->", "<!-- /main -->")
    table_head = grab(r'<table class="tborder" cellpadding="6" cellspacing="1" border="0" width="100%" align="center">\n<thead>.*?</thead>', main)
    # stock FORUMHOME: guest welcome inside the forum table, plus the Moderator column (doom9 3.6.4)
    welcome = between(d9, "\t<!-- guest welcome message -->", "<!-- / guest welcome message -->")
    welcome = re.sub(r"Welcome to the [^<]*\.", "Welcome to the %s." % C.BBTITLE, welcome)
    welcome = re.sub(r"s=[0-9a-f]{32}", "", welcome).replace(".php?\"", ".php\"")
    modcol = between(d9, '\t  <td class="thead">Posts</td>\n', '<td class="thead">Moderator</td>\n\t  \n')
    table_head = table_head.replace("<thead>\n\t\n", "<thead>\n\t\n" + welcome + "\n\t\n", 1)
    table_head = table_head.replace('\t  <td class="thead">Posts</td>\n\t  \n', modcol, 1)

    cat_tpl = grab(r'<tbody>\n\t<tr>\n\t\t<td class="tcat" colspan="5">.*?</tbody>\n', main)
    rows_open = grab(r'<tbody id="collapseobj_forumbit_\d+" style="">\n', main)
    row_tpl = grab(r'<tr align="center">\n\t<td class="alt2"><img src="images/statusicon/forum_old\.gif".*?</tr>\n', main)
    foot = grab(r'<tbody>\n\t<tr>\n\t\t<td class="tfoot" align="center" colspan="5">.*?</tbody>\n', main)
    mod_td = grab(r'\t<td class="alt1"><div class="smallfont"><a href="member\.php\?[^"]*u=\d+" rel="nofollow">[^<]*</a>&nbsp;</div></td>\n', d9)
    subforum_div = grab(r'\t\t<div class="smallfont" style="margin-top:6px"><strong>Sub-Forums</strong>: <img [^>]*> <a href="forumdisplay\.php\?f=74">[^<]*</a></div>\n', vbcom)

    body = ""
    for cat, forums in C.CATEGORIES:
        cid = CAT_IDS[cat]
        c = cat_tpl.replace('colspan="5"', 'colspan="6"')
        c = re.sub(r"forumbit_\d+", "forumbit_%d" % cid, c)
        c = re.sub(r'<a href="forumdisplay\.php\?f=\d+">[^<]*</a>', '<a href="forumdisplay.php?f=%d">%s</a>' % (cid, cat), c)
        body += c + "\n" + rows_open.replace(re.search(r"forumbit_\d+", rows_open).group(0), "forumbit_%d" % cid)
        for f in forums:
            fid = FORUM_IDS[f["name"]]
            title, who, when = f["last"]
            r = row_tpl
            if is_new(when):
                r = r.replace("statusicon/forum_old.gif", "statusicon/forum_new.gif")
            r = re.sub(r'id="forum_statusicon_\d+"', 'id="forum_statusicon_%d"' % fid, r)
            r = re.sub(r'id="f\d+"', 'id="f%d"' % fid, r)
            r = re.sub(r'<a href="forumdisplay\.php\?f=\d+"><strong>[^<]*</strong></a>',
                       '<a href="forumdisplay.php?f=%d"><strong>%s</strong></a>' % (fid, f["name"]), r)
            r = re.sub(r"\(\d+ Viewing\)", "(%d Viewing)" % f["viewing"], r)
            r = re.sub(r'<div class="smallfont">[^<]*</div>\n\t\t\n',
                       '<div class="smallfont">%s</div>\n\t\t\n' % f["desc"], r, count=1)
            if f.get("subforums"):
                links = ", ".join(
                    re.search(r"<img [^>]*> ", subforum_div).group(0)
                    .replace("http://images.vbulletin.com/images_vb3/", "images/")
                    .replace('id="forum_statusicon_74"', 'id="forum_statusicon_%d"' % SUBFORUM_IDS[s])
                    + '<a href="forumdisplay.php?f=%d">%s</a>' % (SUBFORUM_IDS[s], s)
                    for s in f["subforums"])
                sub = re.sub(r"<strong>Sub-Forums</strong>: .*</div>", "<strong>Sub-Forums</strong>: " + links + "</div>", subforum_div)
                r = re.sub(r"(<div class=\"smallfont\">[^<]*</div>\n)\t\t\n", lambda m: m.group(1) + sub, r, count=1)
            tid = THREAD_ID0 + 1 if f.get("current") else THREAD_ID0 + 40 + fid
            short = title if len(title) <= 50 else title[:50].rstrip() + "..."
            r = re.sub(r'<a href="showthread\.php\?goto=newpost&amp;t=\d+" title="Go to first unread post in thread \'[^"]*\'"><strong>[^<]*</strong></a>',
                       lambda m: '<a href="showthread.php?goto=newpost&amp;t=%d" title="Go to first unread post in thread \'%s\'"><strong>%s</strong></a>'
                       % (tid, esc_attr(title), short), r)
            r = re.sub(r'(by <a href="member\.php\?find=lastposter&amp;f=)\d+(" rel="nofollow">)[^<]*(</a>)',
                       lambda m: m.group(1) + str(fid) + m.group(2) + who + m.group(3), r)
            r = re.sub(r'\t\t[^\n<]*<span class="time">[^<]*</span>',
                       '\t\tToday <span class="time">%s</span>' % when, r, count=1)
            pid = POST_ID0 + 4 if f.get("current") else POST_ID0 - 100 * fid
            r = re.sub(r'showthread\.php\?p=\d+#post\d+', "showthread.php?p=%d#post%d" % (pid, pid), r)
            r = re.sub(r'<td class="alt1">[\d,]+</td>\n\t<td class="alt2">[\d,]+</td>\n\t\n',
                       '<td class="alt1">%s</td>\n\t<td class="alt2">%s</td>\n\t\n' % (f["threads"], f["posts"]), r)
            mods = ", ".join('<a href="member.php?u=%d" rel="nofollow">%s</a>' % (uid(m), m) for m in f["mods"])
            r = r.replace("\t\n</tr>\n", "\t\n" + re.sub(r'<a href=.*</a>', mods, mod_td) + "\t\n</tr>\n")
            body += r
        body += "\n</tbody>\n\n\n"
    foot = foot.replace('colspan="5"', 'colspan="6"')
    html = html.replace(main, "<!-- main -->\n" + table_head + "\n" + body + foot + "</table>\n<!-- /main -->")

    # ---- what's going on ------------------------------------------------
    s = C.STATS
    html = re.sub(r'Currently Active Users</a>: [\d,]+ \([\d,]+ members and [\d,]+ guests\)',
                  'Currently Active Users</a>: %s (%s members and %s guests)' % (s["online_total"], s["online_members"], s["online_guests"]), html)
    html = re.sub(r"Most users ever online was [\d,]+, [^<]*\.",
                  "Most users ever online was %s, %s." % (s["record_users"], s["record_date"]), html)
    online = ", ".join('<a href="member.php?u=%d" rel="nofollow">%s</a>' % (uid(u), u) for u in C.ACTIVE_USERS)
    html = re.sub(r'(<div style="white-space: nowrap">Most users ever online[^\n]*\n\t\t\t\t<div>).*?(</div>)',
                  lambda m: m.group(1) + online + m.group(2), html, flags=re.S)
    html = re.sub(r"Threads: [\d,]+,\n(\s*)Posts: [\d,]+,\n(\s*)Members: [\d,]+",
                  lambda m: "Threads: %s,\n%sPosts: %s,\n%sMembers: %s" % (s["threads"], m.group(1), s["posts"], m.group(2), s["members"]), html)
    html = re.sub(r'Welcome to our newest member, <a href="member\.php\?u=\d+" rel="nofollow">[^<]*</a>',
                  'Welcome to our newest member, <a href="member.php?u=%d" rel="nofollow">%s</a>' % (uid(s["newest"]), s["newest"]), html)
    html = html.replace("day=2007-02-03", "day=2007-02-12")
    bdays = ", ".join('<!--rlm--><a href="member.php?u=%d">%s</a> <!--rlm-->(%d)' % (uid(n), n, a) for n, a in C.BIRTHDAYS)
    html = re.sub(r'(<td class="alt1" width="100%"><div class="smallfont">)<!--rlm-->.*?(</div></td>)',
                  lambda m: m.group(1) + bdays + m.group(2), html)
    return finish(time_now(html))


# --------------------------------------------------------------------------
# forumdisplay
# --------------------------------------------------------------------------

def thread_row(tpl, t, tid, multipage_tpl):
    title, starter, replies, views, last_user, last_time, sticky, new = t
    nrep = int(replies.replace(",", ""))
    nviews = int(views.replace(",", ""))
    hot = nrep >= 15 or nviews >= 150
    icon = "thread" + ("_hot" if hot else "") + ("_new" if is_new(last_time) else "")
    r = re.sub(r"(_|statusicon_|threadtitle_|title_)\d+", lambda m: m.group(1) + str(tid), tpl)
    r = re.sub(r"statusicon/thread[a-z_]*\.gif", "statusicon/%s.gif" % icon, r)
    r = re.sub(r'(<td class="alt1" id="td_threadtitle_\d+" title=")[^"]*(")',
               lambda m: m.group(1) + (C.POSTS[0][2][:200].rsplit(" ", 1)[0] + "..." if tid == MAIN_T else "") + m.group(2), r, flags=re.S)
    r = re.sub(r'(<a href="showthread\.php\?t=)\d+(" id="thread_title_\d+">)[^<]*(</a>)',
               lambda m: m.group(1) + str(tid) + m.group(2) + title + m.group(3), r)
    pages = math.ceil((nrep + 1) / PER_PAGE)
    if pages > 1:
        links = " ".join('<a href="showthread.php?t=%d%s">%d</a>' % (tid, "&amp;page=%d" % p if p > 1 else "", p)
                         for p in range(1, min(pages, 5) + 1))
        if pages > 5:
            links += ' ... <a href="showthread.php?t=%d&amp;page=%d">Last Page</a>' % (tid, pages)
        mp = re.sub(r'(border="0" />  ).*(\)</span>)', lambda m: m.group(1) + links + m.group(2), multipage_tpl)
        r = r.replace(" id=\"thread_title_%d\">%s</a>\n" % (tid, title),
                      " id=\"thread_title_%d\">%s</a>\n%s" % (tid, title, mp), 1)
    onclick = " onclick=\"window.open('member.php?u=%d', '_self')\"" % uid(starter)
    r = re.sub(r'<span style="cursor:pointer" onclick="[^"]*">[^<]*</span>',
               '<span style="cursor:pointer"%s>%s</span>' % (onclick, starter), r)
    r = re.sub(r'title="Replies: [\d,]+, Views: [\d,]+"', 'title="Replies: %s, Views: %s"' % (replies, views), r)
    r = re.sub(r'\t\t\t[^\n<]*<span class="time">[^<]*</span><br />',
               '\t\t\tToday <span class="time">%s</span><br />' % last_time, r)
    r = re.sub(r'(by <a href="member\.php\?find=lastposter&amp;t=)\d+(" rel="nofollow">)[^<]*(</a>)',
               lambda m: m.group(1) + str(tid) + m.group(2) + last_user + m.group(3), r)
    pid = POST_ID0 + 4 if tid == MAIN_T else POST_ID0 - 7 * tid % 9000
    r = re.sub(r"showthread\.php\?p=\d+#post\d+", "showthread.php?p=%d#post%d" % (pid, pid), r)
    r = re.sub(r'<a href="#" onclick="who\(\d+\); return false;">[\d,]+</a>',
               '<a href="#" onclick="who(%d); return false;">%s</a>' % (tid, replies), r)
    r = re.sub(r'<td class="alt2" align="center">[\d,]+</td>', '<td class="alt2" align="center">%s</td>' % views, r)
    return r


def build_forumdisplay():
    html = common(read("pages/forumdisplay.php.html"))
    f = C.FORUM
    fid = FORUM_IDS[f["name"]]
    cat = C.CATEGORIES[0][0]
    html = re.sub(r"<title>[^<]*</title>", "<title>%s - %s</title>" % (f["name"], C.BBTITLE), html)
    html = re.sub(r'title="%s - [^"]*- RSS Feed" href="external\.php\?type=RSS2&amp;forumids=\d+"' % re.escape(C.BBTITLE),
                  'title="%s - %s - RSS Feed" href="external.php?type=RSS2&amp;forumids=%d"' % (C.BBTITLE, f["name"], fid), html)
    html = re.sub(r'<meta name="keywords" content="[^"]*" />',
                  '<meta name="keywords" content="%s, vbulletin,forum,bbs,discussion,jelsoft,bulletin board" />' % f["name"], html)
    html = navbits(html, [("forumdisplay.php?f=%d" % CAT_IDS[cat], cat)], (f["name"], "/forumdisplay.php?f=%d" % fid))
    # hot-thread threshold in the icon key follows the stock setting (150 views) used for the icons
    html = html.replace("More than 15 replies or 20 views", "More than 15 replies or 150 views")
    html = re.sub(r"(forumid|forumchoice\[\]|f)\" value=\"11\"", r'\1" value="%d"' % fid, html)
    html = html.replace("f=11", "f=%d" % fid).replace("forumids=11", "forumids=%d" % fid)
    html = html.replace("<span class=\"normal\"> : Audio Format</span>", "<span class=\"normal\"> : %s</span>" % f["name"])
    html = html.replace("forumdisplay.php?do=markread&amp;f=%d" % fid, "forumdisplay.php?do=markread&amp;f=%d" % fid)
    html = re.sub(r'<a href="forumdisplay\.php\?f=8" rel="nofollow">View Parent Forum</a>',
                  '<a href="forumdisplay.php?f=%d" rel="nofollow">View Parent Forum</a>' % CAT_IDS[cat], html)

    # ad rows at the top and bottom of the thread list
    html = re.sub(r'\n<tr>\n<td align="center" class="alt1">-</td>.*?Sponsored Links</td>.*?</tr>\n', "\n", html, flags=re.S)
    # thread list: viewer filtered to "Last Day", so 9 threads and no page navigation
    html = re.sub(r'<div class="pagenav" align="right">\n<table class="tborder".*?</table>\n</div>', "", html, flags=re.S)

    rows = between(html, "\t<!-- show threads -->", "\t<!-- end show threads -->")
    sticky_tpl = grab(r'<tr>\n\t<td class="alt1" id="td_threadstatusicon_1473">.*?</tr>', rows)
    normal_tpl = grab(r'<tr>\n\t<td class="alt1" id="td_threadstatusicon_6016">.*?</tr>', rows)
    multipage_tpl = grab(r'\t\t\t<span class="smallfont" style="white-space:nowrap">\(<img class="inlineimg" src="images/misc/multipage\.gif"[^\n]*\n', html)
    sticky_tpl = sticky_tpl.replace("images/icons/icon4.gif\" alt=\"Exclamation\"", "images/icons/icon4.gif\" alt=\"Exclamation\"")
    out = "\t<!-- show threads -->\n\t\n\t"
    for i, t in enumerate(C.THREADS):
        tpl = sticky_tpl if t[6] else normal_tpl
        out += thread_row(tpl, t, THREAD_ID0 + i, multipage_tpl) + "\n\t\n\t"
    html = html.replace(rows, out.rstrip("\t") + "\t<!-- end show threads -->")

    # display options / active users / moderators
    n = len(C.THREADS)
    html = re.sub(r"Showing threads 1 to \d+ of [\d,]+", "Showing threads 1 to %d of %d" % (n, n), html)
    readers = [u for u in C.ACTIVE_USERS if u in ("RadeonRaider", "GTX_Newbie", "Heatsink_Hank", "OC_Overlord", "Mobo_Mike", "SATA_Sam", "CoolerMaster_Carl")]
    html = html.replace('<td class="thead">1 (0 members &amp; 1 guests)</td>',
                        '<td class="thead">%d (%d members &amp; %d guests)</td>' % (f["viewing"], len(readers), f["viewing"] - len(readers)))
    html = html.replace('<td class="alt1"><div class="smallfont"></div></td>',
                        '<td class="alt1"><div class="smallfont">%s</div></td>' %
                        ", ".join('<a href="member.php?u=%d">%s</a>' % (uid(u), u) for u in readers))
    mods = f["mods"]
    html = html.replace('<td class="thead">Moderators : 3</td>', '<td class="thead">Moderators : %d</td>' % len(mods))
    html = re.sub(r'(<td class="alt1"><div class="smallfont">)<a href="member\.php\?u=5042">.*?(&nbsp;</div></td>)',
                  lambda m: m.group(1) + ", ".join('<a href="member.php?u=%d">%s</a>' % (uid(x), x) for x in mods) + m.group(2), html)
    html = html.replace('<option value="1" >Last Day</option>', '<option value="1" selected="selected">Last Day</option>')
    html = html.replace('<option value="-1" selected="selected">Beginning</option>', '<option value="-1" >Beginning</option>')
    html = html.replace('<input type="hidden" name="daysprune" value="-1" />', '<input type="hidden" name="daysprune" value="1" />')
    html = forum_jump(html, f["name"])
    return finish(time_now(html))


# --------------------------------------------------------------------------
# showthread
# --------------------------------------------------------------------------

def rep_html(tpl_img, name, level):
    phrase, pos, high = REP[level]
    one = re.sub(r'alt="[^"]*"', 'alt="%s %s"' % (name, phrase), tpl_img)
    return one * pos + one.replace("reputation_pos.gif", "reputation_highpos.gif") * high


def build_showthread():
    html = common(read("pages/showthread.php.html"))
    f = C.FORUM
    fid = FORUM_IDS[f["name"]]
    cat = C.CATEGORIES[0][0]
    tid = MAIN_T
    title = C.THREAD_TITLE
    html = re.sub(r"<title>[^<]*</title>", "<title>%s - %s</title>" % (title, C.BBTITLE), html)
    html = re.sub(r'<meta name="keywords" content="[^"]*" />',
                  '<meta name="keywords" content="%s, vbulletin,forum,bbs,discussion,jelsoft,bulletin board" />' % esc_attr(title), html)
    html = re.sub(r'<meta name="description" content="[^"]*" />',
                  '<meta name="description" content="%s %s" />' % (esc_attr(title), f["name"]), html)
    html = re.sub(r'title="%s - [^"]*- RSS Feed" href="external\.php\?type=RSS2&amp;forumids=\d+"' % re.escape(C.BBTITLE),
                  'title="%s - %s - RSS Feed" href="external.php?type=RSS2&amp;forumids=%d"' % (C.BBTITLE, f["name"], fid), html)
    html = navbits(html, [("forumdisplay.php?f=%d" % CAT_IDS[cat], cat), ("forumdisplay.php?f=%d" % fid, f["name"])],
                   (title, "/showthread.php?t=%d" % tid))
    # 5 posts fit on one page
    html = re.sub(r'<div class="pagenav" align="right">\n<table class="tborder".*?</table>\n</div>', "", html, flags=re.S)

    posts = between(html, '<div id="posts">', '<div id="lastpost"></div></div>')
    inner = grab(r"(?<=\n)<!-- post #7989 -->\n\n\t<!-- open content container -->.*?<!-- / post #7989 -->", posts.split("<!-- post #7989 -->", 2)[0] + "\n<!-- post #7989 -->" + posts.split("<!-- post #7989 -->", 2)[2])
    tpl = inner
    # strip this board's postbit additions (avatar via image.php kept out: our users have none)
    tpl = re.sub(r'\t\t\t<td class="alt2"><a href="member\.php\?u=\d+"><img src="image\.php[^>]*></a></td>\n', "", tpl)
    tpl = re.sub(r'(\t\t\t\t<div class="smallfont">[^<]*</div>\n\t\t\t\t\n).*?\t\t\t</td>\n<br>\n\n(\t\t\t<td width="100%">)',
                 lambda m: m.group(1) + "\n\t\t\t</td>\n" + m.group(2), tpl, flags=re.S)
    tpl = re.sub(r"(Posts: [\d,]+) \| Shouts: \d+", r"\1", tpl)
    tpl = re.sub(r"\t\t<!-- edit note -->.*?<!-- / edit note -->\n", "", tpl, flags=re.S)
    rep_img = grab(r'<img class="inlineimg" src="images/reputation/reputation_pos\.gif" alt="[^"]*" border="0" />', tpl)
    sig_tpl = grab(r"\t\t<!-- sig -->.*?<!-- / sig -->\n", posts)
    quote_tpl = grab(r'<div style="margin:20px; margin-top:5px; ">.*?</table>\n</div>', posts)
    online_img = '<img class="inlineimg" src="images/statusicon/user_online.gif" alt="%s is online now" border="0" />'

    out = '<div id="posts">'
    for n, p in enumerate(C.POSTS, 1):
        name, when = p[0], p[1]
        quote = p[2] if len(p) == 4 else None
        text = p[-1]
        u = C.USERS[name]
        pid = POST_ID0 + n - 1
        b = tpl.replace("7989", str(pid)).replace("u=1951", "u=%d" % uid(name))
        b = b.replace("Humpa", name)
        b = re.sub(r'name="1"><strong>1</strong>', 'name="%d"><strong>%d</strong>' % (n, n), b)
        b = b.replace("postcount=1", "postcount=%d" % n)
        if is_new(when):
            b = b.replace('statusicon/post_old.gif" alt="Old"', 'statusicon/post_new.gif" alt="New"')
        b = re.sub(r"\n\t\t\t\n\t\t\t\t\d\d-\d\d-\d{4}, [^\n]*\n", "\n\t\t\t\n\t\t\t\tToday, %s\n" % when, b)
        if name in C.ACTIVE_USERS:
            b = re.sub(r'<img class="inlineimg" src="images/statusicon/user_offline\.gif" alt="[^"]*" border="0" />',
                       online_img % name, b)
        b = re.sub(r'<div class="smallfont">Master Of His Domain</div>', '<div class="smallfont">%s</div>' % u["title"], b)
        b = re.sub(r"<div>Join Date: [^<]*</div>", "<div>Join Date: %s</div>" % u["joined"], b)
        if u.get("location"):
            b = re.sub(r"<div>Location: [^<]*</div>", "<div>Location: %s</div>" % u["location"], b)
        else:
            b = re.sub(r"\t\t\t\t\t<div>Location: [^<]*</div>\n", "", b)
        b = re.sub(r"Posts: [\d,]+", "Posts: %s" % u["posts"], b)
        b = re.sub(r"<div>(<img class=\"inlineimg\" src=\"images/reputation/[^\n]*)</div>",
                   lambda m: "<div>" + rep_html(rep_img, name, u["rep"]) + "</div>", b)
        if n == 1:
            b = re.sub(r"<strong>[^<]*</strong>\n\t\t\t</div>\n\t\t\t<hr",
                       "<strong>%s</strong>\n\t\t\t</div>\n\t\t\t<hr" % title, b)
        else:
            b = re.sub(r"\t\t\n\t\t\t<!-- icon and title -->.*?<!-- / icon and title -->\n", "", b, flags=re.S)
        body = text
        if quote:
            q = quote_tpl
            q = re.sub(r"Originally Posted by <strong>[^<]*</strong>", "Originally Posted by <strong>%s</strong>" % quote[0], q)
            q = re.sub(r'(<div style="font-style:italic">).*?(</div>)', lambda m: m.group(1) + quote[1] + m.group(2), q, flags=re.S)
            body = q + body
        b = re.sub(r'(<div id="post_message_%d">).*?(</div>\n\t\t<!-- / message -->)' % pid,
                   lambda m: m.group(1) + body + m.group(2), b, flags=re.S)
        if u.get("sig"):
            sig = re.sub(r"(__________________<br />\n\t\t\t\t).*?(\n\t\t\t</div>)",
                         lambda m: m.group(1) + u["sig"] + m.group(2), sig_tpl, flags=re.S)
            b = b.replace("\t\t<!-- / message -->\n", "\t\t<!-- / message -->\n\t\n\t\t\n\t\t\n\t\t\n" + sig, 1)
        if n == len(C.POSTS):
            b = b.replace("<!-- this is not the last post shown on the page -->", "<!-- this is the last post shown on the page -->")
        out += b
    out += '<div id="lastpost"></div></div>'
    html = html.replace(posts, out)

    html = re.sub(r"newreply\.php\?do=newreply&amp;noquote=1&amp;p=\d+", "newreply.php?do=newreply&amp;noquote=1&amp;p=%d" % (POST_ID0 + 4), html)
    html = html.replace("t=1440", "t=%d" % tid).replace("p=7989", "p=%d" % POST_ID0).replace("#post7989", "#post%d" % POST_ID0)
    viewers = ["RadeonRaider", "GTX_Newbie", "Heatsink_Hank"]
    html = html.replace('Currently Active Users Viewing This Thread: 1 <span class="normal">(0 members and 1 guests)</span>',
                        'Currently Active Users Viewing This Thread: %d <span class="normal">(%d members and %d guests)</span>'
                        % (len(viewers) + 2, len(viewers), 2))
    html = html.replace('<td class="alt1" colspan="2">\n\t\t\t<span class="smallfont">&nbsp;</span>',
                        '<td class="alt1" colspan="2">\n\t\t\t<span class="smallfont">%s</span>' %
                        ", ".join('<a href="member.php?u=%d">%s</a>' % (uid(v), v) for v in viewers))

    # similar threads: rows cloned from the source block
    sim = between(html, '<tbody id="collapseobj_similarthreads" style="">', "</tbody>")
    head = grab(r'<tr class="thead" align="center">.*?</tr>\n', sim)
    row = grab(r"<tr>\n\t<td class=\"alt1\" align=\"left\">.*?</tr>\n", sim)
    similar = [(C.THREADS[5], "Graphics Cards"), (C.THREADS[8], "Graphics Cards"),
               (("Arctic Cooling Accelero for 8800 GTX - worth it?", "Heatsink_Hank", "37", "", "", "02-03-2007 08:41 PM", False, False), "Overclocking &amp; Cooling"),
               (("Reference cooler fan speed tweak (RivaTuner guide)", "OC_Overlord", "112", "", "", "01-21-2007 11:02 AM", False, False), "Overclocking &amp; Cooling")]
    rows_out = ""
    for i, (t, forum) in enumerate(similar):
        when = t[5] if " " in t[5] and "-" in t[5] else "Today " + t[5]
        d, tm = (when.split(" ", 1) if not when.startswith("Today") else ("Today", when[6:]))
        r = re.sub(r'<a href="showthread\.php\?t=\d+" title="[^"]*">[^<]*</a>',
                   '<a href="showthread.php?t=%d" title="">%s</a>' % (THREAD_ID0 + 20 + i, t[0]), row, flags=re.S)
        r = re.sub(r'(<td class="alt2" nowrap="nowrap"><span class="smallfont">)[^<]*', lambda m: m.group(1) + t[1], r)
        r = re.sub(r'(<td class="alt1" nowrap="nowrap"><span class="smallfont">)[^<]*', lambda m: m.group(1) + forum, r)
        r = re.sub(r'(<td class="alt2" align="center"><span class="smallfont">)[\d,]+', lambda m: m.group(1) + t[2], r)
        r = re.sub(r'(<td class="alt1" align="right"><span class="smallfont">)[^<]*<span class="time">[^<]*</span>',
                   lambda m: m.group(1) + '%s <span class="time">%s</span>' % (d, tm), r)
        rows_out += r
    html = html.replace(sim, '<tbody id="collapseobj_similarthreads" style="">\n' + head + rows_out)
    html = forum_jump(html, f["name"])
    return finish(time_now(html))


# --------------------------------------------------------------------------
# member profile (frame: forumdisplay source page; body: vbulletin.org 3.6.x MEMBERINFO)
# --------------------------------------------------------------------------

def build_member():
    name = C.VIEWER
    u = C.USERS[name]
    page = common(read("pages/forumdisplay.php.html"))
    paul = read("graft/vborg_member_paulm.html")
    marco = read("graft/vborg_member_marco.html")

    head, rest = page.split("<!-- threads list  -->", 1)
    foot = rest[rest.index("<br />\n<div class=\"smallfont\" align=\"center\">All times are GMT."):]
    head = re.sub(r"<title>[^<]*</title>", "<title>%s - View Profile: %s</title>" % (C.BBTITLE, name), head)
    head = re.sub(r'\n<link rel="alternate" type="application/rss\+xml" title="[^"]*- RSS Feed"[^>]*>\n', "\n", head)
    head = navbits(head, [], ("View Profile: %s" % name, "/member.php?u=%d" % uid(name)))
    head = head.replace('<td width="100%"><span class="navbar"><a href="index.php" accesskey="1">',
                        '<td width="100%"><span class="navbar"><a href="index.php" accesskey="1">')

    body = between(paul, "<!-- main info - avatar, profilepic etc. -->", "</table>\n\n<!-- Hack Information -->")
    body = body[: -len("\n\n<!-- Hack Information -->")]
    body = re.sub(r"s=[0-9a-f]{32}(&amp;)?", "", body)
    # template cellpadding comes from the style; the stock style uses 6
    body = body.replace('cellpadding="4" cellspacing="1"', 'cellpadding="6" cellspacing="1"')
    # vbulletin.org additions: stray cell, avatar, "release level" title link, staff colour
    body = re.sub(r'\t\t\t<td class="smallfont" valign="top" align="right">\n\t\t\t\n', "", body)
    body = re.sub(r"\t\t\t\t<td><img src=\"/custompics[^\n]*</td>\n\t\t\t\n", "", body)
    body = re.sub(r'<strong class="staffcolor" style="font-style:italic">Paul M</strong>', "<strong>%s</strong>" % name, body)
    body = re.sub(r'<div class="smallfont"><a style="[^"]*" href="[^"]*" title="[^"]*">Administrator</a></div>',
                  '<div class="smallfont">%s</div>' % u["title"], body)
    body = body.replace("View Profile<span class=\"normal\">: Paul M</span>", "View Profile<span class=\"normal\">: %s</span>" % name)
    body = re.sub(r"Last Activity: Today <span class=\"time\">[^<]*</span>", 'Last Activity: Today <span class="time">11:58 PM</span>', body)
    body = re.sub(r'(<td class="alt1" title="Signature"><div class="smallfont">).*?(</div></td>)',
                  lambda m: m.group(1) + u["sig"] + m.group(2), body, flags=re.S)
    body = re.sub(r"Join Date: <strong>[^<]*</strong>", "Join Date: <strong>%s</strong>" % u["joined_long"], body)
    body = re.sub(r"Total Posts: <strong>[\d,]+</strong> \([\d.]+ posts per day\)",
                  "Total Posts: <strong>%s</strong> (%s posts per day)" % (u["posts"], u["ppd"]), body)
    body = re.sub(r"\t\t\t<!-- Hack: Username Management Addon[^\n]*\n", "", body)
    body = re.sub(r"u=63698", "u=%d" % uid(name), body)
    body = body.replace("searchuser=Paul+M", "searchuser=%s" % name).replace("Paul M", name)
    # contact info: none for this member (vbulletin.org markup for that case)
    nocontact = grab(r'\t\t\t\t<tr>\n\t\t\t\t\t<td><strong>[^<]* has no contact information\.</strong></td>\n\t\t\t\t</tr>', marco)
    nocontact = re.sub(r"<strong>.* has no contact", "<strong>%s has no contact" % name, nocontact)
    body = re.sub(r"\t\t\t\t<tr>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t<strong>Home Page</strong>:.*?</tr>", lambda m: nocontact, body, flags=re.S)
    # additional information: birthday rows (Paul M) + profile fields (Marco, dt/dd)
    body = body.replace("November 27, 1962", "February 12, 1978").replace("\t\t\t\t\t\t44\n", "\t\t\t\t\t\t%d\n" % u["age"])
    # profile fields use the same row markup vBulletin printed for Date of Birth / Age
    row = grab(r"\t\t\t\t<tr>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t<strong>Age</strong>:  \n\t\t\t\t\t\t\d+\n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n", body)
    fields = "".join(row.replace("Age", k).replace("\t%d\n" % u["age"], "\t%s\n" % v) for k, v in
                     (("Biography", u["bio"]), ("Location", u["location"]), ("Interests", u["interests"]), ("Occupation", u["occupation"])))
    body = body.replace(row, row + fields, 1)
    html = head + "\n\n\n\n\n\n\n\n\n" + body + "\n\n<br />\n" + foot
    return finish(time_now(html))


# --------------------------------------------------------------------------
# links, forms, museum bar
# --------------------------------------------------------------------------

def link_target(url):
    frag = ""
    if "#" in url:
        url, frag = url.split("#", 1)
        frag = "#" + frag
    u = url.replace("&amp;", "&")
    if re.match(r"(index\.php)?\??$", u) and u != "":
        return "index.html"
    if re.match(r"forumdisplay\.php\?f=%d$" % FORUM_IDS[C.FORUM["name"]], u):
        return "forumdisplay.html"
    u = re.sub(r"^/forums/", "", u)
    if re.match(r"forumdisplay\.php\?f=%d$" % FORUM_IDS[C.FORUM["name"]], u):
        return "forumdisplay.html"
    m = re.match(r"showthread\.php\?(.*)$", u)
    if m and re.search(r"goto=next|mode=", m.group(1)):
        return None
    if m and ("t=%d" % MAIN_T in m.group(1).split("&") or re.search(r"p=(\d+)", m.group(1)) and
              POST_ID0 <= int(re.search(r"p=(\d+)", m.group(1)).group(1)) < POST_ID0 + len(C.POSTS)):
        return "showthread.html" + frag
    if re.match(r"/?member\.php\?u=%d$" % uid(C.VIEWER), u):
        return "member.html"
    return None


def finish(html):
    def href(m):
        val = m.group(2)
        if val.startswith(("#", "javascript:")):
            return m.group(0)
        t = link_target(val)
        return m.group(1) + (t if t else "#") + m.group(3)

    html = re.sub(r'(\bhref=")([^"]*)(")', href, html)
    # starter names in thread lists open the profile with window.open()
    html = re.sub(r"window\.open\('member\.php\?u=(\d+)', '_self'\)",
                  lambda m: "window.open('member.html', '_self')" if int(m.group(1)) == uid(C.VIEWER) else "return false", html)
    html = html.replace(' onclick="return false"', "")
    html = re.sub(r'(<form\b[^>]*?\baction=")[^"]*(")', r"\1#\2", html)
    html = re.sub(r'(<form\b[^>]*?)\bmethod="post"', r'\1method="get"', html)
    html = re.sub(r'(<input type="password"[^>]*?) name="[^"]*"', r"\1", html)
    html = re.sub(r'onclick="who\(\d+\); return false;"', 'onclick="return false;"', html)
    html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + BAR, html, count=1)
    leftovers = re.findall(r"cdma|v710|google|urchin|arcade|photoplog|vbshout|AdaptHost", html, re.I)
    if leftovers:
        raise SystemExit("source-board leftovers: %s" % sorted(set(leftovers)))
    return html


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {"index.html": build_index, "forumdisplay.html": build_forumdisplay,
             "showthread.html": build_showthread, "member.html": build_member}
    for fname, fn in pages.items():
        html = fn()
        with open(os.path.join(OUT, fname), "w", encoding="latin-1", errors="xmlcharrefreplace") as fh:
            fh.write(html)
        print("wrote", fname, len(html))


if __name__ == "__main__":
    main()
