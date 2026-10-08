"""Fictional community content for the Overclock Hardware Forums exhibit.

Names, forums, threads, posts and signatures carried over from the previous
(hand-built) exhibit. "Now" is Monday 12 February 2007, 11:59 PM GMT.
"""

BBTITLE = "Overclock Hardware Forums"
NOW_TIME = "11:59 PM"
TODAY = "02-12-2007"

STATS = {"threads": "83,214", "posts": "1,492,883", "members": "42,611",
         "newest": "FrostyFSB",
         "online_total": "1,204", "online_members": "312", "online_guests": "892",
         "record_users": "2,871", "record_date": "11-08-2006 at 09:12 PM"}

# viewer is logged in
VIEWER = "RadeonRaider"
LAST_VISIT = "Today at 09:14 PM"
PM_UNREAD, PM_TOTAL = 3, 41

# username -> profile
USERS = {
    "RadeonRaider": dict(title="Senior Member", joined="Jan 2004", joined_long="01-14-2004",
                         posts="4,812", rep=3, reppower=24, location="Portland, Oregon",
                         age=29, ppd="4.28",
                         bio="Been building and breaking my own PCs since the Socket 478 days; current rig lives in the signature.",
                         interests="LAN parties, benchmarking, fixing other people's PCs",
                         occupation="Network technician",
                         sig="Core 2 Duo E6400 @ 3.2GHz | ASUS P5B Deluxe | 2GB Corsair XMS2 DDR2-800<br />\nXFX GeForce 8800 GTX | Seagate 320GB SATA | Antec NeoHE 550W | Lian Li PC-7"),
    "Mobo_Mike": dict(title="Moderator", joined="Sep 2002", posts="6,318", rep=2, location="Columbus, Ohio",
                      age=34, mod=True,
                      sig="Mobo_Mike<br />\n--------------------------------------<br />\n"
                          "Core 2 Duo E6600 @ stock | 2x 8800 GTX SLI | 2GB DDR2-800 | Asus P5B Deluxe<br />\n"
                          "Windows Vista Ultimate x64 | Antec P180 | 650W PSU<br />\n"
                          "&quot;It's not a bottleneck if you can't tell the difference.&quot;"),
    "OC_Overlord": dict(title="Silicon Veteran", joined="Mar 2002", posts="9,384", rep=5, location="Austin, TX",
                        mod=True,
                        sig="<b>Forum rules</b> | <b>Overclocking FAQ</b> | Search before you post.<br />\n"
                            "Opteron 165 @ 2.8GHz | DFI LanParty UT nF4 Ultra-D | 2x1GB OCZ Platinum | 7900 GTX"),
    "Heatsink_Hank": dict(title="Heatsink Enthusiast", joined="Jun 2005", posts="1,247", rep=1, location="Leeds, UK"),
    "GTX_Newbie": dict(title="Junior Member", joined="Feb 2007", posts="23", rep=0, location=""),
    "BIOS_Bob": dict(title="Senior Member", joined="Apr 2003", posts="2,906", rep=2),
    "ThermalThrottle_Tom": dict(title="Member", joined="Jul 2005", posts="88", rep=1, age=22),
    "SATA_Sam": dict(title="Senior Member", joined="Nov 2004", posts="1,033", rep=1),
    "Quad_Core_Chris": dict(title="Senior Member", joined="Aug 2005", posts="742", rep=1),
    "VistaVictim": dict(title="Member", joined="Jan 2007", posts="61", rep=0),
    "CoolerMaster_Carl": dict(title="Senior Member", joined="Feb 2005", posts="1,580", rep=2),
    "PS3_Problems": dict(title="Member", joined="Nov 2006", posts="97", rep=0),
    "WiiWaitList": dict(title="Junior Member", joined="Dec 2006", posts="14", rep=0),
    "ZuneZealot": dict(title="Member", joined="Nov 2006", posts="45", rep=0),
    "FrostyFSB": dict(title="Junior Member", joined="Feb 2007", posts="0", rep=0),
}

MODERATORS = ["Mobo_Mike", "OC_Overlord"]

# category -> forums.  forum: name, desc, threads, posts, viewing, new, mods, lastpost(thread, user, time)
CATEGORIES = [
    ("Hardware", [
        dict(name="General Hardware Discussion",
             desc="Power supplies, cases, storage, and anything that doesn't fit the boards below.",
             threads="18,432", posts="342,901", viewing=4, new=True, mods=["OC_Overlord"],
             subforums=["Archived Hardware &amp; Classifieds"],
             last=("Building a NAS on the cheap", "SATA_Sam", "11:42 PM")),
        dict(name="CPUs &amp; Motherboards",
             desc="Core 2 Duo, Core 2 Quad, Athlon 64, chipsets, BIOS tuning.",
             threads="21,660", posts="401,774", viewing=7, new=False, mods=["Mobo_Mike"],
             last=("Q6600 availability in Feb?", "Quad_Core_Chris", "11:51 PM")),
        dict(name="Graphics Cards",
             desc="GeForce, Radeon, SLI, CrossFire, and driver complaints.",
             threads="19,845", posts="378,220", viewing=12, new=True, mods=["OC_Overlord", "Mobo_Mike"],
             last=("GeForce 8800 GTX temps - is 75C normal under load?", "GTX_Newbie", "11:58 PM"),
             current=True),
        dict(name="Overclocking &amp; Cooling",
             desc="Air, water, phase change, and voltmod horror stories.",
             threads="14,560", posts="289,112", viewing=5, new=True, mods=["OC_Overlord"],
             last=("Best fan controller for a hot-running 8800?", "OC_Overlord", "07:33 PM")),
    ]),
    ("Community", [
        dict(name="Off-Topic Lounge",
             desc="PS3 scarcity, Wii shortages, Zune sightings, and everything else.",
             threads="8,717", posts="80,876", viewing=2, new=False, mods=["Mobo_Mike"],
             last=("Did anyone catch the iPhone announcement?", "ZuneZealot", "10:12 PM")),
    ]),
]

ACTIVE_USERS = ["RadeonRaider", "Mobo_Mike", "BIOS_Bob", "ThermalThrottle_Tom", "SATA_Sam",
                "Quad_Core_Chris", "OC_Overlord", "GTX_Newbie", "VistaVictim", "CoolerMaster_Carl",
                "PS3_Problems", "Heatsink_Hank", "WiiWaitList", "ZuneZealot"]

BIRTHDAYS = [("RadeonRaider", 29), ("Mobo_Mike", 34), ("ThermalThrottle_Tom", 22)]

# forumdisplay: Graphics Cards.  (title, starter, replies, views, last user, last time, sticky, new, rating, icon)
FORUM = CATEGORIES[0][1][2]
THREADS = [
    ("Please read before posting - forum rules", "OC_Overlord", "12", "98,432", "OC_Overlord", "03:14 PM", True, False),
    ("GeForce 8800 GTX temps - is 75C normal under load?", "RadeonRaider", "4", "1,212", "GTX_Newbie", "11:58 PM", False, True),
    ("AMD/ATI - thoughts on the merger?", "Mobo_Mike", "342", "28,901", "BIOS_Bob", "11:40 PM", False, True),
    ("Vista driver issues megathread", "VistaVictim", "567", "54,320", "ThermalThrottle_Tom", "11:21 PM", False, False),
    ("Official &quot;what card are you running&quot; thread", "CoolerMaster_Carl", "891", "61,004", "SATA_Sam", "10:58 PM", False, True),
    ("8800 GTS vs GTX - worth the price difference?", "GTX_Newbie", "76", "6,432", "RadeonRaider", "09:47 PM", False, False),
    ("Still waiting on a PS3 restock, settled for a GPU upgrade instead", "PS3_Problems", "54", "4,218", "Quad_Core_Chris", "09:02 PM", False, True),
    ("SLI scaling in actual games vs. benchmarks", "Heatsink_Hank", "29", "2,890", "Mobo_Mike", "08:15 PM", False, False),
    ("Best fan controller for a hot-running 8800?", "ThermalThrottle_Tom", "18", "1,654", "OC_Overlord", "07:33 PM", False, False),
]

THREAD_TITLE = "GeForce 8800 GTX temps - is 75C normal under load?"
POSTS = [
    ("RadeonRaider", "06:48 PM",
     "Just finished my first real gaming session on the 8800 GTX and the temperature readout in nTune is showing 75C under load after about forty minutes of running benchmarks back to back. Fans are at the default profile, case has decent airflow. Is that actually normal for this card or should I be looking at a better cooler already?"),
    ("Heatsink_Hank", "07:15 PM",
     "75C at stock fan settings is right in line with what everyone's been reporting for this card - Nvidia set the default fan curve pretty conservatively on the reference cooler, probably to keep noise complaints down. If it bothers you, bump the fan speed up manually with RivaTuner and you'll see it drop ten degrees easily at the cost of a louder card."),
    ("OC_Overlord", "08:02 PM",
     ("Heatsink_Hank", "75C at stock fan settings is right in line with what everyone's been reporting for this card - Nvidia set the default fan curve pretty conservatively on the reference cooler..."),
     "Hank's right. We've had about a dozen threads on this already since launch, I'll probably merge a few of them this weekend. Short version: 75-80C is within spec for the reference 8800 GTX cooler, the GPU itself is rated well past that. Manual fan curve or an aftermarket cooler if you want it quieter or cooler, but you're not damaging anything running stock."),
    ("Mobo_Mike", "09:30 PM",
     "Seconding the manual fan curve suggestion. I run mine at a fixed 55% and idle sits around 42C, load tops out around 68C in anything I've thrown at it so far. Card's a beast either way, just picked up the second one for SLI once the tax refund clears."),
    ("GTX_Newbie", "11:58 PM",
     "Thanks for this thread, first post here but it answered exactly what I was worried about before ordering one. Going with the reference cooler for now and revisiting the fan curve once it actually arrives."),
]
