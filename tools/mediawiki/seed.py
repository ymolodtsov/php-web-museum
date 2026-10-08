#!/usr/bin/env python3
"""Retrocomputing Wiki seed content for MediaWiki 1.10.2 (archive date 11 September 2007).

Writes two files into the directory given as argv[1]:
  users.sql  - the wiki's registered users (inserted before the import)
  pages.xml  - every page with its full revision history, for maintenance/importDump.php

Earlier revisions are derived from the final text (sections cut, sentences
replaced) so that History and diffs show plausible, real changes.
"""
import hashlib
import os
import re
import sys
from xml.sax.saxutils import escape

USERS = [
    # name, registered, groups
    ("Datasette Dave", "20070304185112", ["sysop", "bureaucrat"]),
    ("SpriteWrangler64", "20070321203317", []),
    ("Front Panel Phil", "20070402221004", []),
    ("VIC II fan", "20070428150233", []),
    ("Zilog Zed", "20070506114019", []),
    ("Tramiel Historian", "20070526091248", []),
    ("Bitplane", "20070617132541", []),
]


def cut(text, *headings):
    """Remove whole sections (heading line up to the next heading of the same or higher level)."""
    for h in headings:
        m = re.search(r"^(=+) *" + re.escape(h) + r" *\1 *$", text, re.M)
        if not m:
            raise SystemExit("no section " + h)
        level = len(m.group(1))
        rest = text[m.end():]
        n = re.search(r"^={1,%d}[^=]" % level, rest, re.M)
        if n:
            end = m.end() + n.start()
        else:  # last section: keep the category links at the bottom
            c = rest.find("\n[[Category:")
            end = m.end() + (c + 1 if c >= 0 else len(rest))
        text = text[: m.start()] + text[end:]
    return text


def sub(text, *pairs):
    for old, new in pairs:
        if old not in text:
            raise SystemExit("not found: " + old[:60])
        text = text.replace(old, new, 1)
    return text


PAGES = []  # (title, [(timestamp, user, comment, minor, text)])


def page(title, *revs):
    PAGES.append((title, list(revs)))


def sig(user, when):
    if re.match(r"^\d+\.\d+\.\d+\.\d+$", user):
        return "[[Special:Contributions/%s|%s]] %s (UTC)" % (user, user, when)
    return "[[User:%s|%s]] %s (UTC)" % (user, user, when)


# ---------------------------------------------------------------- templates

INFOBOX = """{| class="toccolours" style="float:right; margin:0 0 0.8em 1em; width:250px; font-size:90%;" cellpadding="3"
! colspan="2" style="background:#d8d0b8; text-align:center; font-size:110%;" | {{{name}}}
|-
| style="width:40%;" | '''Manufacturer''' || {{{manufacturer}}}
|-
| '''Type''' || {{{type}}}
|-
| '''Released''' || {{{released}}}
|-
| '''Introductory price''' || {{{price}}}
|-
| '''Discontinued''' || {{{discontinued}}}
|-
| '''CPU''' || {{{cpu}}}
|-
| '''Memory''' || {{{memory}}}
|-
| '''Storage''' || {{{storage}}}
|-
| '''Display''' || {{{display}}}
|-
| '''Sound''' || {{{sound}}}
|-
| '''Operating system''' || {{{os}}}
|}<noinclude>
This is the standard information box for articles about a particular computer model. Copy the code below to the top of the article and fill in every field. If something is not known, put a question mark rather than leaving it empty.

<pre>
{{Infobox computer
| name         =
| manufacturer =
| type         =
| released     =
| price        =
| discontinued =
| cpu          =
| memory       =
| storage      =
| display      =
| sound        =
| os           =
}}
</pre>

[[Category:Templates]]
</noinclude>"""

page("Template:Infobox computer",
     ("20070405201833", "Datasette Dave", "Infobox for computer articles, loosely based on the one on Wikipedia", False,
      sub(INFOBOX, ("If something is not known, put a question mark rather than leaving it empty.\n\n", ""))),
     ("20070406091502", "Datasette Dave", "ask for a ? instead of empty fields, they show up as {{{...}}}", False, INFOBOX))

STUB = """<div style="border:1px solid #c8c0a8; background:#fbfaf5; padding:3px 8px; margin:1em 0; font-size:90%;">''This article is a [[Retrocomputing Wiki:Stubs|stub]]. You can help the Retrocomputing Wiki by expanding it.''</div><noinclude>
Put this at the bottom of short articles.
[[Category:Templates]]
</noinclude><includeonly>[[Category:Stubs]]</includeonly>"""

page("Template:Stub",
     ("20070310171209", "Datasette Dave", "stub notice", False, STUB))

# ---------------------------------------------------------------- Commodore 64

C64 = """{{Infobox computer
| name         = Commodore 64
| manufacturer = [[Commodore International]]
| type         = [[Home computer]]
| released     = August 1982
| price        = US$595
| discontinued = April 1994
| cpu          = [[MOS Technology 6510]] at 1.02 MHz (NTSC) / 0.99 MHz (PAL)
| memory       = 64 [[kilobyte|KB]] RAM, 20 KB ROM
| storage      = [[Commodore Datasette|Datasette]] cassette, [[Commodore 1541|1541]] floppy disk drive
| display      = [[VIC-II]]; 320 &times; 200, 16 colours, 8 hardware sprites
| sound        = [[MOS Technology SID|SID]] 6581, three voices
| os           = [[Commodore BASIC]] 2.0 and KERNAL in ROM
}}
The '''Commodore 64''', commonly abbreviated as the '''C64''', is an [[:Category:8-bit computers|8-bit]] [[home computer]] introduced by [[Commodore International]] in August 1982. Built around the [[MOS Technology 6510]] microprocessor and 64 kilobytes of RAM, it was aggressively priced for its specifications and sold through department stores and discount retailers rather than exclusively through computer shops, a distribution strategy championed by company president [[Jack Tramiel]].

The machine's audio and graphics capabilities were considered advanced for a mass-market computer of its era. Its [[MOS Technology SID|SID]] sound chip gave rise to an enduring tradition of chiptune music, and the [[VIC-II]] graphics chip supported hardware sprites and smooth scrolling, features that made the platform a favourite among game developers throughout the 1980s.

== History ==
The 64 was designed in the second half of 1981 by a small team at [[MOS Technology]], Commodore's own chip-making subsidiary in Pennsylvania. The engineers had just finished a pair of new chips, a video chip and a sound chip, originally intended for a games console. Instead, Commodore decided to put them in a home computer that would replace the [[VIC-20]]. A working prototype was shown at the Winter [[Consumer Electronics Show]] in Las Vegas in January 1982, and the machine went on sale that August for $595.

Because Commodore owned MOS Technology, it could build the computer from its own chips far more cheaply than its competitors could buy theirs. This allowed Tramiel to cut the price repeatedly during the home computer price war of 1983, in which the [[Texas Instruments TI-99/4A]] and several other machines were driven off the market. By the end of 1983 the 64 was selling for under $300 in many stores, and it could be found in toy shops and supermarkets as well as computer dealers.

Tramiel left Commodore in January 1984 after a disagreement with chairman Irving Gould. The 64 continued to sell well without him, and Commodore produced a number of variants:

* The '''SX-64''' (1984), a portable "luggable" version with a built-in 5-inch colour screen and a 1541 drive.
* The '''Commodore 64C''' (1986), with a lighter, wedge-shaped case matching the [[Commodore 128]]. It was usually sold with the [[GEOS]] graphical operating system.
* The '''Commodore 64 Games System''' (1990), a games-only console derivative with no keyboard, sold mainly in Europe. It was not a success.

Production of the 64 ended when Commodore went bankrupt in April 1994. By then it had been on the market, in substantially the same form, for over eleven years, an unusually long run for a computing platform.

== Hardware ==
=== Processor and memory ===
The [[MOS Technology 6510]] is a version of the [[MOS Technology 6502|6502]] with a built-in six-bit I/O port. The 64 uses this port to switch the BASIC and KERNAL ROMs and the I/O area in and out of the address space, which means that nearly all of the 64 KB of RAM can be used by machine language programs. BASIC programs only see 38,911 bytes, which is the number printed on the start-up screen.

=== Graphics ===
The [[VIC-II]] (MOS 6567 in NTSC machines, 6569 in PAL machines) produces a 40 &times; 25 character text screen and a 320 &times; 200 bitmap mode, with a fixed palette of 16 colours. It also handles eight hardware sprites of 24 &times; 21 pixels, raster interrupts and fine scrolling. Programmers soon found ways to push it beyond its documented limits, such as opening the top and bottom borders or showing more than eight sprites by reusing them further down the screen.

=== Sound ===
The [[MOS Technology SID|SID]] (Sound Interface Device) was designed by [[Bob Yannes]]. It has three voices, each with its own ADSR envelope and a choice of four waveforms, as well as a programmable filter. At a time when most home computers could only beep, the SID made the 64 a real musical instrument, and composers such as [[Rob Hubbard]], [[Martin Galway]] and [[Ben Daglish]] became well known through their game soundtracks.

=== Peripherals ===
The 64 has a cartridge port, a user port, two joystick ports compatible with [[Atari]] joysticks, a cassette port and a serial bus for disk drives and printers. The [[Commodore 1541|1541]] disk drive is notoriously slow over this serial bus, at around 400 bytes per second, so "fast loader" cartridges such as the Epyx FastLoad and the Action Replay were among the most popular add-ons.

== Software ==
Thousands of commercial titles were released for the 64, most of them games. Well-known examples include ''Impossible Mission'', ''Paradroid'', ''Bruce Lee'', ''Maniac Mansion'' and ''The Last Ninja''. Productivity software was also available, including word processors such as ''Paperclip'' and ''Easy Script'', and Berkeley Softworks' [[GEOS]], which gave the 64 a windowed desktop in 1986.

The machine boots straight into [[Commodore BASIC]] version 2.0, a Microsoft-derived BASIC with no commands for graphics or sound. Users had to <code>POKE</code> values directly into the chip registers, which is one reason so many 64 owners ended up learning machine language.

== Sales ==
The Commodore 64 is often called the best-selling single computer model of all time. Figures between 17 and 30 million have been quoted over the years, but the true number is not known, as Commodore never published official totals. Most estimates by people who have looked at the production records put it somewhere between 12 and 17 million units. See the [[Talk:Commodore 64|talk page]] for discussion.

== Legacy ==
Collectors and emulation enthusiasts have kept the platform active well past its commercial lifetime. Emulators such as [[VICE]] and CCS64 run on modern PCs, and in 2004 the C64 Direct-to-TV, a joystick with a complete 64 and 30 games built in, sold well in the United States.

The 64 was also home to one of the first large [[demoscene]] communities, and new demos, games and music are still being released for it, on disk as well as on cartridge. SID tunes are collected in the High Voltage SID Collection, which has over 30,000 entries, and chiptune musicians still use real SID chips on stage.

== See also ==
* [[VIC-20]]
* [[Commodore 128]]
* [[Amiga 500]]
* [[MOS Technology 6502]]

[[Category:8-bit computers]]
[[Category:Commodore hardware]]
[[Category:1982 introductions]]"""

C64_STUB = """The '''Commodore 64''' (C64) is an 8-bit home computer made by [[Commodore International]]. It came out in 1982 and has 64 KB of RAM, which is where the name comes from. It was very popular for games.

It uses a [[MOS Technology 6510]] processor and has a special sound chip called the SID.

[[Category:8-bit computers]]
[[Category:Commodore hardware]]"""

C64_R2 = C64_STUB + """

== Technical specifications ==
* CPU: MOS 6510 at about 1 MHz
* RAM: 64 KB
* ROM: 20 KB (BASIC, KERNAL and character set)
* Graphics: VIC-II, 320x200 pixels, 16 colours, 8 sprites
* Sound: SID 6581, 3 voices
* Ports: cartridge, user port, serial bus, cassette, 2 joystick ports"""

# Build intermediate C64 revisions by removing material from the final text.
C64_HW = cut(C64, "History", "Software", "Sales", "Legacy", "See also")
C64_HW = sub(C64_HW,
    ("Built around the [[MOS Technology 6510]] microprocessor and 64 kilobytes of RAM, it was aggressively priced for its specifications and sold through department stores and discount retailers rather than exclusively through computer shops, a distribution strategy championed by company president [[Jack Tramiel]].",
     "It is built around the [[MOS Technology 6510]] microprocessor and has 64 kilobytes of RAM."),
    ("[[MOS Technology SID|SID]] sound chip gave", "SID sound chip gave"),
    ("[[Category:1982 introductions]]", ""))
C64_HW = C64_HW.split("}}\n", 1)[1]  # no infobox yet

C64_INFOBOX = "{{Infobox computer" + C64.split("{{Infobox computer", 1)[1].split("}}\n", 1)[0] + "}}\n" + C64_HW
C64_HIST = cut(C64, "Software", "Sales", "Legacy", "See also")
C64_HIST = sub(C64_HIST,
    (", it was aggressively priced for its specifications and sold through department stores and discount retailers rather than exclusively through computer shops, a distribution strategy championed by company president [[Jack Tramiel]].",
     ", it was sold at a very low price for its specifications."),
    ("[[MOS Technology SID|SID]] sound chip gave", "SID sound chip gave"),
    ("* The '''Commodore 64 Games System''' (1990), a games-only console derivative with no keyboard, sold mainly in Europe. It was not a success.\n", ""))
C64_RETAIL = sub(cut(C64, "Legacy", "See also"),
    ("[[MOS Technology SID|SID]] sound chip gave", "SID sound chip gave"),
    ("* The '''Commodore 64 Games System''' (1990), a games-only console derivative with no keyboard, sold mainly in Europe. It was not a success.\n", ""))
C64_SIDLINK = sub(cut(C64, "Legacy"),
    ("* The '''Commodore 64 Games System''' (1990), a games-only console derivative with no keyboard, sold mainly in Europe. It was not a success.\n", ""))
C64_LEGACY = sub(C64,
    ("* The '''Commodore 64 Games System''' (1990), a games-only console derivative with no keyboard, sold mainly in Europe. It was not a success.\n", ""))

page("Commodore 64",
     ("20070304194033", "Datasette Dave", "new article", False, C64_STUB),
     ("20070318154710", "68.42.117.203", "", False, C64_R2),
     ("20070322211904", "SpriteWrangler64", "rewrote intro, replaced spec list with Hardware section (graphics, sound, peripherals)", False, C64_HW),
     ("20070405203540", "Datasette Dave", "added {{Infobox computer}}", False, C64_INFOBOX),
     ("20070527102215", "Tramiel Historian", "History section: design at MOS, CES 1982, price war, Tramiel leaving, variants", False, C64_HIST),
     ("20070721221006", "Tramiel Historian", "Software and Sales sections; sales figure is disputed, see talk", False, sub(C64_RETAIL,
         (", it was aggressively priced for its specifications and sold through department stores and discount retailers rather than exclusively through computer shops, a distribution strategy championed by company president [[Jack Tramiel]].",
          ", it was sold at a very low price for its specifications."))),
     ("20070814112703", "Tramiel Historian", "Added background on retail distribution strategy", False, C64_RETAIL),
     ("20070827180511", "VIC II fan", "Fixed SID chip wikilink, minor copyedit", True, C64_SIDLINK),
     ("20070905224108", "Datasette Dave", "Expanded Legacy section, mentioned chiptune communities", False, C64_LEGACY),
     ("20070911091422", "SpriteWrangler64", "Added note on Commodore 64 Games System derivative", False, C64))

page("C64",
     ("20070709193012", "Datasette Dave", "redirect", False, "#REDIRECT [[Commodore 64]]"))

C64_TALK = """== Sales figures ==
You see figures as high as 30 million quoted on the web, which I'm fairly sure is way too high, so I've written the Sales section to say the real number is unknown. The 17 million figure seems to come from Commodore's own marketing and gets repeated everywhere, including the Guinness book. People who have gone through serial numbers and production reports come out lower, somewhere around 12.5 million. I don't think we should pick one number as fact. --""" + sig("Tramiel Historian", "22:13, 21 July 2007") + """

:Agreed. "Best-selling single model" is probably still true either way, nothing else from that era comes close except maybe the Spectrum family if you count all the clones. --""" + sig("SpriteWrangler64", "09:40, 22 July 2007") + """

::Only if you count the Russian clones, and nobody has any figures for those. Leave it as it is. --""" + sig("Zilog Zed", "18:02, 22 July 2007") + """

:::Fine by me. If anyone finds a proper source (Commodore annual reports?) please add it here first. --""" + sig("Datasette Dave", "19:12, 6 September 2007") + """

== Pictures ==
Can we get some photos for the article? I have a breadbin 64 and a 64C and could take pictures of both, but uploads are switched off on this wiki. --""" + sig("SpriteWrangler64", "21:55, 3 August 2007") + """

:Uploads are off for now because of the spam we had on the old forum. I'll turn them on once we have a few more admins. --""" + sig("Datasette Dave", "07:31, 4 August 2007") + """

== Games System ==
Is the C64GS worth its own article? It's a pretty obscure machine. --""" + sig("68.42.117.203", "15:20, 11 September 2007")

C64_TALK_1 = C64_TALK.split("\n\n== Pictures ==")[0].split("\n\n:::Fine by me.")[0]
C64_TALK_2 = C64_TALK.split("\n\n:::Fine by me.")[0] + "\n\n== Pictures ==" + C64_TALK.split("\n\n== Pictures ==")[1].split("\n\n== Games System ==")[0]
C64_TALK_2a = C64_TALK_2.split("\n\n:Uploads are off")[0]
C64_TALK_3 = C64_TALK.split("\n\n== Games System ==")[0]

page("Talk:Commodore 64",
     ("20070721221330", "Tramiel Historian", "/* Sales figures */ new section", False, C64_TALK.split("\n\n:Agreed.")[0]),
     ("20070722094012", "SpriteWrangler64", "/* Sales figures */", False, C64_TALK.split("\n\n::Only if")[0]),
     ("20070722180244", "Zilog Zed", "/* Sales figures */", False, C64_TALK_1),
     ("20070803215531", "SpriteWrangler64", "/* Pictures */ new section", False, C64_TALK_2a),
     ("20070804073148", "Datasette Dave", "/* Pictures */ re", False, C64_TALK_2),
     ("20070906191237", "Datasette Dave", "/* Sales figures */", False, C64_TALK_3),
     ("20070911152031", "68.42.117.203", "/* Games System */ new section", False, C64_TALK))

# ---------------------------------------------------------------- VIC-20

VIC20 = """The '''VIC-20''' is an [[:Category:8-bit computers|8-bit]] [[home computer]] made by [[Commodore International]]. It was first sold in Japan in 1980 as the '''VIC-1001''', and in North America and Europe from 1981 at a price of US$299.95. In Germany it was called the '''VC-20''', for "VolksComputer".

The VIC-20 uses a [[MOS Technology 6502]] at about 1 MHz and has only 5 KB of RAM, of which 3,583 bytes are free for BASIC programs. Its video chip, the VIC (Video Interface Chip, MOS 6560/6561), gives a screen of just 22 columns by 23 rows. Despite these limits it was the first computer of any kind to sell one million units, helped by a television advertising campaign starring William Shatner which asked "Why buy just a video game?"

Most of its software came on cartridges and cassettes. Many owners added RAM expansion cartridges of 3, 8 or 16 KB. Commodore stopped making the VIC-20 in January 1985, by which time it had been overtaken by its successor, the [[Commodore 64]].

{{stub}}

[[Category:8-bit computers]]
[[Category:Commodore hardware]]
[[Category:1980 introductions]]"""

page("VIC-20",
     ("20070310170524", "Datasette Dave", "stub", False, sub(VIC20,
         (" Despite these limits it was the first computer of any kind to sell one million units, helped by a television advertising campaign starring William Shatner which asked \"Why buy just a video game?\"", ""),
         ("{{stub}}\n\n", ""))),
     ("20070310171422", "Datasette Dave", "", True, sub(VIC20,
         (" Despite these limits it was the first computer of any kind to sell one million units, helped by a television advertising campaign starring William Shatner which asked \"Why buy just a video game?\"", ""))),
     ("20070624201810", "Tramiel Historian", "one million units, Shatner adverts", False, VIC20))

# ---------------------------------------------------------------- Altair 8800

ALTAIR = """{{Infobox computer
| name         = Altair 8800
| manufacturer = [[MITS]]
| type         = Kit computer
| released     = January 1975
| price        = US$397 (kit), $498 (assembled)
| discontinued = 1977
| cpu          = [[Intel 8080]] at 2 MHz
| memory       = 256 bytes standard, up to 64 KB
| storage      = Paper tape, cassette, 8-inch floppy disk (later)
| display      = Front panel lamps; serial terminal optional
| sound        = None
| os           = None built in; Altair BASIC, Altair DOS, [[CP/M]]
}}
The '''Altair 8800''' is a [[microcomputer]] designed in 1974 by [[MITS]] (Micro Instrumentation and Telemetry Systems) of Albuquerque, New Mexico, and sold from early 1975 as a kit and as an assembled machine. It was the first microcomputer to sell in large numbers, and is widely seen as the spark that started the personal computer industry. It also gave [[Microsoft]] its first product.

== History ==
MITS was a small company run by [[Ed Roberts]] that had made model rocket telemetry kits and then electronic calculators. By 1974 the calculator business was being crushed by large chip makers, and the company was deeply in debt. Roberts decided to build a computer kit around Intel's new [[Intel 8080|8080]] processor, which he was able to buy in quantity for $75 each, far below the list price.

The Altair appeared on the cover of the January 1975 issue of ''Popular Electronics'', which went on sale in December 1974. The magazine's technical editor, Les Solomon, had been looking for a computer project to publish. The machine on the cover was actually an empty mock-up, as the only working prototype had been lost in shipping. MITS had hoped to sell a few hundred kits in total; it received orders for several thousand within the first months, and struggled for most of 1975 to deliver them.

In 1977 MITS was sold to the Pertec Computer Corporation, which dropped the Altair name within about a year.

== Design ==
A basic Altair has no keyboard, no screen and no storage. It is a blue and grey box with a front panel of toggle switches and red LEDs. Programs were entered one byte at a time by setting the switches to a binary value and flipping the "deposit" switch, and the result was read off the lights. The standard machine came with only 256 bytes of memory.

Inside, the computer is built from plug-in cards on a backplane with 100-pin connectors. This bus was copied by many other manufacturers, and in 1976 it was renamed the [[S-100 bus]]. Cards were soon available from other companies for memory, serial and parallel ports, video displays and disk controllers, and an expanded Altair could be a genuinely useful computer.

== Software ==
In early 1975 [[Bill Gates]] and [[Paul Allen]] wrote a BASIC interpreter for the Altair without having access to one, using an 8080 simulator running on a PDP-10 at Harvard. Allen flew to Albuquerque to demonstrate it, loading it from paper tape, and it worked the first time. MITS licensed it as '''Altair BASIC''', and Gates and Allen set up their company, then called "Micro-Soft", to sell it. Allen became MITS's Director of Software.

Altair BASIC was widely copied by hobbyists who did not want to pay MITS's price for it, which led to Gates's well-known "Open Letter to Hobbyists" in early 1976.

== Influence ==
The Altair was shown at the first meeting of the [[Homebrew Computer Club]] in March 1975, and many of the club's members went on to build their own computers or start companies. One famous early demonstration was by Steve Dompier, who wrote a program that made the Altair play "The Fool on the Hill" through the radio interference picked up by a nearby transistor radio.

Clones and compatible machines followed quickly, most notably the [[IMSAI 8080]]. Original Altairs are now valuable collector's items.

== See also ==
* [[MOS Technology 6502]], the much cheaper processor that appeared later in 1975
* [[Apple II]]
* [[TRS-80]]

[[Category:8-bit computers]]
[[Category:Kit computers]]
[[Category:1975 introductions]]"""

ALTAIR_1 = sub(cut(ALTAIR, "Software", "Influence", "See also"),
    (" It also gave [[Microsoft]] its first product.", ""),
    (" The machine on the cover was actually an empty mock-up, as the only working prototype had been lost in shipping.", ""),
    ("which he was able to buy in quantity for $75 each, far below the list price", "which he was able to buy cheaply in quantity"))
ALTAIR_1 = ALTAIR_1.split("}}\n", 1)[1]
ALTAIR_2 = sub(cut(ALTAIR, "See also"),
    (" The machine on the cover was actually an empty mock-up, as the only working prototype had been lost in shipping.", ""),
    ("Original Altairs are now valuable collector's items.", "Original Altairs are now very collectable."))
ALTAIR_3 = sub(ALTAIR,
    (" The machine on the cover was actually an empty mock-up, as the only working prototype had been lost in shipping.", ""))

page("Altair 8800",
     ("20070402224812", "Front Panel Phil", "new article", False, ALTAIR_1),
     ("20070420215037", "Front Panel Phil", "Software and Influence sections, infobox", False, ALTAIR_2),
     ("20070812160355", "Front Panel Phil", "See also, copyedit", True, sub(ALTAIR_3,
         (" One famous early demonstration was by Steve Dompier, who wrote a program that made the Altair play \"The Fool on the Hill\" through the radio interference picked up by a nearby transistor radio.", ""))),
     ("20070812161940", "Front Panel Phil", "Dompier and the radio", False, ALTAIR_3),
     ("20070908163012", "Front Panel Phil", "the cover machine was a mock-up", False, ALTAIR))

# ---------------------------------------------------------------- MOS 6502

M6502 = """The '''MOS Technology 6502''' is an [[:Category:8-bit computers|8-bit]] microprocessor designed by a small team led by [[Chuck Peddle]] and [[Bill Mensch]] at [[MOS Technology]] and introduced in September 1975. It sold for $25 at a time when the [[Intel 8080]] and [[Motorola 6800]] cost around $150 to $180, and its low price made it the processor of choice for the first wave of home computers and video game consoles.

== History ==
Peddle and most of his team had worked on the Motorola 6800 and left Motorola in 1974 after the company showed no interest in a cheaper version. At MOS Technology they designed two processors, the 6501, which fitted the same socket as the 6800, and the 6502, which had a different pinout and an on-chip clock generator. Motorola sued over the 6501, and MOS agreed to drop it.

The 6502 was launched at the WESCON trade show in San Francisco, where it was sold over the counter from a jar. Buyers included [[Steve Wozniak]], who used it in the Apple I and later the [[Apple II]]. MOS Technology also sold the KIM-1, a single-board computer intended to help engineers learn the chip, which became popular with hobbyists in its own right.

[[Commodore International]] bought MOS Technology in 1976, which gave Commodore its own supply of processors for the [[Commodore PET]], the [[VIC-20]] and the [[Commodore 64]].

== Design ==
The 6502 has a small set of registers: an 8-bit accumulator (A), two 8-bit index registers (X and Y), an 8-bit stack pointer and a status register. Its 16-bit address bus can reach 64 KB of memory. To make up for the small number of registers, the first 256 bytes of memory, the ''zero page'', can be reached with shorter and faster instructions, and programmers use it almost like a large register file. The stack is fixed at page one ($0100-$01FF).

The instruction set has 56 instructions and was designed with simplicity in mind. A 1 MHz 6502 is roughly as fast as a 2 MHz 8080 in typical code, because most instructions take only two to four clock cycles.

=== Quirks ===
* The indirect jump instruction <code>JMP ($xxFF)</code> does not cross a page boundary correctly: it takes the high byte of the target from $xx00 instead of the next page.
* Undocumented opcodes do useful (and sometimes useless) things, and some programmers used them to save a few cycles.
* The processor has a decimal mode for BCD arithmetic, which the Ricoh version used in the NES left out.

== Variants ==
{| class="toccolours" cellpadding="4"
! Chip !! Used in !! Notes
|-
| 6502 || [[Apple II]], [[Commodore PET]], [[VIC-20]], [[Atari 8-bit family]], [[BBC Micro]] || original NMOS part
|-
| 6507 || [[Atari 2600]] || only 13 address lines, 28-pin package
|-
| 6510 || [[Commodore 64]] || adds a 6-bit I/O port
|-
| 2A03 || Nintendo Entertainment System || made by Ricoh, no decimal mode, sound on chip
|-
| 65C02 || Apple IIc, enhanced Apple IIe || CMOS version from the Western Design Center
|-
| 65C816 || Apple IIGS, Super Nintendo || 16-bit extension, 6502 compatible
|}

[[Category:Microprocessors]]"""

page("MOS Technology 6502",
     ("20070414193855", "Front Panel Phil", "new article", False, sub(cut(M6502, "Quirks", "Variants"),
         (" MOS Technology also sold the KIM-1, a single-board computer intended to help engineers learn the chip, which became popular with hobbyists in its own right.", ""))),
     ("20070415110420", "SpriteWrangler64", "variants table, the 6510 is in the C64", False, sub(cut(M6502, "Quirks"),
         (" MOS Technology also sold the KIM-1, a single-board computer intended to help engineers learn the chip, which became popular with hobbyists in its own right.", ""))),
     ("20070624210233", "Front Panel Phil", "KIM-1", True, cut(M6502, "Quirks")),
     ("20070829225110", "VIC II fan", "Quirks: JMP indirect bug, illegal opcodes", False, M6502))

page("6502",
     ("20070812162544", "Front Panel Phil", "redirect", False, "#REDIRECT [[MOS Technology 6502]]"))

# ---------------------------------------------------------------- Apple II

APPLE2 = """{{Infobox computer
| name         = Apple II
| manufacturer = [[Apple Computer]]
| type         = [[Home computer]]
| released     = June 1977
| price        = US$1,298 (4 KB), $2,638 (48 KB)
| discontinued = 1979 (replaced by the Apple II Plus)
| cpu          = [[MOS Technology 6502]] at 1.023 MHz
| memory       = 4 KB, expandable to 48 KB
| storage      = Cassette, [[Disk II]] 5.25-inch floppy drive (from 1978)
| display      = 40 &times; 24 text; 280 &times; 192 high-resolution graphics
| sound        = 1-bit speaker
| os           = Integer BASIC in ROM; Apple DOS from disk
}}
The '''Apple II''' is an [[:Category:8-bit computers|8-bit]] personal computer designed by [[Steve Wozniak]] and introduced by [[Apple Computer]] at the West Coast Computer Faire in April 1977. It was one of the first personal computers to be sold fully assembled in a plastic case, with a keyboard and colour graphics, and together with the [[Commodore PET]] and the [[TRS-80]] it is often counted as one of the "1977 trinity" of ready-made home computers. The Apple II and its successors were made for sixteen years and were Apple's main source of income until the late 1980s.

== Development ==
Wozniak had already designed the Apple I, a bare circuit board sold to hobbyists in 1976. The Apple II was a much more complete machine. Its colour video was generated with very few chips by taking advantage of the way NTSC television signals work, and it had eight expansion slots on the motherboard, which Wozniak insisted on against [[Steve Jobs]]'s wishes.

[[Mike Markkula]] invested $250,000 in the company and helped write its business plan, and Rod Holt designed a switching power supply that did not need a cooling fan. The beige plastic case was designed by Jerry Manock.

== Hardware ==
The Apple II uses a [[MOS Technology 6502]] at just over 1 MHz. The base model shipped with 4 KB of RAM and could be expanded to 48 KB on the motherboard. Wozniak's [[Integer BASIC]] was built into ROM, so the computer was ready to program as soon as it was switched on.

The video hardware offers a 40 &times; 24 upper-case text mode, a low-resolution graphics mode of 40 &times; 48 blocks in 16 colours and a high-resolution mode of 280 &times; 192 pixels. On the earliest boards high-resolution mode showed four colours (black, white, green and violet); later boards added orange and blue. Sound comes from a single speaker that the program clicks on and off directly.

=== Disk II ===
In 1978 Apple released the [[Disk II]] floppy drive and controller card, also designed by Wozniak, which used far fewer chips than other controllers of the time. With DOS 3.3 (1980) a disk holds 140 KB. The Disk II made the Apple II much more practical for business use and was an important reason for its success.

== VisiCalc ==
In 1979 Personal Software released [[VisiCalc]], the first spreadsheet program for personal computers, written by Dan Bricklin and Bob Frankston. For more than a year it was only available on the Apple II, and many businesses bought the computer just to run it. It is often called the first "killer application".

== Successors ==
* '''Apple II Plus''' (1979): Applesoft BASIC (licensed from [[Microsoft]]) in ROM, 48 KB as standard.
* '''Apple IIe''' (January 1983): upper and lower case, 64 KB, fewer chips. The longest-lived model, sold until 1993.
* '''Apple IIc''' (April 1984): a compact, semi-portable version with a built-in disk drive.
* '''Apple IIGS''' (September 1986): a 16-bit machine with a 65C816 processor and a much better sound chip, compatible with older Apple II software.
* '''Apple IIc Plus''' (1988): the last new model.

Apple stopped selling the Apple IIe in November 1993.

[[Category:8-bit computers]]
[[Category:Apple hardware]]
[[Category:1977 introductions]]"""

APPLE2_1 = sub(cut(APPLE2, "Disk II", "VisiCalc", "Successors"),
    (", and Rod Holt designed a switching power supply that did not need a cooling fan. The beige plastic case was designed by Jerry Manock.",
     "."))
page("Apple II",
     ("20070429201544", "VIC II fan", "new article", False, APPLE2_1),
     ("20070429203102", "VIC II fan", "", True, sub(APPLE2_1, (" helped write its business plan.", " helped write its business plan, and Rod Holt designed a switching power supply that did not need a cooling fan. The beige plastic case was designed by Jerry Manock."))),
     ("20070602140017", "Front Panel Phil", "VisiCalc, successors", False, cut(APPLE2, "Disk II")),
     ("20070905083014", "VIC II fan", "added Disk II section", False, APPLE2))

# ---------------------------------------------------------------- TRS-80

TRS80 = """{{Infobox computer
| name         = TRS-80 Model I
| manufacturer = [[Tandy Corporation]] / Radio Shack
| type         = [[Home computer]]
| released     = August 1977
| price        = US$599.95 with monitor and cassette recorder
| discontinued = January 1981
| cpu          = [[Zilog Z80]] at 1.77 MHz
| memory       = 4 KB, expandable to 48 KB
| storage      = Cassette, 5.25-inch floppy disk via the Expansion Interface
| display      = 64 &times; 16 text, 128 &times; 48 block graphics, monochrome
| sound        = None (cassette port often used for sound)
| os           = Level I or Level II BASIC in ROM; TRSDOS
}}
The '''TRS-80''' (from '''T'''andy/'''R'''adio '''S'''hack, Z-'''80''' processor) is a line of computers sold by [[Tandy Corporation]] through its Radio Shack stores. This article is about the first model, later called the '''TRS-80 Model I''', which was announced in August 1977. Because Radio Shack had thousands of stores across the United States, the TRS-80 was the easiest of the early computers to buy, and for a few years it outsold the [[Apple II]] and the [[Commodore PET]].

== History ==
The TRS-80 was designed by Don French, a Radio Shack buyer who had built his own computer from a kit, and Steve Leininger, an engineer hired from National Semiconductor. Tandy management was not convinced there was a market and ordered a first production run of only 3,500 machines, so that if they did not sell they could at least be used in the company's own stores. Around 10,000 orders arrived within the first month.

The computer was sold as a complete system with a monochrome monitor (a modified RCA black-and-white television) and a Radio Shack cassette recorder, for $599.95.

== Hardware ==
The main unit contains the keyboard, the [[Zilog Z80]] processor and 4 KB of RAM. The original ROM held '''Level I BASIC''', a small BASIC based on Li-Chen Wang's Tiny BASIC. It was replaced in 1978 by '''Level II BASIC''', a 12 KB [[Microsoft]] BASIC.

The video display shows 16 lines of 64 characters. There are no lower-case letters without a modification, and graphics are made from 2 &times; 3 blocks within each character cell, for a resolution of 128 &times; 48.

The '''Expansion Interface''', which sat under the monitor, added more memory, a floppy disk controller, a printer port and a second cassette port. It was connected by a short ribbon cable and had a reputation for unreliable connections and random reboots.

== Reception ==
The Model I was popular but had a number of problems. Keys often "bounced", producing double letters, until a software fix was released. Its cases leaked a great deal of radio interference, and when the US Federal Communications Commission introduced new rules on interference from home computers, Tandy decided to stop making the Model I rather than redesign it. It was replaced by the [[TRS-80 Model III]] in 1980.

Critics and owners sometimes called it the "Trash-80", although this was usually said with some affection.

[[Category:8-bit computers]]
[[Category:Tandy hardware]]
[[Category:1977 introductions]]"""

page("TRS-80",
     ("20070513200917", "Datasette Dave", "new article", False, sub(cut(TRS80, "Reception"),
         (" Tandy management was not convinced there was a market and ordered a first production run of only 3,500 machines, so that if they did not sell they could at least be used in the company's own stores. Around 10,000 orders arrived within the first month.", ""))),
     ("20070520114233", "Front Panel Phil", "Reception; first production run", False, TRS80))

# ---------------------------------------------------------------- ZX Spectrum

ZX = """{{Infobox computer
| name         = ZX Spectrum
| manufacturer = [[Sinclair Research]]
| type         = [[Home computer]]
| released     = 23 April 1982
| price        = &pound;125 (16 KB), &pound;175 (48 KB)
| discontinued = 1992
| cpu          = [[Zilog Z80]]A at 3.5 MHz
| memory       = 16 KB or 48 KB RAM, 16 KB ROM
| storage      = Cassette; [[ZX Microdrive]] via Interface 1
| display      = 256 &times; 192, 15 colours, colour attributes per 8 &times; 8 cell
| sound        = 1-bit beeper
| os           = Sinclair BASIC in ROM
}}
The '''ZX Spectrum''' is an [[:Category:8-bit computers|8-bit]] [[home computer]] released in the United Kingdom by [[Sinclair Research]] on 23 April 1982. It followed the black-and-white [[Sinclair ZX81]] and was Sinclair's first colour computer. Cheap, small and easy to program, it became the best-selling computer in Britain in the early 1980s and was the machine on which a large part of the British games industry got its start. Its fans often call it the '''Speccy'''.

== Design ==
The Spectrum was designed by Richard Altwasser, who did the electronics, and Rick Dickinson, who designed the case and the keyboard. The ROM, containing Sinclair BASIC, was written by Steve Vickers and John Grant of Nine Tiles. To keep the price down the machine uses an uncommitted logic array (ULA) made by Ferranti in place of dozens of separate chips, and it was assembled under contract by [[Timex Corporation|Timex]] in Dundee, Scotland.

The original model has a keyboard of grey rubber keys, which gave it the nickname "dead flesh" keyboard. Each key carries up to six functions, and BASIC keywords are entered with a single keypress: pressing P in the right mode types <code>PRINT</code>, for example. This saved memory and typing, but took some getting used to.

== Graphics and sound ==
The screen is 256 &times; 192 pixels with eight colours, each in a normal and a bright version (black looks the same in both, so there are 15 distinct colours). To save memory, colour is stored separately from the pixels, with one ink and one paper colour for each block of 8 &times; 8 pixels. When two differently coloured objects overlap the same block, one of them changes colour. This effect is known as '''attribute clash''' or '''colour clash''' and is one of the most recognisable things about Spectrum games. Many games avoided it by using only one colour for the playing area.

Sound comes from a small beeper driven directly by the processor. Clever programmers managed to get two or more channels of music out of it, but the processor could do little else while doing so.

== Storage ==
Programs were normally loaded from ordinary audio cassettes, which took several minutes for a large game and did not always work the first time. In 1983 Sinclair introduced the [[ZX Microdrive]], a fast tape loop cartridge drive that connected through the ''Interface 1'', which also added an RS-232 port and a simple local network.

== Models ==
{| class="toccolours" cellpadding="4"
! Model !! Year !! Notes
|-
| ZX Spectrum 16K / 48K || 1982 || rubber keyboard
|-
| ZX Spectrum+ || 1984 || hard plastic keys and a reset button, 48 KB
|-
| ZX Spectrum 128 || 1985 (Spain), 1986 (UK) || 128 KB, AY-3-8912 sound chip, improved BASIC
|-
| ZX Spectrum +2 || 1986 || Amstrad model with built-in cassette recorder
|-
| ZX Spectrum +3 || 1987 || Amstrad model with a 3-inch floppy disk drive
|}

In April 1986 Sinclair Research sold its computer business and the Sinclair brand to [[Amstrad]], which made the +2 and +3 and kept the Spectrum in production until 1992. In the United States a modified version was sold as the Timex Sinclair 2068, without much success. Unlicensed clones were built in large numbers in Eastern Europe and the Soviet Union.

== Software ==
Several thousand games were published for the Spectrum, many of them written by one or two people in their bedrooms. Well-known titles include ''Manic Miner'' and ''Jet Set Willy'' by Matthew Smith, ''Knight Lore'' and ''Sabre Wulf'' by Ultimate Play the Game, ''Skool Daze'', ''Head Over Heels'' and the Spectrum version of ''[[Elite (video game)|Elite]]''. Many later British developers, including Rare, the company that grew out of Ultimate, began on the Spectrum.

Spectrum emulators are available for almost every modern platform, and the World of Spectrum website keeps a large archive of the machine's software, with permission from many of the original publishers.

== See also ==
* [[Sinclair ZX81]]
* [[BBC Micro]]
* [[Commodore 64]]

[[Category:8-bit computers]]
[[Category:Sinclair hardware]]
[[Category:1982 introductions]]"""

ZX_1 = sub(cut(ZX, "Storage", "Models", "Software", "See also"),
    (" Its fans often call it the '''Speccy'''.", ""),
    (" Many games avoided it by using only one colour for the playing area.", ""),
    (" Clever programmers managed to get two or more channels of music out of it, but the processor could do little else while doing so.", ""),
    ("attribute clash''' or '''colour clash'''", "colour clash'''"))
ZX_2 = sub(cut(ZX, "See also"),
    (" Its fans often call it the '''Speccy'''.", ""),
    ("attribute clash''' or '''colour clash'''", "colour clash'''"),
    ("| ZX Spectrum 128 || 1985 (Spain), 1986 (UK) ||", "| ZX Spectrum 128 || 1986 ||"))
ZX_3 = sub(cut(ZX, "See also"),
    (" Its fans often call it the '''Speccy'''.", ""),
    ("attribute clash''' or '''colour clash'''", "colour clash'''"))
ZX_4 = sub(cut(ZX, "See also"),
    ("attribute clash''' or '''colour clash'''", "colour clash'''"))

page("ZX Spectrum",
     ("20070506121807", "Zilog Zed", "new article", False, ZX_1),
     ("20070603193342", "Zilog Zed", "storage, models, software", False, ZX_2),
     ("20070630133120", "81.152.67.23", "the 128 came out in Spain first", True, ZX_3),
     ("20070710212407", "Zilog Zed", "Speccy", True, ZX_4),
     ("20070909142240", "Zilog Zed", "attribute clash, see also", False, ZX))

ZX_TALK = """== Colour or color? ==
Should we use British or American spelling? The C64 article says "colour" but the Apple II one says "color" in a couple of places. --""" + sig("VIC II fan", "20:44, 4 June 2007") + """

:My vote is to use whatever fits the machine: British spelling for British computers and American for American ones, like Wikipedia does. The main thing is not to keep changing it back and forth. --""" + sig("Zilog Zed", "21:30, 4 June 2007") + """

::Sounds sensible. I'll add it to the [[Retrocomputing Wiki:Community Portal|community portal]] as a style rule. --""" + sig("Datasette Dave", "08:15, 5 June 2007") + """

== Sales ==
Does anyone have a reliable number for how many Spectrums were sold? I've seen "over 5 million" a few times but never with a source. --""" + sig("81.152.67.23", "13:40, 30 June 2007") + """

:Not that I know of. Sinclair stopped quoting figures after Amstrad took over. I've left it out of the article for now. --""" + sig("Zilog Zed", "14:20, 9 September 2007")

page("Talk:ZX Spectrum",
     ("20070604204410", "VIC II fan", "/* Colour or color? */ new section", False, ZX_TALK.split("\n\n:My vote")[0]),
     ("20070604213017", "Zilog Zed", "/* Colour or color? */", False, ZX_TALK.split("\n\n::Sounds sensible")[0]),
     ("20070605081544", "Datasette Dave", "/* Colour or color? */", False, ZX_TALK.split("\n\n== Sales ==")[0]),
     ("20070630134051", "81.152.67.23", "/* Sales */ new section", False, ZX_TALK.split("\n\n:Not that I know")[0]),
     ("20070909142017", "Zilog Zed", "/* Sales */", False, ZX_TALK))

# ---------------------------------------------------------------- BBC Micro

BBC = """{{Infobox computer
| name         = BBC Microcomputer
| manufacturer = [[Acorn Computers]]
| type         = [[Home computer]]
| released     = December 1981
| price        = &pound;235 (Model A), &pound;335 (Model B)
| discontinued = 1994 (Master series)
| cpu          = [[MOS Technology 6502|6502A]] at 2 MHz
| memory       = 16 KB (Model A), 32 KB (Model B)
| storage      = Cassette, 5.25-inch floppy disk with DFS
| display      = 8 screen modes up to 640 &times; 256; teletext Mode 7
| sound        = Texas Instruments SN76489, three voices plus noise
| os           = Acorn MOS, [[BBC BASIC]] in ROM
}}
The '''BBC Microcomputer''', usually called the '''BBC Micro''' or just '''the Beeb''', is a series of [[:Category:8-bit computers|8-bit computers]] built by [[Acorn Computers]] for the British Broadcasting Corporation's Computer Literacy Project. It went on sale in December 1981. The BBC Micro was used in the great majority of British schools during the 1980s, and a whole generation of British programmers learned on it.

== Background ==
In 1980 the BBC planned a television series about computers and wanted a machine that viewers could buy and that would be featured in the programmes. Several British companies were considered, including Sinclair and Newbury Laboratories. Acorn, based in Cambridge, won the contract after [[Hermann Hauser]] and [[Chris Curry]] had their engineers build a working prototype in about a week for the BBC's visit.

The series, ''The Computer Programme'', was first shown in January 1982, and was followed by several others. Demand was much higher than expected and early buyers had to wait months for their machines. The original prices of &pound;235 for the Model A and &pound;335 for the Model B were soon raised to &pound;299 and &pound;399.

== Hardware ==
The BBC Micro was designed mainly by [[Steve Furber]] and [[Sophie Wilson]]. It uses a 6502 running at 2 MHz, which made it one of the fastest 8-bit home computers. The Model B has 32 KB of RAM, shared between programs and the screen.

The machine is well known for its many ports. Alongside the cassette, printer and RS-423 serial ports there is a user port, an analogue port for joysticks, a "1 MHz bus" for scientific equipment, and the '''Tube''', which allowed a second processor to be connected. Second processors were sold with a faster 6502, a [[Zilog Z80|Z80]] for running [[CP/M]], and a 32016. Most machines in schools were also fitted with [[Econet]], Acorn's low-cost network, so that a classroom could share a disk drive and a printer.

=== Screen modes ===
There are eight screen modes, numbered 0 to 7. The highest resolution is 640 &times; 256 in two colours (Mode 0), and Mode 2 gives 160 &times; 256 in 16 colours (eight of them flashing). Mode 7 uses a Mullard SAA5050 teletext chip to show colourful text and block graphics while using only 1 KB of memory, which is why so many BBC programs, from school software to the BBC's own Ceefax pages, look the way they do.

== Software ==
[[BBC BASIC]], written by Sophie Wilson, was one of the best BASICs of its time. It has procedures and functions with local variables, long variable names and a built-in 6502 assembler, so that assembly language could be mixed with BASIC in the same program.

The most famous BBC Micro game is ''[[Elite (video game)|Elite]]'' (1984), a 3D space trading game by David Braben and Ian Bell, published by Acornsoft. Other popular games include ''Repton'', ''Chuckie Egg'' and ''Citadel''.

== Later models and legacy ==
Acorn released the cheaper [[Acorn Electron]] in 1983, the BBC Model B+ in 1985 and the BBC Master in 1986. About 1.5 million BBC Micros were sold in total.

Acorn's engineers went on to design their own processor, the Acorn RISC Machine or [[ARM architecture|ARM]], using BBC Micros with second processors to simulate it. The first ARM chips were tested in 1985 attached to a BBC Micro through the Tube.

[[Category:8-bit computers]]
[[Category:Acorn hardware]]
[[Category:1981 introductions]]"""

BBC_1 = sub(cut(BBC, "Screen modes", "Later models and legacy"),
    (" Most machines in schools were also fitted with [[Econet]], Acorn's low-cost network, so that a classroom could share a disk drive and a printer.", ""),
    ("The most famous BBC Micro game is ''[[Elite (video game)|Elite]]'' (1984), a 3D space trading game by David Braben and Ian Bell, published by Acornsoft. Other popular games include ''Repton'', ''Chuckie Egg'' and ''Citadel''.",
     "Popular games include ''Elite'', ''Repton'' and ''Chuckie Egg''."))
BBC_2 = sub(BBC,
    (" Most machines in schools were also fitted with [[Econet]], Acorn's low-cost network, so that a classroom could share a disk drive and a printer.", ""),
    ("The most famous BBC Micro game is ''[[Elite (video game)|Elite]]'' (1984), a 3D space trading game by David Braben and Ian Bell, published by Acornsoft. Other popular games include ''Repton'', ''Chuckie Egg'' and ''Citadel''.",
     "Popular games include ''Elite'', ''Repton'' and ''Chuckie Egg''."))

page("BBC Micro",
     ("20070519161205", "Zilog Zed", "new article", False, BBC_1),
     ("20070707102618", "Zilog Zed", "screen modes, later models, ARM", False, BBC_2),
     ("20070904211044", "Zilog Zed", "Econet, more on Elite", False, BBC))

# ---------------------------------------------------------------- Amiga 500

A500 = """{{Infobox computer
| name         = Amiga 500
| manufacturer = [[Commodore International]]
| type         = [[Home computer]]
| released     = 1987
| price        = US$699, &pound;499
| discontinued = 1991 (replaced by the A500 Plus)
| cpu          = [[Motorola 68000]] at 7.09 MHz (PAL) / 7.16 MHz (NTSC)
| memory       = 512 KB chip RAM, expandable
| storage      = Built-in 3.5-inch floppy drive, 880 KB
| display      = OCS; up to 32 colours from 4,096 (4,096 in HAM mode)
| sound        = Paula; four 8-bit PCM channels, stereo
| os           = [[AmigaOS]] 1.2/1.3 (Kickstart in ROM, Workbench on disk)
}}
The '''Amiga 500''', also known as the '''A500''', is a [[:Category:16-bit computers|16-bit]] [[home computer]] made by [[Commodore International]]. Announced in early 1987 alongside the professional [[Amiga 2000]], it was the low-cost model of the Amiga range and put the graphics and sound of the original [[Amiga 1000]] into a single keyboard case. It became the best-selling Amiga by far, and in Europe it was one of the most popular games machines of the late 1980s and early 1990s.

== Background ==
The Amiga was designed by a small company in California, originally called Hi-Toro and later Amiga Corporation, where [[Jay Miner]] led the design of the custom chipset. Amiga ran out of money in 1984 and was bought by Commodore, which launched the Amiga 1000 in 1985. The 1000 was technically impressive but too expensive for the home market, so Commodore set out to build a cheaper version.

== Hardware ==
Like the [[Atari ST]], the A500 uses a [[Motorola 68000]] processor, but most of its power comes from three custom chips, known together as the Original Chip Set (OCS):

* '''Agnus''' contains the blitter, which copies and combines blocks of graphics in memory, and the copper, a simple co-processor that can change hardware registers at chosen points on the screen.
* '''Denise''' produces the display, including eight hardware sprites. Normal modes show up to 32 colours from a palette of 4,096; Extra Half-Brite gives 64, and Hold-And-Modify (HAM) can show all 4,096 at once.
* '''Paula''' handles four channels of 8-bit sampled sound, two on each stereo side, as well as the floppy disk and serial port.

The machine has 512 KB of RAM as standard. Most owners bought the A501 expansion, which fits in a trapdoor underneath the computer and adds another 512 KB and a battery-backed clock.

== Software ==
The operating system, AmigaOS, consists of the Kickstart ROM and the Workbench disk. It offered pre-emptive multitasking in 1985, years before the Macintosh or Windows did. Most games, however, took over the whole machine and booted directly from their own disks.

Notable games include ''Shadow of the Beast'' (1989), ''Lemmings'' (1991), ''Speedball 2'' (1990), ''Sensible Soccer'' (1992), ''Turrican II'' and ''The Secret of Monkey Island''. The Amiga was also popular for graphics and music work, with programs such as ''Deluxe Paint''.

=== Trackers and the demoscene ===
In 1987 Karsten Obarski released ''Ultimate Soundtracker'', a music program that used the four sound channels to play short samples arranged in patterns. Its file format, MOD, was copied by many later trackers such as ProTracker and is still in use today. Together with the large number of A500s in Europe, this helped the Amiga become the centre of the [[demoscene]] in the late 1980s.

== Later history ==
In 1991 the A500 was replaced by the A500 Plus, with the Enhanced Chip Set and Kickstart 2.04, and in 1992 by the smaller A600. Commodore went bankrupt in April 1994, and the rights to the Amiga have changed hands several times since. AmigaOS 4.0 was released in December 2006 for new PowerPC-based hardware, but the classic A500 remains the machine most people mean when they talk about the Amiga.

[[Category:16-bit computers]]
[[Category:Commodore hardware]]
[[Category:1987 introductions]]"""

A500_1 = sub(cut(A500, "Trackers and the demoscene", "Later history"),
    (" Most owners bought the A501 expansion, which fits in a trapdoor underneath the computer and adds another 512 KB and a battery-backed clock.", ""))
A500_2 = sub(A500, ("''Turrican II''", "''Turican II''"))

page("Amiga 500",
     ("20070617140310", "Bitplane", "new article", False, A500_1),
     ("20070802192255", "Bitplane", "trackers/demoscene, later history, A501", False, sub(A500_2, ("''Lemmings'' (1991)", "''Lemmings'' (1990)"))),
     ("20070803081104", "SpriteWrangler64", "Lemmings came out in February 1991", True, A500_2),
     ("20070907120533", "Bitplane", "typo", True, A500))

# ---------------------------------------------------------------- IBM PC

IBMPC = """{{Infobox computer
| name         = IBM Personal Computer
| manufacturer = [[IBM]]
| type         = Personal computer
| released     = 12 August 1981
| price        = US$1,565 (16 KB, no disk drives)
| discontinued = April 1987
| cpu          = [[Intel 8088]] at 4.77 MHz
| memory       = 16 KB to 256 KB on the motherboard (640 KB with cards)
| storage      = Cassette interface; one or two 5.25-inch floppy drives (160 KB)
| display      = [[Monochrome Display Adapter|MDA]] or [[Color Graphics Adapter|CGA]] card
| sound        = PC speaker
| os           = Cassette BASIC in ROM; [[PC DOS]] 1.0, [[CP/M-86]], UCSD p-System
}}
The '''IBM Personal Computer''', model number '''5150''' and usually called the '''IBM PC''', is a personal computer announced by [[IBM]] on 12 August 1981. It was IBM's first successful microcomputer. Because IBM built it from standard parts and published its technical details, other companies were able to build compatible machines, and the "IBM compatible" PC went on to become the standard business computer and, in time, the most common personal computer of any kind.

== Development ==
By 1980 IBM was worried that it was missing out on the fast-growing personal computer market, where the [[Apple II]] and the [[TRS-80]] were selling in large numbers. A small team at IBM's Entry Systems division in Boca Raton, Florida, first under William Lowe and then under [[Don Estridge]], was given about a year to produce a machine. To work this quickly the team broke with IBM tradition and used parts from outside suppliers, including the Intel 8088 processor, and bought in software rather than writing it.

The operating system came from [[Microsoft]], which had bought an existing system called 86-DOS from Seattle Computer Products and adapted it for IBM. IBM sold it as PC DOS, while Microsoft kept the right to license it to other manufacturers as [[MS-DOS]].

== Hardware ==
The [[Intel 8088]] is a version of the 16-bit 8086 with an 8-bit external data bus, which allowed IBM to use cheaper 8-bit support chips. The base model had only 16 KB of RAM and a cassette port, but most were sold with 64 KB and one or two floppy disk drives. The motherboard has five expansion slots, and display adapters were sold as separate cards: the Monochrome Display Adapter for sharp text on IBM's green screen monitor, and the Color Graphics Adapter for colour graphics at up to 320 &times; 200 in four colours.

The keyboard was large and heavy, with a solid key feel that many users still prefer, although its unusual layout of the Shift and Return keys was criticised.

== Clones ==
The only part of the PC that IBM did not publish openly was the BIOS ROM. In 1982 Compaq produced a compatible BIOS using engineers who had never seen IBM's code, and the Compaq Portable went on sale in 1983. Phoenix Technologies began licensing its own compatible BIOS to any manufacturer in 1984, and from then on dozens of companies built PC clones. By the late 1980s IBM's own share of the market it had created was falling steadily.

== Successors ==
* '''IBM PC XT''' (1983): a 10 MB hard disk and eight expansion slots.
* '''IBM PCjr''' (1983): a cheaper home version that sold poorly.
* '''IBM PC AT''' (1984): the [[Intel 80286]] processor and a 16-bit expansion bus.
* '''IBM Personal System/2''' (1987): replaced the original PC range.

The 5150 itself was discontinued in April 1987 when the PS/2 was announced.

== See also ==
* [[Apple II]]
* [[Altair 8800]]

[[Category:16-bit computers]]
[[Category:IBM hardware]]
[[Category:1981 introductions]]"""

IBM_1 = sub(cut(IBMPC, "See also"),
    ("* '''IBM PCjr''' (1983): a cheaper home version that sold poorly.\n", ""),
    ("\n\nThe keyboard was large and heavy, with a solid key feel that many users still prefer, although its unusual layout of the Shift and Return keys was criticised.", ""))
IBM_2 = sub(cut(IBMPC, "See also"),
    ("\n\nThe keyboard was large and heavy, with a solid key feel that many users still prefer, although its unusual layout of the Shift and Return keys was criticised.", ""))

page("IBM Personal Computer",
     ("20070708171544", "Tramiel Historian", "new article", False, IBM_1),
     ("20070908230215", "24.61.198.110", "PCjr", True, IBM_2),
     ("20070909104720", "Tramiel Historian", "keyboard, see also", False, IBMPC))

page("IBM PC",
     ("20070709192845", "Datasette Dave", "redirect", False, "#REDIRECT [[IBM Personal Computer]]"))

# ---------------------------------------------------------------- categories

page("Category:8-bit computers",
     ("20070322212530", "SpriteWrangler64", "new category", False,
      "Home and personal computers built around an 8-bit microprocessor, such as the [[MOS Technology 6502]], the [[Zilog Z80]] or the [[Intel 8080]]. Most of the machines covered by this wiki belong here.\n\n[[Category:Computers]]"))
page("Category:16-bit computers",
     ("20070617141021", "Bitplane", "new category", False,
      "Computers built around a 16-bit processor, or a processor with 16-bit internals such as the [[Intel 8088]] and the [[Motorola 68000]].\n\n[[Category:Computers]]"))
page("Category:Commodore hardware",
     ("20070322212811", "SpriteWrangler64", "new category", False,
      "Computers and peripherals made by [[Commodore International]].\n\n[[Category:Manufacturers]]"))
page("Category:Computers",
     ("20070322213107", "SpriteWrangler64", "", False,
      "The main category for articles about individual computer models. Please put articles in one of the subcategories below rather than here."))
page("Category:Stubs",
     ("20070310171630", "Datasette Dave", "", False,
      "Short articles that need expanding. Pages are added to this category by the {{tl|stub}} template.".replace("{{tl|stub}}", "<nowiki>{{stub}}</nowiki>")))

# ---------------------------------------------------------------- project pages

PORTAL = """Welcome to the '''Community Portal'''. This is the place to find out what needs doing on the Retrocomputing Wiki and how we do things.

== How to help ==
* Write an article about a computer you know well. Have a look at [[Special:Wantedpages|wanted pages]] for ideas.
* Expand an existing article. Short articles are listed in [[:Category:Stubs]].
* Check facts. If you have the original manuals or magazines, please add dates and prices from them.

== Wanted articles ==
* [[Commodore PET]]
* [[Atari 8-bit family]]
* [[Sinclair ZX81]]
* [[Amstrad CPC]]
* [[Commodore 128]]
* [[Acorn Electron]]
* [[MSX]]
* [[Zilog Z80]]

== Style guide ==
# Use the article name that the manufacturer used (''Commodore 64'', not ''C64'' or ''Commodore C-64''). Create a redirect for common short names.
# Put the {{tl|Infobox computer}} at the top of articles about a computer model.
# Use British spelling for British computers and American spelling for American ones. Don't change other people's spelling just because it isn't yours. (See [[Talk:ZX Spectrum]].)
# Write in your own words. Do not copy text from Wikipedia, magazines or manuals.
# Sign your posts on talk pages with four tildes (<nowiki>~~~~</nowiki>).

== Admins ==
* [[User:Datasette Dave|Datasette Dave]]

If something needs deleting or a page needs protecting, leave a message on [[User talk:Datasette Dave|my talk page]]."""

PORTAL = PORTAL.replace("{{tl|Infobox computer}}", "<nowiki>{{Infobox computer}}</nowiki>")
page("Retrocomputing Wiki:Community Portal",
     ("20070306211512", "Datasette Dave", "first version", False, cut(PORTAL, "Style guide").replace("* Expand an existing article. Short articles are listed in [[:Category:Stubs]].\n", "")),
     ("20070310171854", "Datasette Dave", "stubs", True, cut(PORTAL, "Style guide")),
     ("20070605082012", "Datasette Dave", "style guide", False, PORTAL.replace("* [[Zilog Z80]]\n", "")),
     ("20070829221344", "Datasette Dave", "wanted: Z80", True, PORTAL))

ABOUT = """The '''Retrocomputing Wiki''' is a collaborative encyclopedia about vintage computers: the kit machines, home computers and early personal computers of the 1970s and 1980s, and the people, chips and software behind them.

It was started in March 2007 by a few regulars of a Commodore collectors' forum who wanted somewhere to write things down properly. Anyone can edit, and you don't need an account, although having one makes it easier to keep track of your edits.

The wiki runs on [http://www.mediawiki.org/ MediaWiki], the software behind Wikipedia. Text is available under the GNU Free Documentation License.

See the [[Retrocomputing Wiki:Community Portal|Community Portal]] for ways to help."""

page("Retrocomputing Wiki:About",
     ("20070306213320", "Datasette Dave", "", False, ABOUT))

page("User:Datasette Dave",
     ("20070311110509", "Datasette Dave", "", False,
      "Hi, I'm Dave. I started this wiki in March 2007.\n\nI've been collecting Commodore machines since my first [[VIC-20]] in 1982. Currently own: a VIC-20, three [[Commodore 64|C64s]] (two breadbins and a 64C), a 1541 and a 1541-II, an SX-64 that needs a new screen, and an [[Amiga 500]] with the A501 expansion.\n\nIf you need an admin for something, leave a message on [[User talk:Datasette Dave|my talk page]]."))
page("User:SpriteWrangler64",
     ("20070322200417", "SpriteWrangler64", "", False,
      "C64 coder since 1985, mostly sprite multiplexers that never made it into finished games. I mainly edit [[Commodore 64]] and the [[MOS Technology 6502|6502]] article."))
page("User talk:Datasette Dave",
     ("20070415113022", "SpriteWrangler64", "/* Template */ new section", False,
      "== Template ==\nThanks for setting up the infobox template, it makes the C64 article look a lot more finished. --" + sig("SpriteWrangler64", "11:30, 15 April 2007")),
     ("20070617143205", "Bitplane", "/* 16-bit category */ new section", False,
      "== Template ==\nThanks for setting up the infobox template, it makes the C64 article look a lot more finished. --" + sig("SpriteWrangler64", "11:30, 15 April 2007") +
      "\n\n== 16-bit category ==\nI made [[:Category:16-bit computers]] for the Amiga article. Hope that's OK. --" + sig("Bitplane", "14:32, 17 June 2007")),
     ("20070617201945", "Datasette Dave", "/* 16-bit category */", False,
      "== Template ==\nThanks for setting up the infobox template, it makes the C64 article look a lot more finished. --" + sig("SpriteWrangler64", "11:30, 15 April 2007") +
      "\n\n== 16-bit category ==\nI made [[:Category:16-bit computers]] for the Amiga article. Hope that's OK. --" + sig("Bitplane", "14:32, 17 June 2007") +
      "\n\n:Perfect, thanks. Welcome aboard! --" + sig("Datasette Dave", "20:19, 17 June 2007")))

# ---------------------------------------------------------------- Main Page

BOX = """{| style="width:100%%; border:1px solid #c8c0a8; background:#fcfbf6; margin-bottom:0.8em;" cellpadding="4"
! style="background:#e6dfca; text-align:left; font-size:110%%; padding:2px 6px;" | %s
|-
| style="padding:4px 8px;" |
%s
|}"""


def mainpage(featured, dyk, news, wanted, count_line=True):
    welcome = """__NOTOC__
{| style="width:100%; border:1px solid #c8c0a8; background:#f6f3e8; margin-bottom:0.8em;" cellpadding="6"
|
<div style="font-size:160%; padding-bottom:0.2em;">Welcome to the '''Retrocomputing Wiki'''</div>
The free encyclopedia of vintage computers that anyone can edit. We write about home and personal computers from the kit machines of the 1970s to the end of the 16-bit era, and the chips, people and software behind them.""" + ("""

We currently have '''{{NUMBEROFARTICLES}}''' articles. New here? Read the [[Retrocomputing Wiki:About|About]] page, then see the [[Retrocomputing Wiki:Community Portal|Community Portal]] for things that need doing.""" if count_line else "") + """
|}
{| style="width:100%;" cellspacing="0" cellpadding="0"
| style="width:56%; vertical-align:top; padding-right:0.8em;" |
"""
    browse = """'''8-bit:''' [[Altair 8800]] &middot; [[Apple II]] &middot; [[TRS-80]] &middot; [[VIC-20]] &middot; [[BBC Micro]] &middot; [[Commodore 64]] &middot; [[ZX Spectrum]]

'''16-bit:''' [[IBM Personal Computer]] &middot; [[Amiga 500]]

'''Chips:''' [[MOS Technology 6502]]

'''Categories:''' [[:Category:8-bit computers|8-bit computers]] &middot; [[:Category:16-bit computers|16-bit computers]] &middot; [[:Category:Commodore hardware|Commodore hardware]]"""
    left = BOX % ("Featured article", featured) + "\n" + BOX % ("Browse the wiki", browse)
    right = BOX % ("Did you know...", dyk) + "\n" + BOX % ("Wiki news", news) + "\n" + BOX % ("Wanted articles", wanted)
    return welcome + left + '\n| style="width:44%; vertical-align:top;" |\n' + right + "\n|}"


FEAT_C64 = """'''The [[Commodore 64]]''' is an 8-bit home computer introduced by Commodore International in August 1982. Built around the MOS Technology 6510 and 64 KB of RAM, it was sold through department stores and toy shops as well as computer dealers, and its price fell below $300 during the price war of 1983. Its SID sound chip and VIC-II graphics chip made it a favourite with game developers, and it is often called the best-selling single computer model of all time, although nobody knows exactly how many were made. Production ended only when Commodore went bankrupt in 1994.

''[[Commodore 64|Read more...]]''"""

FEAT_ALTAIR = """'''The [[Altair 8800]]''' is a microcomputer kit sold by MITS of Albuquerque from January 1975, when it appeared on the cover of ''Popular Electronics''. It had no keyboard or screen, only switches and lights, but it sold thousands of units and started the personal computer industry. Two young programmers, Bill Gates and Paul Allen, wrote a BASIC for it and founded Microsoft to sell it.

''[[Altair 8800|Read more...]]''"""

DYK_1 = """* ...that the [[ZX Spectrum]] entered BASIC keywords with a single keypress?
* ...that the [[Altair 8800]] on the cover of ''Popular Electronics'' was an empty box?
* ...that the [[VIC-20]] was the first computer to sell one million units?
* ...that the [[TRS-80]] was discontinued because of radio interference rules?"""

DYK_2 = """* ...that the [[ZX Spectrum]] entered BASIC keywords with a single keypress?
* ...that the [[BBC Micro]]'s Mode 7 used a teletext chip and only 1 KB of memory?
* ...that the [[VIC-20]] was the first computer to sell one million units?
* ...that the first [[ARM architecture|ARM]] chips were tested on a [[BBC Micro]]?
* ...that the [[MOS Technology 6502]] was sold over the counter from a jar for $25?"""

NEWS_1 = """* '''August 2007:''' The [[Amiga 500]] article has been expanded with a section on trackers and the demoscene.
* '''July 2007:''' New article on the [[IBM Personal Computer]].
* '''June 2007:''' Welcome to [[User:Bitplane|Bitplane]], our first Amiga editor.
* '''March 2007:''' The wiki is open!"""

NEWS_2 = """* '''September 2007:''' All the machines on the original wish list now have articles. Thanks, everyone! The next list is on the [[Retrocomputing Wiki:Community Portal|Community Portal]].
* '''August 2007:''' The [[Amiga 500]] article has been expanded with a section on trackers and the demoscene.
* '''July 2007:''' New article on the [[IBM Personal Computer]].
* '''March 2007:''' The wiki is open!"""

WANTED_1 = "[[Commodore PET]] &middot; [[Atari 8-bit family]] &middot; [[Sinclair ZX81]] &middot; [[Amstrad CPC]] &middot; [[Commodore 128]] &middot; [[Acorn Electron]] &middot; [[MSX]]"

MAIN_FIRST = """'''Welcome to the Retrocomputing Wiki!'''

This is a new wiki about vintage computers. Anyone can edit. To start with, we need articles on:
* [[Commodore 64]]
* [[VIC-20]]
* [[Apple II]]
* [[ZX Spectrum]]
* [[Altair 8800]]
* [[BBC Micro]]
* [[Amiga 500]]

See the [[Retrocomputing Wiki:Community Portal|Community Portal]] for more."""

page("Main Page",
     ("20070304190217", "Datasette Dave", "Welcome", False, MAIN_FIRST),
     ("20070615203300", "Datasette Dave", "new main page layout", False,
      mainpage(FEAT_ALTAIR, DYK_1, NEWS_1.split("\n", 2)[2], WANTED_1, count_line=False)),
     ("20070615204115", "Datasette Dave", "article count", True,
      mainpage(FEAT_ALTAIR, DYK_1, NEWS_1.split("\n", 2)[2], WANTED_1)),
     ("20070829221730", "Datasette Dave", "news", False,
      mainpage(FEAT_ALTAIR, DYK_1, NEWS_1, WANTED_1)),
     ("20070910201522", "Datasette Dave", "new featured article: Commodore 64; did you know; news", False,
      mainpage(FEAT_C64, DYK_2, NEWS_2, WANTED_1)))


# ---------------------------------------------------------------- output

def iso(ts):
    return "%s-%s-%sT%s:%s:%sZ" % (ts[0:4], ts[4:6], ts[6:8], ts[8:10], ts[10:12], ts[12:14])


def main(out):
    os.makedirs(out, exist_ok=True)
    x = ['<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.3/" version="0.3" xml:lang="en">']
    for title, revs in PAGES:
        x.append("  <page>\n    <title>%s</title>" % escape(title))
        last = ""
        for ts, user, comment, minor, text in sorted(revs, key=lambda r: r[0]):
            assert text != last, (title, ts)
            last = text
            who = ("<ip>%s</ip>" if re.match(r"^\d+\.\d+\.\d+\.\d+$", user) else "<username>%s</username>") % escape(user)
            x.append("    <revision>\n      <timestamp>%s</timestamp>\n      <contributor>%s</contributor>\n%s"
                     "      <comment>%s</comment>\n      <text xml:space=\"preserve\">%s</text>\n    </revision>"
                     % (iso(ts), who, "      <minor/>\n" if minor else "", escape(comment), escape(text)))
        x.append("  </page>")
    x.append("</mediawiki>\n")
    with open(os.path.join(out, "pages.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(x))

    edits = {}
    for title, revs in PAGES:
        for r in revs:
            edits[r[1]] = edits.get(r[1], 0) + 1
    sql = []
    for i, (name, reg, groups) in enumerate(USERS):
        uid = i + 2  # WikiSysop is user 1
        sql.append("INSERT INTO user (user_id, user_name, user_real_name, user_password, user_newpassword, user_email, "
                   "user_options, user_touched, user_token, user_registration, user_editcount) VALUES "
                   "(%d, '%s', '', '', '', '', '', '%s', '%032x', '%s', %d);"
                   % (uid, name, "20070911120000", int(hashlib.md5(name.encode()).hexdigest(), 16), reg, edits.get(name, 0)))
        for g in groups:
            sql.append("INSERT INTO user_groups (ug_user, ug_group) VALUES (%d, '%s');" % (uid, g))
    with open(os.path.join(out, "users.sql"), "w") as fh:
        fh.write("\n".join(sql) + "\n")
    print(len(PAGES), "pages,", sum(len(r) for _, r in PAGES), "revisions")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
