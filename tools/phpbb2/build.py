#!/usr/bin/env python3
"""Render the Pixel Arena phpBB 2.0.x exhibit from the real subSilver templates.

Templates in ./templates are copied verbatim from phpBB 2.0.23 (GPL), except
index_body.tpl, which carries the Birthday MOD template edit. Theme values,
language strings and output formats follow the 2.0.23 source.
"""
import math
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, "templates")
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "exhibits", "phpbb"))

# phpbb_themes row 1 (install/schemas/mysql_basic.sql)
THEME = {
    "T_HEAD_STYLESHEET": "subSilver.css", "T_BODY_BACKGROUND": "",
    "T_BODY_BGCOLOR": "#E5E5E5", "T_BODY_TEXT": "#000000", "T_BODY_LINK": "#006699",
    "T_BODY_VLINK": "#5493B4", "T_BODY_ALINK": "#", "T_BODY_HLINK": "#DD6900",
    "T_TR_COLOR1": "#EFEFEF", "T_TR_COLOR2": "#DEE3E7", "T_TR_COLOR3": "#D1D7DC",
    "T_TH_COLOR1": "#98AAB1", "T_TH_COLOR2": "#006699", "T_TH_COLOR3": "#FFFFFF",
    "T_TH_CLASS1": "cellpic1.gif", "T_TH_CLASS2": "cellpic3.gif", "T_TH_CLASS3": "cellpic2.jpg",
    "T_TD_COLOR1": "#FAFAFA", "T_TD_COLOR2": "#FFFFFF", "T_TD_COLOR3": "#",
    "T_TD_CLASS1": "row1", "T_TD_CLASS2": "row2",
    "T_FONTFACE1": "Verdana, Arial, Helvetica, sans-serif", "T_FONTFACE2": "Trebuchet MS",
    "T_FONTFACE3": "Courier, 'Courier New', sans-serif",
    "T_FONTSIZE1": "10", "T_FONTSIZE2": "11", "T_FONTSIZE3": "12",
    "T_FONTCOLOR1": "#444444", "T_FONTCOLOR2": "#006600", "T_FONTCOLOR3": "#FFA34F",
}

IMG = "templates/subSilver/images"
SITENAME = "Pixel Arena Forums"
NOW = "Tue Oct 17, 2006 3:22 pm"

FORUMS = [
    # id, cat, name, desc, topics, posts, moderators, last_time, last_user, last_post_id
    (1, "Pixel Arena", "General Discussion",
     "Site news, introductions, and anything that doesn't fit anywhere else.",
     1248, 18342, ["Kestrel"], "Tue Oct 17, 2006 1:42 pm", "Zane", 214377),
    (2, "Gaming", "PC Gaming",
     "Patches, mods, LAN parties and the eternal framerate complaints.",
     2903, 41560, ["Kestrel"], "Tue Oct 17, 2006 2:14 pm", "Kestrel", 214391),
    (3, "Gaming", "Console Gaming",
     "Xbox 360, PS2, GameCube, handhelds -- and whatever is launching next month.",
     2114, 33890, ["Kestrel"], "Tue Oct 17, 2006 3:09 pm", "NorthernLight", 214402),
    (4, "Gaming", "Hardware",
     "Building, upgrading and overclocking. Post your specs before asking for help.",
     1675, 22408, ["Kestrel", "Trip_Wire"], "Tue Oct 17, 2006 9:07 am", "Trip_Wire", 214322),
    (5, "Everything Else", "Off Topic",
     "Movies, music, desktops and everything else. Keep it civil.",
     3320, 58774, ["QuakeWidow"], "Tue Oct 17, 2006 3:18 pm", "MoogleKnight", 214405),
]
TOTAL_POSTS = sum(f[5] for f in FORUMS)
TOTAL_USERS = 4812

USERS = {
    "Zane": 2, "Kestrel": 7, "NorthernLight": 1490, "MoogleKnight": 1188,
    "ctrl_alt_defeat": 2311, "QuakeWidow": 61, "LANwolf": 845, "Trip_Wire": 133,
    "Vectrex_Kid": 4917, "dropbear": 3020, "PolygonPete": 1752, "sk8rgrl88": 3388,
}


def u(name):
    return "profile.html?mode=viewprofile&amp;u=%d" % USERS[name]


def ulink(name, cls=None):
    c = ' class="%s"' % cls if cls else ""
    return '<a href="%s"%s>%s</a>' % (u(name), c, name)


# --- tiny phpBB2 template engine ---------------------------------------------

BLOCK = re.compile(r"<!-- BEGIN (\w+) -->(.*?)<!-- END \1 -->", re.S)
VAR = re.compile(r"\{([A-Za-z0-9_.]+)\}")


def render_level(text, path, data):
    def block(m):
        items = data.get(m.group(1))
        if not isinstance(items, list):
            return ""
        return "".join(render_level(m.group(2), path + [m.group(1)], it) for it in items)

    text = BLOCK.sub(block, text)
    prefix = ".".join(path) + "." if path else ""

    def var(m):
        key = m.group(1)
        if prefix:
            if key.startswith(prefix) and "." not in key[len(prefix):] and key[len(prefix):] in data:
                return str(data[key[len(prefix):]])
        elif "." not in key and key in data:
            return str(data[key])
        return m.group(0)

    return VAR.sub(var, text)


def render(name, data):
    out = render_level(open(os.path.join(TPL, name), encoding="latin-1").read(), [], data)
    return VAR.sub("", out)  # unset template variables render as empty, as in phpBB


# --- shared page furniture ---------------------------------------------------

def header(page_title):
    d = dict(THEME)
    d.update({
        "S_CONTENT_DIRECTION": "ltr", "S_CONTENT_ENCODING": "iso-8859-1",
        "SITENAME": SITENAME, "PAGE_TITLE": page_title,
        "SITE_DESCRIPTION": "where your framerate matters more than your social life",
        "U_INDEX": "index.html", "L_INDEX": "%s Forum Index" % SITENAME,
        "U_FAQ": "#", "L_FAQ": "FAQ", "U_SEARCH": "#", "L_SEARCH": "Search",
        "U_MEMBERLIST": "#", "L_MEMBERLIST": "Memberlist",
        "U_GROUP_CP": "#", "L_USERGROUPS": "Usergroups",
        "U_REGISTER": "#", "L_REGISTER": "Register",
        "U_PROFILE": "#", "L_PROFILE": "Profile",
        "U_PRIVATEMSGS": "#", "PRIVATE_MESSAGE_INFO": "Log in to check your private messages",
        "U_LOGIN_LOGOUT": "index.html#login", "L_LOGIN_LOGOUT": "Log in",
        "switch_user_logged_out": [{}],
    })
    html = render("overall_header.tpl", d)
    bar = ('<div style="background:#23466C;color:#FFFFFF;font:11px Verdana,Arial,sans-serif;'
           'padding:4px 10px;">&larr; <a href="../../index.html" target="_top" '
           'style="color:#FFFFFF;">Return to PHP Web Museum</a></div>\n')
    return html.replace('<a name="top"></a>', bar + '<a name="top"></a>', 1)


def footer():
    return render("overall_footer.tpl", {})


def jumpbox(selected=None):
    opts = ['<option value="-1">Select a forum</option>']
    last_cat = None
    for f in FORUMS:
        if f[1] != last_cat:
            opts += ['<option value="-1">&nbsp;</option>', '<option value="-1">%s</option>' % f[1],
                     '<option value="-1">----------------</option>']
            last_cat = f[1]
        sel = ' selected="selected"' if f[0] == selected else ""
        opts.append('<option value="%d"%s>%s</option>' % (f[0], sel, f[2]))
    select = ('<select name="f" onchange="if(this.options[this.selectedIndex].value != -1)'
              '{ forms[\'jumpbox\'].submit() }">' + "".join(opts) + "</select>")
    return render("jumpbox.tpl", {"S_JUMPBOX_ACTION": "viewforum.html", "L_JUMP_TO": "Jump to",
                                  "S_JUMPBOX_SELECT": select, "L_GO": "Go"})


def static_forms(html):
    # python http.server cannot answer POST; also keeps typed passwords out of URLs
    html = html.replace('method="post"', 'method="get"')
    return html.replace('type="password" name="password"', 'type="password"')


def write(name, html):
    html = static_forms(html)
    html.encode("ascii")  # page is declared iso-8859-1; content is kept 7-bit like most 2006 posts
    with open(os.path.join(OUT, name), "w", encoding="ascii", newline="\n") as fh:
        fh.write(html)


def latest_reply(post_id):
    return ('<a href="viewtopic.html?p=%d#%d"><img src="%s/icon_latest_reply.gif" border="0" '
            'alt="View latest post" title="View latest post" /></a>' % (post_id, post_id, IMG))


def pagination(total_pages, on_page, base):
    def link(i):
        return '<a href="%s">%d</a>' % (base, i) if i != on_page else "<b>%d</b>" % i
    if total_pages <= 1:
        return ""
    s = ""
    if total_pages > 10:
        s = ", ".join(link(i) for i in range(1, 4))
        if 1 < on_page < total_pages:
            start = max(4, on_page - 1)
            end = min(total_pages - 3, on_page + 1)
            s += " ... " if start > 4 else ", "
            s += ", ".join(link(i) for i in range(start, end + 1))
            s += " ... " if end < total_pages - 3 else ", "
        else:
            s += " ... "
        s += ", ".join(link(i) for i in range(total_pages - 2, total_pages + 1))
    else:
        s = ", ".join(link(i) for i in range(1, total_pages + 1))
    if on_page > 1:
        s = ' <a href="%s">Previous</a>&nbsp;&nbsp;' % base + s
    if on_page < total_pages:
        s += '&nbsp;&nbsp;<a href="%s">Next</a>' % base
    return "Goto page " + s


SMILIES = {":D": ("icon_biggrin.gif", "Very Happy"), ":?": ("icon_confused.gif", "Confused"),
           ":roll:": ("icon_rolleyes.gif", "Rolling Eyes"), ":)": ("icon_smile.gif", "Smile"),
           ";)": ("icon_wink.gif", "Wink"), ":lol:": ("icon_lol.gif", "Laughing")}


def bbcode(text):
    text = text.replace("\n", "<br />")
    for code, (img, alt) in sorted(SMILIES.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(" " + code, ' <img src="images/smiles/%s" alt="%s" border="0" />' % (img, alt))

    def quote(m):
        return ('</span><table width="90%%" cellspacing="1" cellpadding="3" border="0" align="center">'
                '<tr> \n\t  <td><span class="genmed"><b>%s wrote:</b></span></td>\n\t</tr>\n\t<tr>\n'
                '\t  <td class="quote">%s</td>\n\t</tr>\n</table>\n<span class="postbody">'
                % (m.group(1), m.group(2)))
    text = re.sub(r'\[quote="([^"]+)"\](.*?)\[/quote\](<br />)?', quote, text, flags=re.S)
    text = re.sub(r"\[url=([^\]]+)\](.*?)\[/url\]",
                  r'<a href="\1" target="_blank" class="postlink">\2</a>', text)
    return text


# --- avatars (uploaded 64x64 pixel-art GIFs, hashed filenames as phpBB stored them) ---

SPRITES = {
    "13945834114536c6b2a7e83.gif": ("#9CC3E6", {"b": "#7A4A23", "o": "#D9822B", "k": "#1E1E1E", "y": "#F2C230"}, [
        "................", "................", ".......bbb......", "......bbbbo.....",
        ".....bbkbbby....", ".....bbbbbbyy...", "....bbbbbbb.....", "...bbbbbbbbb....",
        "..bbbobbbbbbb...", ".bbboo.bbbbbbb..", "bbbo....bbbbbbb.", "........bb..bb..",
        "........b....b..", "................", "................", "................"]),
    "17220558484534f0e1b9c12.gif": ("#4B2C6E", {"g": "#B9BDC4", "d": "#6D727A", "k": "#111111", "r": "#C0392B"}, [
        "......rrr.......", ".....rrrrr......", "....rr.r........", "....gggggg......",
        "...gggggggg.....", "..ggggggggggg...", "..gddddddddg....", "..gkkkkkkkkg....",
        "..gddddddddg....", "..gggggggggg....", "..gdgdgdgdgg....", "..gggggggggg....",
        "...gggggggg.....", "....dddddd......", "................", "................"]),
    "203816722245361a9d5f8b0.gif": ("#101010", {"w": "#EDEDED", "k": "#101010", "g": "#9A9A9A"}, [
        "................", ".....wwwwww.....", "....wwwwwwww....", "...wwwwwwwwww...",
        "...wwwwwwwwww...", "...wkkwwwwkkw...", "...wkkwwwwkkw...", "...wwwwkkwwww...",
        "....wwwwwwww....", ".....wgwgwgw....", ".....wwwwwww....", "......wgwgw.....",
        "................", "................", "................", "................"]),
}
AVATAR = {"Kestrel": "13945834114536c6b2a7e83.gif", "MoogleKnight": "17220558484534f0e1b9c12.gif",
          "ctrl_alt_defeat": "203816722245361a9d5f8b0.gif"}


def make_avatars():
    os.makedirs(os.path.join(OUT, "images", "avatars"), exist_ok=True)
    for fname, (bg, pal, rows) in SPRITES.items():
        im = Image.new("RGB", (16, 16), bg)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in pal:
                    im.putpixel((x, y), Image.new("RGB", (1, 1), pal[ch]).getpixel((0, 0)))
        im = im.resize((64, 64), Image.NEAREST).convert("P", palette=Image.ADAPTIVE, colors=16)
        im.save(os.path.join(OUT, "images", "avatars", fname))


def avatar_img(name):
    return '<img src="images/avatars/%s" alt="" border="0" />' % AVATAR[name] if name in AVATAR else ""


# --- index.html --------------------------------------------------------------

def build_index():
    catrows, cats = [], {}
    for f in FORUMS:
        if f[1] not in cats:
            cats[f[1]] = {"U_VIEWCAT": "index.html", "CAT_DESC": f[1], "forumrow": []}
            catrows.append(cats[f[1]])
        mods = ", ".join(ulink(m) for m in f[6])
        cats[f[1]]["forumrow"].append({
            "FORUM_FOLDER_IMG": IMG + "/folder_big.gif", "L_FORUM_FOLDER_ALT": "No new posts",
            "U_VIEWFORUM": "viewforum.html?f=%d" % f[0], "FORUM_NAME": f[2], "FORUM_DESC": f[3],
            "L_MODERATOR": "Moderators:" if len(f[6]) > 1 else "Moderator:", "MODERATORS": mods,
            "TOPICS": f[4], "POSTS": f[5],
            "LAST_POST": "%s<br />%s %s" % (f[7], ulink(f[8]), latest_reply(f[9])),
        })
    d = {
        "CURRENT_TIME": "The time now is " + NOW, "U_INDEX": "index.html",
        "L_INDEX": "%s Forum Index" % SITENAME,
        "U_SEARCH_UNANSWERED": "#", "L_SEARCH_UNANSWERED": "View unanswered posts",
        "L_FORUM": "Forum", "L_TOPICS": "Topics", "L_POSTS": "Posts", "L_LASTPOST": "Last Post",
        "catrow": catrows, "S_TIMEZONE": "All times are GMT",
        "U_VIEWONLINE": "#", "L_WHO_IS_ONLINE": "Who is Online",
        "TOTAL_POSTS": "Our users have posted a total of <b>%d</b> articles" % TOTAL_POSTS,
        "TOTAL_USERS": "We have <b>%d</b> registered users" % TOTAL_USERS,
        "NEWEST_USER": "The newest registered user is <b>%s</b>" % ulink("Vectrex_Kid"),
        "TOTAL_USERS_ONLINE": "In total there are <b>7</b> users online :: 2 Registered, 0 Hidden and 5 Guests",
        "L_WHOSONLINE_ADMIN": '<span style="color:#FFA34F">Administrator</span>',
        "L_WHOSONLINE_MOD": '<span style="color:#006600">Moderator</span>',
        "RECORD_USERS": "Most users ever online was <b>142</b> on Mon Aug 14, 2006 4:51 pm",
        "LOGGED_IN_USER_LIST": "Registered Users: %s, %s" % (ulink("ctrl_alt_defeat"), ulink("LANwolf")),
        "L_WHOSBIRTHDAY_TODAY": "Congratulations to: <b>%s (19), %s (24)</b>"
                                % (ulink("MoogleKnight"), ulink("LANwolf")),
        "L_WHOSBIRTHDAY_WEEK": "Users with a birthday within the next 7 days: %s (31), %s (22)"
                               % (ulink("Trip_Wire"), ulink("sk8rgrl88")),
        "L_ONLINE_EXPLAIN": "This data is based on users active over the past five minutes",
        "switch_user_logged_out": [{"switch_allow_autologin": [{}]}],
        "S_LOGIN_ACTION": "index.html", "L_LOGIN_LOGOUT": "Log in",
        "L_USERNAME": "Username", "L_PASSWORD": "Password",
        "L_AUTO_LOGIN": "Log me on automatically each visit", "L_LOGIN": "Log in",
        "L_NEW_POSTS": "New posts", "L_NO_NEW_POSTS": "No new posts", "L_FORUM_LOCKED": "Forum is locked",
    }
    write("index.html", header("Index") + render("index_body.tpl", d) + footer())


# --- viewforum.html (Console Gaming, page 1) ----------------------------------

TOPICS = [
    # type, title, author, replies, views, last_time, last_user, last_post_id, poll, locked
    ("announce", "Forum rules -- read before posting", "Zane", 0, 4512,
     "Sat Mar 19, 2005 2:10 pm", "Zane", 61204, False, True),
    ("sticky", "Release dates: Holiday 2006", "Kestrel", 47, 3906,
     "Mon Oct 16, 2006 6:02 pm", "Kestrel", 214288, False, False),
    ("sticky", "Post your Gamertag / Friend Codes here", "Kestrel", 132, 5871,
     "Sun Oct 15, 2006 4:31 pm", "dropbear", 214011, False, False),
    ("normal", "Official Nintendo Wii discussion", "MoogleKnight", 214, 9877,
     "Tue Oct 17, 2006 3:09 pm", "NorthernLight", 214402, True, False),
    ("normal", "PS3 launch -- who's actually queuing?", "LANwolf", 88, 3120,
     "Tue Oct 17, 2006 2:47 pm", "QuakeWidow", 214399, False, False),
    ("normal", "Okami -- anyone picked it up?", "Kestrel", 31, 1288,
     "Tue Oct 17, 2006 11:20 am", "MoogleKnight", 214361, False, False),
    ("normal", "Gears of War hype thread", "ctrl_alt_defeat", 57, 2214,
     "Tue Oct 17, 2006 10:04 am", "LANwolf", 214340, False, False),
    ("normal", "Best DS games so far?", "NorthernLight", 42, 1630,
     "Mon Oct 16, 2006 11:51 pm", "Vectrex_Kid", 214305, False, False),
    ("normal", "Twilight Princess -- really launching with the Wii this time?", "QuakeWidow", 19, 902,
     "Mon Oct 16, 2006 9:30 pm", "Kestrel", 214297, False, False),
    ("normal", "Xbox Live Gold: worth it?", "dropbear", 14, 455,
     "Mon Oct 16, 2006 7:12 pm", "ctrl_alt_defeat", 214291, False, False),
    ("normal", "Is anyone still playing their PS2?", "PolygonPete", 23, 811,
     "Mon Oct 16, 2006 4:45 pm", "Zane", 214270, False, False),
    ("normal", "Sold my GameCube... regretting it already", "sk8rgrl88", 9, 288,
     "Mon Oct 16, 2006 1:18 pm", "MoogleKnight", 214251, False, False),
    ("normal", "Guitar Hero II -- November can't come soon enough", "LANwolf", 26, 1022,
     "Mon Oct 16, 2006 12:03 pm", "PolygonPete", 214244, False, False),
    ("normal", "Burnout Revenge vs. Most Wanted", "dropbear", 11, 390,
     "Sun Oct 15, 2006 10:40 pm", "QuakeWidow", 214198, False, False),
    ("normal", "Dead Rising: can't read the text on my TV", "NorthernLight", 18, 744,
     "Sun Oct 15, 2006 7:26 pm", "sk8rgrl88", 214177, False, False),
    ("normal", "360 wireless controller keeps disconnecting", "PolygonPete", 7, 214,
     "Sun Oct 15, 2006 3:02 pm", "Trip_Wire", 214150, False, False),
    ("normal", "LocoRoco is the happiest game ever made", "MoogleKnight", 12, 401,
     "Sun Oct 15, 2006 11:47 am", "Kestrel", 214132, False, False),
    ("normal", "Second controller for Smash Bros -- regular pad or Wavebird?", "Vectrex_Kid", 5, 166,
     "Sat Oct 14, 2006 9:58 pm", "LANwolf", 214090, False, False),
    ("normal", "Best console of this generation?", "QuakeWidow", 76, 2650,
     "Sat Oct 14, 2006 6:30 pm", "dropbear", 214071, True, False),
    ("normal", "Anyone importing Japanese games?", "ctrl_alt_defeat", 3, 121,
     "Sat Oct 14, 2006 2:15 pm", "NorthernLight", 214052, False, False),
]


def goto_page(replies, posts_per_page=15):
    if replies + 1 <= posts_per_page:
        return ""
    total = math.ceil((replies + 1) / posts_per_page)
    pages = [1] + list(range(total - 3, total + 1)) if total > 4 else list(range(1, total + 1))
    links = ['<a href="viewtopic.html">%d</a>' % p for p in pages]
    body = links[0] + " ... " + ", ".join(links[1:]) if total > 4 else ", ".join(links)
    return (' [ <img src="%s/icon_minipost.gif" alt="Goto page" title="Goto page" />Goto page: %s ] '
            % (IMG, body))


def build_viewforum():
    rows = []
    for i, t in enumerate(TOPICS):
        kind, title, author, replies, views, ltime, luser, lpid, poll, locked = t
        if kind == "announce":
            folder, alt, prefix = "folder_announce.gif", "Announcement", "<b>Announcement:</b> "
        elif kind == "sticky":
            folder, alt, prefix = "folder_sticky.gif", "Sticky", "<b>Sticky:</b> "
        elif locked:
            folder, alt, prefix = "folder_lock.gif", "This topic is locked, you cannot edit posts or make replies", ""
        elif replies >= 25:
            folder, alt, prefix = "folder_hot.gif", "No new posts [ Popular ]", ""
        else:
            folder, alt, prefix = "folder.gif", "No new posts", ""
        if poll:
            prefix += "<b>[ Poll ]</b> "
        rows.append({
            "TOPIC_FOLDER_IMG": "%s/%s" % (IMG, folder), "L_TOPIC_FOLDER_ALT": alt,
            "TOPIC_TYPE": prefix, "U_VIEW_TOPIC": "viewtopic.html?t=%d" % (48210 - i * 37),
            "TOPIC_TITLE": title, "GOTO_PAGE": goto_page(replies),
            "REPLIES": replies, "TOPIC_AUTHOR": ulink(author), "VIEWS": views,
            "LAST_POST_TIME": ltime, "LAST_POST_AUTHOR": ulink(luser), "LAST_POST_IMG": latest_reply(lpid),
        })
    days = ('<select name="topicdays"><option value="0" selected="selected">All Topics</option>'
            '<option value="1">1 Day</option><option value="7">7 Days</option><option value="14">2 Weeks</option>'
            '<option value="30">1 Month</option><option value="90">3 Months</option>'
            '<option value="180">6 Months</option><option value="364">1 Year</option></select>')
    auth = "".join("You <b>cannot</b> %s in this forum<br />" % s for s in
                   ["post new topics", "reply to topics", "edit your posts", "delete your posts", "vote in polls"])
    total_pages = math.ceil(2114 / 20)
    d = {
        "S_POST_DAYS_ACTION": "viewforum.html", "U_VIEW_FORUM": "viewforum.html?f=3",
        "FORUM_NAME": "Console Gaming", "L_MODERATOR": "Moderator", "MODERATORS": ulink("Kestrel"),
        "LOGGED_IN_USER_LIST": "Users browsing this forum: %s, %s" % (ulink("ctrl_alt_defeat"), ulink("LANwolf")),
        "PAGINATION": pagination(total_pages, 1, "viewforum.html?f=3"),
        "U_POST_NEW_TOPIC": "#", "POST_IMG": IMG + "/lang_english/post.gif", "L_POST_NEW_TOPIC": "Post new topic",
        "U_INDEX": "index.html", "L_INDEX": "%s Forum Index" % SITENAME,
        "U_MARK_READ": "#", "L_MARK_TOPICS_READ": "Mark all topics read",
        "L_TOPICS": "Topics", "L_REPLIES": "Replies", "L_AUTHOR": "Author", "L_VIEWS": "Views",
        "L_LASTPOST": "Last Post", "topicrow": rows,
        "L_DISPLAY_TOPICS": "Display topics from previous", "S_SELECT_TOPIC_DAYS": days, "L_GO": "Go",
        "S_TIMEZONE": "All times are GMT", "PAGE_NUMBER": "Page <b>1</b> of <b>%d</b>" % total_pages,
        "JUMPBOX": jumpbox(3),
        "FOLDER_NEW_IMG": IMG + "/folder_new.gif", "L_NEW_POSTS": "New posts",
        "FOLDER_IMG": IMG + "/folder.gif", "L_NO_NEW_POSTS": "No new posts",
        "FOLDER_ANNOUNCE_IMG": IMG + "/folder_announce.gif", "L_ANNOUNCEMENT": "Announcement",
        "FOLDER_HOT_NEW_IMG": IMG + "/folder_new_hot.gif", "L_NEW_POSTS_HOT": "New posts [ Popular ]",
        "FOLDER_HOT_IMG": IMG + "/folder_hot.gif", "L_NO_NEW_POSTS_HOT": "No new posts [ Popular ]",
        "FOLDER_STICKY_IMG": IMG + "/folder_sticky.gif", "L_STICKY": "Sticky",
        "FOLDER_LOCKED_NEW_IMG": IMG + "/folder_lock_new.gif", "L_NEW_POSTS_LOCKED": "New posts [ Locked ]",
        "FOLDER_LOCKED_IMG": IMG + "/folder_lock.gif", "L_NO_NEW_POSTS_LOCKED": "No new posts [ Locked ]",
        "S_AUTH_LIST": auth,
    }
    write("viewforum.html", header("View Forum - Console Gaming") + render("viewforum_body.tpl", d) + footer())


# --- viewtopic.html (Wii thread, last page) -----------------------------------

POSTERS = {
    # name: rank, joined, posts, location, sig, contact buttons
    "MoogleKnight": ("Veteran", "02 Jun 2004", 1944, "Austin, TX",
                     "Now playing: Okami, Kingdom Hearts II", ["www", "aim", "msn", "icq"]),
    "Kestrel": ("Moderator", "11 Jul 2003", 7431, "Columbus, OH",
                'Please read the [url=viewtopic.html]forum rules[/url] before posting. Seriously.', ["aim"]),
    "ctrl_alt_defeat": ("Member", "14 Jan 2005", 203, "Sacramento, CA",
                        "Athlon 64 3200+ | 1GB DDR | Radeon X800 XL | XP Pro", ["msn"]),
    "QuakeWidow": ("Elite", "03 Sep 2003", 2887, "Raleigh, NC", "", ["yim", "icq"]),
    "NorthernLight": ("Veteran", "22 Nov 2004", 1206, "Minneapolis, MN",
                      "Xbox Live: NorthernLight77", ["www", "msn"]),
}

POSTS = [
    (214381, "MoogleKnight", "Mon Oct 16, 2006 9:12 pm", "",
     "Put my deposit down at GameStop on the way home from class. Wii, Zelda and an extra Wiimote, "
     "which works out to a lot more than $250 once you add it all up :? Still worth it.\n\n"
     "Twilight Princess has been delayed so many times I'll believe it when the disc is actually in the tray."),
    (214386, "Kestrel", "Mon Oct 16, 2006 10:40 pm", "Re: Official Nintendo Wii discussion",
     "Quick reminder since this thread is busy again: launch-line plans, camping meetups and "
     "\"is it in stock at your Target\" posts go in here, not in new threads. I've merged four of them today.\n\n"
     "For what it's worth I'm skipping launch. Red Steel looks like a tech demo and I'd rather wait for a few "
     "more games."),
    (214394, "ctrl_alt_defeat", "Tue Oct 17, 2006 8:55 am", "",
     '[quote="MoogleKnight"]Wii, Zelda and an extra Wiimote, which works out to a lot more than $250 once you '
     'add it all up[/quote]\nDon\'t forget a Nunchuk for the second Wiimote if you want two players in '
     "anything besides Wii Sports.\n\nVirtual Console is what sold me though. 800 points for Super Metroid? Done. :D"),
    (214398, "QuakeWidow", "Tue Oct 17, 2006 1:30 pm", "",
     "I'll be the grumpy one then. Every launch preview I've read says the controls are \"interesting\", "
     "which is reviewer for \"not finished\". I'll pick one up in the spring when there's more than one game "
     "I actually want :roll:"),
    (214402, "NorthernLight", "Tue Oct 17, 2006 3:09 pm", "",
     "Talked to the manager at the GameStop by me and he reckons they're getting about 40 units for launch day, "
     "and most of those are already spoken for. If you haven't put a deposit down somewhere yet, do it this week."),
]

CONTACT = {
    "www": ("WWW_IMG", "icon_www.gif", "Visit poster's website"),
    "aim": ("AIM_IMG", "icon_aim.gif", "AIM Address"),
    "yim": ("YIM_IMG", "icon_yim.gif", "Yahoo Messenger"),
    "msn": ("MSN_IMG", "icon_msnm.gif", "MSN Messenger"),
    "icq": ("ICQ_IMG", "icon_icq_add.gif", "ICQ Number"),
}


def btn(img, alt, href="#"):
    return ('<a href="%s"><img src="%s/lang_english/%s" alt="%s" title="%s" border="0" /></a>'
            % (href, IMG, img, alt, alt))


def build_viewtopic():
    rows = []
    for i, (pid, name, date, subject, text) in enumerate(POSTS):
        rank, joined, nposts, loc, sig, contacts = POSTERS[name]
        row = {
            "ROW_CLASS": "row1" if i % 2 == 0 else "row2", "U_POST_ID": pid,
            "POSTER_NAME": name, "POSTER_RANK": rank, "RANK_IMAGE": "", "POSTER_AVATAR": avatar_img(name),
            "POSTER_JOINED": "Joined: " + joined, "POSTER_POSTS": "Posts: %d" % nposts,
            "POSTER_FROM": "Location: " + loc,
            "U_MINI_POST": "viewtopic.html?p=%d#%d" % (pid, pid), "MINI_POST_IMG": IMG + "/icon_minipost.gif",
            "L_MINI_POST_ALT": "Post", "POST_DATE": date, "POST_SUBJECT": subject,
            "QUOTE_IMG": btn("icon_quote.gif", "Reply with quote"),
            "MESSAGE": bbcode(text),
            "SIGNATURE": "<br />_________________<br />" + bbcode(sig) if sig else "",
            "PROFILE_IMG": btn("icon_profile.gif", "View user's profile", u(name)),
            "PM_IMG": btn("icon_pm.gif", "Send private message"),
        }
        for c in contacts:
            key, img, alt = CONTACT[c]
            row[key] = btn(img, alt)
        rows.append(row)

    votes = [("Yes, already preordered", 61), ("Yes, if I can find one", 47),
             ("Waiting for more games / a price drop", 38), ("No, getting a PS3", 12), ("Not interested", 9)]
    total = sum(v for _, v in votes)
    options = [{"POLL_OPTION_CAPTION": cap, "POLL_OPTION_IMG": IMG + "/voting_bar.gif",
                "POLL_OPTION_IMG_WIDTH": round(v / total * 205),
                "POLL_OPTION_PERCENT": "%d%%" % int(v / total * 100), "POLL_OPTION_RESULT": v}
               for cap, v in votes]
    poll = render("viewtopic_poll_result.tpl", {"POLL_QUESTION": "Are you getting a Wii at launch?",
                                                 "poll_option": options, "L_TOTAL_VOTES": "Total Votes",
                                                 "TOTAL_VOTES": total})
    post_days = ('<select name="postdays"><option value="0" selected="selected">All Posts</option>'
                 '<option value="1">1 Day</option><option value="7">7 Days</option><option value="14">2 Weeks</option>'
                 '<option value="30">1 Month</option><option value="90">3 Months</option>'
                 '<option value="180">6 Months</option><option value="364">1 Year</option></select>')
    order = ('<select name="postorder"><option value="asc" selected="selected">Oldest First</option>'
             '<option value="desc">Newest First</option></select>')
    auth = "".join("You <b>cannot</b> %s in this forum<br />" % s for s in
                   ["post new topics", "reply to topics", "edit your posts", "delete your posts", "vote in polls"])
    d = {
        "U_VIEW_TOPIC": "viewtopic.html?t=48099", "TOPIC_TITLE": "Official Nintendo Wii discussion",
        "PAGINATION": pagination(15, 15, "viewtopic.html?t=48099"),
        "U_POST_NEW_TOPIC": "#", "POST_IMG": IMG + "/lang_english/post.gif", "L_POST_NEW_TOPIC": "Post new topic",
        "U_POST_REPLY_TOPIC": "#", "REPLY_IMG": IMG + "/lang_english/reply.gif", "L_POST_REPLY_TOPIC": "Reply to topic",
        "U_INDEX": "index.html", "L_INDEX": "%s Forum Index" % SITENAME,
        "U_VIEW_FORUM": "viewforum.html?f=3", "FORUM_NAME": "Console Gaming",
        "U_VIEW_OLDER_TOPIC": "viewtopic.html", "L_VIEW_PREVIOUS_TOPIC": "View previous topic",
        "U_VIEW_NEWER_TOPIC": "viewtopic.html", "L_VIEW_NEXT_TOPIC": "View next topic",
        "POLL_DISPLAY": poll, "L_AUTHOR": "Author", "L_MESSAGE": "Message",
        "L_POSTED": "Posted", "L_POST_SUBJECT": "Post subject", "L_BACK_TO_TOP": "Back to top",
        "postrow": rows, "S_POST_DAYS_ACTION": "viewtopic.html", "L_DISPLAY_POSTS": "Display posts from previous",
        "S_SELECT_POST_DAYS": post_days, "S_SELECT_POST_ORDER": order, "L_GO": "Go",
        "S_TIMEZONE": "All times are GMT", "PAGE_NUMBER": "Page <b>15</b> of <b>15</b>",
        "JUMPBOX": jumpbox(3), "S_AUTH_LIST": auth,
    }
    write("viewtopic.html", header("View topic - Official Nintendo Wii discussion")
          + render("viewtopic_body.tpl", d) + footer())


# --- profile.html (MoogleKnight) ---------------------------------------------

def build_profile():
    d = {
        "U_INDEX": "index.html", "L_INDEX": "%s Forum Index" % SITENAME,
        "L_VIEWING_PROFILE": "Viewing profile :: MoogleKnight",
        "L_AVATAR": "Avatar", "L_ABOUT_USER": "All about MoogleKnight",
        "AVATAR_IMG": avatar_img("MoogleKnight"), "POSTER_RANK": "Veteran",
        "L_JOINED": "Joined", "JOINED": "02 Jun 2004",
        "L_TOTAL_POSTS": "Total posts", "POSTS": 1944,
        "POST_PERCENT_STATS": "%.2f%% of total" % (1944 / TOTAL_POSTS * 100),
        "POST_DAY_STATS": "%.2f posts per day" % (1944 / 867),
        "U_SEARCH_USER": "#", "L_SEARCH_USER_POSTS": "Find all posts by MoogleKnight",
        "L_LOCATION": "Location", "LOCATION": "Austin, TX",
        "L_WEBSITE": "Website",
        "WWW": '<a href="#" target="_userwww">http://moogleknight.deviantart.com</a>',
        "L_OCCUPATION": "Occupation", "OCCUPATION": "Student",
        "L_INTERESTS": "Interests", "INTERESTS": "JRPGs, drawing, staying up too late",
        "L_CONTACT": "Contact", "USERNAME": "MoogleKnight",
        "L_EMAIL_ADDRESS": "E-mail address", "EMAIL_IMG": btn("icon_email.gif", "Send e-mail"),
        "L_PM": "Private Message", "PM_IMG": btn("icon_pm.gif", "Send private message"),
        "L_MESSENGER": "MSN Messenger", "MSN": "moogleknight@hotmail.com",
        "L_YAHOO": "Yahoo Messenger", "YIM_IMG": "&nbsp;",
        "L_AIM": "AIM Address", "AIM_IMG": btn("icon_aim.gif", "AIM Address"),
        "L_ICQ_NUMBER": "ICQ Number", "ICQ_IMG": btn("icon_icq_add.gif", "ICQ Number"),
        "JUMPBOX": jumpbox(),
    }
    write("profile.html", header("Viewing profile") + render("profile_view_body.tpl", d) + footer())


if __name__ == "__main__":
    make_avatars()
    build_index()
    build_viewforum()
    build_viewtopic()
    build_profile()
    print("wrote", OUT)
