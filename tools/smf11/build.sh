#!/bin/sh
# Rebuild exhibits/smf from the real Simple Machines Forum 1.1.3 release. See tools/METHOD.md.
# SMF 1.1.3 (built 25 June 2007) is the newest 1.1.x before the 21 July 2007 archive date.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/smf11"
WORK=${WORK:-/tmp/museum-smf}
PORT=8902
BASE=http://127.0.0.1:$PORT
NOW="2007-07-21 15:22:00"   # archive date; the app clock is faked with libfaketime

mkdir -p "$WORK" && cd "$WORK"
# download.simplemachines.org sits behind a bot challenge; the Wayback Machine has the original file.
[ -f smf_1-1-3_install.tar.gz ] || curl -sfL -o smf_1-1-3_install.tar.gz \
  "https://web.archive.org/web/20200228113219id_/https://download.simplemachines.org/index.php/smf_1-1-3_install.tar.gz"
rm -rf smf && mkdir smf && tar xzf smf_1-1-3_install.tar.gz -C smf
# MySQL 4 syntax that MariaDB 10.3 rejects (environment fix only).
sed -i.orig -e 's/) TYPE=MyISAM;/) ENGINE=MyISAM;/' -e 's/timestamp(14)/timestamp/' smf/install_1-1.sql
sed -i.orig "s/\$replaces\[') TYPE=MyISAM;'\]/\$replaces[') ENGINE=MyISAM;']/" smf/install.php
rm -f smf/*.orig && chmod -R a+rwX smf

docker build -q -t museum-smf-faketime "$HERE/faketime" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS smf; CREATE DATABASE smf;"
docker rm -f museum-smf >/dev/null 2>&1 || true
docker run -d --name museum-smf --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e "FAKETIME=@$NOW" -e FAKETIME_DONT_FAKE_MONOTONIC=1 \
  -v "$WORK/smf":/var/www/html museum-smf-faketime >/dev/null
sleep 3

# The real installer, default options (no gzip output so the capture reads plain HTML).
PW=$(openssl rand -hex 8)
curl -sf -o /dev/null -X POST "$BASE/install.php?step=1" --data-urlencode "mbname=Aperture Photography Community" \
  --data-urlencode "boardurl=$BASE" -d dbsession=on -d db_server=museum-db -d db_user=root -d db_passwd=museum \
  -d db_name=smf -d db_prefix=smf_
curl -sf -o /dev/null -X POST "$BASE/install.php?step=2" -d username=dan -d "password1=$PW" -d "password2=$PW" \
  -d email=dan@example.com -d password3=museum
rm -f smf/install.php

python3 "$HERE/gen_seed.py"
docker exec -i museum-db mysql -uroot -pmuseum smf < "$HERE/seed.sql"
docker exec -i museum-db mysql -uroot -pmuseum smf < "$HERE/online.sql"

# Pages to capture. Profiles get one page per member; links to individual messages of the
# captured topics are aliased to the topic pages.
ARGS=$(python3 - "$HERE" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
import content as C
pages = [("/", "index.html"), ("/index.php?board=4.0", "board.html"),
         ("/index.php?topic=20.0", "topic.html"), ("/index.php?topic=7.0", "topic-poll.html"),
         ("/index.php?action=recent", "recent.html"), ("/index.php?action=calendar", "calendar.html"),
         ("/index.php?action=help", "help.html"), ("/index.php?action=search", "search.html"),
         ("/index.php?action=login", "login.html")]
for m in C.MEMBERS:
    pages.append((f"/index.php?action=profile;u={m[0]}", "profile.html" if m[1] == "harborlight" else f"profile-{m[1].lower()}.html"))
nmsg = sum(len(t["posts"]) for t in C.TOPICS)
aliases = []
for tid, fname in ((20, "topic.html"), (7, "topic-poll.html")):
    for mid in range(1, nmsg + 2):
        aliases += [(f"/index.php?topic={tid}.msg{mid}", fname), (f"/index.php?topic={tid}.msg{mid};topicseen", fname)]
    aliases += [(f"/index.php?topic={tid}.new", fname), (f"/index.php?topic={tid}.0;topicseen", fname)]
print(" ".join(f"--page '{u}={f}'" for u, f in pages) + " " + " ".join(f"--alias '{u}={f}'" for u, f in aliases))
PY
)
cd "$ROOT"
eval python3 tools/capture.py --base "$BASE" --out exhibits/smf $ARGS
# Images the default theme only swaps in from JavaScript (header collapse, footer hover, sort order).
for f in upshrink2.gif sort_up.gif h_powered-mysql.gif h_powered-php.gif h_valid-css.gif h_valid-xhtml10.gif; do
  cp "$WORK/smf/Themes/default/images/$f" exhibits/smf/Themes/default/images/
done

docker rm -f museum-smf >/dev/null
