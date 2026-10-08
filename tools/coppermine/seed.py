#!/usr/bin/env python3
"""Write seed.sql: titles, captions, views, ratings and comments for the photos
that Coppermine has already added (matched on filepath/filename).

usage: seed.py photos.json > seed.sql
"""
import hashlib
import json
import sys

ALBUM_AID = {"seasia": 1, "tokyo": 2, "alps": 3, "portugal": 4, "morocco": 5, "newengland": 6}
ALBUM_THUMB = {"seasia": "angkor_sunrise", "tokyo": "shinjuku_neon", "alps": "matterhorn_gornergrat",
               "portugal": "cabo_da_roca", "morocco": "jemaa_storytellers", "newengland": "green_mountains"}
CAT_THUMB = {2: "halong_bay", 3: "matterhorn_flowers", 4: "fes_tannery"}
ADMIN = "danwalsh"


def q(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "''") + "'"


def main():
    plan = json.load(open(sys.argv[1]))
    out = ["-- Wanderlens Travel Gallery: per-photo content (run after the batch add)"]
    where = {}
    for p in plan:
        w = "filepath=%s AND filename=%s" % (q(p["folder"] + "/"), q(p["file"]))
        where[p["name"]] = w
        votes = p["votes"]
        rating = round(sum(votes) * 2000 / len(votes)) if votes else 0
        out.append("UPDATE cpg133_pictures SET title=%s, caption=%s, hits=%d, votes=%d, pic_rating=%d, mtime=FROM_UNIXTIME(ctime) WHERE %s;" % (
            q(p["title"]), q(p["caption"]), p["hits"], len(votes), rating, w))
    for folder, name in ALBUM_THUMB.items():
        out.append("UPDATE cpg133_albums SET thumb=(SELECT pid FROM cpg133_pictures WHERE %s) WHERE aid=%d;" % (where[name], ALBUM_AID[folder]))
    for cid, name in CAT_THUMB.items():
        out.append("UPDATE cpg133_categories SET thumb=(SELECT pid FROM cpg133_pictures WHERE %s) WHERE cid=%d;" % (where[name], cid))
    out.append("DELETE FROM cpg133_comments;")
    rows = []
    for p in plan:
        for author, date, text in p["comments"]:
            if author == "Dan":
                author, aid, md5 = ADMIN, 1, ""
            else:
                aid, md5 = 0, hashlib.md5(author.encode()).hexdigest()
            ip = "%d.%d.%d.%d" % tuple(int(hashlib.md5((author + "ip").encode()).hexdigest()[i:i + 2], 16) % 200 + 20 for i in (0, 2, 4, 6))
            rows.append((date, "((SELECT pid FROM cpg133_pictures WHERE %s), %s, %s, %s, %s, %s, %s, %d)" % (
                where[p["name"]], q(author), q(text), q(date), q(ip), q(ip), q(md5), aid)))
    rows.sort()
    for _, r in rows:
        out.append("INSERT INTO cpg133_comments (pid, msg_author, msg_body, msg_date, msg_raw_ip, msg_hdr_ip, author_md5_id, author_id) VALUES %s;" % r)
    # login.php stamps user_lastvisit with the database clock
    out.append("UPDATE cpg133_users SET user_regdate='2004-09-02 20:11:42', user_lastvisit='2005-06-07 22:41:05' WHERE user_id=1;")
    # page views during capture must not change the seeded view counts
    out.append("DROP TRIGGER IF EXISTS cpg133_freeze_hits;")
    out.append("CREATE TRIGGER cpg133_freeze_hits BEFORE UPDATE ON cpg133_pictures FOR EACH ROW SET NEW.hits = OLD.hits, NEW.mtime = OLD.mtime;")
    print("\n".join(out))


if __name__ == "__main__":
    main()
