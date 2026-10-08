"""Soundwave Music Community -- fictional content poured into real IPB 2.1.5 output.

Board clock: Thursday 4 May 2006, 12:04 PM. "Today" = 4 May, "Yesterday" = 3 May.
Text values are HTML (IPB stores titles/posts already entity-encoded).
"""

BOARD = "Soundwave Music Community"
HOME_LINK = "Soundwave Music Community"
NOW_LONG = "4th May 2006 - 12:04 PM"          # gfooter "Time is now"
NOW_SHORT = "Today, 12:04 PM"                  # "your last visit was"
NEWS_TITLE = "Soundwave is now running Invision Power Board 2.1&#33;"
VERSION = "v2.1.5"

# name -> member record. pips/titles follow IPB's default ranks
# (Newbie 0 posts/1 pip, Member 10/2, Advanced Member 30/3).
MEMBERS = {
    "sonicwaveadmin": dict(id=1, group="Admin", title="Advanced Member", pips=3, posts="3,127", joined="11-June 03", where=""),
    "DJ_Nocturne": dict(id=3, group="Moderators", title="Moderator", pips=3, posts="6,018", joined="11-June 03", where="Leeds, UK"),
    "vinylvelvet": dict(id=214, group="Members", title="Advanced Member", pips=3, posts="1,342", joined="14-February 04", where="Portland, OR"),
    "indiefan84": dict(id=1033, group="Members", title="Advanced Member", pips=3, posts="912", joined="28-November 04", where="Glasgow"),
    "bassfaceBrian": dict(id=2876, group="Members", title="Advanced Member", pips=3, posts="284", joined="2-September 05", where=""),
    "Lauren_M": dict(id=4655, group="Members", title="Advanced Member", pips=3, posts="47", joined="19-January 06", where=""),
    "TourDiaries": dict(id=1580, group="Members", title="Advanced Member", pips=3, posts="2,411", joined="3-May 05", where=""),
    "vinyl_kid": dict(id=3902, group="Members", title="Member", pips=2, posts="22", joined="8-December 05", where=""),
    "fret_wizard": dict(id=761, group="Members", title="Advanced Member", pips=3, posts="1,904", joined="17-August 04", where=""),
    "drummerdave23": dict(id=2290, group="Members", title="Advanced Member", pips=3, posts="356", joined="21-June 05", where=""),
    "reverb_junkie": dict(id=4917, group="Members", title="Newbie", pips=1, posts="0", joined="4-May 06", where=""),
}

# ---- board index -------------------------------------------------------
CATEGORIES = [
    dict(id=1, name="Music Talk", forums=[
        dict(id=2, name="General Music Discussion",
             desc="Talk about anything music related -- genres, artists, lyrics, the lot.",
             topics="2,184", replies="38,912",
             last=("Today, 11:42 AM", 30981, "Anyone else obsessed with the new Gnarls Barkley single?", "indiefan84")),
        dict(id=3, name="New Releases &amp; Reviews",
             desc="New albums, EPs and singles -- post your reviews here.",
             topics="1,046", replies="15,730", page="showforum.html",
             last=("Today, 11:52 AM", 30988, "Review: The Paper Lanterns - &quot;Low Tide&quot; (2006)", "Lauren_M")),
        dict(id=4, name="Live Shows &amp; Tour Dates",
             desc="Who&#39;s touring, who got tickets, and who&#39;s bragging about the mosh pit.",
             topics="612", replies="9,845",
             last=("Yesterday, 09:03 PM", 30962, "Anyone catching Halcyon Youth in Manchester?", "TourDiaries")),
    ]),
    dict(id=5, name="Gear &amp; Community", forums=[
        dict(id=6, name="Gear &amp; Production",
             desc="Guitars, pedals, DAWs, home recording -- show us your setup.",
             topics="389", replies="5,204",
             last=("May 2 2006, 10:28 PM", 30941, "Best budget audio interface under $200?", "bassfaceBrian")),
        dict(id=7, name="Off Topic Lounge",
             desc="Everything that isn&#39;t music. Keep it civil.",
             topics="1,523", replies="27,660",
             last=("Today, 08:51 AM", 30979, "What are you watching this weekend?", "Lauren_M")),
    ]),
]

# who was active in the last 15 minutes (name, last click time)
ACTIVE = [("Lauren_M", "12:03 PM"), ("DJ_Nocturne", "12:01 PM"), ("indiefan84", "11:58 AM"),
          ("bassfaceBrian", "11:55 AM"), ("TourDiaries", "11:53 AM"), ("vinyl_kid", "11:51 AM"),
          ("sonicwaveadmin", "11:49 AM")]
GUESTS = 14
BIRTHDAYS = [("drummerdave23", 24), ("Lauren_M", 19), ("fret_wizard", 31)]
TOTAL_MEMBERS = "4,917"
NEWEST = "reverb_junkie"
RECORD = ("312", "Mar 2 2006, 09:41 PM")

# ---- forum view (New Releases & Reviews) --------------------------------
FORUM_PAGES = 35            # 1,046 topics / 30 per page
# (tid, title, desc, starter, replies, views, last action, last poster, pinned)
TOPICS = [
    (30214, "Forum Rules &amp; Posting Guidelines - Read Before Posting", "", "sonicwaveadmin", 3, "4,021", "2nd January 2006 - 04:12 PM", "sonicwaveadmin", True),
    (30988, "Review: The Paper Lanterns - &quot;Low Tide&quot; (2006)", "moodier, reverb-heavy, great bridge on track 4", "vinylvelvet", 4, "212", "Today, 11:52 AM", "Lauren_M", False),
    (30903, "Official Crimson Static &quot;Afterglow&quot; Thread", "new album out 22nd May", "TourDiaries", 187, "6,540", "Today, 11:50 AM", "bassfaceBrian", False),
    (30984, "Tool - 10,000 Days", "first impressions", "fret_wizard", 33, "1,177", "Today, 11:31 AM", "drummerdave23", False),
    (30986, "Pearl Jam - Pearl Jam (the avocado album)", "", "DJ_Nocturne", 12, "388", "Today, 10:57 AM", "indiefan84", False),
    (30959, "Anyone else hyped for the new Driftwood Radio EP?", "", "indiefan84", 41, "2,215", "Yesterday, 06:44 PM", "Lauren_M", False),
    (30948, "Worst album of the year so far?", "", "fret_wizard", 76, "3,982", "Yesterday, 02:09 PM", "DJ_Nocturne", False),
    (30970, "Snow Patrol - Eyes Open", "UK release this week", "indiefan84", 19, "604", "Yesterday, 11:20 AM", "vinyl_kid", False),
    (30937, "Halcyon Youth announce surprise acoustic release", "", "TourDiaries", 15, "897", "2nd May 2006 - 04:33 PM", "indiefan84", False),
    (30941, "Red Hot Chili Peppers - Stadium Arcadium", "double album, 9th May", "bassfaceBrian", 28, "1,093", "2nd May 2006 - 01:15 PM", "fret_wizard", False),
    (30925, "Review Round-up: April 2006 New Releases", "", "DJ_Nocturne", 9, "611", "1st May 2006 - 09:17 AM", "vinylvelvet", False),
    (30912, "The Raconteurs - Broken Boy Soldiers", "Jack White side project", "drummerdave23", 22, "740", "30th April 2006 - 10:48 PM", "TourDiaries", False),
    (30887, "Is the physical CD release dead? (debate)", "", "bassfaceBrian", 58, "4,126", "29th April 2006 - 03:02 PM", "fret_wizard", False),
    (30876, "Morrissey - Ringleader of the Tormentors", "", "vinylvelvet", 17, "655", "28th April 2006 - 07:26 PM", "DJ_Nocturne", False),
    (30851, "Flaming Lips - At War with the Mystics", "", "indiefan84", 14, "498", "27th April 2006 - 11:41 AM", "Lauren_M", False),
    (30839, "Built to Spill - You in Reverse", "", "fret_wizard", 8, "302", "26th April 2006 - 08:55 PM", "vinylvelvet", False),
    (30822, "Arctic Monkeys - still the album of the year?", "", "vinyl_kid", 64, "2,870", "26th April 2006 - 05:10 PM", "bassfaceBrian", False),
    (30806, "Paper Lanterns &quot;Low Tide&quot; leaked?", "locked - see review thread", "vinyl_kid", 6, "1,412", "24th April 2006 - 09:38 AM", "DJ_Nocturne", False),
    (30797, "Yeah Yeah Yeahs - Show Your Bones", "", "Lauren_M", 11, "463", "23rd April 2006 - 02:21 PM", "indiefan84", False),
    (30781, "Placebo - Meds", "", "drummerdave23", 21, "819", "21st April 2006 - 06:47 PM", "TourDiaries", False),
    (30762, "Neko Case - Fox Confessor Brings the Flood", "", "vinylvelvet", 9, "341", "19th April 2006 - 10:03 PM", "DJ_Nocturne", False),
    (30744, "Best album covers of 2006 (so far)", "post scans please, no hotlinking", "TourDiaries", 37, "1,560", "18th April 2006 - 01:36 PM", "vinyl_kid", False),
    (30729, "Gnarls Barkley - St. Elsewhere", "", "indiefan84", 26, "1,021", "16th April 2006 - 11:14 PM", "Lauren_M", False),
    (30711, "Strokes - First Impressions of Earth, four months on", "", "fret_wizard", 31, "1,288", "15th April 2006 - 08:29 PM", "bassfaceBrian", False),
    (30694, "Albums you bought on the strength of a review here", "", "DJ_Nocturne", 45, "1,734", "13th April 2006 - 05:52 PM", "drummerdave23", False),
    (30680, "Dixie Chicks - Taking the Long Way (pre-release single)", "", "bassfaceBrian", 7, "296", "12th April 2006 - 09:07 AM", "fret_wizard", False),
    (30663, "Crimson Static - &quot;Afterglow&quot; tracklist confirmed", "", "TourDiaries", 18, "977", "10th April 2006 - 07:40 PM", "vinylvelvet", False),
    (30648, "Re-issues worth buying this spring", "", "vinylvelvet", 13, "402", "9th April 2006 - 12:18 PM", "indiefan84", False),
    (30631, "Rate the last album you bought (1-10)", "", "drummerdave23", 92, "3,415", "7th April 2006 - 10:55 PM", "Lauren_M", False),
    (30617, "Debut albums to watch out for in 2006", "", "fret_wizard", 24, "1,106", "6th April 2006 - 04:44 PM", "TourDiaries", False),
]
HOT = 15  # IPB default hot topic threshold (replies)

# ---- topic view ----------------------------------------------------------
TOPIC = dict(id=30988, title="Review: The Paper Lanterns - &quot;Low Tide&quot; (2006)",
             desc="moodier, reverb-heavy, great bridge on track 4", views="212")
# (pid, author, time, html)
POSTS = [
    (241503, "vinylvelvet", "Today, 10:15 AM",
     "Picked this one up at lunch today and already spun it twice. &quot;Low Tide&quot; is a lot moodier than their last EP"
     " -- way more reverb-heavy, feels like it was recorded in someone&#39;s basement at 3am. Track 4 (&quot;Harbor Lights&quot;)"
     " is probably my favourite so far, the bridge gives me chills.<br /><br />Anyone else grabbed a copy yet? Curious what the"
     " rest of you think about the production on this one."),
    (241510, "bassfaceBrian", "Today, 10:41 AM",
     "QUOTE:241503:May 4 2006, 10&#58;15 AM:vinylvelvet:Track 4 (&quot;Harbor Lights&quot;) is probably my favourite so far, the bridge gives me chills."
     "|Agreed on &quot;Harbor Lights&quot;, that bassline in the bridge is criminally simple but it works so well. I&#39;m still not"
     " sold on the mixing though, the vocals get buried under the guitars on a couple of tracks when I listen on my computer"
     " speakers. Might just be my setup."),
    (241517, "DJ_Nocturne", "Today, 11:03 AM",
     "Good timing on this thread, I was going to put this album in the review round-up anyway. For anyone who missed it, the"
     " band did a short acoustic session for a local radio station last week -- worth a listen if you want to hear"
     " &quot;Harbor Lights&quot; stripped down.<br /><br />Adding this one to the round-up list for May."),
    (241526, "indiefan84", "Today, 11:38 AM",
     "Just ordered the CD from the label&#39;s site since I like having the liner notes for albums like this. Should be here by"
     " next week hopefully, the shipping estimate said 5-7 days. EMO:smile"),
    (241531, "Lauren_M", "Today, 11:52 AM",
     "New here but had to chime in -- this is the first album in a while that&#39;s made me actually sit and listen start to"
     " finish instead of skipping around. The closing track caught me off guard too, wasn&#39;t expecting that key change at"
     " the end. EMO:biggrin"),
]
# Signatures exist in the data, but IPB 2.1 hides post signatures from guests
# (guests_sig), so the archived guest view shows them only on the profile page.
SIGNATURES = {
    "indiefan84": "&quot;you can&#39;t skip track 4&quot; -- my sister, probably",
    "vinylvelvet": "<i>now spinning:</i> The Paper Lanterns - Low Tide<br />college radio, Tuesdays 10pm-midnight",
}

# ---- profile (vinylvelvet) ------------------------------------------------
PROFILE = dict(
    name="vinylvelvet", local_time="May 4 2006, 12:04 PM",
    per_day="1.7", pct="1.30", most_active=("New Releases &amp; Reviews", "612", "45.6"),
    last_active="Today, 10:22 AM", aim="vinylvelvetPDX",
    interests="Record collecting, college radio, shoegaze, anything on 180g vinyl",
)

# topic start times (the title tooltip in the forum view)
STARTED = {
    30214: "Jan 2 2006, 04:05 PM", 30988: "Today, 10:15 AM", 30903: "Mar 29 2006, 07:12 PM",
    30984: "May 1 2006, 08:40 PM", 30986: "May 2 2006, 06:22 PM", 30959: "Apr 30 2006, 01:17 PM",
    30948: "Apr 29 2006, 11:03 AM", 30970: "May 1 2006, 09:55 AM", 30937: "Apr 27 2006, 03:48 PM",
    30941: "Apr 28 2006, 10:31 AM", 30925: "Apr 25 2006, 08:02 PM", 30912: "Apr 24 2006, 05:29 PM",
    30887: "Apr 21 2006, 02:14 PM", 30876: "Apr 20 2006, 07:50 PM", 30851: "Apr 18 2006, 12:36 PM",
    30839: "Apr 17 2006, 09:11 PM", 30822: "Apr 15 2006, 04:27 PM", 30806: "Apr 13 2006, 11:45 PM",
    30797: "Apr 12 2006, 06:08 PM", 30781: "Apr 10 2006, 02:33 PM", 30762: "Apr 8 2006, 10:19 PM",
    30744: "Apr 7 2006, 01:52 PM", 30729: "Apr 5 2006, 08:44 PM", 30711: "Apr 4 2006, 05:06 PM",
    30694: "Apr 2 2006, 03:39 PM", 30680: "Apr 1 2006, 11:58 AM", 30663: "Mar 30 2006, 07:21 PM",
    30648: "Mar 28 2006, 09:47 AM", 30631: "Mar 26 2006, 04:15 PM", 30617: "Mar 24 2006, 10:02 PM",
}
