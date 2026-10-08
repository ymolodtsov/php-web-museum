"""Inkwell: a forum for webcomic creators and readers, as of 27 March 2007 (MyBB 1.2.3).

Times are board-local (the board's default time zone is GMT-5, as most US admins set it)
and are written "YYYY-MM-DD HH:MM". gen_seed.py turns this into SQL for MyBB's own tables.
Text is MyCode, stored the way MyBB stores it (raw, parsed on display).
"""

NOW = "2007-03-27 16:14"          # board-local; = 21:14 UTC, the libfaketime start
TZ_OFFSET = -5                     # board default time zone (settings: timezoneoffset)

# uid, username, usergroup, regdate, birthday (j-n-Y or ""), location, sex, website, avatar,
# custom usertitle, aim/msn/icq/yahoo, signature, lastactive (board-local), timeonline (hours)
MEMBERS = [
    (1, "Quillfeather", 4, "2005-08-14 22:05", "9-11-1978", "Portland, Oregon", "Female",
     "http://www.lanternfishcomic.com/", "butterfly.gif", "", ("", "quillfeather@hotmail.com", "", ""),
     "[b][url=http://www.lanternfishcomic.com/]Lanternfish[/url][/b] - a fantasy comic about a lighthouse at the bottom of the sea. Updates M/W/F.",
     None, 610),
    (2, "inkslinger_dave", 6, "2005-08-15 09:41", "2-6-1981", "Columbus, Ohio", "Male",
     "http://cubiclefauna.comicgen.com/", "stimpy.gif", "Resident Grump", ("inkslingerdave", "", "", ""),
     "[url=http://cubiclefauna.comicgen.com/]Cubicle Fauna[/url] -- the office is a jungle. Daily strip since 2004.",
     "2007-03-27 16:03", 455),
    (3, "mothlight", 2, "2005-09-02 01:17", "14-7-1985", "Vancouver, BC", "Female",
     "http://hollowhill.smackjeeves.com/", "courage.jpg", "", ("", "", "", ""),
     "[i]Hollow Hill[/i] - chapter 4 is up! [url=http://hollowhill.smackjeeves.com/]read from the start[/url]",
     None, 388),
    (4, "halftone_harriet", 2, "2005-09-20 19:30", "", "Baltimore, MD", "Female",
     "", "", "Bristol Board Snob", ("", "", "", ""),
     "Real ink. Real paper. Real smudges.",
     "2007-03-27 09:03", 240),
    (5, "gutterpunk", 2, "2005-11-03 23:48", "22-1-1982", "Austin, TX", "Male",
     "http://www.staticorbit.net/", "athlon.gif", "", ("gutterpunk82", "", "", ""),
     "[url=http://www.staticorbit.net/]STATIC ORBIT[/url] :: space junk, bad decisions :: new page every Tuesday",
     "2007-03-27 13:30", 301),
    (6, "zipatone", 2, "2005-12-11 15:20", "27-3-1968", "Minneapolis, MN", "Male",
     "", "", "", ("", "", "", ""),
     "Been making comics since you needed a photocopier and a stapler.",
     "2007-03-27 08:20", 150),
    (7, "Kirabel", 2, "2006-01-08 06:12", "3-9-1984", "Melbourne, Australia", "Female",
     "http://kirabel.deviantart.com/", "blue_bg.gif", "", ("", "kirabel_art@hotmail.com", "", ""),
     "Colourist for hire - [url=http://kirabel.deviantart.com/]gallery on dA[/url]",
     "2007-03-27 06:31", 270),
    (8, "cobaltjay", 2, "2006-02-19 20:02", "", "Glasgow, Scotland", "Male",
     "", "spam.gif", "", ("", "", "", ""),
     "[b]Rust Belt Knights[/b] on Drunk Duck. Robots. Pubs. Robots in pubs.",
     "2007-03-26 21:30", 120),
    (9, "Sketchwerk", 2, "2006-03-30 12:44", "", "San Jose, CA", "Male",
     "", "suckxp.gif", "", ("sketchwerk", "", "", ""),
     "Graphic designer by day, terrible cartoonist by night.",
     None, 210),
    (10, "Pagecount", 2, "2006-04-17 21:15", "", "Chicago, IL", "Male",
     "", "", "", ("", "", "", ""),
     "I don't draw, I just read everything.",
     "2007-03-26 22:15", 140),
    (11, "Brushfire", 2, "2006-05-22 17:39", "30-3-1987", "Sacramento, CA", "Female",
     "", "", "", ("", "", "", ""),
     "Manga Studio or bust.",
     "2007-03-26 20:05", 165),
    (12, "MarginNotes", 2, "2006-06-30 10:58", "", "Boston, MA", "Female",
     "", "", "", ("", "", "", ""),
     "",
     "2007-03-24 12:40", 60),
    (13, "pixelpatch", 2, "2006-07-12 16:03", "8-4-1990", "Dayton, Ohio", "Male",
     "", "supertux.gif", "", ("pixelpatch90", "", "", ""),
     "[b]Respawn Point[/b] - a sprite comic (all original sprites now!)",
     "2007-03-26 17:32", 95),
    (14, "ProjectPete", 2, "2006-10-28 13:27", "", "Seattle, WA", "Male",
     "", "", "", ("", "", "", ""),
     "",
     "2007-03-26 13:02", 70),
    (15, "tonerkid", 2, "2006-11-19 19:46", "17-10-1990", "Fresno, CA", "Male",
     "", "", "", ("", "", "", ""),
     "",
     "2007-03-25 21:44", 45),
    (16, "fennec_ink", 2, "2006-12-02 08:31", "", "Utrecht, Netherlands", "Female",
     "", "", "", ("", "", "", ""),
     "[i]Tea & Tentacles[/i] - coming soon, honestly",
     "2007-03-27 05:10", 40),
    (17, "nibpoint", 2, "2007-01-10 20:55", "", "Toronto, ON", "Male",
     "", "", "", ("", "", "", ""),
     "",
     "2007-03-23 22:30", 25),
    (18, "Rook", 2, "2007-02-05 14:10", "", "Atlanta, GA", "Male",
     "", "", "", ("", "", "", ""),
     "",
     "2007-03-21 19:05", 12),
    (19, "lunchbox_legion", 2, "2007-02-27 23:02", "", "Denver, CO", "Female",
     "", "", "", ("", "", "", ""),
     "",
     None, 9),
    (20, "Ollie_V", 2, "2007-03-26 19:22", "", "Leeds, UK", "Male",
     "", "", "", ("", "", "", ""),
     "",
     None, 1),
]

# Who is on the board at the archive moment (minutes before NOW, location).
# (uid, minutes before the capture, location). lunchbox_legion browses invisibly.
ONLINE = [
    (1, 1, "/showthread.php?tid={Photoshop CS3}"),
    (9, 2, "/showthread.php?tid={Photoshop CS3}"),
    (20, 4, "/showthread.php?tid={Spring Sketch Swap}"),
    (3, 7, "/forumdisplay.php?fid=5"),
    (2, 11, "/newreply.php?tid={Photoshop CS3}"),
    (19, 9, "/index.php"),
]
GUESTS = [
    (3, "/showthread.php?tid={Hollow Hill}"), (5, "/forumdisplay.php?fid=7"), (6, "/index.php"),
    (11, "/memberlist.php"), (13, "/showthread.php?tid={Webcomics you}"),
]
MOST_ONLINE = (27, "2007-01-14 21:37")

# fid, name, description, parent (0 = category), disporder
FORUMS = [
    (1, "General", "", 0, 1),
    (2, "Announcements", "News, rules and housekeeping from the staff.", 1, 1),
    (3, "Introductions", "New here? Say hi and tell us what you draw (or read).", 1, 2),
    (4, "Making Comics", "", 0, 2),
    (5, "Show &amp; Tell", "Post your comic and get feedback. One thread per comic, please, and bump it when you update.", 4, 1),
    (6, "Art &amp; Technique", "Pencils, inks, colours, lettering, page layout and writing.", 4, 2),
    (7, "Tools of the Trade", "Tablets, software, pens, paper and scanners.", 4, 3),
    (8, "Hosting &amp; Promotion", "Keenspot, Comic Genesis, Drunk Duck, Smack Jeeves, your own domain, ads and link swaps.", 4, 4),
    (9, "Everything Else", "", 0, 3),
    (10, "Off-Topic", "Anything that isn't comics. Or is comics, but in a movie.", 9, 1),
    (11, "Conventions &amp; Meetups", "Tabling, travel, hotels and meeting up in person.", 10, 1),
]
MODERATED = {"inkslinger_dave": [5, 6, 7, 8]}

# Post icons (mybb_icons): 0 none, 2 Exclamation, 3 Question, 4 Smile, 6 Wink, 7 Cool, 8 Big Grin, 10 Rolleyes
T = []


def topic(fid, subject, posts, icon=0, views=0, sticky=0, closed="", poll=None, edits=None):
    T.append(dict(fid=fid, subject=subject, posts=posts, icon=icon, views=views, sticky=sticky,
                  closed=closed, poll=poll, edits=edits or {}))


Q = "Quillfeather"; D = "inkslinger_dave"; M = "mothlight"; H = "halftone_harriet"; G = "gutterpunk"
Z = "zipatone"; K = "Kirabel"; C = "cobaltjay"; S = "Sketchwerk"; P = "Pagecount"; B = "Brushfire"
MN = "MarginNotes"; PX = "pixelpatch"; PP = "ProjectPete"; TK = "tonerkid"; F = "fennec_ink"
N = "nibpoint"; R = "Rook"; L = "lunchbox_legion"; O = "Ollie_V"

# ---------------------------------------------------------------- Announcements
topic(2, "Forum rules - please read before posting", [
    (Q, "2005-08-14 22:40", """Welcome to Inkwell! This is a forum for people who make webcomics and people who read them. A few ground rules:

[list=1]
[*]Be decent. Critique the work, not the person.
[*]Show & Tell is for your own comics. One thread per comic, and bump it when you update rather than starting a new one.
[*]No hotlinking huge images. If a page is wider than 800 pixels, post a thumbnail or a link.
[*]Link swaps and ads go in Hosting & Promotion, not in every thread you post in.
[*]Nothing you wouldn't want your mom to see in the main forums. If your comic is adult, say so and link to it.
[*]No warez. Don't ask for a "free" copy of Photoshop or Manga Studio here.
[/list]

That's it. Mods are inkslinger_dave and me. PM either of us if something's wrong.

- Jess"""),
], icon=2, views=1420, sticky=1, closed="yes")

topic(2, "Board upgraded to MyBB 1.2.3", [
    (Q, "2007-02-16 23:10", """Just upgraded the forum to MyBB 1.2.3, which came out on Wednesday. It's mostly bug fixes plus a couple of security patches, so nothing should look different.

If something is broken (avatars, signatures, the calendar, anything) post here and I'll take a look."""),
    (D, "2007-02-17 08:44", "Quick reply box seems faster. Or I'm imagining it."),
    (C, "2007-02-17 10:31", "My avatar went back to the spam can. Was it always the spam can? I think it was always the spam can."),
    (Q, "2007-02-17 11:02", """[quote=cobaltjay]My avatar went back to the spam can.[/quote]
It was always the spam can, you picked it in October. ;)"""),
    (TK, "2007-02-18 19:27", "is there a way to make my signature smaller? it has a huge line break under it"),
    (Q, "2007-02-18 21:50", "That's just how the default theme spaces it. Take out the empty line at the end of your signature in the User CP and it'll tighten up a bit."),
], icon=1, views=388)

topic(2, "Spring Sketch Swap 2007 - sign-ups open until March 31", [
    (Q, "2007-03-12 20:15", """It's back! Same as last year:

[b]How it works[/b]
[list]
[*]Reply here to sign up before [b]Saturday March 31[/b].
[*]On April 1 I'll PM everyone the name and mailing address of the person they're drawing for.
[*]Draw them something on real paper, any size up to 11x17, any medium. Their characters, your characters, a crossover, whatever.
[*]Mail it by [b]April 21[/b]. Post a scan in this thread when yours arrives.
[/list]

International is fine, just be prepared to pay postage. Last year we had 14 people and only one envelope went missing (sorry Pagecount)."""),
    (D, "2007-03-12 20:40", "In. Again. I will draw your characters as office animals whether you like it or not."),
    (H, "2007-03-12 21:12", "In. Bristol, ink, maybe a little grey wash if I'm feeling fancy."),
    (M, "2007-03-13 00:03", "Sign me up! Canada again, so I'll mail early."),
    (P, "2007-03-13 09:17", """[quote=Quillfeather]only one envelope went missing (sorry Pagecount)[/quote]
I'm still not over it. In anyway, I'll do stick figures with very sincere feelings."""),
    (K, "2007-03-13 18:40", "In! Australia is a long way, so I'll post mine the first week."),
    (G, "2007-03-14 22:05", "Count me in."),
    (F, "2007-03-17 06:44", "Can I join even though Tea & Tentacles isn't up yet? I have characters, they just live in a sketchbook."),
    (Q, "2007-03-17 10:20", "Of course. Sketchbook characters count."),
    (B, "2007-03-19 17:55", "In! Is it OK if I do mine digitally and print it out? My inking on paper is... a work in progress."),
    (H, "2007-03-19 18:30", "Brushfire, that's what the swap is for! Go on, get some ink on your fingers. :P"),
    (B, "2007-03-19 19:02", "Fiiiine. Paper it is."),
    (Z, "2007-03-24 11:40", "I'm in. Will include a free zine from 1996 whether you want it or not."),
    (O, "2007-03-27 15:58", "Just joined yesterday - is it too late to sign up? I can do a proper drawing, promise."),
], icon=8, views=512, sticky=1)

# ---------------------------------------------------------------- Introductions
topic(3, "Long time lurker, first post", [
    (MN, "2006-07-01 13:20", """Hi all. I've been reading this forum since last winter without an account. I don't draw at all, I just read way too many webcomics (my bookmarks folder is a disaster) and I run a small LiveJournal community where we post links to new comics we find.

Mostly here to say thanks for the Show & Tell threads, that's where I found Hollow Hill and Cubicle Fauna."""),
    (M, "2006-07-01 15:02", "Aww, thank you! Welcome! What's the LJ community called?"),
    (MN, "2006-07-01 15:40", "It's tiny, about 200 watchers. I'll put it in Hosting & Promotion if that's allowed, don't want to spam."),
    (Q, "2006-07-01 17:11", "Totally allowed in Hosting & Promotion. Welcome aboard!"),
    (G, "2006-07-02 00:15", "A reader who says nice things about Static Orbit? Welcome, please stay forever."),
], icon=4, views=231)

topic(3, "Hello from Fresno", [
    (TK, "2006-11-19 20:10", "hi. im 16 and i draw a comic called Dumpster Kingdom about raccoons who run a city out of a dumpster. i draw on a Graphire3 that my uncle gave me. i want to get better at backgrounds"),
    (D, "2006-11-19 21:30", "Raccoon city-state in a dumpster is a great premise. Welcome. Backgrounds are everyone's weak spot, there's a thread about it in Art & Technique."),
    (H, "2006-11-20 08:02", "Welcome! Draw buildings from life. Sit outside a gas station with a sketchbook for an hour. Seriously."),
    (TK, "2006-11-20 16:44", "ok ill try that. thanks"),
    (K, "2006-11-21 05:30", "Welcome! Raccoons are very underrated comic animals."),
], views=164)

topic(3, "Manga Studio convert says hi", [
    (B, "2006-05-22 18:10", """Hi everyone! I'm Brushfire, I'm 19 and I just switched my whole process to Manga Studio after years of Photoshop and a lot of crying over screentones. I'm working on a shoujo-ish story called Glass Garden that I want to start posting this summer.

I found you guys through Quillfeather's Lanternfish links page. :D"""),
    (Q, "2006-05-22 19:47", "Oh nice, I'm flattered! Welcome!"),
    (M, "2006-05-22 22:30", "Another Manga Studio person! We should start a club."),
    (B, "2006-05-23 15:05", "Yes please. I have so many questions about the rulers."),
], icon=8, views=198)

topic(3, "New here - Ollie from Leeds", [
    (O, "2007-03-26 19:41", """Hello! Found this place through a link on Cubicle Fauna. I'm 24, I work in a print shop, and I've been drawing a comic about two postmen in Yorkshire for about a year but never put it online. Thinking of finally doing it this spring.

Not sure yet whether to go with Comic Genesis, Drunk Duck or get my own site. Any advice welcome, I'll go read the Hosting forum."""),
    (D, "2007-03-26 20:02", "Welcome! Glad the strip sent someone here and not just my mom. Yorkshire postmen is a great setup."),
    (C, "2007-03-26 20:30", "Another UK member, excellent. Drunk Duck has a good crowd for newcomers. Read the hosting thread first though, it's got everything."),
    (Q, "2007-03-26 22:18", "Welcome Ollie! There's a Sketch Swap running right now if you want to jump in, sign-ups close Saturday."),
    (O, "2007-03-27 15:50", "Cheers everyone, off to sign up!"),
], icon=4, views=58)

# ---------------------------------------------------------------- Show & Tell
topic(5, "[Lanternfish] fantasy, updates M/W/F", [
    (Q, "2005-08-15 00:20", """Figured I should start the Show & Tell forum off with my own thing.

[b]Lanternfish[/b] is about Wren, a girl who keeps a lighthouse at the bottom of the sea for ships that sank a long time ago. It's watercolour, scanned, cleaned up in Photoshop. It updates Monday, Wednesday and Friday.

[url=http://www.lanternfishcomic.com/]www.lanternfishcomic.com[/url]

Be honest, I can take it."""),
    (D, "2005-08-15 09:58", "The water effects are gorgeous. The lettering is a little small on the first few pages though, I had to squint."),
    (Q, "2005-08-15 11:30", "Yeah, I know, I redid the font size from page 12 on. Going back to fix the early ones eventually."),
    (H, "2005-09-21 20:14", "Just read the whole archive in one sitting. The page where the ghost ship comes in is beautiful."),
    (M, "2006-03-03 01:45", "Bumping because chapter 3 just ended and I'm emotionally wrecked."),
    (Q, "2007-03-26 09:30", "Chapter 5 starts today! Also redid the whole site layout, it's 800 pixels wide now so it should look better on laptops."),
    (P, "2007-03-26 12:15", "New layout is a big improvement. The archive dropdown is much easier to use."),
    (K, "2007-03-27 06:20", "The colours on the chapter 5 cover are lovely. That teal!"),
], views=2264)

topic(5, "Cubicle Fauna - office animals, daily", [
    (D, "2005-08-15 10:30", """Gag-a-day strip about the animals who work at Consolidated Paper Supply. The boss is a badger. The intern is a very nervous ferret. I've been doing it on Keenspace since early 2004, Comic Genesis now I guess since they renamed.

[url=http://cubiclefauna.comicgen.com/]cubiclefauna.comicgen.com[/url]"""),
    (Z, "2005-12-12 09:10", "The fax machine strip got me. I worked in a place exactly like that."),
    (G, "2006-01-14 22:41", "Ferret is the best character. Give him a storyline."),
    (D, "2006-01-15 10:12", "He's getting one. It involves the copier."),
    (P, "2006-09-07 17:30", "Just wanted to say the copier arc was worth it."),
    (D, "2007-03-19 08:15", "Strip #800 went up today. Somehow I haven't missed a weekday in three years. My buffer is two strips. Pray for me."),
    (Q, "2007-03-19 09:40", "800! Congratulations Dave."),
    (C, "2007-03-19 12:02", "Absolute machine. 800 strips and I can't finish one page a week."),
], icon=8, views=1630)

topic(5, "Hollow Hill - chapter 4 is up!", [
    (M, "2006-02-10 02:12", """Hi! This is my comic, Hollow Hill. It's about three kids who find out the hill behind their school is hollow and full of very old, very polite monsters. It's black and white with screentones, I draw it in Manga Studio and post twice a week on Smack Jeeves.

[url=http://hollowhill.smackjeeves.com/]hollowhill.smackjeeves.com[/url]

Crit welcome, especially on the paneling!"""),
    (H, "2006-02-10 10:20", "Your blacks are really confident for screentone work. Page 6 is a little crowded, five panels plus all that dialogue. Maybe split it?"),
    (M, "2006-02-10 15:47", "You're right, I'll try to keep it to four panels max."),
    (MN, "2006-07-01 13:45", "This is one of my favourite comics, just saying."),
    (M, "2007-03-24 23:58", "Chapter 4 starts tonight! New cover page, and I'm finally doing a colour page for the chapter opener."),
    (B, "2007-03-25 00:30", "THE COLOUR PAGE. It's so pretty! What brushes did you use?"),
    (M, "2007-03-25 01:12", "Mostly the default airbrush on low opacity plus a watercolour texture overlay. I'll do a little walkthrough in Art & Technique."),
    (P, "2007-03-25 14:18", "The bit with the polite monster offering tea made me laugh out loud at work."),
    (F, "2007-03-27 05:02", "Read the whole thing last night instead of sleeping. No regrets."),
], icon=8, views=1188)

topic(5, "critique my first page please (be nice)", [
    (TK, "2006-11-25 21:10", """here is the first page of Dumpster Kingdom. the raccoon in the crown is King Tibbs.

[url=http://img.photobucket.com/albums/dk_page1.jpg]page 1[/url]

i know the background is bad"""),
    (D, "2006-11-25 22:02", """Not bad for a first page at all. A few things:
[list]
[*]Your speech bubbles are crowding the faces. Leave room for them when you pencil.
[*]Tibbs' crown changes size between panels 1 and 3.
[*]The background is actually fine, it's just all the same line weight as the characters. Use a thinner line for stuff that's further away.
[/list]"""),
    (H, "2006-11-26 09:44", "What Dave said about line weight. Thicker on the characters, thinner behind. Instant depth."),
    (K, "2006-11-26 17:10", "Love Tibbs' expression in the last panel. Very regal for a raccoon."),
    (TK, "2006-11-27 16:20", "thanks! ill redo the bubbles. the line weight thing is really helpful"),
    (TK, "2007-02-11 20:35", "update: redid page 1 and finished pages 2 to 9. [url=http://img.photobucket.com/albums/dk_page1b.jpg]new page 1[/url]"),
    (D, "2007-02-11 21:30", "Huge improvement. Look at those bubbles. Proud of you, kid."),
], icon=3, views=402)

topic(5, "STATIC ORBIT just hit page 100", [
    (G, "2007-03-20 22:10", """Page 100 went up tonight! For anyone who hasn't seen it: Static Orbit is about a salvage crew that pulls junk satellites out of orbit and keeps finding things they shouldn't. Updates every Tuesday on my own domain.

[url=http://www.staticorbit.net/]staticorbit.net[/url]

Two years, 100 pages, one dead scanner. Thanks to everyone here who gave crit along the way."""),
    (Q, "2007-03-20 22:33", "Congrats! The space-walk spread on page 99 was so good."),
    (S, "2007-03-21 01:02", "Nice milestone. The new logo looks sharp too."),
    (P, "2007-03-21 08:55", "Read from page 1 again to celebrate. The art change from page 1 to page 100 is wild."),
    (G, "2007-03-21 12:40", """[quote=Pagecount]The art change from page 1 to page 100 is wild.[/quote]
Please never link anyone to page 1."""),
    (C, "2007-03-21 13:15", "Everyone's page 1 is bad. That's the rule."),
    (Z, "2007-03-22 07:50", "100 pages is the point where it stops being a hobby and starts being a habit. Good on you."),
], icon=8, views=455)

topic(5, "Respawn Point (sprite comic) - honest crit?", [
    (PX, "2006-07-13 17:20", "This is my sprite comic Respawn Point. Its about two guys who live in a video game and know they are in a video game. I use sprites from old SNES games and edit them. Is it any good?"),
    (P, "2006-07-13 19:45", "The jokes are better than most sprite comics I've seen. But I recognize those sprites, and so will everyone else."),
    (D, "2006-07-13 20:30", "Seconding that. Ripped sprites will hold you back, a lot of readers skip sprite comics on sight. If you can edit sprites, you can make your own."),
    (PX, "2006-07-14 15:12", "ok. i didnt think of it like that"),
    (PX, "2006-12-30 14:25", "Update: I redrew everything with my own sprites! It took like four months. Still pixel art but its all original now."),
    (G, "2006-12-30 18:40", "That's a serious amount of work. They look good, the walk cycles especially."),
    (Q, "2006-12-30 21:02", "Look at that! Really nice job pixelpatch."),
], icon=3, views=377)

# ---------------------------------------------------------------- Art & Technique
topic(6, "Lettering: hand vs. fonts", [
    (H, "2006-04-02 19:20", "Hot take: hand lettering looks better than any font. Comic Sans is a crime. Discuss."),
    (D, "2006-04-02 19:55", "Nobody here uses Comic Sans, Harriet. I use one of the free Blambot fonts and it's saved me hours every week."),
    (Q, "2006-04-02 20:30", "I made a font from my own handwriting with one of those online services. Best of both worlds, except my lowercase e looks drunk."),
    (S, "2006-04-03 10:14", "Font for dialogue, hand-lettered sound effects. That's my rule."),
    (Z, "2006-04-03 18:02", "I hand-lettered with an Ames guide for ten years. My wrist does not miss it."),
    (H, "2006-04-03 18:40", "Fine. FINE. But you'll never get the bounce of a real hand-lettered word balloon."),
    (B, "2007-02-20 16:30", "Old thread but - does anyone letter in Manga Studio? The text tool is kind of awful."),
    (M, "2007-02-20 21:15", "I export the pages and letter in Photoshop. Manga Studio's text tool was clearly made by someone who never lettered a comic."),
], icon=3, views=644)

topic(6, "Brush vs. nib - the inking thread", [
    (H, "2006-01-22 14:10", """Let's settle this. What do you ink with?

Me: Winsor & Newton Series 7 #2 brush for figures, Hunt 102 for details, Microns for panel borders. Higher Ground or Speedball Super Black ink."""),
    (Z, "2006-01-22 15:40", "Hunt 102 for everything. I'm a simple man."),
    (Q, "2006-01-22 17:20", "Pentel pocket brush pen. Don't judge me."),
    (H, "2006-01-22 17:44", "Judging you a little."),
    (K, "2006-01-23 04:55", "I ink digitally in Photoshop with a hard round brush at 3px, pressure for size. Is that cheating?"),
    (D, "2006-01-23 08:30", "It's not cheating if it looks good. Mine are scanned Microns, very cheating by Harriet standards."),
    (N, "2007-01-12 20:10", "Bringing this back - any tips for brush inking? Every time I try the Series 7 my lines go everywhere."),
    (H, "2007-01-12 21:05", "Load the brush, then wipe most of it off on the side of the jar. Rest your hand on a scrap of paper, pull the line towards you, don't push. And practice on cheap paper, a whole page of just lines and circles every day for a week."),
    (N, "2007-01-13 18:22", "Did 2 pages of lines tonight. They're better already. Thanks!"),
], icon=0, views=811)

topic(6, "How far ahead is your buffer?", [
    (C, "2007-03-05 19:30", "Honest answers. How many pages/strips are you ahead? I am currently -1. I owe my readers a page from last week."),
    (D, "2007-03-05 19:58", "Two strips. It was 20 at the start of last year."),
    (G, "2007-03-05 21:10", "Six pages. I won't launch a new chapter until I have the whole thing pencilled."),
    (Q, "2007-03-05 22:40", "About three weeks. The watercolours take forever so I have to stay ahead."),
    (M, "2007-03-06 00:15", "I live in fear and update the night it goes up. Please don't tell my readers."),
    (P, "2007-03-06 08:50", "As a reader: I would rather have a late page than a filler page. Just post a sketch and say it'll be late."),
    (C, "2007-03-06 12:05", "Noted. Sketch going up tonight then."),
], icon=3, views=296)

topic(6, "Flatting and colouring in Photoshop - a walkthrough", [
    (K, "2006-08-14 06:40", """People keep asking how I colour, so here's my process for a typical page:

[list=1]
[*]Scan inks at 600dpi, bitmap mode, clean up, then convert to greyscale and then RGB.
[*]Put the lineart layer on top, set to Multiply.
[*]Flats: a new layer under the lines. Magic wand with anti-alias OFF on the lineart, fill each area with a flat colour. Every object gets its own colour, even if it'll end up the same.
[*]Lock transparency on the flats layer, then shade on a layer above with a hard brush, layer set to Multiply.
[*]Lighting on another layer set to Screen or Overlay.
[*]Flatten a copy, resize to 900 pixels wide, Save for Web as JPG around quality 70.
[/list]

The flats step is boring but it makes everything after it ten times faster."""),
    (B, "2006-08-14 16:20", "Thank you SO much for this. The anti-alias off thing is what I was doing wrong."),
    (Q, "2006-08-14 19:30", "Stickying this in my brain. Also bookmarking."),
    (S, "2006-08-15 11:02", "Pro tip: record the flats cleanup as an Action and bind it to an F-key."),
    (TK, "2007-02-15 19:44", "this helped so much. what do you do about gaps in the lineart, the fill goes everywhere"),
    (K, "2007-02-16 05:10", "Close the gaps on a separate layer with a 1px pencil before you fill, then delete that layer. Or just fix them in the inks, it's good practice!"),
], icon=0, views=1355)

topic(6, "Mothlight's colour page walkthrough (Hollow Hill ch. 4)", [
    (M, "2007-03-26 01:30", """As promised! Here's how I did the chapter 4 colour page.

1. Inks done in Manga Studio, exported as a 600dpi PSD.
2. Flats the Kirabel way (thanks!!).
3. Shadows: one Multiply layer in a lavender colour instead of grey. This is the big trick, grey shadows look dead.
4. Airbrush on a Soft Light layer for the glow from the lanterns.
5. A scanned watercolour paper texture over everything on Overlay at about 30%.

Took about 9 hours total. Probably not doing that every chapter."""),
    (K, "2007-03-26 05:50", "Lavender shadows!! You learned well. :D"),
    (B, "2007-03-26 18:40", "The texture overlay is genius. Trying it this weekend."),
    (H, "2007-03-27 09:03", "I don't colour but this was a nice read. The lantern glow is lovely."),
], icon=0, views=143)

# ---------------------------------------------------------------- Tools of the Trade
topic(7, "Photoshop CS3 beta - anyone tried it?", [
    (S, "2006-12-16 13:05", """Adobe put out a public beta of Photoshop CS3 yesterday. It's free to try until sometime in the spring if you already own CS2. Big news for Mac people: it runs natively on the Intel Macs.

I've been playing with it all morning. Quick Selection tool is nice, the new panels collapse into icons, and it starts up a lot faster than CS2 on my machine."""),
    (G, "2006-12-16 15:30", "Finally. CS2 under Rosetta on my MacBook is painful."),
    (Q, "2006-12-16 19:12", "Is it stable enough to do real pages in?"),
    (S, "2006-12-16 20:20", "Crashed on me once. I wouldn't use it for anything with a deadline, keep CS2 around."),
    (K, "2006-12-18 06:44", "The new Black & White adjustment is great for greytones, way better than desaturate."),
    (B, "2007-01-04 17:15", "Does it still need a serial from CS2? I only have Elements."),
    (S, "2007-01-04 18:30", "Yeah, you need a CS2 serial for the beta."),
    (G, "2007-03-27 13:22", "Adobe just announced CS3 for real today. Photoshop should ship in April."),
    (S, "2007-03-27 15:40", """Prices are out: Photoshop CS3 is $649, $199 to upgrade from CS2. There's also a new Photoshop CS3 Extended for $999 with 3D and video stuff none of us need.

The beta runs out once the real one ships, so plan accordingly."""),
    (D, "2007-03-27 16:02", "$199 isn't terrible. Still running CS on a Windows 2000 box over here, so maybe it's time."),
], icon=7, views=902)

topic(7, "Graphire4 or save up for an Intuos3?", [
    (N, "2007-01-18 21:40", "I've got about $120. Get the Graphire4 6x8 now or wait a couple months and get an Intuos3 6x8? I mostly ink and colour, no painting."),
    (S, "2007-01-18 22:10", "Intuos3 has way more pressure levels (1024 vs 512) and the tilt sensing. If you can wait, wait."),
    (K, "2007-01-19 05:15", "I've had an Intuos3 6x8 for two years and it's the best money I've spent on art. The express keys are great too."),
    (TK, "2007-01-19 16:45", "my graphire3 is fine for everything i do. but its small"),
    (H, "2007-01-19 18:00", "Or buy a good brush and a bottle of ink for $20 and keep the change. Just saying."),
    (N, "2007-01-20 12:30", "Harriet I KNEW you'd say that. Waiting for the Intuos3, thanks all."),
    (N, "2007-03-23 22:30", "Update: got the Intuos3 6x8 off eBay for $230. It's amazing. The Graphire would've been fine but this is so much nicer."),
], icon=3, views=468)

topic(7, "Manga Studio EX 3 - worth the upgrade from Debut?", [
    (B, "2006-11-08 18:20", "Debut is starting to feel limiting. EX 3.0 is pricey though. Anyone using EX who can say if it's worth it?"),
    (M, "2006-11-08 21:45", """I use EX. Things you get that Debut doesn't:
[list]
[*]All the screentones, not just a handful
[*]Perspective and parallel rulers (a lifesaver for backgrounds)
[*]Multiple pages / story files
[*]Better export options
[/list]
If you do a lot of buildings or tone, it's worth it. If you mostly do characters, Debut is fine."""),
    (B, "2006-11-09 14:10", "The perspective rulers... I'm sold. My backgrounds are tragic."),
    (S, "2006-11-09 17:30", "Check if there's a student discount. e frontier had one last year."),
    (B, "2006-12-26 13:00", "Christmas money -> Manga Studio EX. Perspective rulers are everything I dreamed."),
], icon=3, views=377)

topic(7, "Scanner for 11x17 originals?", [
    (H, "2006-10-02 20:15", "I draw on 11x17 Strathmore 500 bristol and my scanner is letter size. Anyone have a tabloid size scanner they'd recommend that doesn't cost $1000?"),
    (Z, "2006-10-02 21:30", "Scan in two halves and stitch them in Photoshop with the layer on Difference to line it up. It's what everyone does."),
    (G, "2006-10-02 22:40", "My old Epson died doing exactly that, 200 pages of two-half scans. RIP."),
    (S, "2006-10-03 09:50", "Photomerge in CS2 can stitch them automatically, if your halves overlap by an inch or so."),
    (H, "2006-10-03 18:22", "Photomerge it is. Thanks Sketchwerk."),
    (D, "2006-10-03 19:10", "Or draw on 10x15 and save yourself the trouble. That's what I switched to."),
], icon=3, views=312)

topic(7, "How do you make your final art?", [
    (Q, "2007-03-08 21:00", "Curious how everyone works these days. Pick the one closest to how you make your [i]final[/i] pages, not your sketches."),
    (H, "2007-03-08 21:10", "Paper all the way. Shocking, I know."),
    (K, "2007-03-09 05:22", "Pencils on paper, scan, ink and colour in Photoshop."),
    (B, "2007-03-09 14:15", "Manga Studio from start to finish now!"),
    (PX, "2007-03-09 16:02", "Is pixel art \"fully digital\"? I picked that one."),
    (Q, "2007-03-09 17:30", "Yep, pixel art counts as digital."),
    (C, "2007-03-10 11:45", "Flash. Rust Belt Knights is all vector. Nobody ever believes me."),
    (G, "2007-03-11 23:10", "Pencils and inks on paper, colour in Photoshop. Old school but the colours are the fun part."),
], icon=3, views=301, poll=dict(
    question="How do you make your final art?",
    options=["Pencils and inks on paper, scanned", "Pencils on paper, digital inks", "Fully digital (Photoshop, Painter, pixel art)",
             "Manga Studio", "Vector / Flash", "I don't draw, I just read"],
    votes={H: 1, Z: 1, G: 1, D: 1, K: 2, Q: 2, S: 2, TK: 2, F: 2, B: 4, M: 4, N: 4, PX: 3, C: 5, P: 6, MN: 6, L: 6, R: 6},
    dateline="2007-03-08 21:00"))

# ---------------------------------------------------------------- Hosting & Promotion
topic(8, "Project Wonderful - anyone tried it?", [
    (PP, "2006-10-29 14:00", """Has anyone tried Project Wonderful yet? It's a new ad service from Ryan North (Dinosaur Comics). Instead of paying per click, people bid for your ad box by the day, and whoever bids highest gets the spot. Lots of boxes are going for $0.00 a day right now, so it's basically free advertising.

I put a box on my site yesterday and someone's already bidding 3 cents. Riches!"""),
    (D, "2006-10-29 15:20", "Signed up. The interface is very clean. No pop-ups, no punch-the-monkey ads, which is why I never did Google ads."),
    (G, "2006-10-30 00:40", "I bid $0.05/day on a couple of bigger comics. Got more new readers in a week than from a year of link swaps."),
    (M, "2006-10-30 13:10", "Smack Jeeves lets you put the code in your template, I just added a box. Thanks for the tip!"),
    (PP, "2007-01-15 19:30", "Three-month report: my box made $11.42. Spent $9.00 on ads elsewhere. I am a business genius."),
    (C, "2007-01-15 20:10", "You're in profit! That's more than most of us."),
    (PP, "2007-03-26 13:02", "Bump - my box is up to 9 cents a day now. Still the best ad thing going for small comics."),
], icon=0, views=692)

topic(8, "Comic Genesis down again?", [
    (D, "2007-03-14 07:30", "Is everyone else's CG site down or is it just me? Strip didn't go up this morning and I can't get into the FTP."),
    (C, "2007-03-14 07:52", "It's not just you. The forums are down too."),
    (Q, "2007-03-14 09:10", "This is the third time this month. I love CG for getting me started but I'm so glad I moved to my own domain."),
    (D, "2007-03-14 13:44", "Back up. Autokeen posted the strip late. Good thing I wasn't paying for it. Oh wait."),
    (P, "2007-03-14 14:20", "Readers notice, but we also forgive. Everyone knows CG is like this."),
    (Q, "2007-03-14 15:30", "Dave, if you ever want to move, DreamHost is about $8 a month and I'm happy to help set up the site."),
    (D, "2007-03-14 16:05", "I might take you up on that. Eight hundred strips to move though..."),
], icon=5, views=284)

topic(8, "Drunk Duck vs Smack Jeeves vs your own domain", [
    (O, "2007-03-26 20:50", "As promised in my intro thread: where should a brand new comic go? I'm leaning towards Drunk Duck because of the community, but I'm worried about looking amateur."),
    (C, "2007-03-26 21:12", "Drunk Duck pros: built-in readers, people actually comment, the front page can send you a lot of traffic. Cons: the URL, and the site can be slow."),
    (M, "2007-03-26 21:40", "Smack Jeeves gives you more control over your layout, which is why I picked it. The community is smaller though."),
    (Q, "2007-03-26 22:30", """Own domain if you're serious about it long-term, but there are no readers there until you bring them. A lot of people start on Drunk Duck or SJ and move once they have an archive. If you do, put a big link on the old site pointing to the new one.

Whatever you pick, buy the .com for your title now. It's $9 and you'll regret it if someone else grabs it."""),
    (G, "2007-03-26 23:40", "+1 to buying the domain now. And launch with at least 10 pages up and a buffer."),
    (O, "2007-03-27 09:15", "Bought the domain last night! Going to start on Drunk Duck and see how it goes. Thanks, all."),
], icon=3, views=97)

topic(8, "Keenspot submissions - anyone ever got in?", [
    (R, "2007-02-06 18:30", "Long time Keenspot reader. Has anyone here ever applied to Keenspot? What does it take?"),
    (D, "2007-02-06 19:10", "I applied in 2005 and never heard back. As far as I can tell, you need a big audience before they notice you, and by then you don't really need them."),
    (P, "2007-02-06 20:02", "The only Keenspot comics I still read every day are the old ones. Most of my favourites now are independent."),
    (Z, "2007-02-07 08:20", "The landscape's changed a lot. Ten years ago being on a collective was the only way to be seen. Now you've got Project Wonderful and LiveJournal and DeviantArt and people just find you."),
    (R, "2007-02-07 17:45", "That makes sense. Guess I'll just make the thing first."),
    (Q, "2007-02-07 18:30", "Best advice there is. Make the thing first."),
], icon=3, views=255)

topic(8, "Link and banner swap thread (post yours here)", [
    (Q, "2006-02-01 20:00", "Instead of a hundred \"link me!\" threads, let's keep them all here. Post your 88x31 button or 468x60 banner and what kind of comic you're looking to swap with."),
    (G, "2006-02-01 21:30", "Static Orbit, sci-fi, looking for other sci-fi or adventure comics. 88x31 button on the links page."),
    (M, "2006-02-10 02:30", "Hollow Hill, fantasy/all ages. Happy to swap with anything all-ages friendly!"),
    (C, "2006-02-20 18:30", "Rust Belt Knights (Drunk Duck), robots and pubs, swapping with anyone who doesn't mind a bit of swearing."),
    (MN, "2006-07-02 10:05", "Not a comic, but the LJ community I run will post your comic if you leave the link here. We do a weekly round-up post on Sundays."),
    (PX, "2007-01-05 15:40", "Respawn Point, all original sprites now. Swapping with game comics or anything really."),
    (F, "2007-03-27 05:10", "Tea & Tentacles, launching in May. Can I reserve a spot?? :)"),
], icon=0, views=870, sticky=1)

# ---------------------------------------------------------------- Off-Topic
topic(10, "What's on your playlist while you draw?", [
    (G, "2007-03-07 22:20", "Neon Bible came out yesterday and I inked four pages to it. What's everyone listening to?"),
    (M, "2007-03-07 23:30", "The Shins, Wincing the Night Away, on loop since January."),
    (H, "2007-03-08 08:30", "Public radio. Old time radio dramas when I'm inking. Inking needs words, colouring needs music."),
    (S, "2007-03-08 12:10", "LCD Soundsystem. The new one comes out in a couple of weeks."),
    (K, "2007-03-08 18:40", "Anything on my iPod shuffle. Which is mostly Muse right now."),
    (C, "2007-03-09 13:02", "Glasgow representing: Franz Ferdinand forever."),
    (Z, "2007-03-10 09:00", "Tom Waits. Always Tom Waits."),
    (B, "2007-03-12 16:30", "Anime soundtracks. Yoko Kanno makes my pages 20% better."),
    (S, "2007-03-21 11:44", "Sound of Silver is out. It's fantastic. That is all."),
], icon=4, views=344)

topic(10, "Webcomics you're reading right now", [
    (P, "2007-01-08 20:45", """New year, new bookmarks. What are you reading? Mine at the moment:

Dresden Codak, Gunnerkrigg Court, Achewood, Questionable Content, Perry Bible Fellowship, Octopus Pie, Wondermark, Girl Genius, A Softer World, and xkcd."""),
    (MN, "2007-01-08 21:30", "Templar, Arizona is the one I keep telling everyone about. Also Scary Go Round."),
    (D, "2007-01-08 22:02", "Diesel Sweeties, Dinosaur Comics, PvP and Penny Arcade, same as every year."),
    (Q, "2007-01-09 00:10", "Copper by Kazu Kibuishi. It's monthly but every one is perfect."),
    (K, "2007-01-09 06:30", "Gunnerkrigg Court is so beautiful. Tom Siddell's use of colour is amazing."),
    (L, "2007-02-28 19:20", "Saw this thread from Google - I'm new, but I read basically everything Pagecount listed plus Hollow Hill, which I found here!"),
    (M, "2007-02-28 22:00", "Hi lunchbox_legion and thank you!! :D"),
    (P, "2007-03-22 13:10", "Adding Family Man. Our tastes are all the same, aren't they."),
], icon=0, views=715)

topic(10, "300 - seen it yet?", [
    (C, "2007-03-10 23:40", "Saw 300 tonight. It's a Frank Miller comic come to life, every shot is a panel. Very loud. Lots of shouting."),
    (G, "2007-03-11 00:30", "It's ridiculous but the colours are incredible. Very Lynn Varley."),
    (H, "2007-03-11 10:20", "I'll wait for the DVD. I don't need to see that many abs on a screen 40 feet high."),
    (S, "2007-03-12 09:44", "Thing made $70 million in a weekend. Expect every graphic novel ever to be optioned by Friday."),
    (TK, "2007-03-24 19:15", "TMNT was better"),
    (D, "2007-03-24 20:40", "The kid has spoken."),
], icon=7, views=265)

topic(10, "LiveJournal communities - still worth posting to?", [
    (MN, "2007-02-12 12:00", "Question for the artists: do you still get readers from LJ comms, or is everyone on DeviantArt now? Trying to figure out if my community is still useful."),
    (K, "2007-02-12 17:30", "DeviantArt brings me commissions, LJ brings me actual comic readers. Different crowds."),
    (M, "2007-02-12 20:15", "LJ is where I get the most comments. dA is mostly favourites and \"nice art\"."),
    (Q, "2007-02-13 10:40", "Your community sent me maybe 300 visitors when you featured Lanternfish. That's not nothing!"),
    (MN, "2007-02-13 12:20", "That's really good to hear. I'll keep the Sunday round-ups going then."),
], icon=3, views=188)

# ---------------------------------------------------------------- Conventions & Meetups
topic(11, "Comic-Con 2007: hotel plans?", [
    (G, "2007-03-01 21:15", """Who's going to San Diego this year? Last year the downtown hotels near the convention center sold out in about a day once the reservations opened and I ended up in Mission Valley on the trolley.

It's basically a lottery at this point. What's everyone's plan?"""),
    (Q, "2007-03-01 22:30", "I'm going! Splitting a room with three friends from my critique group. Hoping for the Gaslamp, but expecting Hotel Circle."),
    (C, "2007-03-02 08:15", "Flights from Glasgow are about 600 quid, so I'm watching from here with envy."),
    (D, "2007-03-02 09:40", "Hotel Circle is fine. The trolley is easy and the hotels are cheaper. Bring comfortable shoes, the convention center is enormous."),
    (S, "2007-03-02 11:20", "Driving down from San Jose. I'll have a car if anyone wants to carpool from the hotel."),
    (G, "2007-03-02 21:55", "Let's do an Inkwell meetup Saturday night. I'll start a thread closer to the date."),
    (M, "2007-03-03 00:12", "If I can get across the border with my sketchbooks I'm in!"),
], icon=3, views=402)

topic(11, "Anyone tabling at MoCCA or SPX this year?", [
    (Z, "2007-02-20 09:00", "I'm sharing a half table at MoCCA in New York with a friend. First time in years I'm showing zines. Anyone else exhibiting?"),
    (H, "2007-02-20 18:30", "I'll be at SPX in the fall, not tabling, just shopping. My wallet is already scared."),
    (G, "2007-02-21 00:30", "Applied for SPX. Fingers crossed. Printing a Static Orbit collection if I get in."),
    (Q, "2007-02-21 10:10", "Make sure you post photos zipatone! We'll want to see the table."),
    (Z, "2007-02-21 13:25", "Will do. Assuming my camera works. It is older than some of you."),
], icon=0, views=176)

# Reputation: (to, from, +/-1, board-local time, comment)
REPUTATION = [
    (K, B, 1, "2006-08-14 16:25", "Flatting walkthrough saved my life"),
    (K, M, 1, "2006-08-14 21:30", "So helpful, thank you!"),
    (K, TK, 1, "2007-02-16 16:12", "thanks for the gaps tip"),
    (H, N, 1, "2007-01-13 18:25", "Brush inking tips worked"),
    (H, TK, 1, "2006-11-26 15:30", "line weight thing"),
    (D, TK, 1, "2006-11-25 22:40", "great crit"),
    (D, O, 1, "2007-03-26 20:10", "Thanks for the welcome!"),
    (Q, MN, 1, "2006-07-01 17:30", "Running a lovely forum"),
    (Q, O, 1, "2007-03-26 22:40", "Great hosting advice"),
    (Q, G, 1, "2007-03-20 22:50", ""),
    (M, B, 1, "2006-11-08 22:00", "Manga Studio EX breakdown"),
    (M, MN, 1, "2006-07-01 15:10", "Hollow Hill is great"),
    (M, K, 1, "2007-03-26 06:00", "Lavender shadows!"),
    (S, G, 1, "2006-12-16 15:40", "Thanks for the CS3 beta heads-up"),
    (S, H, 1, "2006-10-03 18:25", "Photomerge tip"),
    (PP, G, 1, "2006-10-30 00:45", "Project Wonderful tip paid off"),
    (PP, M, 1, "2006-10-30 13:15", ""),
    (G, P, 1, "2007-03-21 09:00", "100 pages!"),
    (PX, D, 1, "2006-12-30 19:00", "Redrawing every sprite takes guts"),
    (TK, D, 1, "2007-02-11 21:35", "Huge improvement"),
    (P, PX, -1, "2006-07-13 21:00", "harsh"),
    (Z, Q, 1, "2006-04-03 18:30", "Ames guide veteran"),
    (P, MN, 1, "2007-01-08 21:35", "Great reading list"),
    (MN, Q, 1, "2007-02-13 10:45", "Thanks for the LJ round-ups"),
]

# Calendar events: (subject, author, j-n-Y, description)
EVENTS = [
    ("Sketch Swap sign-ups close", Q, "31-3-2007", "Last day to sign up for the Spring Sketch Swap. Reply in the Announcements thread."),
    ("Sketch Swap: names go out", Q, "1-4-2007", "Everyone who signed up gets a PM with their swap partner."),
    ("Sketch Swap mailing deadline", Q, "21-4-2007", "Get your drawing in the mail by today! Post a scan when yours arrives."),
    ("Static Orbit page 100", G, "20-3-2007", "Page 100 goes up tonight."),
    ("Cubicle Fauna strip #800", D, "19-3-2007", "Eight hundred weekday strips."),
]
