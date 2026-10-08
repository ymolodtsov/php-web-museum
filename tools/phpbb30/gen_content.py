#!/usr/bin/env python3
"""Turn content.py into the JSON data file that seed.php feeds to phpBB's own functions.

Also generates the rest of the member list (the board had ~7,100 registered accounts;
the named regulars are in content.py, the others get plausible 2003-2008 handles and join
dates interpolated between the named members' ids, since ids grow with registration date).
Ids continue the phpBB 2 exhibit: topic ~48,200 and post ~214,400 on 17 October 2006.
"""
import calendar
import json
import os
import random
import sys
import time

sys.dont_write_bytecode = True

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

rnd = random.Random(20081017)


def ts(s):
    fmt = "%Y-%m-%d %H:%M" if len(s) <= 16 else "%Y-%m-%d %H:%M:%S"
    return calendar.timegm(time.strptime(s, fmt))


NOW = ts(C.NOW)
T2006 = ts("2006-10-17 15:22")


def topic_id_at(t):
    return int(48215 + (t - T2006) / 86400 * 24.4)


def post_id_at(t):
    return int(214405 + (t - T2006) / 86400 * 120.5)


# ---- members ---------------------------------------------------------------------
named = {m["id"]: m for m in C.MEMBERS}
by_name = {m["name"]: m for m in C.MEMBERS}
anchors = sorted((m["id"], ts(m["joined"])) for m in C.MEMBERS)

ADJ = ("dark silent crazy mad red blue iron shadow frost night lucky angry lazy rusty toxic rapid fuzzy steel "
       "cosmic wild grim lone little big hyper sneaky nuclear pixel retro turbo mega ultra crimson golden burnt "
       "evil happy sleepy cold hot black white green grey stealth atomic sonic chrome bloody savage quiet "
       "broken clever tiny giant wicked ninja flying angry_").split()
NOUN = ("wolf fox hawk ninja pirate monkey panda viking knight wizard sniper gunner rider tiger dragon raven falcon "
        "bear badger otter goblin robot zombie toast pickle waffle taco noodle camper medic rocket phantom ghost "
        "reaper spartan ranger hunter cobra viper jackal moose penguin llama gecko squirrel lobster walrus "
        "samurai pilot drifter outlaw nomad ronin bandit marine gamer slayer paladin rogue druid mage warlock "
        "shaman cowboy duck goose turtle hamster ferret yeti cyborg android").split()
FIRST = ("mike dave chris matt jen katie steve tom josh alex sam dan nick ben jake ryan kyle adam eric jason sarah "
         "amy lisa rob tim greg pete joe andy will liz brian kevin scott mark paul jeff tony carl gary luke sean "
         "aaron derek travis brandon justin megan rachel emily laura heather nicole anna claire becky").split()
LAST = ("smith jones miller davis wilson moore taylor clark lewis walker hall young king wright scott green baker "
        "adams nelson hill campbell mitchell roberts carter phillips evans turner torres parker collins edwards "
        "stewart morris murphy cook rogers morgan cooper peterson reed bailey bell kelly howard ward cox").split()
GAMER = ("Gordon Freeman Shepard Kerrigan Raynor Samus Ryu Cloud Squall Vivi Sephiroth Tidus Link Kirby Yoshi Wario "
         "Sonic Tails Knuckles Duke Doomguy Ranger Sarge Minsc Garrett Thief Corvo Raziel Kain Tycho Gabe Chief "
         "Arbiter Fox Falco Snake Otacon Raiden Dante Vergil Kratos Ratchet Jak Daxter Sly Spyro Crash Banjo").split()
PLACES = ("Chicago, IL|Houston, TX|Seattle, WA|Denver, CO|Atlanta, GA|Boston, MA|Phoenix, AZ|Dallas, TX|"
          "Orlando, FL|Columbus, OH|Cincinnati, OH|Detroit, MI|St. Louis, MO|Kansas City, MO|Omaha, NE|"
          "Madison, WI|Milwaukee, WI|Minneapolis, MN|Portland, OR|San Jose, CA|Los Angeles, CA|San Diego, CA|"
          "Sacramento, CA|Las Vegas, NV|Salt Lake City, UT|Albuquerque, NM|Austin, TX|Nashville, TN|"
          "Charlotte, NC|Richmond, VA|Baltimore, MD|Philadelphia, PA|Pittsburgh, PA|Buffalo, NY|New York, NY|"
          "Hartford, CT|Toronto, ON|Vancouver, BC|Calgary, AB|Montreal, QC|London, UK|Manchester, UK|"
          "Glasgow, UK|Dublin, Ireland|Sydney, Australia|Melbourne, Australia|Auckland, NZ|Stockholm, Sweden|"
          "Amsterdam|Berlin, Germany|USA|Canada|UK|Texas|California|Ohio|Florida|in front of my PC|"
          "behind you|the basement|Earth|Black Mesa|Vault 101|Hyrule").split("|")
TLD_NUM = [str(n) for n in range(70, 96)] + [str(n) for n in range(0, 100)] + ["2k", "007", "1337", "69", "420", "64", "360"]


def make_name(i):
    p = rnd.random()
    if p < 0.22:
        return rnd.choice(ADJ).rstrip("_").capitalize() + rnd.choice(NOUN).capitalize()
    if p < 0.36:
        return rnd.choice(ADJ).rstrip("_") + "_" + rnd.choice(NOUN)
    if p < 0.55:
        return rnd.choice(FIRST) + rnd.choice(TLD_NUM)
    if p < 0.65:
        return rnd.choice(FIRST)[0] + rnd.choice(LAST) + (rnd.choice(TLD_NUM) if rnd.random() < 0.5 else "")
    if p < 0.72:
        return rnd.choice(NOUN) + rnd.choice(TLD_NUM)
    if p < 0.79:
        return rnd.choice(GAMER) + rnd.choice(["", "_", "-"]) + rnd.choice(["Fan", "Jr", "X", "007", "99", "_PA", "2"])
    if p < 0.84:
        return rnd.choice(FIRST).capitalize() + " " + rnd.choice(LAST).capitalize()
    if p < 0.88:
        return "The" + rnd.choice(NOUN).capitalize()
    if p < 0.92:
        return rnd.choice(NOUN).capitalize() + rnd.choice(["Master", "Man", "King", "Lord", "Boy", "Girl", "Fan"])
    if p < 0.95:
        return "xX" + rnd.choice(ADJ).rstrip("_").capitalize() + rnd.choice(NOUN).capitalize() + "Xx"
    return rnd.choice(["Mr", "Dr", "Captain", "Sir", "Lord", "Agent"]) + rnd.choice(["_", ""]) + rnd.choice(NOUN).capitalize()


def regdate_for(uid):
    for (a_id, a_t), (b_id, b_t) in zip(anchors, anchors[1:]):
        if a_id <= uid <= b_id:
            return a_t + (b_t - a_t) * (uid - a_id) / (b_id - a_id)
    return anchors[-1][1]


taken = {m["name"].lower() for m in C.MEMBERS} | {"anonymous"}
fill_ids = [i for i in range(3, C.MAX_USER_ID) if i not in named]
n_named = len(C.MEMBERS)
n_drop = len(fill_ids) + n_named - C.TOTAL_MEMBERS_TARGET
dropped = set(rnd.sample(fill_ids, n_drop))
fillers = []
prev_t = 0
for uid in fill_ids:
    base = regdate_for(uid)
    t = int(base + rnd.uniform(-1800, 1800))
    t = max(t, prev_t + 7)
    prev_t = t
    if uid in dropped:
        continue
    while True:
        name = make_name(uid)
        if name.lower() not in taken and 3 <= len(name) <= 20:
            break
    taken.add(name.lower())
    age = (NOW - t) / 86400
    r = rnd.random()
    if r < 0.45:
        posts = rnd.randint(0, 3)
    elif r < 0.75:
        posts = rnd.randint(4, 40)
    elif r < 0.93:
        posts = rnd.randint(41, 250)
    else:
        posts = int(min(age * 1.2, rnd.uniform(250, 1500)))
    # last visit: active members recently, drive-bys shortly after registering
    if posts > 40 and rnd.random() < 0.6:
        last = NOW - int(rnd.uniform(3600, 86400 * 60))
    else:
        last = t + int(rnd.uniform(600, max(1200, min(NOW - t, 86400 * 400) )))
    last = min(last, NOW - 300)
    loc = rnd.choice(PLACES) if rnd.random() < (0.45 if t < ts("2006-01-01 00:00") else 0.3) else ""
    fillers.append([uid, name, t, posts, max(last, t + 60), loc])

members = []
for m in C.MEMBERS:
    members.append(dict(
        id=m["id"], name=m["name"], regdate=ts(m["joined"]), posts=m["posts"], group=m.get("group"),
        rank=m.get("rank", ""), loc=m["loc"], occ=m["occ"], interests=m["interests"], www=m["www"],
        sig=m["sig"], bday=m["bday"], avatar=m["avatar"], im=m["im"], last=ts(m["last"]),
        viewonline=0 if m.get("hidden") else 1))

# ---- topics ----------------------------------------------------------------------
posts_all = []
topics = []
for t in C.TOPICS:
    start = ts(t["posts"][0][1])
    topics.append(dict(t, start=start))
    for i, (author, when, text) in enumerate(t["posts"]):
        posts_all.append((ts(when), len(topics) - 1, i, author, text))

filler_topics = []
for forum, rows in C.FILLER.items():
    for row in rows:
        title, author, started, replies, views, lastu, lastt = row[:7]
        ttype = row[7] if len(row) > 7 else 0
        locked = row[8] if len(row) > 8 else False
        filler_topics.append(dict(forum=forum, title=title, poster=by_name[author]["id"], time=ts(started),
                                  replies=replies, views=views, last_poster=by_name[lastu]["id"],
                                  last_time=ts(lastt), type=ttype, locked=locked))

# topic ids by creation time (real and filler topics share the sequence)
seq = sorted([(t["start"], "r", i) for i, t in enumerate(topics)] +
             [(f["time"], "f", i) for i, f in enumerate(filler_topics)])
last_id = 0
for when, kind, i in seq:
    tid = max(topic_id_at(when), last_id + 1)
    last_id = tid
    (topics if kind == "r" else filler_topics)[i]["id"] = tid

# post ids by time
posts_all.sort()
last_id = 0
post_rows = {}
for when, ti, pi, author, text in posts_all:
    pid = max(post_id_at(when), last_id + 1)
    last_id = pid
    post_rows[(ti, pi)] = pid
assert last_id < post_id_at(NOW) + 50

rules_id = next(t["id"] for t in topics if t.get("key") == "rules")
rules_url = "http://127.0.0.1:8916/viewtopic.php?f=2&t=%d" % rules_id
for m in members:
    m["sig"] = m["sig"].replace("{RULES_URL}", rules_url)

out_topics = []
for ti, t in enumerate(topics):
    posts = []
    for pi, (author, when, text) in enumerate(t["posts"]):
        assert ts(when) <= NOW, when
        posts.append(dict(id=post_rows[(ti, pi)], poster=by_name[author]["id"], time=ts(when),
                          subject=t["title"] if pi == 0 else "Re: " + t["title"], text=text))
    poll = None
    if t["poll"]:
        p = t["poll"]
        poll = dict(title=p["title"], max=p["max"], length=p["length"], start=ts(p["start"]),
                    options=p["options"])
    out_topics.append(dict(id=t["id"], forum=t["forum"], title=t["title"], type=t["type"],
                           locked=t["locked"], views=t["views"], poll=poll, key=t.get("key"), posts=posts))

for f in filler_topics:
    f["first_post_id"] = post_id_at(f["time"])
    f["last_post_id"] = post_id_at(f["last_time"])
    assert f["last_time"] <= NOW and f["time"] <= f["last_time"], f["title"]

# nobody posts before they joined; "last visited" is never before their latest post
activity = {}
for t in out_topics:
    for p in t["posts"]:
        assert ts(named[p["poster"]]["joined"]) <= p["time"], (named[p["poster"]]["name"], t["title"])
        activity[p["poster"]] = max(activity.get(p["poster"], 0), p["time"])
for f in filler_topics:
    for uid, when in ((f["poster"], f["time"]), (f["last_poster"], f["last_time"])):
        assert ts(named[uid]["joined"]) <= when, (named[uid]["name"], f["title"])
        activity[uid] = max(activity.get(uid, 0), when)
for m in members:
    m["last"] = min(NOW - 30, max(m["last"], activity.get(m["id"], 0) + 240))

online = [by_name[n]["id"] for n in C.ONLINE]
data = dict(
    now=NOW, sitename=C.SITENAME, site_desc=C.SITE_DESC, board_start=ts(C.BOARD_START),
    forums=[dict(id=f[0], parent=f[1], name=f[2], desc=f[3], topics=f[4], posts=f[5],
                 mods=[by_name[n]["id"] for n in f[6]]) for f in C.FORUMS],
    ranks=C.RANKS, members=members, fillers=fillers, max_user_id=C.MAX_USER_ID,
    topics=out_topics, filler_topics=filler_topics,
    online=online, guests_online=C.GUESTS_ONLINE, bots_online=C.BOTS_ONLINE,
    record_online=[C.RECORD_ONLINE[0], ts(C.RECORD_ONLINE[1])],
)
json.dump(data, sys.stdout, indent=0)
print("%d members (+%d named), %d topics, %d posts, %d filler topics" %
      (len(fillers), len(members), len(out_topics), len(posts_all), len(filler_topics)), file=sys.stderr)
