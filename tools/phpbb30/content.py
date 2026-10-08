# Pixel Arena Forums, two years on -- fictional content for the phpBB 3.0.2 exhibit.
# Archive date: Friday 17 October 2008, 15:22 UTC (board timezone GMT, as in the phpBB 2 exhibit).
# The board was converted from phpBB 2.0.x in the summer of 2008, so member ids, join dates
# and topic/post id ranges continue from the phpBB 2 exhibit (17 October 2006).

NOW = "2008-10-17 15:22"
SITENAME = "Pixel Arena Forums"
SITE_DESC = "where your framerate matters more than your social life"
BOARD_START = "2003-07-05 19:40"

# Forums in display order: (id, parent, name, description, topics, posts, moderators)
# Categories have parent 0 and no counts. Counts are the board's real size (most topics
# predate the snapshot); only the pages captured for the exhibit hold full content.
FORUMS = [
    (1, 0, "Pixel Arena", "", 0, 0, []),
    (2, 1, "General Discussion", "Site news, introductions, and anything that doesn't fit anywhere else.",
     1702, 25934, []),
    (3, 0, "Gaming", "", 0, 0, []),
    (4, 3, "PC Gaming", "Patches, mods, LAN parties and the eternal framerate complaints.",
     4011, 58217, ["LANwolf"]),
    (5, 3, "Console Gaming", "Xbox 360, PS3, Wii, handhelds -- and whatever is launching next month.",
     3220, 51466, ["NorthernLight"]),
    (6, 3, "Hardware", "Building, upgrading and overclocking. Post your specs before asking for help.",
     2381, 32951, ["Trip_Wire"]),
    (7, 0, "Everything Else", "", 0, 0, []),
    (8, 7, "Off Topic", "Movies, music, desktops and everything else. Keep it civil.",
     4789, 84322, ["QuakeWidow"]),
]

# Ranks: (title, min posts, special)
RANKS = [("Moderator", 0, 1), ("Newbie", 0, 0), ("Member", 25, 0), ("Veteran", 1000, 0), ("Elite", 2500, 0)]

# Named members. id, name, joined, posts, group (admin/gmod/None), special rank, location,
# occupation, interests, website, signature, birthday (d-m-Y), avatar, im {icq, aim, msnm, yim, jabber},
# last visit, shows in "Who is online" (False = hidden)
MEMBERS = [
    dict(id=2, name="Zane", joined="2003-07-05 19:40", posts=6114, group="admin", rank="Site Admin",
         loc="Cleveland, OH", occ="Network admin", interests="Quake, Counter-Strike, keeping this place running",
         www="", sig="Pixel Arena admin. Problems with the new board? Post in [b]phpBB3 feedback[/b] in General.",
         bday="", avatar="", im=dict(aim="ZaneAtPA"), last="2008-10-17 14:51"),
    dict(id=7, name="Kestrel", joined="2003-07-11 21:02", posts=9881, group="gmod", rank="Moderator",
         loc="Columbus, OH", occ="Paralegal", interests="RPGs, strategy, birds (the real kind)",
         www="", sig="Please read the [url={RULES_URL}]forum rules[/url] before posting. Seriously.",
         bday="", avatar="Kestrel.gif", im=dict(aim="kestrel_pa"), last="2008-10-17 15:10", hidden=True),
    dict(id=61, name="QuakeWidow", joined="2003-09-03 18:27", posts=3644, rank="",
         loc="Raleigh, NC", occ="Nurse", interests="Railguns, gardening, bad horror movies",
         www="", sig="", bday="", avatar="", im=dict(icq="88213407", yim="quakewidow"), last="2008-10-17 12:40"),
    dict(id=133, name="Trip_Wire", joined="2003-11-19 02:14", posts=2958, rank="",
         loc="Pittsburgh, PA", occ="Electrician", interests="Overclocking, water cooling, the Steelers",
         www="", sig="Q6600 @ 3.4GHz | P5Q Pro | 4GB DDR2-1066 | 8800GTS 512 | custom loop, ask me about it",
         bday="21-10-1975", avatar="", im=dict(msnm="tripwire_pgh@hotmail.com"), last="2008-10-17 09:12"),
    dict(id=845, name="LANwolf", joined="2004-03-08 16:55", posts=2417, rank="",
         loc="Milwaukee, WI", occ="IT support", interests="LAN parties, TF2, Rock Band drums",
         www="", sig="Pixel Arena LAN #19 -- Saturday 15 November. Sign-up thread in General.",
         bday="17-10-1982", avatar="", im=dict(msnm="lanwolf@hotmail.com", aim="lanwolf82"), last="2008-10-17 15:19"),
    dict(id=1188, name="MoogleKnight", joined="2004-06-02 23:31", posts=2706, rank="",
         loc="Austin, TX", occ="Student (graphic design)", interests="JRPGs, drawing, staying up too late",
         www="http://moogleknight.deviantart.com", sig="Now playing: Disgaea 3, Braid. Fable II on Tuesday!",
         bday="17-10-1987", avatar="MoogleKnight.gif", im=dict(msnm="moogleknight@hotmail.com", aim="moogleknight"),
         last="2008-10-17 15:21"),
    dict(id=1490, name="NorthernLight", joined="2004-11-22 20:48", posts=1893, rank="",
         loc="Minneapolis, MN", occ="Accountant", interests="Halo, hockey, achievement hunting",
         www="", sig="Xbox Live: NorthernLight77 -- 41,230G and counting",
         bday="", avatar="", im=dict(msnm="northernlight77@hotmail.com"), last="2008-10-17 15:16"),
    dict(id=1752, name="PolygonPete", joined="2004-12-29 13:07", posts=1134, rank="",
         loc="Portland, OR", occ="QA tester", interests="Racing games, old Sega stuff",
         www="", sig="I test games for a living. No, it is not as fun as it sounds.",
         bday="", avatar="", im={}, last="2008-10-16 23:05"),
    dict(id=2311, name="ctrl_alt_defeat", joined="2005-01-14 10:22", posts=618, rank="",
         loc="Sacramento, CA", occ="", interests="",
         www="", sig="E8400 @ 3.6 | 4GB DDR2 | HD 4850 | Vista x64 (it's fine now, really)",
         bday="", avatar="ctrl_alt_defeat.gif", im=dict(msnm="ctrlaltdefeat@hotmail.com"), last="2008-10-17 13:58"),
    dict(id=3020, name="dropbear", joined="2005-09-02 07:41", posts=1302, rank="",
         loc="Brisbane, Australia", occ="Uni student", interests="Cricket, Burnout, complaining about AU prices",
         www="", sig="AU$99.95 for a new 360 game. Ninety-nine dollars. Ninety-five cents.",
         bday="", avatar="", im={}, last="2008-10-17 11:30"),
    dict(id=3388, name="sk8rgrl88", joined="2006-01-21 19:16", posts=877, rank="",
         loc="San Diego, CA", occ="Barista", interests="Skating, Guitar Hero, Tony Hawk (the old ones)",
         www="", sig="Rock Band 2 drums: 87% on Expert and climbing",
         bday="22-10-1984", avatar="", im=dict(aim="sk8rgrl88"), last="2008-10-17 06:12"),
    dict(id=4917, name="Vectrex_Kid", joined="2006-10-16 22:40", posts=964, rank="",
         loc="Boston, MA", occ="Software developer", interests="Retro collecting, homebrew, vector monitors",
         www="", sig="Collection: 41 consoles, 2 working Vectrexes, 0 shelf space",
         bday="", avatar="", im={}, last="2008-10-17 15:18"),
    dict(id=5486, name="rocketjump", joined="2007-03-11 20:05", posts=1215, rank="",
         loc="Leeds, UK", occ="Student", interests="TF2, Quake Live beta, cheap Steam games",
         www="", sig="TF2: mostly Soldier, sometimes Medic when nobody else will",
         bday="", avatar="", im={}, last="2008-10-17 14:47"),
    dict(id=5911, name="halfpint", joined="2007-08-24 01:33", posts=402, rank="",
         loc="Denver, CO", occ="Line cook", interests="",
         www="", sig="", bday="", avatar="", im={}, last="2008-10-17 03:20"),
    dict(id=6214, name="jenn_plays", joined="2008-01-06 17:52", posts=233, rank="",
         loc="Tampa, FL", occ="Teacher", interests="Wii, DS, Animal Crossing",
         www="", sig="Wii friend code on request :)",
         bday="", avatar="", im={}, last="2008-10-16 21:44"),
    dict(id=6533, name="BrassMonkey", joined="2008-04-12 15:09", posts=318, rank="",
         loc="Phoenix, AZ", occ="Machinist", interests="Benching, Folding@home",
         www="", sig="Folding@home team Pixel Arena -- join us, we have cookies",
         bday="", avatar="", im={}, last="2008-10-17 15:20"),
    dict(id=6871, name="sputnik", joined="2008-07-03 04:26", posts=97, rank="",
         loc="Toronto, ON", occ="", interests="",
         www="", sig="", bday="", avatar="", im={}, last="2008-10-17 10:02"),
    dict(id=7341, name="PipBoy3000", joined="2008-10-16 19:12", posts=5, rank="",
         loc="Dayton, OH", occ="", interests="Fallout, Fallout 2, counting the days",
         www="", sig="", bday="", avatar="", im={}, last="2008-10-17 14:35"),
]
MAX_USER_ID = 7341          # member ids above this are the search-engine bots
TOTAL_MEMBERS_TARGET = 7136  # registered accounts still on the board (some ids were pruned)

# Who is online at capture time (besides the capturing guest): members, guests, bots.
ONLINE = ["MoogleKnight", "LANwolf", "BrassMonkey", "Vectrex_Kid", "NorthernLight", "Kestrel"]
GUESTS_ONLINE = 15
BOTS_ONLINE = ["Google [Bot]"]
RECORD_ONLINE = (214, "2008-01-06 20:41")

# Topics. type: 0 normal, 1 sticky, 3 global announcement. Each post: (author, time, text).
# Reply subjects default to "Re: <title>", as phpBB's posting form fills them in.
TOPICS = []


def topic(forum, title, posts, views, type=0, locked=False, poll=None, key=None):
    TOPICS.append(dict(forum=forum, title=title, posts=posts, views=views, type=type, locked=locked,
                       poll=poll, key=key))


# ---- global announcement ---------------------------------------------------------
topic(2, "Welcome to phpBB3 -- what's new on the board", [
    ("Zane", "2008-08-03 18:05",
     "We're back! Thanks for your patience over the weekend while the board was down. Pixel Arena is now running "
     "[b]phpBB 3.0.2[/b]. All your posts, private messages and settings came across from the old board, and your "
     "password still works.\n\n"
     "The short version of what's new:\n\n"
     "[list][*][b]User Control Panel[/b] -- everything about your account is now in one place (click [i]User Control "
     "Panel[/i] at the top of any page). Profile, signature, avatar, board preferences, subscriptions.\n"
     "[*][b]Friends and foes[/b] -- add people as friends and they show up at the top of the UCP when they're online. "
     "Add someone as a foe and their posts are hidden from you (moderators excepted, sorry).\n"
     "[*][b]Bookmarks[/b] -- bookmark a topic from the bottom of the page and find it again in the UCP. Separate from "
     "watching a topic, so no more emails you didn't want.\n"
     "[*][b]Attachments[/b] -- you can now attach screenshots and files to posts instead of hotlinking from "
     "Photobucket. 256 KB per file for now, we'll see how the disk holds up.\n"
     "[*][b]Private messages[/b] got folders, rules and drafts.\n"
     "[*][b]Quick-mod tools[/b] -- for the mods: lock, move, split and merge without going through three pages each "
     "time. Kestrel is very happy about this.[/list]\n\n"
     "The new look is called prosilver. The old subSilver look is technically still available, but we're only "
     "going to maintain one style, and it's this one. Give it a couple of weeks before you decide you hate it :)\n\n"
     "Bugs, missing posts, broken avatars: reply in the [b]phpBB3 feedback[/b] thread in General Discussion, not here."),
    ("Kestrel", "2008-08-03 18:31",
     "Also: your old phpBB 2 ranks carried over, and moderators can now see reported posts in one place. "
     "Please use the report button (the little exclamation mark on each post) instead of PMing me screenshots."),
    ("MoogleKnight", "2008-08-03 19:02",
     "The bookmarks thing is great. I had 14 topics \"watched\" just so I could find them again."),
    ("ctrl_alt_defeat", "2008-08-03 20:47",
     "Friends list is nice. Foes list is nicer. :twisted:"),
    ("dropbear", "2008-08-04 02:15",
     "Took me ten minutes to find where to change my signature. It's UCP > Profile > Edit signature, for anyone else "
     "looking."),
    ("Zane", "2008-08-04 08:40",
     "Thanks dropbear. Locking this so it stays readable -- feedback thread is in General Discussion."),
], 8834, type=3, locked=True, key="welcome")

# ---- General Discussion ----------------------------------------------------------
topic(2, "Forum rules (updated for phpBB3)", [
    ("Zane", "2008-08-03 17:50",
     "Same rules as before, a little tidier:\n\n"
     "[list=1][*]Be civil. Argue about games, not about each other.\n"
     "[*]No warez, cracks, keygens, or \"where can I download\" requests. Instant ban.\n"
     "[*]Search before posting a new topic. Release-date questions go in the release dates sticky in Console Gaming.\n"
     "[*]Signatures: max 4 lines, no images taller than 100 pixels.\n"
     "[*]Attachments are for screenshots and files that belong to the post. Don't upload your music collection.\n"
     "[*]Spoilers for anything less than a month old must be marked. Put a warning in the topic title.\n"
     "[*]Use the report button for problems. Don't start a thread about it.[/list]\n\n"
     "Moderators: Kestrel (global), LANwolf (PC Gaming), NorthernLight (Console Gaming), Trip_Wire (Hardware), "
     "QuakeWidow (Off Topic)."),
], 5120, type=1, locked=True, key="rules")

topic(2, "phpBB3 feedback and bug reports", [
    ("Kestrel", "2008-08-03 18:20",
     "One thread for everything about the new board: things that broke in the conversion, things you can't find, "
     "things you miss. Zane and I are reading it."),
    ("QuakeWidow", "2008-08-03 18:52",
     "First impression: it's very... blue. And everything is rounded. I'll get used to it.\n\n"
     "Real problem: my avatar is gone."),
    ("Zane", "2008-08-03 19:15",
     "[quote=\"QuakeWidow\"]Real problem: my avatar is gone.[/quote]\n"
     "Remote avatars (the ones linked from other sites) didn't convert. Uploaded ones did. Re-upload it in UCP > "
     "Profile > Edit avatar and it'll stick."),
    ("PolygonPete", "2008-08-03 21:40",
     "Where did quick reply go? I have to click Post Reply and wait for a whole new page every time now."),
    ("Zane", "2008-08-03 22:02",
     "There's no quick reply in phpBB3 yet. There are MODs for it but I'm not installing MODs on a fresh 3.0 board "
     "until the updates slow down. The phpBB team says it's on their list."),
    ("Vectrex_Kid", "2008-08-04 12:18",
     "Signature editor shows a preview now, which is nice. Also the font size buttons at the top right -- my eyes "
     "thank you."),
    ("sk8rgrl88", "2008-08-06 01:33",
     "Getting logged out every time I close the browser even with \"remember me\" ticked."),
    ("Zane", "2008-08-06 07:58",
     "sk8rgrl88: clear your cookies for the site once. The old phpBB 2 cookie has the same name and confuses it. "
     "A few people had this."),
    ("sk8rgrl88", "2008-08-06 17:10", "That fixed it, thanks!"),
    ("dropbear", "2008-10-16 10:51",
     "Bit late but: is there a way to make the board show my local time? Everything says GMT and I'm 10 hours ahead."),
    ("Kestrel", "2008-10-16 13:27",
     "UCP > Board preferences > Edit global settings > Timezone. Set it to +10 and it'll show times in Brisbane "
     "time from then on."),
], 2904, key="feedback")

topic(2, "Most anticipated release this fall?", [
    ("MoogleKnight", "2008-10-12 20:14",
     "The next six weeks are insane. Fable II, Fallout 3, LittleBigPlanet, Gears 2, Wrath, Left 4 Dead... my bank "
     "account is not ready. What's the one you'd pick if you could only buy one?"),
    ("NorthernLight", "2008-10-12 20:39", "Gears 2. Horde mode alone, honestly."),
    ("rocketjump", "2008-10-12 21:05", "Fallout 3, no contest. Then Left 4 Dead. Then sleep."),
    ("Kestrel", "2008-10-12 22:18",
     "Fallout 3, but with a little voice in the back of my head saying \"Oblivion with guns\". We'll see."),
    ("jenn_plays", "2008-10-13 01:44",
     "Is it weird that I'm most excited about Animal Crossing City Folk? Probably weird."),
    ("dropbear", "2008-10-13 07:02", "LittleBigPlanet. Assuming it comes out this year, now. :roll:"),
    ("halfpint", "2008-10-14 04:11", "Wrath. I already know I'll lose November to it."),
    ("Trip_Wire", "2008-10-15 12:50", "Far Cry 2, as a benchmark if nothing else."),
    ("MoogleKnight", "2008-10-17 13:22",
     "Fallout is pulling ahead. Fable II and LBP would be closer if they weren't splitting the console vote."),
], 1612, poll=dict(title="Which one game are you buying first this fall?", max=1, length=0,
                   start="2008-10-12 20:14",
                   options=[("Fallout 3", 31), ("Gears of War 2", 22), ("LittleBigPlanet", 14), ("Fable II", 11),
                            ("Wrath of the Lich King", 13), ("Left 4 Dead", 9), ("Far Cry 2", 3),
                            ("Something else / nothing", 6)]), key="poll")

topic(2, "Hello from Dayton -- found you through the Fallout 3 thread", [
    ("PipBoy3000", "2008-10-16 19:31",
     "Hi all. Been lurking the Fallout 3 thread for about a month and finally registered. 29, Dayton, OH. Played "
     "Fallout 1 and 2 to death in high school. Mostly PC, I have a 360 for the stuff that never comes to PC.\n\n"
     "Yes, the username is a bit much. It was free."),
    ("Kestrel", "2008-10-16 19:58",
     "Welcome! Rules are stickied at the top of this forum. Practically neighbours -- I'm in Columbus."),
    ("Vectrex_Kid", "2008-10-16 20:40",
     "Welcome. Do you still have the original Fallout box? Asking for my shelf."),
    ("PipBoy3000", "2008-10-16 21:05",
     "[quote=\"Vectrex_Kid\"]Do you still have the original Fallout box?[/quote]\nBig box, manual and the reference "
     "card. Not for sale :P"),
    ("LANwolf", "2008-10-17 14:31",
     "Welcome aboard. If you're anywhere near Milwaukee in November, we've got a LAN on the 15th."),
], 211, key="intro")

topic(2, "Pixel Arena LAN #19 -- Saturday 15 November", [
    ("LANwolf", "2008-10-04 15:12",
     "Same place as last time (the VFW hall in West Allis), doors at 10am, out by midnight.\n\n"
     "[b]$15 at the door[/b], covers the hall and pizza. Bring your own PC, monitor, power strip and a network "
     "cable. We'll have the gigabit switches.\n\n"
     "Planned: TF2, Left 4 Dead if the demo is out by then, UT2004 for old times' sake, Rock Band in the corner.\n\n"
     "Reply here if you're coming so I know how many tables to ask for."),
    ("rocketjump", "2008-10-04 16:40",
     "Wish I could. Flights from Leeds are a bit much for a LAN :("),
    ("ctrl_alt_defeat", "2008-10-04 19:03", "In. Bringing the new 4850 to show off."),
    ("Trip_Wire", "2008-10-05 10:26", "In. I'll drive up Friday night. Can someone remind me to pack the coolant this time."),
    ("BrassMonkey", "2008-10-06 22:15",
     "First one for me, if that's OK. Phoenix to Milwaukee is a stretch but I've got family there that weekend."),
    ("LANwolf", "2008-10-07 08:04", "Of course. Everyone's welcome. That's 14 so far, counting the regulars who told me in person."),
    ("sk8rgrl88", "2008-10-17 06:12", "Is there room for a Rock Band drum kit? Asking for me."),
], 690, type=1, key="lan")

# ---- PC Gaming -------------------------------------------------------------------
topic(4, "Fallout 3 -- 11 days to go", [
    ("rocketjump", "2008-09-29 18:02",
     "New trailer and the dev diary about VATS went up last week. Thread for everything Fallout 3 until it ships "
     "on the 28th (30th for us in Europe, of course).\n\n"
     "Who's preordered, what version, and are you getting the Collector's Edition with the lunchbox?"),
    ("sputnik", "2008-09-29 18:40",
     "PC, Survival Edition from Amazon. The Pip-Boy clock is ridiculous and I want it."),
    ("Kestrel", "2008-09-29 19:12",
     "360 Collector's Edition. I'm worried about the PC version needing Games for Windows Live, and I'd rather "
     "play on the couch anyway."),
    ("LANwolf", "2008-09-29 20:55",
     "[quote=\"Kestrel\"]I'm worried about the PC version needing Games for Windows Live[/quote]\n"
     "As far as I can tell it's only for achievements. You can play without signing in."),
    ("Trip_Wire", "2008-09-30 01:17",
     "PC here, because of mods. Bethesda already said they're releasing the G.E.C.K. editor for it, same as the "
     "Construction Set for Oblivion. Give it six months and the PC version will be a different game."),
    ("QuakeWidow", "2008-09-30 13:40",
     "Everything I've seen looks like Oblivion with guns and a brown filter. I'll wait for reviews :|"),
    ("rocketjump", "2008-09-30 14:22",
     "It IS Oblivion with guns. That's the point. I put 200 hours into Oblivion with swords."),
    ("halfpint", "2008-10-02 03:10",
     "Liam Neeson voicing your dad, Ron Perlman narrating. They're not messing around."),
    ("Vectrex_Kid", "2008-10-05 16:44",
     "Anyone else replaying 1 and 2 first? I'm in the middle of Fallout 2 again and it holds up, except the "
     "inventory."),
    ("dropbear", "2008-10-08 09:30",
     "Australian classification board passed it after they changed the morphine name. So we actually get it. "
     "Small miracles."),
    ("halfpint", "2008-10-14 22:51",
     "System requirements are out: 2.4GHz dual core, 2GB RAM, 8800 or HD 3870 recommended. My 8800GT should be "
     "fine. My 2GB of RAM, less so."),
    ("ctrl_alt_defeat", "2008-10-17 09:44",
     "Eleven days. The GameStop near me said they get stock the Monday before but can't sell it until the 28th. "
     "Pain."),
    ("rocketjump", "2008-10-17 14:47",
     "Ok, it's settled, I'm taking the 30th and 31st off. Tutor can mark me as ill."),
], 4430, key="fallout")

topic(4, "Spore DRM -- three installs, SecuROM, and 2,000 one-star reviews", [
    ("ctrl_alt_defeat", "2008-09-09 21:12",
     "Spore is getting killed on Amazon. Thousands of one-star reviews, and most of them are about SecuROM and the "
     "three-install limit, not the game. Did anyone here actually buy it?"),
    ("Vectrex_Kid", "2008-09-09 21:50",
     "Bought it, installed it, played it for a weekend. The creature editor is amazing, the rest is a collection of "
     "very simple minigames. And now I have two installs left, apparently."),
    ("LANwolf", "2008-09-10 08:17",
     "Three installs is a joke for anyone who rebuilds their PC more than once a year. Which is half of this forum."),
    ("PolygonPete", "2008-09-10 12:05",
     "The funny part is that the cracked version was out before the official release. The DRM only bothers people "
     "who paid."),
    ("Trip_Wire", "2008-09-11 23:40",
     "I'm skipping it. Not because I'm boycotting, I just reformat too often to deal with call-EA-and-beg."),
    ("rocketjump", "2008-09-20 13:25",
     "EA has raised the limit to five installs and say they'll release a de-authorization tool. Still not buying "
     "it, but it's something."),
    ("ctrl_alt_defeat", "2008-09-20 14:02", "Far Cry 2 has the same SecuROM activation limit, by the way. Five, I think."),
    ("BrassMonkey", "2008-10-16 22:37",
     "Picked it up on sale and the creature creator alone is worth twenty bucks. My nephew has made about 300 "
     "creatures with two legs and too many eyes."),
], 2207, key="spore")

topic(4, "WotLK pre-patch (3.0.2) is live -- achievements, barbershop, Death Knights in 4 weeks", [
    ("halfpint", "2008-10-14 23:58",
     "Patch is out. Achievements, new talent trees, Inscription, and the barbershop in every capital city. "
     "My hunter has a mohawk now. Release date for Wrath is still November 13."),
    ("rocketjump", "2008-10-15 00:30",
     "Funny coincidence: WoW and this board are both on 3.0.2 now. Zane's announcement says so."),
    ("Kestrel", "2008-10-15 08:47",
     "Got into the beta for a week in August. Northrend is gorgeous and the Death Knight starting area is the "
     "best thing Blizzard has done in years. Then I had to give it back. :cry:"),
    ("halfpint", "2008-10-15 17:21",
     "Achievement points are going to destroy me. I already got \"Going Down?\" by jumping off the bridge in "
     "Thunder Bluff."),
    ("sputnik", "2008-10-16 10:02",
     "The zombie event before launch is supposed to start soon too. Plague in the capitals. Should be chaos."),
    ("QuakeWidow", "2008-10-17 12:40",
     "I quit WoW last year, and every patch thread makes me want to resubscribe. Stop it."),
], 1544, key="wow")

topic(4, "Steam weekend deals -- my backlog is your fault", [
    ("Vectrex_Kid", "2008-10-10 22:15",
     "Every Friday there's a new half-price deal and every Friday I buy something I won't play until 2010. What "
     "did you grab, and have you actually played it?"),
    ("rocketjump", "2008-10-10 22:42",
     "World of Goo came out on Monday and it's fantastic. Not a sale, just buy it. 2D Boy are two guys."),
    ("BrassMonkey", "2008-10-11 00:20", "Played: TF2. Bought and not played: about 30 others. :oops:"),
    ("PolygonPete", "2008-10-11 11:49",
     "Steam now has more of my games than my shelf does. Not sure how I feel about that. Nothing to sell on when "
     "I'm done."),
    ("LANwolf", "2008-10-12 19:04",
     "Left 4 Dead preorder on Steam gets you into the demo early, if anyone's on the fence. We're playing it at the "
     "LAN if it's out."),
    ("ctrl_alt_defeat", "2008-10-17 13:58",
     "My backlog has a backlog. Still picked up Audiosurf for five bucks yesterday."),
], 980, key="steam")

topic(4, "Far Cry 2 next week -- malaria, jamming guns, fire", [
    ("Trip_Wire", "2008-10-13 17:22",
     "Out on the 21st. Everything I read says it's nothing like the first one. Open Africa, guns jam when they get "
     "old, and you have malaria and have to keep finding pills. Brave, or annoying?"),
    ("rocketjump", "2008-10-13 18:01", "The fire spreading through dry grass looks amazing. Malaria sounds annoying."),
    ("BrassMonkey", "2008-10-14 03:27",
     "Dunia engine supposedly runs well on mid-range cards, unlike a certain Crytek game I could mention."),
    ("Trip_Wire", "2008-10-16 21:09", "And it supports DX10 without the Crysis tax. We'll see."),
], 640)

topic(4, "TF2 -- Pixel Arena server regulars night, Wednesdays", [
    ("LANwolf", "2008-08-20 20:10",
     "Our server is back up after the move: 24 slots, 2fort/dustbowl/goldrush rotation, no crits on Wednesday nights. "
     "Look for \"Pixel Arena | Regulars Night\" in the server browser."),
    ("rocketjump", "2008-08-21 17:44", "Heavy update has ruined pubs. Six Heavies per team. Natascha everywhere."),
    ("NorthernLight", "2008-08-22 01:02", "I'll be on as soon as the Sniper update is out. Never."),
    ("LANwolf", "2008-10-16 22:55", "Reminder: no Wednesday this week, the server box is getting a new drive. Back next week."),
], 1103)

# ---- Console Gaming --------------------------------------------------------------
topic(5, "LittleBigPlanet pulled at the last minute -- delayed over a song", [
    ("dropbear", "2008-10-17 08:14",
     "Sony has recalled LittleBigPlanet days before launch. One of the licensed music tracks apparently has "
     "lines from the Qur'an in it, and they're pressing new discs without it. No new date yet.\n\n"
     "Some shops in Europe already had copies on shelves."),
    ("NorthernLight", "2008-10-17 08:51", "That's a weird one. At least it's a fixable problem. Weeks rather than months?"),
    ("MoogleKnight", "2008-10-17 09:30",
     "My GameStop called me about my preorder. They don't know anything either. I guess I'm playing Fable instead."),
    ("Vectrex_Kid", "2008-10-17 10:22",
     "Remastering a disc and reprinting the whole run is not cheap. Somebody at Sony had a long night."),
    ("halfpint", "2008-10-17 11:05",
     "Wouldn't they just patch the song out? The game needs an online connection for half the features anyway."),
    ("dropbear", "2008-10-17 11:30",
     "[quote=\"halfpint\"]Wouldn't they just patch the song out?[/quote]\nNot every PS3 is online, so they can't ship "
     "the disc with it and hope. Plus retail would never take it."),
    ("jenn_plays", "2008-10-17 15:01", "Too bad, the beta looked like so much fun. My sackboy has a moustache."),
], 744, key="lbp")

topic(5, "Gears of War 2 hype thread (Nov 7)", [
    ("ctrl_alt_defeat", "2008-09-25 20:01",
     "Two years ago I started the Gears 1 hype thread here and it ended up as the biggest thread in Console Gaming. "
     "Let's do it again. Three weeks and change.\n\n"
     "Confirmed so far: Horde mode (5 players vs waves of Locust), 5v5 multiplayer, chainsaw duels, meatshields, "
     "giant Locust everything."),
    ("NorthernLight", "2008-09-25 20:34",
     "Horde. Is. Going. To. Eat. My. Life. Five of us on Friday nights, who's in?"),
    ("PolygonPete", "2008-09-26 11:09",
     "Hoping they fix the host advantage in ranked. Gears 1 online was a coin toss on who got the host."),
    ("sk8rgrl88", "2008-09-28 22:44", "Limited Edition with the art book and the Cog tags, preordered. No regrets."),
    ("ctrl_alt_defeat", "2008-10-09 18:30",
     "\"Bigger, better and more badass.\" Cliff's words, not mine. That man would be great in sales."),
    ("NorthernLight", "2008-10-17 15:16",
     "Rumour is the Gears 2 disc fits on the hard drive once the New Xbox Experience update is out. Two years of "
     "disc noise, gone."),
], 2560, key="gears")

topic(5, "Fable II out Tuesday -- who's getting it?", [
    ("MoogleKnight", "2008-10-15 21:10",
     "Picking it up on Tuesday (21st). Played the Pub Games on Live to bank some gold first. 30,000 gold ready to "
     "go, which apparently buys you about half a house in Albion."),
    ("Kestrel", "2008-10-15 21:40",
     "Peter Molyneux promising things is a tradition. Remember the acorn that grows into a tree? But the dog does "
     "look nice."),
    ("NorthernLight", "2008-10-16 00:04",
     "Co-op is a bit disappointing, the second player can't bring their own character, just a henchman. Still "
     "getting it."),
    ("halfpint", "2008-10-16 03:20", "Can you kick chickens? Asking for real."),
    ("MoogleKnight", "2008-10-16 08:15", "[quote=\"halfpint\"]Can you kick chickens?[/quote]\nThere are achievements for chickens. Draw your own conclusions. :lol:"),
    ("jenn_plays", "2008-10-16 21:44", "The dog is getting me to buy it. The dog. I don't even like dogs."),
    ("MoogleKnight", "2008-10-17 15:21",
     "Just walked past the GameStop on the way back from class and they've got the Fable II standees up. Four days."),
], 1388, key="fable")

topic(5, "New Xbox Experience -- avatars, installs, Netflix on Nov 19", [
    ("NorthernLight", "2008-10-08 19:22",
     "So the dashboard update is dated for November 19. What we know:\n\n"
     "[list][*]Avatars (yes, they look like Miis, yes everyone noticed)\n[*]Installing games to the hard drive\n"
     "[*]Netflix streaming for Gold members\n[*]8-person party chat across games[/list]\n\n"
     "And it's all free. The installs alone are worth it."),
    ("PolygonPete", "2008-10-09 13:15",
     "Installs need a lot of space and the 20GB drive is going to cry. Time to upgrade to the 60."),
    ("dropbear", "2008-10-10 05:41", "Netflix in the US only. Of course. We get nothing again."),
    ("sk8rgrl88", "2008-10-12 03:28", "Party chat is the one I want. Coordinating Rock Band sessions over text is painful."),
    ("NorthernLight", "2008-10-15 23:30",
     "People are saying there'll be a preview for selected members before the full launch. Fingers crossed for "
     "an invite."),
], 1260, key="nxe")

topic(5, "Wii Fit -- five months later, who is still using it?", [
    ("jenn_plays", "2008-10-06 20:12",
     "Honest question. I bought Wii Fit in May, did it every day for six weeks, and now the balance board lives "
     "under the couch. Anyone still going?"),
    ("Kestrel", "2008-10-06 20:56",
     "My mother uses it every morning. She has a better Wii Fit age than me, which she brings up every Sunday."),
    ("PolygonPete", "2008-10-07 09:31", "The board is a great scale. That's how I use it now. :|"),
    ("sk8rgrl88", "2008-10-07 22:15", "Ski jump is still fun after a beer. Not a fitness routine, though."),
    ("MoogleKnight", "2008-10-08 14:44",
     "Wii Fit telling me \"that's overweight\" in a cheerful voice is the reason it's in a closet."),
    ("jenn_plays", "2008-10-16 18:03", "OK, so it's not just me. Rhythm boxing is getting a second chance this weekend."),
], 860, key="wiifit")

topic(5, "Dead Space -- anyone picked it up?", [
    ("PolygonPete", "2008-10-14 22:10",
     "Got it on 360 today. First three hours: no HUD, the health bar is on your back, and cutting off limbs is "
     "actually how you kill things. Tense as hell."),
    ("QuakeWidow", "2008-10-15 13:45", "Is it actually scary or just loud?"),
    ("PolygonPete", "2008-10-15 22:20",
     "Both. Turn the lights off, headphones on. The sound design is the best thing about it."),
    ("Vectrex_Kid", "2008-10-17 15:18", "Waiting for the PC version on Monday. Glad to hear it's not just a shooter with a space coat of paint."),
], 512)

# ---- Hardware --------------------------------------------------------------------
topic(6, "HD 4870 or GTX 260 (216)? ~$280 budget", [
    ("BrassMonkey", "2008-10-09 18:37",
     "Building a new rig for Fallout 3 and Far Cry 2 and stuck on the card. Gaming at 1680x1050 on a 22\".\n\n"
     "HD 4870 512MB: about $270 at Newegg.\nGTX 260 Core 216: about $280.\n\n"
     "Reviews are basically a tie. Which one would you get?"),
    ("Trip_Wire", "2008-10-09 19:20",
     "At 1680x1050 you can't go wrong. The 4870 runs hotter at idle (the fan profile is lazy, fix it with "
     "RivaTuner). The 260 overclocks better and you get PhysX, for the three games that use it."),
    ("ctrl_alt_defeat", "2008-10-09 20:05",
     "Or get the 4850 for $170 like I did and spend the rest on games. It's 80% of the 4870 for 60% of the money."),
    ("BrassMonkey", "2008-10-09 20:40",
     "[quote=\"ctrl_alt_defeat\"]Or get the 4850 for $170[/quote]\nTempting, but I'll keep this card for two "
     "years. Worth the extra."),
    ("LANwolf", "2008-10-10 08:12",
     "The 4870 1GB has just come out. If you're keeping it for two years, the extra memory might matter."),
    ("Trip_Wire", "2008-10-10 12:51",
     "Good point. Also, if you go ATI, Catalyst 8.9 fixed most of the CrossFire problems. Not that "
     "you need CrossFire at 1680."),
    ("dropbear", "2008-10-11 09:15", "For reference, a 4870 here costs AU$399. Be grateful. :evil:"),
    ("BrassMonkey", "2008-10-14 19:44",
     "Went with the 4870 1GB from Sapphire. $299 with a rebate. Box arrives Thursday."),
    ("BrassMonkey", "2008-10-17 15:20",
     "It's in. 3DMark Vantage P9842 at stock, Crysis Warhead on Gamer settings is very playable. Idle temps 78C "
     "out of the box, Trip_Wire wasn't joking. Fan profile edited, now 55C."),
], 1872, key="gpu")

topic(6, "Core i7 / Nehalem -- November launch, X58 and DDR3 prices", [
    ("Trip_Wire", "2008-10-02 14:05",
     "Intel's launching Core i7 in November. What's leaked:\n\n"
     "[list][*]i7 920 (2.66GHz), 940 (2.93GHz), 965 Extreme (3.2GHz)\n[*]Prices around $284, $562 and $999\n"
     "[*]New socket (LGA1366), new chipset (X58), triple-channel DDR3 only\n[*]Hyper-Threading is back[/list]\n\n"
     "The CPU price is fine, the platform isn't. X58 boards supposedly start at $250-300 and 6GB of DDR3 isn't "
     "cheap either."),
    ("BrassMonkey", "2008-10-02 15:33",
     "The 920 is going to be the new Q6600. Everyone will run it at 3.8GHz on air."),
    ("ctrl_alt_defeat", "2008-10-02 18:47",
     "For gaming, my E8400 isn't going anywhere. Games barely use two cores, let alone eight threads."),
    ("Trip_Wire", "2008-10-03 09:20",
     "[quote=\"ctrl_alt_defeat\"]Games barely use two cores[/quote]\nFor now. But yeah, if you're on a C2D at 3.6+ "
     "there's nothing in i7 for you this year."),
    ("Vectrex_Kid", "2008-10-08 21:40", "Compiling at work would love it though. Eight threads for make -j8."),
    ("halfpint", "2008-10-10 02:15", "What's AMD doing? Anything to compete?"),
    ("Trip_Wire", "2008-10-10 08:53",
     "45nm Phenom II, supposedly early next year. Until then the Phenom 9950 is fine and cheap, but no competition "
     "at the top."),
    ("BrassMonkey", "2008-10-16 23:58",
     "Reviews should come out early November. I'll spend my lunch breaks refreshing AnandTech."),
], 1405, key="i7")

topic(6, "Windows 7 -- name's official, PDC at the end of the month", [
    ("Vectrex_Kid", "2008-10-14 13:10",
     "Microsoft confirmed it this week: the next version is officially called Windows 7. They'll show it at the "
     "PDC on the 28th. Rumours are a ribbon in Paint and WordPad, a new taskbar, and fewer UAC prompts."),
    ("ctrl_alt_defeat", "2008-10-14 14:02",
     "Version 6.1 by the way, if you look at the build strings. Same kernel as Vista. Which is fine, honestly, "
     "SP1 fixed most of what was wrong with Vista."),
    ("QuakeWidow", "2008-10-14 18:23", "As long as it's not Vista. Still on XP and staying there."),
    ("Trip_Wire", "2008-10-15 10:45", "Hope they keep the drivers compatible. I don't want to go through 2007 again."),
    ("sputnik", "2008-10-16 18:12", "Windows 7 named after... 7 what? 95, 98, ME, 2000, XP, Vista... that's more than 7."),
    ("Vectrex_Kid", "2008-10-16 18:40",
     "[quote=\"sputnik\"]that's more than 7[/quote]\nThey count the NT line. 1 through 6, then 7. Don't think too "
     "hard about it. :geek:"),
], 1120, key="win7")

topic(6, "Post your rig -- 2008 edition", [
    ("Trip_Wire", "2008-08-05 11:00",
     "New board, new rig thread. Specs and a photo if you have one. Attachments work now, so no need for "
     "Photobucket.\n\n"
     "Mine: Q6600 G0 @ 3.4GHz, Asus P5Q Pro, 4GB Crucial Ballistix, 8800GTS 512, Corsair 650W, custom loop with a "
     "triple rad. Antec P182."),
    ("ctrl_alt_defeat", "2008-08-05 13:19",
     "E8400 @ 3.6 (stock volts), Gigabyte EP45, 4GB DDR2-800, HD 4850, Antec 900. Upgraded from the old Athlon 64 "
     "rig that's been in my sig since 2005."),
    ("PolygonPete", "2008-08-06 22:04", "Dell XPS M1330. Yes, it's a laptop. It plays Peggle beautifully."),
    ("BrassMonkey", "2008-08-09 16:30",
     "Phenom 9850 BE @ 3.0, MSI K9A2 Platinum, 4GB, 2x HD 3870 CrossFire, Thermaltake Armor. Folding 24/7."),
    ("sputnik", "2008-08-14 02:11", "Mac mini. I'll show myself out."),
    ("MoogleKnight", "2008-10-17 15:02",
     "Finally retired my old P4. Athlon X2 5000+, 2GB, HD 4670 (passive, silent, love it), 22\" Samsung. For drawing "
     "more than games, but it runs TF2 fine."),
], 3902, type=1, key="rigs")

topic(2, "What are you playing this weekend?", [
    ("MoogleKnight", "2008-10-17 07:40",
     "Last weekend before the release avalanche. I'm finishing Disgaea 3 (post-game, so \"finishing\" is a strong "
     "word) and maybe starting Braid again for the speedrun achievements. You?"),
    ("dropbear", "2008-10-17 08:20", "Burnout Paradise. Still. The bikes update made it a new game."),
    ("Vectrex_Kid", "2008-10-17 09:41",
     "The Mother 3 fan translation came out today. Two years of work by a handful of people on the internet. Patching "
     "my cart tonight, and yes I own the cart, before anyone asks."),
    ("PolygonPete", "2008-10-17 10:03", "Dead Space with the lights off, as promised in the other thread."),
    ("jenn_plays", "2008-10-17 11:47", "Animal Crossing Wild World to get in shape for City Folk. Paying off my house. Again."),
    ("NorthernLight", "2008-10-17 12:15", "Gears 1 on Insane, to warm up for Gears 2. Three weeks."),
    ("rocketjump", "2008-10-17 13:40",
     "World of Goo and essays. Mostly World of Goo. Don't tell my tutor."),
], 88)

topic(5, "Rock Band 2 vs Guitar Hero World Tour", [
    ("sk8rgrl88", "2008-09-16 03:10",
     "Rock Band 2 has been out for two days and I've already played it more than anything this year. Guitar Hero "
     "World Tour is out next month with its own drums and mic. Is anyone actually buying both? Two sets of plastic "
     "instruments is a lot of plastic."),
    ("LANwolf", "2008-09-16 08:02",
     "RB2 for me. All the Rock Band 1 DLC works in it, I've got about 60 songs downloaded already. Can't throw that "
     "away for a new drum kit."),
    ("PolygonPete", "2008-09-16 12:30",
     "The GH drums have cymbals and look a lot nicer. But Neversoft's note charts... Guitar Hero III's Expert "
     "was just mean."),
    ("NorthernLight", "2008-09-17 22:40", "No Fail mode is the best thing in RB2. My wife plays now. She sings, badly, and nobody fails."),
    ("dropbear", "2008-09-25 06:11", "Rock Band 2 isn't even out here yet. We got Rock Band 1 in May. MAY."),
    ("sk8rgrl88", "2008-10-08 01:55",
     "Update: 87% on Expert drums for \"Painkiller\". My downstairs neighbour has started leaving notes."),
    ("Kestrel", "2008-10-08 09:12", "Please put your Rock Band drums on a rug. Signed, everyone's downstairs neighbour."),
    ("LANwolf", "2008-10-17 13:05", "Bringing the RB2 kit to the LAN. Someone else brings the mic, I'm not singing."),
], 1570)

topic(6, "Intel X25-M -- $600 for 80GB?", [
    ("Vectrex_Kid", "2008-09-09 15:20",
     "Intel's SSD is out: 80GB, 250MB/s reads, 70MB/s writes, and a price of about $595. Reviews say it destroys "
     "everything else, including the Raptor, for random access. Anyone crazy enough?"),
    ("Trip_Wire", "2008-09-09 16:02",
     "The cheap JMicron drives stutter so badly they're unusable for an OS drive. This is the first SSD I'd actually "
     "trust. At $7 a gigabyte, though."),
    ("ctrl_alt_defeat", "2008-09-09 19:40", "$595 is a 4870 and a 360 Arcade. Wake me up when it's $200."),
    ("BrassMonkey", "2008-09-30 22:17",
     "Work bought one for the build server. Boots Vista in about 20 seconds and compiles fly. I'm jealous of a "
     "server."),
    ("Vectrex_Kid", "2008-10-16 18:20", "Seen it for $549 at a couple of places now. Still too much, but heading in the right direction."),
    ("BrassMonkey", "2008-10-17 12:10",
     "Give it a year. Mechanical drives in gaming PCs are going to look as silly as floppy drives do now."),
], 860)

# ---- Off Topic -------------------------------------------------------------------
topic(8, "Google Chrome -- anyone using it?", [
    ("sputnik", "2008-09-03 01:40",
     "Downloaded it as soon as it came out. Fast. Very fast. Every tab is its own process, so when Flash crashes it "
     "takes one tab with it, not the whole browser."),
    ("QuakeWidow", "2008-09-03 13:12",
     "The EULA had a line saying Google gets a licence to anything you post through it. They've already taken it out."),
    ("ctrl_alt_defeat", "2008-09-04 09:30",
     "Using it for Gmail and Google Reader. Firefox 3 for everything else because I need Adblock and my 40 "
     "extensions."),
    ("Vectrex_Kid", "2008-09-05 22:00", "No Mac version. Wake me when there's a Mac version."),
    ("PolygonPete", "2008-10-15 14:08",
     "Six weeks in and I'm still using it. The tabs on top of the window look weird, until you go back to Firefox."),
], 1320, key="chrome")

topic(8, "iPhone 3G -- three months in", [
    ("Vectrex_Kid", "2008-10-11 20:15",
     "Bought it on launch day in July (waited 4 hours outside the AT&T store). Three months later:\n\n"
     "Good: the App Store, maps, real web browsing.\nBad: battery life with 3G on is a joke, and no copy and paste "
     "in 2008 is embarrassing.\n\nThe 2.1 update in September helped the dropped calls a lot."),
    ("jenn_plays", "2008-10-11 21:30", "I want one so badly but $199 + $70 a month for two years is a lot on a teacher's salary."),
    ("PolygonPete", "2008-10-12 10:02", "Still on my RAZR. It makes calls. That's the whole list of features."),
    ("sputnik", "2008-10-13 16:44", "The Super Monkey Ball game on it is surprisingly good. Tilt controls actually work."),
    ("dropbear", "2008-10-17 11:15",
     "Optus wants AU$1,500 over two years for the 16GB one. I'll keep my Nokia, thanks."),
], 980, key="iphone")

topic(8, "The LHC didn't destroy the world (yet)", [
    ("halfpint", "2008-09-10 14:02", "Switched on this morning. We're still here. Disappointed or relieved?"),
    ("Vectrex_Kid", "2008-09-10 14:40",
     "hasthelargehadroncolliderdestroyedtheworldyet.com is my favourite website of 2008."),
    ("QuakeWidow", "2008-09-22 18:21", "And now it's broken for months because of a helium leak. Nature found a way."),
    ("sputnik", "2008-10-16 09:44", "Spring 2009 apparently. We have until then to finish our backlogs."),
], 702)

topic(8, "Quantum of Solace -- who's going?", [
    ("rocketjump", "2008-10-15 19:20",
     "Out on the 31st in the UK, two weeks earlier than the US for once. Casino Royale was the best Bond in 20 years, "
     "so I'm cautiously optimistic. The title is terrible though."),
    ("Kestrel", "2008-10-15 22:05", "Two weeks of spoiler dodging. Thanks, England."),
    ("rocketjump", "2008-10-16 08:00", "I'll put spoiler tags on everything. Probably. :mrgreen:"),
    ("halfpint", "2008-10-17 03:12", "The theme song with Jack White and Alicia Keys is... a choice."),
], 455)

topic(8, "What are you listening to? (autumn 2008)", [
    ("QuakeWidow", "2008-10-01 20:30", "New thread, the old one was 140 pages. Currently: Death Magnetic. Too loud, still good."),
    ("sk8rgrl88", "2008-10-02 03:14", "Vampire Weekend on repeat since January. Send help."),
    ("LANwolf", "2008-10-03 12:52", "Whatever Rock Band 2 has on the drums. Currently \"Painkiller\" on Expert, failing at 40%."),
    ("MoogleKnight", "2008-10-09 23:58", "The Braid soundtrack. Seriously, it's beautiful."),
    ("sputnik", "2008-10-17 10:02", "Fleet Foxes. Last.fm says I've played them 412 times this year, which feels like an intervention."),
], 1530)

# Further topics on the first page of each forum. Title, author, started, replies, views,
# last poster, last post time, type (0/1), locked, poll. Their posts are not part of the exhibit.
FILLER = {
    2: [
        ("Birthday thread -- October", "Kestrel", "2008-10-01 00:12", 23, 412, "LANwolf", "2008-10-17 00:05"),
        ("Pixel Arena is five years old", "Zane", "2008-07-05 19:40", 48, 1720, "Vectrex_Kid", "2008-10-15 22:10"),
        ("Site downtime Saturday night (server move)", "Zane", "2008-10-09 12:00", 7, 344, "Zane", "2008-10-12 06:30"),
        ("Anyone else in Ohio?", "PipBoy3000", "2008-10-17 09:02", 3, 41, "Kestrel", "2008-10-17 10:17"),
        ("Folding@home team -- we're top 2000!", "BrassMonkey", "2008-09-12 20:40", 19, 506, "Trip_Wire", "2008-10-16 20:03"),
        ("Gaming on a budget -- best value games of 2008", "halfpint", "2008-10-02 21:15", 15, 377, "PolygonPete", "2008-10-16 16:44"),
        ("Best game of the year so far?", "QuakeWidow", "2008-09-30 18:10", 41, 1102, "sk8rgrl88", "2008-10-16 05:52"),
        ("Post your phpBB3 avatar here", "MoogleKnight", "2008-08-05 22:40", 37, 991, "jenn_plays", "2008-10-15 20:18"),
        ("Introduce yourself (2008 newcomers)", "Kestrel", "2008-01-02 10:00", 64, 2311, "sputnik", "2008-10-15 03:41"),
        ("Games you're ashamed to love", "PolygonPete", "2008-09-25 23:01", 52, 1418, "MoogleKnight", "2008-10-14 23:12"),
        ("E-mail notifications not arriving?", "dropbear", "2008-10-12 08:20", 4, 97, "Zane", "2008-10-13 07:11"),
        ("Games to look forward to in 2009", "rocketjump", "2008-10-08 16:32", 21, 488, "NorthernLight", "2008-10-13 22:40"),
        ("Most played game of all time", "LANwolf", "2008-09-19 19:55", 33, 870, "dropbear", "2008-10-13 11:02"),
        ("Help: can't upload avatar, \"file too large\"", "sputnik", "2008-10-11 17:20", 3, 76, "Kestrel", "2008-10-11 19:04"),
        ("Unpopular gaming opinions", "ctrl_alt_defeat", "2008-08-28 22:45", 88, 2907, "halfpint", "2008-10-11 04:09"),
        ("Who has been here the longest?", "Vectrex_Kid", "2008-10-03 14:00", 26, 640, "QuakeWidow", "2008-10-10 18:30"),
        ("First game you ever played?", "jenn_plays", "2008-09-14 15:16", 47, 1205, "Trip_Wire", "2008-10-09 13:27"),
        ("Signature images -- 100px rule", "Kestrel", "2008-08-09 11:00", 9, 455, "Kestrel", "2008-10-08 09:41"),
        ("Gaming magazines -- does anyone still buy them?", "PolygonPete", "2008-09-02 12:20", 18, 407, "Vectrex_Kid", "2008-10-06 22:18"),
        ("Halloween costume ideas (gaming edition)", "sk8rgrl88", "2008-10-04 02:45", 12, 266, "jenn_plays", "2008-10-05 21:03"),
    ],
    4: [
        ("Audiosurf -- best $10 on Steam", "sputnik", "2008-09-15 20:00", 12, 290, "rocketjump", "2008-10-01 21:30"),
        ("UT3 -- is anyone still playing?", "QuakeWidow", "2008-08-25 19:00", 20, 610, "LANwolf", "2008-09-30 22:10"),
        ("LAN game list -- vote for the TF2 maps", "LANwolf", "2008-10-04 15:30", 22, 515, "Trip_Wire", "2008-10-17 09:12"),
        ("Crysis Warhead -- runs better than Crysis?", "BrassMonkey", "2008-09-17 22:10", 29, 1044, "Trip_Wire", "2008-10-16 19:20"),
        ("Left 4 Dead -- preorder for early demo access?", "rocketjump", "2008-10-02 11:14", 25, 922, "LANwolf", "2008-10-16 22:31"),
        ("Mount & Blade -- worth $30?", "halfpint", "2008-09-20 03:44", 11, 308, "rocketjump", "2008-10-16 13:02"),
        ("Games for Windows Live -- why?", "ctrl_alt_defeat", "2008-09-26 19:26", 17, 520, "sputnik", "2008-10-15 23:19"),
        ("Quake Live beta invites", "QuakeWidow", "2008-08-14 15:02", 36, 1388, "rocketjump", "2008-10-15 18:47"),
        ("Warhammer Online -- anyone playing?", "sputnik", "2008-09-19 22:08", 14, 433, "halfpint", "2008-10-15 07:20"),
        ("Fallout 3 PC requirements thread", "halfpint", "2008-10-14 22:40", 9, 290, "BrassMonkey", "2008-10-15 02:55"),
        ("Company of Heroes -- still the best RTS?", "Trip_Wire", "2008-10-08 10:30", 6, 177, "LANwolf", "2008-10-14 20:13"),
        ("GTA IV for PC in December -- will it run?", "ctrl_alt_defeat", "2008-08-07 18:12", 31, 1210, "Vectrex_Kid", "2008-10-13 21:00"),
        ("Red Alert 3 beta impressions", "LANwolf", "2008-09-29 20:44", 10, 351, "PolygonPete", "2008-10-13 16:37"),
        ("Counter-Strike: Source -- still playing?", "NorthernLight", "2008-09-09 01:12", 13, 402, "rocketjump", "2008-10-12 22:10"),
        ("King's Bounty: The Legend -- hidden gem", "Vectrex_Kid", "2008-10-04 13:20", 5, 119, "Kestrel", "2008-10-12 15:44"),
        ("Sins of a Solar Empire -- multiplayer night?", "Trip_Wire", "2008-09-30 20:10", 4, 98, "BrassMonkey", "2008-10-11 23:31"),
        ("Age of Conan -- three months later", "halfpint", "2008-08-20 04:01", 27, 912, "sputnik", "2008-10-10 12:08"),
        ("Penny Arcade Adventures Ep. 2 out soon", "PolygonPete", "2008-10-01 17:40", 3, 102, "halfpint", "2008-10-09 08:55"),
        ("Mods to play while waiting for Fallout 3", "rocketjump", "2008-10-02 21:30", 16, 488, "Trip_Wire", "2008-10-08 20:04"),
        ("Fraps alternatives?", "BrassMonkey", "2008-10-03 05:12", 7, 166, "ctrl_alt_defeat", "2008-10-05 14:27"),
    ],
    5: [
        ("Lost Odyssey -- finally finished it", "MoogleKnight", "2008-08-14 01:00", 8, 240, "NorthernLight", "2008-10-04 19:45"),
        ("Bionic Commando Rearmed is brilliant", "Vectrex_Kid", "2008-08-14 18:00", 11, 330, "PolygonPete", "2008-10-03 12:00"),
        ("Release dates: Holiday 2008", "NorthernLight", "2008-08-30 12:00", 64, 4120, "NorthernLight", "2008-10-17 08:55", 1),
        ("Post your Gamertag / PSN ID / Friend Codes", "Kestrel", "2008-08-03 20:00", 151, 6210, "PipBoy3000", "2008-10-16 21:20", 1),
        ("Resistance 2 -- 60 player online!", "dropbear", "2008-10-05 07:22", 18, 610, "PolygonPete", "2008-10-16 22:46"),
        ("Animal Crossing: City Folk -- Wii Speak?", "jenn_plays", "2008-10-02 19:40", 13, 377, "MoogleKnight", "2008-10-16 20:12"),
        ("Disgaea 3 -- 9,999 levels of grinding", "MoogleKnight", "2008-09-02 22:30", 21, 540, "sputnik", "2008-10-16 11:30"),
        ("PS3 price cut -- worth it at $399?", "PolygonPete", "2008-08-19 14:10", 38, 1322, "dropbear", "2008-10-15 19:58"),
        ("Wii Music -- is Nintendo serious?", "QuakeWidow", "2008-07-16 02:30", 44, 1650, "jenn_plays", "2008-10-15 16:04"),
        ("Braid is on XBLA and it's brilliant", "Vectrex_Kid", "2008-08-07 16:10", 26, 890, "MoogleKnight", "2008-10-14 23:41"),
        ("Red Ring of Death -- third console", "NorthernLight", "2008-09-11 23:15", 31, 1012, "ctrl_alt_defeat", "2008-10-14 12:20"),
        ("Mirror's Edge demo?", "rocketjump", "2008-10-09 11:31", 8, 260, "NorthernLight", "2008-10-13 21:09"),
        ("Saints Row 2 -- better than GTA IV?", "halfpint", "2008-10-14 04:02", 9, 231, "PolygonPete", "2008-10-16 20:45"),
        ("Too Human -- so... yeah", "ctrl_alt_defeat", "2008-08-20 18:05", 19, 640, "halfpint", "2008-10-12 03:12"),
        ("Metal Gear Solid 4 -- spoiler thread", "dropbear", "2008-06-13 06:30", 82, 2944, "Kestrel", "2008-10-11 20:22"),
        ("Super Smash Bros. Brawl -- Wi-Fi lag", "jenn_plays", "2008-09-03 22:10", 16, 520, "MoogleKnight", "2008-10-10 22:41"),
        ("Valkyria Chronicles is out November", "MoogleKnight", "2008-10-01 17:00", 6, 188, "NorthernLight", "2008-10-09 07:15"),
        ("DSi -- worth upgrading?", "jenn_plays", "2008-10-02 12:20", 10, 302, "Vectrex_Kid", "2008-10-08 17:30"),
        ("Soulcalibur IV -- Vader or Yoda?", "PolygonPete", "2008-08-01 21:30", 23, 744, "sk8rgrl88", "2008-10-06 02:11"),
    ],
    6: [
        ("Router recommendations for gaming?", "jenn_plays", "2008-09-19 21:00", 9, 230, "Trip_Wire", "2008-10-02 22:30"),
        ("Arctic Silver 5 vs MX-2", "BrassMonkey", "2008-09-01 18:20", 14, 380, "LANwolf", "2008-10-01 08:10"),
        ("Read before posting: how to ask for help", "Trip_Wire", "2006-11-04 10:00", 0, 3320, "Trip_Wire", "2006-11-04 10:00", 1, True),
        ("First build -- please check my parts list", "PipBoy3000", "2008-10-16 20:15", 5, 74, "Trip_Wire", "2008-10-17 09:01"),
        ("Netbooks: Eee PC 1000H or Aspire One?", "sputnik", "2008-09-28 18:40", 17, 511, "PolygonPete", "2008-10-16 15:33"),
        ("Dell 2408WFP input lag -- noticeable?", "NorthernLight", "2008-09-17 22:05", 12, 398, "ctrl_alt_defeat", "2008-10-16 10:25"),
        ("PhysX on GeForce 8 -- does it do anything?", "rocketjump", "2008-08-14 09:00", 20, 755, "Trip_Wire", "2008-10-15 21:12"),
        ("Antec 900 vs Cooler Master 690", "halfpint", "2008-10-06 04:30", 11, 287, "BrassMonkey", "2008-10-15 03:40"),
        ("Vista SP1 or stay on XP?", "QuakeWidow", "2008-08-22 18:55", 40, 1412, "ctrl_alt_defeat", "2008-10-14 18:09"),
        ("E8400 vs Q9450 for gaming", "BrassMonkey", "2008-09-05 16:40", 28, 945, "Trip_Wire", "2008-10-14 08:44"),
        ("Water cooling: first loop questions", "LANwolf", "2008-07-26 13:11", 34, 1180, "Trip_Wire", "2008-10-13 19:30"),
        ("Laptop for college, under $1000", "jenn_plays", "2008-08-11 20:02", 19, 563, "Vectrex_Kid", "2008-10-12 21:48"),
        ("How much RAM for Vista 64?", "sputnik", "2008-10-11 23:03", 8, 201, "LANwolf", "2008-10-12 10:04"),
        ("HD 4850 single slot cooler -- running hot", "ctrl_alt_defeat", "2008-07-30 21:20", 22, 921, "BrassMonkey", "2008-10-11 17:16"),
        ("Recommend a 5.1 headset", "sk8rgrl88", "2008-09-23 03:15", 9, 260, "PolygonPete", "2008-10-10 13:27"),
        ("Corsair 650TX or Antec Neo 650?", "halfpint", "2008-09-30 01:12", 6, 154, "Trip_Wire", "2008-10-08 22:00"),
        ("Overclocking competition: October", "BrassMonkey", "2008-10-01 18:00", 13, 405, "BrassMonkey", "2008-10-07 21:44"),
        ("Home server -- WHS or Linux?", "Vectrex_Kid", "2008-09-15 20:20", 15, 377, "sputnik", "2008-10-06 14:30"),
        ("Dead pixel policy -- which brands?", "dropbear", "2008-09-27 09:42", 7, 189, "NorthernLight", "2008-10-04 23:58"),
        ("Keyboard recommendations (mechanical?)", "rocketjump", "2008-09-21 17:10", 18, 520, "Vectrex_Kid", "2008-10-03 18:18"),
    ],
    8: [
        ("The Office (US) season 5", "halfpint", "2008-09-26 03:30", 11, 260, "jenn_plays", "2008-10-05 20:44"),
        ("The Dark Knight -- second viewing thread (spoilers)", "Kestrel", "2008-07-19 20:00", 96, 3950, "halfpint", "2008-10-17 05:44"),
        ("Election 2008 -- keep it civil or keep it out", "QuakeWidow", "2008-09-01 12:00", 0, 1240, "QuakeWidow", "2008-09-01 12:00", 1, True),
        ("Rate the desktop above you", "MoogleKnight", "2008-08-10 23:12", 77, 2633, "BrassMonkey", "2008-10-17 14:58"),
        ("Fringe -- worth watching?", "sputnik", "2008-09-17 16:30", 14, 377, "Kestrel", "2008-10-16 22:08"),
        ("Heroes season 3 -- already lost", "halfpint", "2008-09-23 04:15", 22, 560, "QuakeWidow", "2008-10-16 18:51"),
        ("What did you have for dinner?", "dropbear", "2008-03-12 09:20", 412, 9122, "sk8rgrl88", "2008-10-16 03:05"),
        ("Facebook or MySpace?", "jenn_plays", "2008-08-30 20:20", 31, 935, "PolygonPete", "2008-10-15 19:10"),
        ("Twitter -- does anyone use this?", "Vectrex_Kid", "2008-09-08 13:00", 16, 388, "sputnik", "2008-10-15 13:20"),
        ("Iron Man on DVD -- extended scenes?", "rocketjump", "2008-09-30 18:44", 9, 246, "NorthernLight", "2008-10-14 21:19"),
        ("Post your pets", "jenn_plays", "2008-02-14 18:30", 138, 4410, "MoogleKnight", "2008-10-14 13:22"),
        ("WALL-E -- Pixar did it again", "MoogleKnight", "2008-07-02 22:00", 28, 870, "jenn_plays", "2008-10-13 23:54"),
        ("Breaking Bad -- anybody watching?", "PolygonPete", "2008-03-20 22:00", 12, 344, "Vectrex_Kid", "2008-10-12 20:40"),
        ("xkcd -- favourite strips", "Vectrex_Kid", "2008-08-21 15:10", 34, 1120, "rocketjump", "2008-10-12 09:15"),
        ("Coffee or tea? (the eternal debate)", "sk8rgrl88", "2008-09-04 08:00", 47, 1066, "halfpint", "2008-10-11 06:30"),
        ("Gas prices -- $4 a gallon here", "Trip_Wire", "2008-06-20 14:20", 39, 1250, "LANwolf", "2008-10-10 18:15"),
        ("Recommend me a book", "Kestrel", "2008-08-27 21:00", 30, 810, "QuakeWidow", "2008-10-09 23:01"),
        ("Last.fm users -- post your profiles", "sputnik", "2008-09-11 01:15", 15, 404, "LANwolf", "2008-10-08 12:40"),
        ("Mythbusters -- best episode", "halfpint", "2008-09-26 03:20", 19, 452, "Trip_Wire", "2008-10-07 21:05"),
        ("Back to school / uni thread", "rocketjump", "2008-09-01 10:30", 25, 612, "MoogleKnight", "2008-10-06 22:22"),
    ],
}
