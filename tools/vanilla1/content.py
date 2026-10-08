# Clearfix: seed content for the Vanilla 1.1.5a exhibit (archive date Thursday 16 October 2008, 15:42 UTC).
# gen_seed.py turns this into seed.sql. All text is plain ASCII; Vanilla's stock "Text" formatter
# escapes it and turns CRLF line breaks into <br />.

NOW = "2008-10-16 15:42:00"

CATEGORIES = [
    # id, name, description
    (1, "General", "Web standards, browsers, tools and the trade in general."),
    (2, "CSS & Layout", "Floats, grids, hacks and getting it all to behave in IE6."),
    (3, "JavaScript", "jQuery, Prototype, YUI, and plain old DOM scripting."),
    (4, "Showcase & Critique", "Post your work and ask for honest feedback."),
    (5, "Jobs", "Hiring or looking for work. Say where you are and whether remote is OK."),
    (6, "Off Topic", "Everything that isn't the other five."),
]

# Extra role created through Settings > Roles & Permissions (RoleID 5).
MODERATOR_ROLE = ("Moderator", "Keeps Clearfix tidy. Ask a moderator if a post goes missing.")

# id, name, first, last, role id (3 member, 4 admin, 5 moderator), joined, last active, visits,
# attributes [(label, value)]
MEMBERS = [
    (1, "dmitri", "Dmitri", "Kessler", 4, "2007-02-26 21:14:00", "2008-10-16 15:31:00", 1412,
     [("Location", "Toronto, Canada"), ("Website", "http://dmitrikessler.example.com/")]),
    (2, "jenpowell", "Jen", "Powell", 5, "2007-02-28 17:02:00", "2008-10-16 14:58:00", 1096,
     [("Location", "Portland, OR"), ("Website", "http://jenpowell.example.net/"), ("Twitter", "jenpowell")]),
    (3, "zoom1", "Marcus", "Ohlsson", 3, "2007-03-09 08:41:00", "2008-10-16 15:17:00", 688,
     [("Location", "Malmo, Sweden")]),
    (4, "kerning", "Ana", "Ruiz", 3, "2007-04-17 19:20:00", "2008-10-16 12:44:00", 523,
     [("Location", "Barcelona"), ("Website", "http://anaruiz.example.org/")]),
    (5, "brendan_k", "Brendan", "Kelly", 3, "2007-05-02 22:05:00", "2008-10-16 11:09:00", 461,
     [("Location", "Dublin, Ireland")]),
    (6, "gridlock", "Tom", "Becker", 3, "2007-06-21 06:33:00", "2008-10-16 09:51:00", 377,
     [("Location", "Berlin"), ("Website", "http://tombecker.example.de/")]),
    (7, "sarah_m", "Sarah", "Mitchell", 3, "2007-07-30 10:12:00", "2008-10-16 08:26:00", 302,
     [("Location", "Melbourne, Australia")]),
    (8, "nate_w", "Nate", "Wallace", 3, "2007-08-14 15:47:00", "2008-10-15 23:02:00", 268,
     [("Location", "Austin, TX"), ("Currently using", "TextMate, Firefox 3, a very old Aeron")]),
    (9, "floatleft", "Priya", "Raman", 3, "2007-09-03 13:28:00", "2008-10-16 13:40:00", 241,
     [("Location", "Bangalore")]),
    (10, "tomasz", "Tomasz", "Nowak", 3, "2007-10-11 18:55:00", "2008-10-15 20:37:00", 196,
     [("Location", "Krakow, Poland"), ("Website", "http://tnowak.example.pl/")]),
    (11, "liza", "Liza", "Chen", 3, "2007-11-05 04:19:00", "2008-10-16 07:12:00", 174,
     [("Location", "San Francisco")]),
    (12, "validator", "Kevin", "Moore", 3, "2007-12-12 20:40:00", "2008-10-16 10:03:00", 158,
     [("Location", "Leeds, UK")]),
    (13, "ricardo", "Ricardo", "Alves", 3, "2008-01-22 14:08:00", "2008-10-15 19:15:00", 121,
     [("Location", "Sao Paulo")]),
    (14, "hannah_j", "Hannah", "Jensen", 3, "2008-02-19 09:36:00", "2008-10-16 06:58:00", 109,
     [("Location", "Copenhagen")]),
    (15, "emdash", "Owen", "Price", 3, "2008-03-27 22:51:00", "2008-10-14 21:44:00", 87,
     [("Location", "Cardiff")]),
    (16, "mpatel", "Meera", "Patel", 3, "2008-04-08 11:25:00", "2008-10-14 16:20:00", 43,
     [("Location", "Chicago, IL"), ("Company", "Northside Interactive")]),
    (17, "jbaker", "Jonas", "Baker", 3, "2008-05-15 16:03:00", "2008-10-16 15:24:00", 66,
     [("Location", "Vancouver, BC")]),
    (18, "pixelfreak", "Danny", "Ross", 3, "2008-06-29 02:17:00", "2008-10-15 22:31:00", 58,
     [("Location", "Glasgow")]),
    (19, "chloe_d", "Chloe", "Dubois", 3, "2008-08-04 12:46:00", "2008-10-15 14:08:00", 31,
     [("Location", "Lyon, France")]),
    (20, "aaronw", "Aaron", "Webb", 3, "2008-09-18 19:33:00", "2008-10-13 18:27:00", 14,
     [("Location", "Denver, CO")]),
    (21, "mike_t", "Mike", "Turner", 3, "2008-09-14 17:10:00", "2008-10-12 13:41:00", 4, []),
]

# Discussions: category, title, sticky, closed, comments [(author, datetime, body)].
# The first comment is the discussion itself. Bodies use \n; gen_seed.py stores \r\n.
DISCUSSIONS = [
 (1, "Welcome to Clearfix - please read", 1, 1, [
  ("dmitri", "2007-03-01 20:10:00", """Welcome to Clearfix, a forum for people who build the front end of the web: designers, CSS people, JavaScript people, and anyone who has ever lost an afternoon to IE6.

A few ground rules:

1. Search before you post. Most float and IE questions have been asked before.
2. When asking for help, post a link to a test case. A stripped-down page with the bug is worth ten screenshots.
3. Say which browsers you tested in, and which versions.
4. Critique the work, not the person.
5. Jobs posts go in the Jobs category and nowhere else.

Jen and I keep an eye on things. If something looks wrong, send one of us a message.

- Dmitri"""),
 ]),
 (5, "How to post in Jobs", 1, 1, [
  ("jenpowell", "2007-03-01 19:05:00", """Please start the title with [Hiring] or [For hire] so people can scan the list.

Include: location (or "remote"), full time / contract / freelance, and a rough rate or salary range if you can. Posts with no way to contact you will be removed.

Recruiters are welcome, but one post per role, please. Bumping your own thread every day will get it closed."""),
 ]),
 (2, "IE8 beta 2: EmulateIE7 meta tag, yes or no?", 0, 0, [
  ("liza", "2008-10-14 18:05:00", """Our lead wants to add this to every page template before IE8 ships:

<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" />

The idea is that we don't have to test in IE8 at all for now. I tested the main templates in beta 2 in standards mode and only two things broke (a negative margin on the nav and a min-height). Is it worth locking ourselves into IE7 mode just for that?"""),
  ("zoom1", "2008-10-14 18:41:00", """I'd fix the two bugs. IE8 standards mode is the first IE in years that does what the spec says most of the time. Pinning everything to IE7 means you keep every IE7 bug you already work around, forever, or until someone remembers to take the tag out."""),
  ("validator", "2008-10-14 19:22:00", """Counterpoint: it's a beta. Microsoft has changed rendering between betas before. For a big site with lots of templates I can see why a lead would want the safety net until the final release is out."""),
  ("liza", "2008-10-14 20:03:00", """That's pretty much his argument. He also doesn't want the "compatibility view" button showing up for our users."""),
  ("jenpowell", "2008-10-15 01:12:00", """We did both: the meta tag goes out with the next release, and there's a ticket to remove it and test properly once IE8 final is out. Writing the ticket is the important part. Otherwise it stays there for five years."""),
  ("brendan_k", "2008-10-15 09:47:00", """Note you can send it as an HTTP header too, so you can turn it off server side without touching the templates:

X-UA-Compatible: IE=EmulateIE7"""),
  ("liza", "2008-10-16 14:52:00", """Header it is. Thanks all. Fixed the min-height thing anyway, it was a missing doctype on one include. Embarrassing."""),
  ("zoom1", "2008-10-16 15:17:00", """Happens to all of us. Quirks mode is the gift that keeps on giving."""),
 ]),
 (1, "Firefox 3.1 beta 1 is out", 0, 0, [
  ("nate_w", "2008-10-14 22:30:00", """Released today. The bits I care about: text-shadow, the :nth-child selectors, and border-image (-moz-border-image). The TraceMonkey JIT is in too but off by default (javascript.options.jit.content in about:config).

Anyone tried it yet?"""),
  ("gridlock", "2008-10-15 07:58:00", """text-shadow finally. Safari has had it forever. That just leaves IE, as usual."""),
  ("floatleft", "2008-10-15 11:20:00", """Turned on the JIT and our big jQuery table sort went from about 900 ms to 300. Some extensions don't install because they say max version 3.0.*, Firebug included, so I'm going back to 3.0 for actual work."""),
  ("kerning", "2008-10-15 13:06:00", """You can install it next to 3.0 with a separate profile (firefox -P -no-remote). That's how I keep 2.0, 3.0 and the beta on one machine."""),
  ("nate_w", "2008-10-16 13:40:00", """@kerning that profile trick just saved me a lot of reinstalling, thanks."""),
 ]),
 (2, "clearfix or overflow:hidden?", 0, 0, [
  ("pixelfreak", "2008-10-13 21:15:00", """Given the name of this forum I have to ask. Which one are you using these days for containing floats?

The classic one from positioniseverything:

.clearfix:after { content: "."; display: block; height: 0; clear: both; visibility: hidden; }
.clearfix { display: inline-block; }
/* Hides from IE-mac \\*/
* html .clearfix { height: 1%; }
.clearfix { display: block; }
/* End hide from IE-mac */

or just overflow: hidden on the parent (plus a width or zoom: 1 for IE)?"""),
  ("dmitri", "2008-10-13 21:40:00", """overflow: hidden for most things now. The clearfix is for when the container has something that pokes out of it: a dropdown menu, a negative-margin image, a box-shadow in Safari."""),
  ("zoom1", "2008-10-13 22:02:00", """Same. And nobody needs the IE-mac part anymore. I trimmed mine to:

.clearfix:after { content: "."; display: block; height: 0; clear: both; visibility: hidden; }
.clearfix { zoom: 1; }

zoom goes in the IE stylesheet if you care about validation."""),
  ("sarah_m", "2008-10-14 02:31:00", """overflow: auto bit me once. Scrollbars showed up in Firefox 2 because of a 1px rounding thing with an em-based width. Hidden is safer."""),
  ("tomasz", "2008-10-14 08:15:00", """I still add an empty <div style="clear:both"></div> sometimes. Don't tell anyone."""),
  ("validator", "2008-10-14 08:52:00", """Tomasz, I'm calling the web standards police."""),
  ("brendan_k", "2008-10-14 10:30:00", """One more vote for overflow: hidden. Watch out for it clipping focus outlines on links at the edge of the box, though. Keyboard users notice."""),
  ("pixelfreak", "2008-10-14 12:04:00", """Good point about the outlines, never noticed that. So the answer is "both, depending". Figures."""),
  ("hannah_j", "2008-10-15 06:58:00", """We call the class "group" instead of "clearfix" at work, so it describes what the box is, not how it's coded. Same CSS."""),
  ("jenpowell", "2008-10-15 15:33:00", """+1 for "group". The class name thing comes up in every code review we do."""),
  ("gridlock", "2008-10-16 09:51:00", """Display: table on the parent is another option once you drop IE7. So, around 2012."""),
  ("pixelfreak", "2008-10-16 12:35:00", """Ha. Putting that one in my calendar."""),
 ]),
 (3, "$(document).ready firing twice", 0, 0, [
  ("ricardo", "2008-10-15 16:44:00", """jQuery 1.2.6. I have an alert() in $(document).ready and it shows up twice on one page only. Same script on every other page, only once. What should I look for?"""),
  ("floatleft", "2008-10-15 17:10:00", """Most common reason: jquery.js and your script are included twice. Check the page's view source, not the template. Sometimes a CMS widget adds its own copy."""),
  ("ricardo", "2008-10-15 18:22:00", """No double includes. But the page has an iframe with the same layout in it (a print preview thing). Could that be it?"""),
  ("floatleft", "2008-10-15 18:40:00", """Yes, the iframe loads its own document and runs its own ready handler. If the alert is in a shared file it'll fire once per document."""),
  ("ricardo", "2008-10-15 19:15:00", """That was it. I feel stupid. Thanks!"""),
  ("jbaker", "2008-10-16 11:02:00", """For next time, console.log instead of alert, and Firebug shows which file and line it came from. Much faster to figure out than alerts."""),
 ]),
 (4, "Portfolio redesign - be brutal", 0, 0, [
  ("chloe_d", "2008-10-15 11:30:00", """Finally redid my portfolio after two years. Static XHTML, one stylesheet, a bit of jQuery for the image switcher. Tested in Firefox 3, Safari 3.1, IE6 and IE7.

http://chloedubois.example.fr/

Be honest. I'd rather hear it here than not hear back from studios."""),
  ("kerning", "2008-10-15 12:12:00", """The type is lovely. Georgia for headings at that size works. Body copy is too light though, #999 on white is hard to read. I'd go to #555 at least."""),
  ("gridlock", "2008-10-15 12:50:00", """Work section: thumbnails are all the same size, so nothing stands out. Make your best two projects bigger. Studios look at three things and leave."""),
  ("chloe_d", "2008-10-15 13:31:00", """Both fair. The grey is from the original PSD and I never questioned it."""),
  ("validator", "2008-10-15 14:00:00", """The contact page has two elements with id="nav". Validator complains, IE doesn't care, but the jQuery selector picks the first one only. That's probably why the active state doesn't work on that page."""),
  ("chloe_d", "2008-10-15 14:08:00", """...and that's the bug I've been chasing all week. Thank you."""),
  ("dmitri", "2008-10-16 15:31:00", """Late to this, but the IE6 version is fine apart from the logo PNG having a grey box around it. Either fix it with AlphaImageLoader or save a GIF version for IE6 through a conditional comment."""),
 ]),
 (6, "Obama campaign site and Gotham", 0, 0, [
  ("kerning", "2008-10-15 22:12:00", """Whatever your politics, the Obama campaign's design is the most consistent identity I've seen in a US election. Gotham everywhere, on every sign, every web page, every T-shirt. Somebody at H&FJ is having a very good year."""),
  ("emdash", "2008-10-15 23:01:00", """The website uses images for every heading, though. I counted 40-odd image headings on the issues page. No sIFR, nothing."""),
  ("kerning", "2008-10-16 00:20:00", """Yes, but they're consistent images, and they have proper alt text. It's not like there's a better option for a licensed font on the web."""),
  ("hannah_j", "2008-10-16 06:58:00", """The McCain site uses Optima in places, which is more than I expected."""),
  ("nate_w", "2008-10-16 07:31:00", """Keeping this thread about type, please. I will not survive another three weeks of election talk on every other forum."""),
 ]),
 (1, "Chrome after six weeks", 0, 0, [
  ("brendan_k", "2008-10-14 19:00:00", """Six weeks since Chrome beta came out. Has anyone kept it as their main browser?

I tried for two weeks. The speed is real, the tabs on top are great, and the comic was fun. But no extensions means no Firebug, and the Inspector is fine for looking but not much fun for editing CSS live."""),
  ("aaronw", "2008-10-14 20:15:00", """It renders like Safari 3.1 as far as I can tell (it's WebKit 525). So I test in Safari and assume Chrome is fine. Has anyone found a difference?"""),
  ("floatleft", "2008-10-14 21:40:00", """Form controls are different, Chrome draws its own, and text rendering on Windows uses the system settings instead of Safari's own. Fonts look different at small sizes."""),
  ("liza", "2008-10-15 03:02:00", """The developer in me loves that every tab is a process. The person who has 40 tabs open hates how much memory that is."""),
  ("jenpowell", "2008-10-15 08:44:00", """In our stats it's at 0.9% after six weeks. More than Opera already."""),
  ("brendan_k", "2008-10-16 11:09:00", """Yeah, that's the number that will make clients ask about it. I'll add it to the test list."""),
 ]),
 (2, "960.gs or Blueprint for client work?", 0, 0, [
  ("aaronw", "2008-10-13 14:20:00", """Starting a mid-size site (about 25 templates). Thinking about a grid framework this time instead of hand-rolling the layout. 960.gs or Blueprint 0.7? Or YUI Grids?

Main concern is handing it over to the client's in-house guy later."""),
  ("gridlock", "2008-10-13 15:06:00", """960.gs. It's smaller, it doesn't touch your typography, and the 12 and 16 column versions cover most designs. Blueprint resets and styles a lot of things, which you then fight with."""),
  ("tomasz", "2008-10-13 16:11:00", """I like Blueprint for prototypes because the typography is already decent. For production I end up removing half of it."""),
  ("hannah_j", "2008-10-13 19:44:00", """YUI Grids is good if you need the fluid templates. It's also the only one with a real company behind it and documentation."""),
  ("validator", "2008-10-13 21:10:00", """The thing nobody mentions: class="grid_4 alpha" all over the markup is presentational. Fine for a site you maintain. For the client's in-house guy it's a convention he has to learn."""),
  ("aaronw", "2008-10-14 00:03:00", """That's a fair point, but he's going to have to learn something either way. Our hand-rolled layouts aren't documented at all."""),
  ("gridlock", "2008-10-14 08:22:00", """The 960 PSD and Fireworks templates also help. Give the designer the template, then the grid in the PSD matches the CSS. That alone saved us a day of back and forth on the last project."""),
  ("aaronw", "2008-10-15 09:30:00", """Went with 960.gs, 12 columns. Will report back."""),
 ]),
 (5, "[Hiring] Front-end developer, Chicago, full time", 0, 0, [
  ("mpatel", "2008-10-13 16:20:00", """Northside Interactive is looking for a front-end developer in Chicago (River North). Full time, on site.

You'd be working on marketing sites and a couple of web apps for clients in healthcare and retail.

What we need:
- Hand-coded XHTML and CSS that works in IE6 and up
- jQuery or Prototype
- You've worked with designers and can push back on things that won't work
- Bonus: Rails or PHP templates, accessibility (Section 508)

Salary range is 55-70k depending on experience. Send links to work you coded (not designed) to jobs (at) northside-interactive.example.com"""),
  ("tomasz", "2008-10-13 18:02:00", """Any chance of remote for the right person?"""),
  ("mpatel", "2008-10-14 16:20:00", """Sorry, not for this one. We may have contract work later in the year that could be remote. I'll post it here."""),
 ]),
 (3, "Moving from Prototype to jQuery - worth it?", 0, 0, [
  ("hannah_j", "2008-10-12 10:15:00", """We have about 4000 lines of Prototype 1.6 and script.aculo.us on an intranet app. New hires all know jQuery, nobody knows Prototype. Is it worth porting, or should we only use jQuery for new stuff?"""),
  ("jbaker", "2008-10-12 12:40:00", """Don't run both on the same page without jQuery.noConflict(), they both want $. And don't port working code just because. Port it when you touch it."""),
  ("floatleft", "2008-10-12 14:22:00", """The biggest change is mentally. Prototype extends the DOM elements and has classes (Class.create). jQuery wraps everything and is about selecting things and doing stuff to them. Your Ajax.Updater calls convert easily, your class hierarchies don't."""),
  ("hannah_j", "2008-10-13 09:12:00", """Most of it is Ajax.Updater and some Effect.Fade. Sounds like the easy kind. Still, two libraries is about 120 KB, which on our intranet doesn't matter much."""),
  ("nate_w", "2008-10-14 18:30:00", """For what it's worth, we ported a similar sized app in about two weeks. Main gain was everyone could work on it, not speed."""),
  ("hannah_j", "2008-10-15 10:05:00", """Thanks. We'll port page by page. noConflict for now."""),
 ]),
 (2, "IE6 PNG fix breaks my links", 0, 0, [
  ("emdash", "2008-10-12 21:00:00", """Using the AlphaImageLoader filter on a background PNG in IE6. Looks right, but links inside the element stop being clickable. Is there a fix, or do I have to use GIFs?"""),
  ("zoom1", "2008-10-12 21:44:00", """Classic. Give the links position: relative. Links inside an element with the filter only become clickable again if they're positioned. Don't ask why."""),
  ("emdash", "2008-10-12 22:35:00", """position: relative on the a fixed it. Seriously, how did anyone figure that out?"""),
  ("sarah_m", "2008-10-13 03:20:00", """Also be careful with repeating backgrounds. The filter doesn't do background-repeat or background-position, it scales or crops. For anything that tiles I use an 8-bit PNG with alpha from Fireworks, which IE6 shows with hard edges instead of a grey box."""),
  ("jenpowell", "2008-10-13 08:10:00", """And keep the filter in an IE6-only stylesheet behind a conditional comment, it's slow. Lots of filtered elements make scrolling sluggish in IE6."""),
  ("emdash", "2008-10-14 21:44:00", """Moved it all into ie6.css. The 8-bit PNG trick from Fireworks is great, hadn't seen it before."""),
 ]),
 (1, "Dreamweaver CS4 - anyone upgrading?", 0, 0, [
  ("tomasz", "2008-10-12 08:30:00", """CS4 is shipping this week. Our studio has Dreamweaver on every machine, mostly used as an FTP client with a code view. Live View (WebKit preview) looks good. Is anyone upgrading for that?"""),
  ("dmitri", "2008-10-12 10:45:00", """I'm on TextMate and Coda. Not going back, but CS4 is the first Dreamweaver in a while that seems to know CSS exists."""),
  ("liza", "2008-10-12 13:06:00", """Dreamweaver's code view is fine honestly. I upgraded for Photoshop CS4 anyway, so it comes with the suite."""),
  ("mike_t", "2008-10-12 13:40:00", """We're still on Dreamweaver 8. Works fine."""),
  ("tomasz", "2008-10-15 20:37:00", """Trial installed. Live View is nice. Related files bar (shows the CSS and JS a page uses) is nicer. It still writes <span class="style1"> if you use the property panel, so nothing has changed there."""),
 ]),
 (4, "Bakery site, my first 960.gs build", 0, 0, [
  ("sarah_m", "2008-10-11 05:30:00", """A small site for a bakery in my neighborhood. It's my first site on 960.gs (16 column) and I wanted to keep it simple: five pages, a map, and a menu that the owner can edit as a text file.

http://flourandsalt.example.com.au/

Feedback welcome, especially on the header. The owner wanted "something warm"."""),
  ("kerning", "2008-10-11 09:12:00", """Warm achieved. The brown gradient in the header goes a bit muddy in the middle. A lighter stop in the middle might help."""),
  ("chloe_d", "2008-10-11 18:55:00", """Love the hand-drawn icons. Opening hours should be on the home page, not three clicks away. That's the only thing people want from a bakery site."""),
  ("sarah_m", "2008-10-12 00:40:00", """Ha, the owner said the same thing. Moved hours into the sidebar of every page."""),
  ("gridlock", "2008-10-13 08:01:00", """Looks good. One thing: the Google Map loads before the text on slow connections and pushes the page around. Give the map container a fixed height."""),
  ("sarah_m", "2008-10-16 08:26:00", """Fixed height done. Thanks all, the owner's happy and paid me in bread."""),
 ]),
 (2, "sIFR 3 or just use images?", 0, 0, [
  ("pixelfreak", "2008-10-10 13:30:00", """Client wants the headings in their corporate font (a licensed sans). Options I can see: sIFR 3 (still beta), sIFR 2.0.7, images generated by PHP, or images by hand. What are people doing?"""),
  ("kerning", "2008-10-10 14:44:00", """I've used sIFR 3 on two sites. Works well once set up, but the setup is fiddly (exporting the swf from Flash, the CSS selectors, the sifr-config file). It's also a flash of unstyled text when the page loads."""),
  ("brendan_k", "2008-10-10 17:20:00", """PHP-generated images with GD and a cache folder. Simple, works without Flash, and you get proper alt text. Downside is you need the font file on the server, which might not be allowed by the license."""),
  ("validator", "2008-10-11 10:02:00", """Check the license first in any case. Some foundries don't allow embedding in a swf either."""),
  ("pixelfreak", "2008-10-11 13:15:00", """License says embedding is OK for "non-editable documents". I'm reading that as sIFR is fine. Going with sIFR 3."""),
  ("jbaker", "2008-10-13 11:30:00", """Safari 3.1 supports @font-face already, for what it's worth. Not much help until IE and Firefox do it (IE does EOT only)."""),
 ]),
 (6, "How's the economy hitting your work?", 0, 0, [
  ("nate_w", "2008-10-09 23:10:00", """Two clients have put projects "on hold" this week. One of them is a bank, so I'm not surprised. Anyone else seeing this?"""),
  ("tomasz", "2008-10-10 07:40:00", """Not yet here, but our clients are mostly in Germany and the UK, so I expect it soon."""),
  ("liza", "2008-10-10 18:03:00", """In SF startups are being told to cut and save money. We are still hiring, but slowly."""),
  ("ricardo", "2008-10-11 15:22:00", """Brazil seems OK for now. The dollar went up a lot, which is good for me since I invoice in USD."""),
  ("dmitri", "2008-10-12 22:15:00", """Probably a good time to have savings and a few small clients instead of one big one. That's what got me through 2001."""),
  ("nate_w", "2008-10-15 23:02:00", """One of the projects came back with half the budget. Better than nothing."""),
 ]),
 (3, "YUI 2.6.0 released", 0, 0, [
  ("hannah_j", "2008-10-01 20:30:00", """YUI 2.6.0 is out. New Carousel (beta), Paginator is out of beta, and a long list of DataTable fixes. The YUI blog has the full list."""),
  ("floatleft", "2008-10-02 06:20:00", """The DataTable is the best table widget around, not close. I wish the API was less verbose though."""),
  ("jbaker", "2008-10-02 09:18:00", """And they host it all on Yahoo's servers, so no bandwidth cost for you. I've been using the hosted files on every project."""),
  ("hannah_j", "2008-10-10 13:01:00", """Upgraded the intranet from 2.5.2 without any problems. The new Carousel replaced our home made one."""),
 ]),
 (2, "inline-block in Firefox 2", 0, 0, [
  ("chloe_d", "2008-10-08 17:12:00", """I wanted to use display: inline-block for a list of thumbnails (to avoid floats). Works in Firefox 3, Safari, Opera, and IE with the hasLayout trick. Firefox 2 just ignores it. Is there a solution?"""),
  ("zoom1", "2008-10-08 17:58:00", """Firefox 2 needs display: -moz-inline-box (or -moz-inline-stack). Put it before inline-block, so Firefox 3 uses the standard one:

li { display: -moz-inline-stack; display: inline-block; zoom: 1; *display: inline; }

The last two are for IE6/7."""),
  ("chloe_d", "2008-10-08 19:22:00", """-moz-inline-stack works. But the text inside the li now overflows... ?"""),
  ("zoom1", "2008-10-08 20:10:00", """Yes, it's a XUL box, doesn't wrap. Wrap the contents of the li in a div with a width. Ugly but that's Firefox 2."""),
  ("jenpowell", "2008-10-09 14:44:00", """Firefox 2 is about 9% of our traffic, dropping quickly since Firefox 3. Depending on your stats it may be OK for the grid to look slightly off there."""),
  ("chloe_d", "2008-10-15 14:01:00", """Went with the inner div. Firefox 2 users get the same layout as everyone else now."""),
 ]),
 (1, "Acid3 scores, October edition", 0, 0, [
  ("validator", "2008-10-06 19:30:00", """Current scores on my machine:

Safari 3.1.2: 75/100
WebKit nightly: 100/100 (but not pixel perfect)
Opera 9.6: 85/100
Firefox 3.0.3: 71/100
Firefox 3.1 nightly: 85/100
Chrome 0.2: 78/100
IE8 beta 2: 21/100

I know it's not a measure of anything except Acid3, but the IE number still makes me sad."""),
  ("dmitri", "2008-10-06 21:12:00", """IE8 passing Acid2 was the bigger news for me. Acid3 tests a lot of things nobody uses yet (SVG fonts, SMIL)."""),
  ("aaronw", "2008-10-07 09:43:00", """Acid2 passing in IE8 means CSS 2.1 works properly, and that's what we use every day. Agreed with Dmitri."""),
  ("validator", "2008-10-08 10:03:00", """True. Still, 21."""),
 ]),
 (5, "[For hire] Freelance PSD to XHTML/CSS, Krakow", 0, 0, [
  ("tomasz", "2008-10-07 09:00:00", """I'm a freelance front-end developer with six years of experience. I turn PSDs into hand-coded XHTML/CSS, with jQuery where it's needed. IE6 included, no tables, no extra charge for that.

Available from November for small and medium projects. Remote only, English or Polish. EUR or USD invoices.

Portfolio and rates: http://tnowak.example.pl/"""),
  ("dmitri", "2008-10-07 16:41:00", """Can vouch for Tomasz, he did a couple of projects for me last year. Clean markup and on time."""),
 ]),
 (1, "Testing IE6, IE7 and IE8 on one machine", 0, 0, [
  ("aaronw", "2008-10-04 15:00:00", """What's everyone using to test in multiple IE versions? I have IE7 on my XP machine, and Multiple IE for IE6, but it's buggy (conditional comments don't work right)."""),
  ("brendan_k", "2008-10-04 16:10:00", """Virtual machines. Microsoft gives free Virtual PC images with IE6, IE7 and IE8 beta for testing. They expire every few months but you can download new ones."""),
  ("liza", "2008-10-04 18:44:00", """IETester is a newer tool that shows all IE rendering engines in tabs. It's not perfect either but conditional comments work in it. Good for quick checks, I still do final testing in a VM."""),
  ("jbaker", "2008-10-05 10:33:00", """On a Mac I use VMware Fusion with three XP VMs. Snapshots are the best thing. You install, snapshot, and when Windows starts acting up, you revert."""),
  ("aaronw", "2008-10-05 22:01:00", """Virtual PC images it is. Thanks."""),
 ]),
 (2, "Faux columns or display: table?", 0, 0, [
  ("ricardo", "2008-09-30 20:40:00", """Two column layout, sidebar needs a background the full height of the content. I know the faux columns technique (background image on the container). Is display: table any better now, or is IE7 still the problem?"""),
  ("gridlock", "2008-09-30 21:30:00", """IE7 doesn't support display: table, so you'd need a fallback anyway. Faux columns is still the pragmatic answer. Works everywhere, back to IE5."""),
  ("jenpowell", "2008-10-01 08:05:00", """If the sidebar width is fixed, faux columns are trivial. If both columns are fluid it gets harder. The "One True Layout" equal height trick (huge padding-bottom and negative margin-bottom) works too, but breaks anchors in some browsers."""),
  ("ricardo", "2008-10-01 11:18:00", """Fixed width sidebar, so faux columns. Thanks."""),
 ]),
 (4, "Web 2.0 glossy buttons - too much?", 0, 0, [
  ("aaronw", "2008-09-28 18:00:00", """Client wants "the glossy buttons, like on all the Web 2.0 sites". Reflection, gradient, rounded corners, and a beta badge (it's not a beta). I've done a version with less shine.

Is the glossy look dead yet, or am I just tired of it?"""),
  ("kerning", "2008-09-28 19:44:00", """You're tired of it. Clients aren't. Do the subtle version and show them the loud one next to it, they usually pick the subtle one when they see both side by side."""),
  ("pixelfreak", "2008-09-29 08:02:00", """The beta badge thing is the funniest trend of the last three years. Gmail is still beta."""),
  ("aaronw", "2008-10-13 18:27:00", """Update: they picked the subtle one, and the beta badge is gone. Kerning's trick works."""),
 ]),
 (6, "What's on your desk? October 2008", 0, 0, [
  ("jbaker", "2008-09-25 20:20:00", """Desk thread time. Mine: white MacBook (2007), a 22 inch Dell, Apple keyboard, a Wacom tablet I use maybe once a month, three coffee mugs at various stages."""),
  ("gridlock", "2008-09-26 07:15:00", """Mac Pro, two 20 inch Cinema displays, and an old ThinkPad with XP for IE testing. Plus a stack of A List Apart printouts I promised myself to read."""),
  ("sarah_m", "2008-09-27 03:30:00", """iMac 24, a sketchbook, and a cat who sits on the sketchbook."""),
  ("floatleft", "2008-09-28 11:08:00", """ThinkPad T61, Ubuntu 8.04 with a XP VM, 2 phones for mobile testing (one Nokia, one iPhone 3G)."""),
  ("dmitri", "2008-10-01 22:47:00", """MacBook Pro, 24 inch Dell, Das Keyboard, and a framed print of the CSS Zen Garden "Garden Party" design my wife gave me."""),
  ("jbaker", "2008-10-16 15:24:00", """Update: the white MacBook died, waiting for the new aluminium ones. Dell is going strong."""),
 ]),
 (3, "Firebug 1.2 slows down Firefox 3", 0, 0, [
  ("ricardo", "2008-09-23 10:10:00", """Since upgrading to Firefox 3 and Firebug 1.2, Gmail and some of our Ajax pages are very slow. Disable Firebug and they're fast again. Anyone else?"""),
  ("jbaker", "2008-09-23 12:40:00", """In 1.2 the Console, Script and Net panels are enabled per site. Keep them off for Gmail and anything you're not debugging. Script and Net are the slow ones."""),
  ("nate_w", "2008-09-24 04:15:00", """I keep a separate Firefox profile for development with Firebug and Web Developer toolbar, and a clean one for normal browsing. Problem solved and no more toolbar clutter."""),
  ("ricardo", "2008-09-24 16:30:00", """Turning the panels off for Gmail fixed it. Thanks."""),
 ]),
 (1, "37signals is dropping IE6 - can we?", 0, 0, [
  ("floatleft", "2008-08-12 09:10:00", """37signals stops supporting IE6 in Basecamp and their other apps on August 15. Our IE6 share is about 18% of visitors. Is anyone else planning to drop it?"""),
  ("dmitri", "2008-08-12 11:30:00", """For a web app that people pay for, they can tell customers what browser to use. For a public marketing site, 18% is a lot of people to tell to go away."""),
  ("validator", "2008-08-12 13:51:00", """We did "IE6 gets a basic version". Same content, simpler layout, no PNGs, no fancy JavaScript. Still works, still readable, just less pretty. Takes much less time than pixel perfect."""),
  ("zoom1", "2008-08-12 17:02:00", """Agree with validator. Graceful degradation works for browsers too, not just JavaScript."""),
  ("hannah_j", "2008-08-13 07:40:00", """Our corporate clients still run IE6 on every desktop, so not an option for us. Maybe 2010."""),
  ("jenpowell", "2008-08-14 15:12:00", """There's an argument that the more big sites do it, the faster IE6 goes away. 37signals can afford to make that statement. Most of us have clients who can't."""),
  ("floatleft", "2008-09-02 10:20:00", """Two weeks later: 37signals' world didn't end. Our IE6 share is now 16%, slowly dropping."""),
 ]),
 (2, "Is CSS Zen Garden still worth studying?", 0, 0, [
  ("mike_t", "2008-09-15 20:05:00", """I'm learning CSS (came from print). People keep telling me to look at CSS Zen Garden. It's from 2003, is it still useful, or are the techniques out of date?"""),
  ("kerning", "2008-09-15 21:30:00", """Still useful, maybe more for the idea than the code. The point is that the same HTML can look completely different with only CSS. Look at the designs, then open the CSS and figure out how they did it."""),
  ("gridlock", "2008-09-16 07:44:00", """Some of the old techniques are hacks you don't need now (box model hack for IE5). But most of it is fine. Then read the A List Apart articles: Sliding Doors, Faux Columns, In Search of the Holy Grail. That covers the basics."""),
  ("dmitri", "2008-09-16 22:15:00", """And get a copy of Andy Clarke's Transcending CSS or Dan Cederholm's Bulletproof Web Design. The second one especially."""),
  ("mike_t", "2008-10-09 17:10:00", """Bought Bulletproof Web Design, halfway through it. Thanks for the tips."""),
 ]),
 (6, "iPhone 3G for testing - worth it?", 0, 0, [
  ("pixelfreak", "2008-09-05 12:00:00", """Clients started asking how sites look on the iPhone. Is it worth buying one just for testing, or is Safari on the desktop close enough?"""),
  ("floatleft", "2008-09-05 13:22:00", """The rendering is similar to Safari 3.1, but the viewport is different. Pages zoom out to 980px wide unless you set the viewport meta tag. And fixed positioning doesn't work as you'd expect. You need the real thing for that."""),
  ("liza", "2008-09-05 19:08:00", """The iPhone SDK has a simulator for Mac. It's close enough for a quick look, and it's free."""),
  ("pixelfreak", "2008-09-06 09:43:00", """No Mac at work. I'll borrow a friend's for now."""),
 ]),
 (5, "[Hiring] Contract: WordPress theme from PSD, remote", 0, 0, [
  ("chloe_d", "2008-09-01 09:00:00", """Small design studio in Lyon looking for someone to turn 6 PSDs into a WordPress 2.6 theme. Remote OK. Budget about 1200 EUR, two weeks. Must be valid XHTML and work in IE6.

Contact through my profile page."""),
  ("ricardo", "2008-09-01 14:20:00", """Interested. Sent you an email."""),
  ("chloe_d", "2008-09-08 10:12:00", """Filled, thanks everyone. Ricardo is doing it."""),
 ]),
 (3, "Event delegation in jQuery 1.2", 0, 0, [
  ("aaronw", "2008-09-20 21:30:00", """I'm loading table rows with Ajax and my click handlers don't work on the new rows. I know about the livequery plugin. Is that the right approach, or is there a better way?"""),
  ("floatleft", "2008-09-21 06:55:00", """Event delegation: one handler on the table, check the target.

$('#results').click(function(e) {
    var row = $(e.target).parents('tr:first');
    if (row.length) { ... }
});

The handler stays on the table, so rows added later work without rebinding."""),
  ("aaronw", "2008-09-21 10:12:00", """Way better than rebinding after every load. Thanks."""),
  ("jbaker", "2008-09-22 18:20:00", """Also way faster with big tables. One handler instead of 500."""),
 ]),
]
