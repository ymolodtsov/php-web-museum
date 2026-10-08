#!/bin/sh
# Rebuild exhibits/mybb from the real MyBB 1.2.3 release (14 Feb 2007), stock "MyBB Default" theme.
# See tools/METHOD.md. Archive date 27 March 2007: 1.2.3 was the current release until 1.2.4
# (3 April 2007). The tarball is the official download (mybboard.net/downloads/46.tar.gz) as
# preserved by the Wayback Machine; its SHA-1 matches the digest Wayback recorded for both the
# mybboard.net (22 Feb 2007) and mybboard.com (4 Mar 2007) captures of that file.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/mybb12"
WORK=${WORK:-/tmp/museum-mybb}
PORT=8913
BASE=http://127.0.0.1:$PORT
NOW="2007-03-27 21:14:00"   # archive date (UTC); the app clock is faked with libfaketime
TARBALL_URL='http://web.archive.org/web/20070222152124id_/http://mybboard.net:80/downloads/46.tar.gz'
TARBALL_SHA256=a4272943a2424eb484b76e54a5952ae210ca56ec1c0bbe007beb49aca04ce393

mkdir -p "$WORK" && cd "$WORK"
[ -f mybb_1.2.3.tar.gz ] || curl -sfL --retry 5 -o mybb_1.2.3.tar.gz "$TARBALL_URL"
echo "$TARBALL_SHA256  mybb_1.2.3.tar.gz" | shasum -a 256 -c -
rm -rf src www && mkdir src && tar xzf mybb_1.2.3.tar.gz -C src && cp -R src/Upload www
# MySQL 4 table syntax -> MariaDB 10.3 (environment fix only)
sed -i.orig -e 's/) TYPE=MyISAM;/) ENGINE=MyISAM;/' www/install/resources/mysql_db_tables.php
rm -f www/install/resources/*.orig
chmod -R a+rwX www

docker build -q -t museum-mybb-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS mybb; CREATE DATABASE mybb;"
docker rm -f museum-mybb >/dev/null 2>&1 || true
docker run -d --name museum-mybb --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e "FAKETIME=@$NOW" -e FAKETIME_DONT_RESET=1 \
  -v "$WORK/www":/var/www/html museum-mybb-faketime >/dev/null
sleep 3

# Install through MyBB's own installer, step by step, with its default answers.
# The admin password is random and thrown away.
PW=$(openssl rand -hex 12)
I="$BASE/install/index.php"
curl -sf -o "$WORK/i1.html" -X POST "$I" -d action=create_tables -d dbengine=mysql -d dbhost=museum-db \
  -d dbuser=root -d dbpass=museum -d dbname=mybb -d tableprefix=mybb_
curl -sf -o "$WORK/i2.html" -X POST "$I" -d action=populate_tables
curl -sf -o "$WORK/i3.html" -X POST "$I" -d action=templates
curl -sf -o "$WORK/i4.html" -X POST "$I" -d action=adminuser --data-urlencode "bbname=Inkwell" \
  --data-urlencode "bburl=$BASE" --data-urlencode "websitename=Inkwell" --data-urlencode "websiteurl=$BASE/" \
  -d cookiedomain= -d cookiepath=/ --data-urlencode "contactemail=staff@inkwell-forums.example"
curl -sf -o "$WORK/i5.html" -X POST "$I" -d action=final -d adminuser=Quillfeather --data-urlencode "adminpass=$PW" \
  --data-urlencode "adminpass2=$PW" --data-urlencode "adminemail=quill@inkwell-forums.example"
/usr/bin/grep -q 'lock' "$WORK/i5.html"
rm -rf www/install

# Community content (members, forums, threads, posts, poll, reputation, events) as MyBB's own rows,
# then MyBB's own code rebuilds settings.php and its caches (stats, forums, moderators...).
python3 "$HERE/gen_seed.py" > "$WORK/seed.sql"
docker exec -i museum-db mysql -uroot -pmuseum mybb < "$WORK/seed.sql"
docker cp "$HERE/rebuild.php" museum-mybb:/tmp/rebuild.php
docker exec museum-mybb php /tmp/rebuild.php

# Who's Online: sessions relative to the app's own (faked, running) clock, read from Apache's Date header.
APPNOW=$(python3 -c 'import email.utils,sys; print(int(email.utils.parsedate_to_datetime(sys.argv[1]).timestamp()))' \
  "$(curl -sI "$BASE/" | sed -n 's/^[Dd]ate: //p' | tr -d '\r')")
python3 "$HERE/gen_seed.py" --online "$APPNOW" | docker exec -i museum-db mysql -uroot -pmuseum mybb

# Capture as a guest who last visited at 11:30 PM board time the night before.
LASTVISIT=$(python3 -c 'import calendar,time; print(calendar.timegm(time.strptime("2007-03-27 04:30", "%Y-%m-%d %H:%M")))')
ARGS=$(python3 "$HERE/pages.py")
cd "$ROOT"
eval python3 "$HERE/capture_session.py" "$LASTVISIT" --base "$BASE" --out exhibits/mybb $ARGS
# Images the default theme only swaps in from JavaScript (collapsible tables).
cp "$WORK/www/images/collapse_collapsed.gif" exhibits/mybb/images/

docker rm -f museum-mybb >/dev/null
