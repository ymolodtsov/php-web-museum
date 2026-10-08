#!/usr/bin/env python3
"""Drive a fresh Drupal 6.14 install through its own admin forms.

usage: drupal_ui.py BASE ADMIN_PASSWORD STEP
  STEP = install | modules | content | menu

Content is created through node/add so Drupal builds teasers, revisions and
statistics itself; tools/drupal6/seed.sql then back-dates it and adds users,
comments, terms and blocks. Nodes are created in a fixed order so nids are stable.
"""
import http.cookiejar
import html
import re
import sys
import urllib.parse
import urllib.request

BASE, PASSWORD, STEP = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def url(q):
    return BASE + "/?q=" + q


def get(q):
    with opener.open(url(q), timeout=120) as r:
        return r.read().decode("utf-8")


def post(q, fields):
    data = urllib.parse.urlencode(fields).encode()
    with opener.open(url(q), data, timeout=300) as r:
        return r.read().decode("utf-8")


def form_fields(page, form_id):
    """Default values of the form with the given form_id, as a list of pairs."""
    for m in re.finditer(r"<form\b.*?</form>", page, re.S):
        f = m.group(0)
        if 'value="%s"' % form_id not in f:
            continue
        out = []
        for inp in re.finditer(r"<input\b[^>]*>", f):
            t = inp.group(0)
            name = re.search(r'name="([^"]*)"', t)
            if not name:
                continue
            typ = (re.search(r'type="([^"]*)"', t) or [None, "text"])[1]
            val = re.search(r'value="([^"]*)"', t)
            val = html.unescape(val.group(1)) if val else ""
            if typ in ("submit", "button", "image"):
                continue
            if typ in ("checkbox", "radio") and "checked" not in t:
                continue
            if "disabled" in t:
                continue
            out.append((html.unescape(name.group(1)), val))
        for sel in re.finditer(r'<select\b[^>]*name="([^"]*)"[^>]*>(.*?)</select>', f, re.S):
            for opt in re.finditer(r'<option value="([^"]*)"[^>]*selected', sel.group(2)):
                out.append((html.unescape(sel.group(1)), html.unescape(opt.group(1))))
        for ta in re.finditer(r'<textarea\b[^>]*name="([^"]*)"[^>]*>(.*?)</textarea>', f, re.S):
            out.append((html.unescape(ta.group(1)), html.unescape(ta.group(2))))
        return out
    raise SystemExit("form %s not found" % form_id)


def submit(q, form_id, overrides, op):
    # teaser_js is filled by the teaser splitter JavaScript; posting it empty
    # would tell Drupal the teaser is blank, so leave it out like a non-JS browser
    fields = [(k, v) for k, v in form_fields(get(q), form_id) if k not in overrides and k != "teaser_js"]
    for k, v in overrides.items():
        for item in (v if isinstance(v, list) else [v]):
            fields.append((k, item))
    fields.append(("op", op))
    page = post(q, fields)
    err = re.search(r'<div class="messages error">(.*?)</div>', page, re.S)
    if err:
        raise SystemExit("%s: %s" % (q, re.sub(r"<[^>]+>", " ", err.group(1)).strip()))
    return page


def login():
    submit("user", "user_login", {"name": "admin", "pass": PASSWORD}, "Log in")
    if "Log out" not in get("user"):
        raise SystemExit("login failed")


def modules():
    page = get("admin/build/modules")
    on = {k: v for k, v in form_fields(page, "system_modules")}
    new = ["forum", "search", "contact"]
    over = {"status[%s]" % m: m for m in new}
    submit("admin/build/modules", "system_modules", over, "Save configuration")
    print("enabled", new, "kept", sorted(k for k in on if k.startswith("status[")))


def menu():
    links = [("node/1", "About", -10), ("forum", "Forums", -5), ("search", "Search", 0), ("contact", "Contact", 5)]
    for path, title, weight in links:
        submit("admin/build/menu-customize/primary-links/add", "menu_edit_item",
               {"menu[link_path]": path, "menu[link_title]": title, "menu[weight]": str(weight),
                "menu[parent]": "primary-links:0"}, "Save")
        print("primary link", title)


# (type, title, body). nid order matters: seed.sql refers to these nids.
NODES = [
    ("page", "About the Project", """The Open Computing History Project is a research and preservation effort based in the Department of Computer Science. We collect, catalogue and publish primary sources on the history of computing: hardware, documentation, software, and the recollections of the people who built and used these systems.

The project started in 2006 as a graduate seminar on the history of timesharing and has since grown into a small archive and hardware lab staffed mostly by student and community volunteers. Everything we publish here is released under a Creative Commons Attribution-ShareAlike license unless a donor has asked otherwise.

<h3>What we collect</h3>
<ul>
<li>Manuals, rate cards, internal memos and other paper documentation</li>
<li>Software on original media, which we image and describe</li>
<li>Working and non-working hardware for study and restoration</li>
<li>Oral history interviews with operators, programmers, sysops and users</li>
</ul>

<h3>Getting involved</h3>
The hardware lab meets on the first and third Saturday of each month in room 2.114 of the Engineering Annex. Volunteers do not need any prior experience. If you have material you would like to donate, or questions about using the collection for research, please use the contact form or post in the forums.

The project is supported by a small departmental grant and by individual donors."""),
    ("story", "ARPANET Host Tables, 1973-1983, Now Online", """We have finished transcribing a set of ARPANET host tables covering the decade from 1973 to the NCP-to-TCP/IP transition in January 1983. The tables were printed out at regular intervals by a site that kept them for reference, and they were donated to the project last spring along with a box of RFC printouts.

Each table lists host names, addresses and the type of machine at each site, so taken together they show the network growing from a few dozen hosts to several hundred. We have published the transcriptions as plain text alongside page scans, and we have also compiled a single spreadsheet that tracks each host across the years.

A few of the earlier pages were hard to read and some entries are marked as uncertain. Corrections are welcome. If you worked at one of the listed sites and remember what was actually behind a particular host name, we would like to hear from you."""),
    ("story", "Donation: Complete Run of a 1980s Hobbyist Magazine", """The archive has received a nearly complete run of a regional home computing hobbyist magazine published between 1981 and 1986. The donor subscribed from the second issue onward and kept every copy in good condition, with only three issues missing from the five-year run.

The magazine is especially useful to us because of its type-in program listings. Most issues carried several BASIC programs for the popular home machines of the day, along with letters from readers reporting bugs in earlier listings. We are scanning the listings first and will then try to type in and run a sample of them under emulation, recording which ones work as printed.

Scanning will take most of the winter. If you are interested in helping with the transcription, the hardware lab sessions are a good place to start."""),
    ("story", "Keyboard Membrane Repair Notes, 1982-1984 Models", """Our hardware group has written up the repair notes we have collected over the past year for membrane keyboards found in early 1980s home computers. Membrane keyboards were cheap to make and are now the most common point of failure in the machines we receive.

The notes cover the usual problems: cracked traces on the ribbon tail, keys that stop registering after the conductive ink wears off, and connectors that have corroded from years in a damp basement. For each machine we list what has worked for us, what has not, and which repairs we consider reversible.

The notes are a working document. We would rather publish them now with gaps than wait until they are complete, so please send corrections and additions."""),
    ("story", "Benchmarking a 1983 Home Computer Collection", """A visiting research assistant spent the summer running period benchmark programs across six home computers from the project's collection. The aim was to see how well the published magazine benchmarks of the time hold up when repeated on real hardware that is now more than 25 years old.

All six machines ran the same short set of BASIC programs: loops, string handling, floating point arithmetic and screen output. We timed each run with a stopwatch, as the original reviewers did, and repeated each one five times. In most cases our results came within a few percent of the published figures. The largest difference came from one machine whose results depended heavily on whether the display was enabled during the run.

The full results and the program listings are now in the archive. We plan to repeat the exercise next year with the machines that are currently waiting for repair."""),
    ("story", "Call for Volunteers: Core Memory Cataloguing", """We are looking for volunteers to help catalogue a recent donation of core memory planes and associated documentation. The donation came from a retired field engineer and includes planes from several different mainframe and minicomputer systems, some still in their original shipping cartons.

The work involves photographing each plane, recording its markings and dimensions, and matching it against the documentation where we can. No prior hardware experience is needed, only patience and a steady hand. Training will be given at the start of the next lab session.

Please post in the forums or use the contact form if you can help."""),
    ("story", "Scanned: 1979 Timesharing Service Rate Card", """We have added a scanned rate card from a regional timesharing bureau, listing connect-time, CPU and storage charges for 1979. The card was found tucked inside a programming manual donated earlier this year.

Rate cards like this one are a small but useful source for anyone researching what computing actually cost before personal computers. This one lists separate prime-time and evening rates for connect time, charges per CPU second, monthly rates for disk storage by the track, and a surcharge for printing at the bureau's own site.

The scan and a transcription are now in the archive. If anyone has rate cards from other bureaus of the same period, we would be glad to compare them."""),
    ("story", "Restoring a DEC PDP-11/70 Front Panel", """Volunteers at the project's hardware lab have finished a six-month restoration of a PDP-11/70 front panel donated by a retired systems engineer. The switch register and all of the indicator lamps now work, and the panel is on display in the lab.

Most of the work went into the lamps and switches. Several switches had been broken off at some point and were replaced with parts from a second, damaged panel that came with the donation. Every incandescent lamp was tested and about a third were replaced. We have documented each step with photographs so that other groups working on similar panels can see what we did.

The panel is not connected to a working machine. Getting a complete PDP-11/70 running is a much larger project, and for now the panel is driven by a small test circuit that lets visitors toggle in values and watch the lamps."""),
    ("story", "An Oral History Interview: Running a BBS in 1987", """This month's featured interview revisits the early days of dial-up bulletin board systems through the recollections of a sysop who ran a two-line BBS out of a spare bedroom in Ohio from 1986 to 1991. The system, built around an IBM PC XT clone and a pair of 1200-baud modems, hosted a small but devoted local community of callers trading files, playing door games, and arguing about hardware on public message boards.

Our interviewee describes the daily routine of sysop life: enforcing time limits during the dinner-hour rush, writing batch files to automate nightly FidoNet mail runs, and the constant low-grade anxiety of a second phone line ringing with a complaint from an angry parent. He recalls the leap from 300 to 1200 baud as "like getting a new car," and remembers the board's eventual decline in the early 1990s as callers drifted toward commercial online services with national reach.

The full audio of the interview, along with a transcript and scanned copies of the board's original user list and door-game registration cards, has been added to the project's digital archive this week. Researchers interested in the social history of pre-Web online communities are encouraged to contact the project for access to the complete oral history collection."""),
    ("forum", "Lab sessions for November", """The hardware lab will meet on Saturday November 7 and Saturday November 21, from 10am to 4pm in room 2.114 of the Engineering Annex.

On the 7th we will start on the core memory planes, so if you signed up for that please come to the first session. On the 21st we will continue with the floppy imaging backlog. Coffee is provided, lunch is not."""),
    ("forum", "Anyone have a spare RL02 drive belt?", """One of the two RL02 drives that came with the PDP-11 donation spins up but the belt is cracked and slipping. Does anyone know a source for replacement belts, or a belt that is known to fit from some other drive? I would rather not run it as it is."""),
    ("forum", "Emulator recommendations for paper tape images", """We have a small stack of PDP-8 paper tapes that were read into image files a few years ago. Before we start describing them I would like to check that the images are good by loading them into an emulator. SIMH seems like the obvious choice. Has anyone here used it for this, and is there anything to watch out for?"""),
]

FORUM_TID = {"Lab sessions for November": 5, "Anyone have a spare RL02 drive belt?": 6,
             "Emulator recommendations for paper tape images": 7}


def content():
    for typ, title, body in NODES:
        over = {"title": title, "body": body, "format": "1"}
        if typ == "forum":
            page = get("node/add/forum")
            name = re.search(r'<select name="(taxonomy\[\d+\])"', page).group(1)
            over[name] = str(FORUM_TID[title])
        submit("node/add/" + typ, typ + "_node_form", over, "Save")
        print("created", typ, title)


def install():
    """Run install.php: English, default profile, then the Configure site form."""
    inst = BASE + "/install.php?locale=en&profile=default"
    with opener.open(inst, timeout=300) as r:
        page = r.read().decode("utf-8")
    # the module-install batch without JavaScript advances by meta refresh
    for _ in range(50):
        m = re.search(r'http-equiv="Refresh" content="0; URL=([^"]+)"', page)
        if not m:
            break
        with opener.open(html.unescape(m.group(1)), timeout=300) as r:
            page = r.read().decode("utf-8")
    fields = [(k, v) for k, v in form_fields(page, "install_configure_form")
              if k not in ("site_name", "site_mail", "date_default_timezone")]
    fields += [("site_name", "Open Computing History Project"), ("site_mail", "ochp@cs.example.edu"),
               ("account[name]", "admin"), ("account[mail]", "ochp-admin@cs.example.edu"),
               ("account[pass][pass1]", PASSWORD), ("account[pass][pass2]", PASSWORD),
               ("date_default_timezone", "-18000"), ("clean_url", "0"), ("op", "Save and continue")]
    # leave the update status module unticked: it would phone home and nag about 6.14
    fields = [(k, v) for k, v in fields if not k.startswith("update_status_module")]
    with opener.open(inst, urllib.parse.urlencode(fields).encode(), timeout=300) as r:
        page = r.read().decode("utf-8")
    if "Drupal installation complete" not in page:
        raise SystemExit("install failed")
    print("installed")


if STEP == "install":
    install()
else:
    login()
    {"modules": modules, "content": content, "menu": menu}[STEP]()
