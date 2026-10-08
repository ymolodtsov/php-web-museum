#!/usr/bin/env python3
"""Rebuild exhibits/ipb from real Invision Power Board 2.1.5 pages archived by the
Wayback Machine (see SOURCES.txt) plus the fictional content in content.py.

Every tag, class, image and string of IPB furniture comes from the raw pages in
./raw; this script only swaps the source community's names, numbers and posts for
ours, drops the host's ad slot, and wires the four pages together.

usage: python3 build.py            (assets must already be in raw/assets, see fetch_assets.py)
"""
import os
import re
import shutil

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
ASSETS = os.path.join(RAW, "assets")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "exhibits", "ipb"))

# copied verbatim from tools/capture.py
BAR = ('<div style="background:#23466C;color:#FFFFFF;font:11px Verdana,Arial,sans-serif;'
       'padding:4px 10px;text-align:left;">&larr; <a href="../../index.html" target="_top" '
       'style="color:#FFFFFF;">Return to PHP Web Museum</a></div>')

PAGES = {"index": "index.html", "forum": "showforum.html", "topic": "showtopic.html", "user": "showuser.html"}


def raw(name):
    with open(os.path.join(RAW, name), encoding="latin-1") as fh:
        return fh.read()


def between(text, start, end, inclusive=False):
    i = text.index(start)
    j = text.index(end, i + len(start))
    return text[i:j + len(end)] if inclusive else text[i:j]


def sub1(pattern, repl, text, flags=re.S, count=1):
    new, n = re.subn(pattern, repl, text, count=count, flags=flags)
    if n == 0:
        raise ValueError("pattern not found: " + pattern[:80])
    return new


def rep(text, old, new, count=-1):
    if old not in text:
        raise ValueError("text not found: " + old[:80])
    return text.replace(old, new, count)


# ---------------------------------------------------------------- sources
IDX = raw("index.html")                    # forum.imgburn.com index, 12 May 2006, v2.1.5
SF = raw("index.php_showforum_6")          # forum.imgburn.com showforum=6, 29 Mar 2006, v2.1.5
ST = raw("showtopic_1160.html")            # forum.imgburn.com showtopic=1160, 29 Mar 2006, v2.1.5
ST_QUOTE = raw("showtopic_1255_20060620140329.html")   # quote markup (imgburn, Jun 2006)
QR = raw("ig_showtopic_3525.html")         # invisiongames.org Fast Reply (guests may post there)
XS = raw("xs_showtopic_500142.html")       # xbox-scene emoticon <img> markup (guests saw images)
IPS_IDX = raw("ips_index_20060503080902.html")  # forums.invisionpower.com index, birthdays row
PROF = raw("ips_showuser_129.html")        # forums.invisionpower.com profile, 29 Mar 2006, v2.1.5
ONLINE_IMG = "<img src='style_images/1/p_online.gif' border='0'  alt='User is online!' />"


def member_link(name):
    """IPB writes profile links as <a href='...showuser=N'>name</a>."""
    href = PAGES["user"] if name == C.PROFILE["name"] else "#"
    return "<a href='%s'>%s</a>" % (href, name)


def short_title(t):
    # IPB 2.1 index truncates last-post titles: 27 chars + '...'
    plain = re.sub(r"&[#a-z0-9]+;", "x", t)
    if len(plain) <= 30:
        return t
    # cut on the entity-aware string
    out, n, i = "", 0, 0
    while n < 27 and i < len(t):
        m = re.match(r"&[#a-z0-9]+;", t[i:])
        tok = m.group(0) if m else t[i]
        out += tok
        i += len(tok)
        n += 1
    return out + "..."


# ------------------------------------------------------------ common shell
def shell(title, body):
    head = IDX[:IDX.index("<body>")]
    head = sub1(r"<title>.*?</title>", "<title>%s</title>" % title, head)
    head = sub1(r'<link rel="shortcut icon"[^>]*>\n', "", head)
    head = rep(head, "http://forum.imgburn.com/style_images/css_3.css", "style_images/css_3.css")

    top = between(IDX, "<body>", '<div id="adverts_banner"')
    top = sub1(r'(var ipb_var_base_url\s*= )"http://forum\.imgburn\.com/index\.php\?s=&";', r'\1"";', top)
    top = rep(top, "href='http://forum.imgburn.com/index.php?'", "href='%s'" % PAGES["index"])
    top = rep(top, '<a href="http://www.imgburn.com">ImgBurn Website</a>', '<a href="#">%s</a>' % C.HOME_LINK)

    foot = IDX[IDX.index('<table cellspacing="0" id="gfooter">'):]
    foot = sub1(r"Time is now: [^<]*", "Time is now: " + C.NOW_LONG, foot)
    foot = rep(foot, "v2.1.5", C.VERSION)

    html = head + top + body + foot
    html = rep(html, "<body>", "<body>\n" + BAR, 1)
    return finish(html)


def navstrip(*crumbs):
    nav = between(IDX, '<div id="navstrip">', "</div>", inclusive=True)
    nav = rep(nav, "<a href='http://forum.imgburn.com/index.php?act=idx'>ImgBurn Support Forum</a>",
              "<a href='%s'>%s</a>" % (PAGES["index"], C.BOARD))
    extra = ""
    for label, href in crumbs:
        extra += "&nbsp;>&nbsp;" + ("<a href='%s'>%s</a>" % (href, label) if href else label)
    return nav.replace("</div>", extra + "</div>")


def finish(html):
    """Make the static copy inert the way tools/capture.py does."""
    # any remaining link into the source boards goes nowhere
    # outbound links would leave the reconstruction for today's web (as capture.py does)
    html = re.sub(r"""(href=)(['"])https?://[^'"]*\2""", r"\1\2#\2", html)
    html = re.sub(r"""(href=)(['"])index\.php[^'"]*\2""", r"\1\2#\2", html)
    html = re.sub(r"""(href=)(['"])lofiversion/[^'"]*\2""", r"\1\2#\2", html)
    html = re.sub(r"""(PopUp\(')https?://[^']*'""", r"\1#'", html)
    html = re.sub(r"""(\baction=)(['"])[^'"]*\2""", r"\1\2#\2", html)
    html = re.sub(r'(<form\b[^>]*?)\bmethod\s*=\s*(["\']?)post\2', r'\1method="get"', html, flags=re.I)
    html = re.sub(r'(<input\b[^>]*type=["\']?password["\']?[^>]*?)\sname=(["\'])[^"\']*\2', r"\1", html, flags=re.I)
    html = html.replace("http://forum.imgburn.com/", "").replace("http://forums.invisionpower.com/", "")
    for bad in ("imgburn", "ImgBurn", "invisionpower.com/uploads", "googlesyndication", "invisiongames"):
        if bad in html:
            raise ValueError("source branding left in page: " + bad)
    return html


# ------------------------------------------------------------------ index
def build_index():
    body = IDX[IDX.index('<div id="navstrip">'):IDX.index('<table cellspacing="0" id="gfooter">')]
    body = rep(body, between(IDX, '<div id="navstrip">', "</div>", inclusive=True), navstrip())

    # news / guest login strip
    body = rep(body, "<span>Today, 04:19 PM</span>", "<span>%s</span>" % C.NOW_SHORT)
    body = sub1(r"<b>ImgBurn Support Forum latest news: </b> <i><a href=\"[^\"]*\">[^<]*</a></i>",
                '<b>%s latest news: </b> <i><a href="#">%s</a></i>' % (C.BOARD, C.NEWS_TITLE), body)

    # categories: take the first real category block and its first forum row as templates
    cat_start = body.index('<br /><div class="borderwrap" style="display:none" id="fc_1">')
    cats_end = body.index("<br /><!-- Board Stats -->")
    cat_tpl = body[cat_start:body.index('<br /><div class="borderwrap" style="display:none" id="fc_5">')]
    row_re = re.compile(r"<tr> \n\t\t\t<td align=\"center\" class=\"row2\" width=\"1%\"><a id='f-.*?</td>\n\t\t</tr>", re.S)
    rows = row_re.findall(cat_tpl)
    assert rows, "forum row template not found"
    row_tpl = rows[0]
    cat_tpl = cat_tpl.replace("".join(rows) if "".join(rows) in cat_tpl else rows[0], "{ROWS}")
    for r in rows[1:]:
        cat_tpl = cat_tpl.replace(r, "")

    out = ""
    for cat in C.CATEGORIES:
        c = cat_tpl.replace("togglecategory(1,", "togglecategory(%d," % cat["id"])
        c = c.replace('id="fc_1"', 'id="fc_%d"' % cat["id"]).replace('id="fo_1"', 'id="fo_%d"' % cat["id"])
        c = c.replace('>General</a>', '>%s</a>' % cat["name"])
        rws = ""
        for f in cat["forums"]:
            r = row_tpl
            r = rep(r, "id='f-2'", "id='f-%d'" % f["id"])
            r = rep(r, '<a href="http://forum.imgburn.com/index.php?showforum=2">Announcements</a>',
                    '<a href="%s">%s</a>' % (f.get("page", "#"), f["name"]))
            r = rep(r, "Find out what's happening!", f["desc"])
            r = rep(r, '<td align="center" class="row1">4</td>', '<td align="center" class="row1">%s</td>' % f["topics"])
            r = rep(r, '<td align="center" class="row1">136</td>', '<td align="center" class="row1">%s</td>' % f["replies"])
            when, tid, title, who = f["last"]
            tpage = PAGES["topic"] if tid == C.TOPIC["id"] else "#"
            r = rep(r, 'href="http://forum.imgburn.com/index.php?showtopic=1255&amp;view=getlastpost"', 'href="%s"' % tpage)
            r = rep(r, "<span>Apr 21 2006, 03:07 AM<br />", "<span>%s<br />" % when)
            r = rep(r, "<a href='http://forum.imgburn.com/index.php?showtopic=1255&amp;view=getnewpost' "
                       "title='Go to the first unread post: ImgBurn v1.3.0.0 Released&#33;'>ImgBurn v1.3.0.0 Released!</a>",
                    "<a href='%s' title='Go to the first unread post: %s'>%s</a>" % (tpage, title, short_title(title)))
            r = rep(r, "<a href='http://forum.imgburn.com/index.php?showuser=491'>life</a>", member_link(who))
            rws += r
        out += c.replace("{ROWS}", rws)
    body = body[:cat_start] + out + body[cats_end:]

    # board statistics
    online = len(C.ACTIVE) + C.GUESTS
    total_posts = sum(int(f["topics"].replace(",", "")) + int(f["replies"].replace(",", ""))
                      for c in C.CATEGORIES for f in c["forums"])
    body = rep(body, "15,479 posts &#0124; 2,717 members", "{:,} posts &#0124; {} members".format(total_posts, C.TOTAL_MEMBERS))
    body = rep(body, "<p>8 users online</p>", "<p>%d users online</p>" % online)
    body = rep(body, "8 user(s) active in the past 15 minutes", "%d user(s) active in the past 15 minutes" % online)
    body = rep(body, "<b>6</b> guests, <b>2</b> members <b>0</b> anonymous members",
               "<b>%d</b> guests, <b>%d</b> members <b>0</b> anonymous members" % (C.GUESTS, len(C.ACTIVE)))
    names = ", \n".join("<a href='%s' title='%s'>%s</a>" % (PAGES["user"] if n == C.PROFILE["name"] else "#", t, n)
                        for n, t in C.ACTIVE)
    body = sub1(r'<div class="thin">.*?</div>', '<div class="thin">%s</div>' % names, body)

    # Today's Birthdays rows, from the IPS index of 3 May 2006 (same 2.1.5 skin)
    bday = between(IPS_IDX, '<tr>\n\t\t\t<td class="formsubtitle" colspan="2">Today\'s Birthdays</td>',
                   '\t\t</tr><tr>\n\t\t\t<td class="formsubtitle" colspan="2">Forthcoming', inclusive=False)
    bday = rep(bday, 'http://forums.invisionpower.com/style_images/1/calen.gif', 'style_images/1/calen.gif')
    bday = sub1(r"<td class=\"row2\"><b>15</b> members are celebrating their birthday today<br />.*?</td>",
                '<td class="row2"><b>%d</b> members are celebrating their birthday today<br />%s</td>' % (
                    len(C.BIRTHDAYS), ",\n".join("<a href='#'>%s</a>(<b>%d</b>)" % b for b in C.BIRTHDAYS)), bday)
    body = rep(body, "<!--IBF.WHOSCHATTING-->", "<!--IBF.WHOSCHATTING-->" + bday + "\t\t</tr>", 1)

    body = rep(body, "Our members have made a total of <b>15,479</b> posts<br />We have <b>2,717</b> registered members",
               "Our members have made a total of <b>{:,}</b> posts<br />We have <b>{}</b> registered members".format(
                   total_posts, C.TOTAL_MEMBERS))
    body = rep(body, "<a href='http://forum.imgburn.com/index.php?showuser=3109'>mavdrivr</a>", member_link(C.NEWEST))
    body = rep(body, "Most users ever online was <b>131</b> on <b>Mar 3 2006, 04:16 PM</b>",
               "Most users ever online was <b>%s</b> on <b>%s</b>" % C.RECORD)
    return shell(C.BOARD, body)


# ------------------------------------------------------------------ forum
FORUM = C.CATEGORIES[0]["forums"][1]


def forum_jump(html, selected):
    """Rewrite the real jump menu <optgroup> with our forums."""
    opts = ""
    for cat in C.CATEGORIES:
        opts += '<option value="%d">%s</option>\n' % (cat["id"], cat["name"])
        for f in cat["forums"]:
            sel = ' selected="selected"' if f["id"] == selected else ""
            opts += '<option value="%d"%s>&nbsp;&nbsp;&#0124;-- %s</option>\n' % (f["id"], sel, f["name"])
    return sub1(r'<optgroup label="Forum Jump">.*?</optgroup>', '<optgroup label="Forum Jump">' + opts + "</optgroup>", html)


def page_links(html, pages):
    html = html.replace("12 Pages <img", "%d Pages <img" % pages)
    return html.replace("topicfilter=all', 30, 351 );", "topicfilter=all', 30, %d );" % ((pages - 1) * 30 + 1))


def build_forum():
    body = SF[SF.index('<div id="navstrip">'):SF.index('<table cellspacing="0" id="gfooter">')]
    body = rep(body, between(SF, '<div id="navstrip">', "</div>", inclusive=True),
               navstrip((C.CATEGORIES[0]["name"], "#"), (FORUM["name"], PAGES["forum"])))
    body = rep(body, "&nbsp;ImgBurn Support</div></td>", "&nbsp;%s</div></td>" % FORUM["name"])
    body = page_links(body, C.FORUM_PAGES)
    body = forum_jump(body, FORUM["id"])

    entry = re.compile(r"<!-- Begin Topic Entry (\d+) -->.*?<!-- End Topic Entry \1 -->", re.S)
    entries = {m.group(1): m.group(0) for m in entry.finditer(body)}
    pinned_tpl, normal_tpl = entries["131"], entries["1176"]

    def fill(tpl, src_id, t):
        tid, title, desc, starter, replies, views, last, last_by, pinned = t
        e = tpl.replace(src_id, str(tid))
        e = sub1(r'<a id="tid-link-%d" href="[^"]*" title="This topic was started: [^"]*">[^<]*</a>' % tid,
                 '<a id="tid-link-%d" href="%s" title="This topic was started: %s">%s</a>' % (
                     tid, PAGES["topic"] if tid == C.TOPIC["id"] else "#", started.get(tid, last), title), e)
        # multi-page links (IPB 2.1: 20 posts a page; 1-4 pages listed, else 1 2 3 >> last)
        pages = (replies + 1 + 19) // 20
        mp = ""
        if pages > 1:
            shown = range(1, pages + 1) if pages <= 4 else range(1, 4)
            mp = ('&nbsp;<a href="javascript:multi_page_jump(\'#\', %d, 20 );" title="multipage jump">'
                  "<img src='style_images/1/pages_icon.gif' alt='*' border='0' /></a> " % replies)
            mp += "".join('<span class="minipagelink"><a href="#">%d</a></span>' % p for p in shown)
            if pages > 4:
                mp += '<span class="minipagelinklast"><a href="#">&raquo; %d</a></span>' % pages
        e = sub1(r"(<span id='tid-span-%d'>.*?</a></span>) ?(&nbsp;<a href=\"javascript:multi_page_jump.*?)?\n" % tid,
                 lambda mm: mm.group(1) + " " + mp + "\n", e)
        e = sub1(r"(id='tid-desc-%d'>)[^<]*(</span>)" % tid, r"\g<1>%s\2" % desc.replace("\\", "\\\\"), e)
        e = sub1(r'<a href="javascript:who_posted\(%d\);">\d+</a>' % tid, '<a href="javascript:who_posted(%d);">%d</a>' % (tid, replies), e)
        e = sub1(r"<td align=\"center\" class=\"row2\"><a href='[^']*'>[^<]*</a></td>",
                 '<td align="center" class="row2">%s</td>' % member_link(starter), e)
        e = sub1(r'<td align="center" class="row2">[\d,]+</td>', '<td align="center" class="row2">%s</td>' % views, e)
        e = sub1(r'<span class="lastaction">[^<]*<br /><a href="[^"]*">Last post by:</a> <b><a href=\'[^\']*\'>[^<]*</a></b></span>',
                 '<span class="lastaction">%s<br /><a href="%s">Last post by:</a> <b>%s</b></span>' % (
                     last, PAGES["topic"] if tid == C.TOPIC["id"] else "#", member_link(last_by)), e)
        if tid == 30806:   # locked topic
            e = e.replace("<img src='style_images/1/f_norm_no.gif' border='0'  alt='No New Posts' />",
                          "<img src='style_images/1/f_closed.gif' border='0'  alt='Closed' />")
        elif replies >= C.HOT:
            e = e.replace("<img src='style_images/1/f_norm_no.gif' border='0'  alt='No New Posts' />",
                          "<img src='style_images/1/f_hot_no.gif' border='0'  alt='No new' />")
        return e

    # topic start times (title tooltip); default to last action when unknown
    started = C.STARTED

    # the source's attachment icon belongs to that topic, not the template
    normal_tpl = sub1(r'<span id=\'tid-span-1176\'>', "<span id='tid-span-1176'>", normal_tpl)
    pinned_html = "".join(fill(pinned_tpl, "131", t) for t in C.TOPICS if t[8])
    normal_html = "".join(fill(normal_tpl, "1176", t) for t in C.TOPICS if not t[8])

    first = body.index("<!-- Begin Topic Entry 131 -->")
    last_end = body.rindex("<!-- End Topic Entry")
    last_end = body.index("-->", last_end) + 3
    middle = body[first:last_end]
    divider = between(middle, "<!-- END PINNED -->\n<tr>", "</tr>", inclusive=True)
    body = body[:first] + pinned_html + divider + normal_html + body[last_end:]
    return shell("%s -> %s" % (C.BOARD, FORUM["name"]), body)


# ------------------------------------------------------------------ topic
def emoticon(name):
    src = re.search(r'<img src="http://images\.xbox-scene\.com/forums/style_emoticons/default/smile\.gif" '
                    r'style="vertical-align:middle" emoid=":\)" border="0" alt="smile\.gif" />', XS).group(0)
    emoid = {"smile": ":)", "biggrin": ":D"}[name]
    return (src.replace("http://images.xbox-scene.com/forums/", "")
               .replace("smile.gif", name + ".gif").replace('emoid=":)"', 'emoid="%s"' % emoid))


def post_html(text):
    if text.startswith("QUOTE:"):
        q, rest = text.split("|", 1)
        _, pid, date, name, quoted = q.split(":", 4)
        tpl = re.search(r"<!--quoteo\(post=13824:.*?<!--QuoteEnd--></div><!--QuoteEEnd-->", ST_QUOTE, re.S).group(0)
        inner = between(tpl, "<!--quotec-->", "<!--QuoteEnd-->")
        tpl = tpl.replace(inner, "<br />" + quoted + "<br />")
        tpl = tpl.replace("post=13824:date=Apr 13 2006, 02&#58;17 PM:name=A_T",
                          "post=%s:date=%s:name=%s" % (pid, date, name))
        tpl = tpl.replace("QUOTE(A_T &#064; Apr 13 2006, 02&#58;17 PM)", "QUOTE(%s &#064; %s)" % (name, date))
        tpl = tpl.replace("pid=13824", "pid=" + pid)
        text = tpl + "<br />" + rest
    return re.sub(r"EMO:(\w+)", lambda m: emoticon(m.group(1)), text)


def build_topic():
    body = ST[ST.index('<div id="navstrip">'):ST.index('<table cellspacing="0" id="gfooter">')]
    body = rep(body, between(ST, '<div id="navstrip">', "</div>", inclusive=True),
               navstrip((C.CATEGORIES[0]["name"], "#"), (FORUM["name"], PAGES["forum"])))
    # the source forum's custom "Information" rules box is not part of the default board
    body = rep(body, between(body, "<!-- Show FAQ/Forum Rules -->", "<!-- End FAQ/Forum Rules -->", inclusive=True), "")
    tid = str(C.TOPIC["id"])
    body = body.replace("f=15&amp;t=1160", "f=%d&amp;t=%s" % (FORUM["id"], tid)).replace("f=15", "f=%d" % FORUM["id"])
    body = body.replace("tid=1160", "tid=" + tid).replace("showtopic=1160", "showtopic=" + tid).replace("fid=15", "fid=%d" % FORUM["id"])
    body = rep(body, "&nbsp;<b>Taiyo Yuden 16x DVD+R [YUDEN000-T03-00]</b></div>",
               "&nbsp;<b>%s</b>, %s</div>" % (C.TOPIC["title"], C.TOPIC["desc"]))
    body = rep(body, "style='font-weight: bold;text-decoration:none'>Drives &amp; Media</a>",
               "style='font-weight: bold;text-decoration:none'>%s</a>" % FORUM["name"])
    body = forum_jump(body, FORUM["id"])

    blocks = re.findall(r"<!--Begin Msg Number (\d+)-->(.*?</script>)", body, re.S)
    first_id, tpl = blocks[0]
    tpl = "<!--Begin Msg Number %s-->" % first_id + tpl
    posts = ""
    online = {n for n, _ in C.ACTIVE}
    for n, (pid, who, when, text) in enumerate(C.POSTS, 1):
        m = C.MEMBERS[who]
        p = tpl.replace(first_id, str(pid))
        p = rep(p, "<a href='http://forum.imgburn.com/index.php?showuser=1'>LIGHTNING UK&#33;</a>", member_link(who))
        p = rep(p, "style='padding-bottom:2px' /> Mar 26 2006, 10:56 AM</span>", "style='padding-bottom:2px' /> %s</span>" % when)
        p = rep(p, 'return false;">#1</a>', 'return false;">#%d</a>' % n)
        p = p.replace('class="post2"', 'class="%s"' % ("post2" if n % 2 else "post1"))
        details = "%s<br />\n        \t\t%s<br /><br />\n        \t\tGroup: %s<br />\n        \t\tPosts: %s<br />\n        \t\tJoined: %s<br />\n%s        \t\tMember No.: %s<br /><br />" % (
            m["title"], "<img src='style_images/1/pip.gif' border='0'  alt='*' />" * m["pips"], m["group"], m["posts"],
            m["joined"], ("        \t\tFrom: %s<br />\n" % m["where"]) if m["where"] else "", "{:,}".format(m["id"]))
        p = sub1(r"Author of ImgBurn<br />.*?Member No\.: 1<br /><br />", details.replace("\\", "\\\\"), p)
        p = sub1(r"(<div class=\"postcolor\" id='post-\d+'>).*?(</div>\n\t\t\t<!--IBF.ATTACHMENT_)",
                 lambda mm: mm.group(1) + post_html(text) + mm.group(2), p)
        if who in online:
            p = rep(p, "<img src='style_images/1/p_offline.gif' border='0'  alt='User is offline' />", ONLINE_IMG)
        posts += p
    start = body.index("<!--Begin Msg Number %s-->" % first_id)
    end = body.index("<!-- END TABLE -->")
    body = body[:start] + posts + body[end:]

    # Fast Reply: IPB fills these two placeholders when the viewer may reply
    btn = re.search(r"<a href=\"javascript:ShowHide\('qr_open','qr_closed'\);\" title=\"Open Fast Reply Window\" accesskey=\"f\">"
                    r"<img src='style_images/1/t_qr.gif' border='0'  alt='Fast Reply' /></a>", QR).group(0)
    box = between(QR, "<script type=\"text/javascript\">\n<!--\n\tvar emowindow", "</form>\n</div>\n", inclusive=True)
    box = box.replace('style="display: none; position: relative;"', 'style="display: show; position: relative;"')
    box = box.replace('value="20"', 'value="%d"' % FORUM["id"]).replace('value="3525"', 'value="%s"' % tid)
    box = box.replace('emo_pop(){\n\temowindow = window.open("index.php?act=legends&amp;CODE=emoticons&amp;s="', 'emo_pop(){\n\temowindow = window.open("#"')
    body = rep(body, "<!--IBF.QUICK_REPLY_CLOSED-->", btn)
    body = rep(body, "<!--IBF.QUICK_REPLY_OPEN-->", box)
    return shell("%s - %s" % (C.TOPIC["title"], C.BOARD), body)


# ------------------------------------------------------------------ profile
def build_user():
    P, m = C.PROFILE, C.MEMBERS[C.PROFILE["name"]]
    body = PROF[PROF.index('<div id="navstrip">'):PROF.index('<table cellspacing="0" id="gfooter">')]
    body = rep(body, between(body, '<div id="navstrip">', "</div>", inclusive=True), navstrip(("Viewing Profile", None)))
    body = body.replace("http://forums.invisionpower.com/style_images/", "style_images/")
    body = re.sub(r"<!--TASK-->.*?<!--ETASK-->", "", body, flags=re.S)
    body = rep(body, "Viewing Profile: Furnace", "Viewing Profile: " + P["name"])
    body = rep(body, '<div id="profilename">Furnace</div>', '<div id="profilename">%s</div>' % P["name"])
    body = sub1(r"<div>Spam Happy</div>\n\t\t\t\t<div>(<img[^>]*>)+</div>",
                "<div>%s</div>\n\t\t\t\t<div>%s</div>" % (m["title"], '<img src="style_images/1/pip.gif" border=\'0\'  alt=\'*\' />' * m["pips"]), body)
    body = rep(body, "Joined: 13-February 02", "Joined: " + m["joined"])
    body = sub1(r"(<b>User's local time</b></td>\s*<td class=\"row1\">)[^<]*", r"\g<1>" + P["local_time"], body)
    body = sub1(r"(<td width=\"70%\" class=\"row1\"><b>)764(</b>\s*<br />\( )0\.5 posts per day / 0\.07%",
                r"\g<1>%s\g<2>%s posts per day / %s%%" % (m["posts"], P["per_day"], P["pct"]), body)
    fname, fposts, fpct = P["most_active"]
    body = sub1(r'(<b>Most active in</b></td>\s*<td class="row1">)<a href="[^"]*"><b>[^<]*</b></a><br />\([^)]*\)',
                lambda mm: mm.group(1) + '<a href="%s"><b>%s</b></a><br />( %s posts / %s%% of this member\'s active posts )' % (
                    PAGES["forum"], fname, fposts, fpct), body)
    body = sub1(r"(<b>Last Active</b></td>\s*<td class=\"row1\">)[^<]*", r"\g<1>" + P["last_active"], body)
    body = sub1(r"(alt='AIM' /></td>\s*<td width=\"99%\" class=\"row2\">)<i>No Information</i>|(alt='AIM' /></td>\s*<td width=\"99%\" class=\"row2\">)[^<]*",
                lambda mm: (mm.group(1) or mm.group(2)) + P["aim"], body)
    for label in ("ICQ", "MSN", "Yahoo"):
        body = sub1(r"(alt='%s' /></td>\s*<td width=\"99%%\" class=\"row2\">)(?!<i>)[^<]*" % label,
                    r"\g<1><i>No Information</i>", body) if re.search(
            r"alt='%s' /></td>\s*<td width=\"99%%\" class=\"row2\">(?!<i>)[^<]" % label, body) else body
    body = re.sub(r"&amp;MID=129", "&amp;MID=%d" % m["id"], body)
    body = re.sub(r"mid=129|showuser=129|history\(129\)", lambda mm: mm.group(0).replace("129", str(m["id"])), body)
    # IP.Blog is a separate product; drop its row
    body = sub1(r"<tr>\n\t\t\t\t\t\t<td class=\"row2\" width=\"30%\" valign=\"top\"><b>My Blog</b></td>.*?</tr>", "", body)
    body = sub1(r"(<b>Home Page</b></td>\s*<td width=\"70%\" class=\"row1\">)<a[^>]*>[^<]*</a>", r"\g<1><i>No Information</i>", body)
    body = sub1(r"(<b>Location</b></td>\s*<td class=\"row1\">)[^<]*", r"\g<1>" + m["where"], body)
    body = sub1(r"(<b>Interests</b></td>\s*<td class=\"row1\">)<i>No Information</i>", r"\g<1>" + P["interests"], body)
    body = sub1(r'<div class="signature">.*?</div>', '<div class="signature">%s</div>' % C.SIGNATURES[P["name"]], body)
    return shell("Viewing Profile", body)


# ------------------------------------------------------------------ main
def main():
    pages = {"index": build_index(), "forum": build_forum(), "topic": build_topic(), "user": build_user()}
    if os.path.isdir(OUT):
        for f in os.listdir(OUT):
            p = os.path.join(OUT, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    for key, html in pages.items():
        with open(os.path.join(OUT, PAGES[key]), "w", encoding="latin-1", errors="xmlcharrefreplace") as fh:
            fh.write(html)
    # assets keep their original paths
    for root, _, files in os.walk(ASSETS):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(OUT, os.path.relpath(src, ASSETS))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
    print("wrote", ", ".join(PAGES.values()), "to", OUT)


if __name__ == "__main__":
    main()
