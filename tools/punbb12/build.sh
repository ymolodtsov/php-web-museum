#!/bin/sh
# Rebuild exhibits/punbb from the real PunBB 1.2.10 release (1 Nov 2005), default Oxygen style.
# See tools/METHOD.md. The tarball comes from punbb.org's own "museum" download directory,
# as preserved by the Wayback Machine.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/punbb12"
WORK=${WORK:-/tmp/museum-punbb}
PORT=8903
BASE=http://127.0.0.1:$PORT
TARBALL_URL='http://web.archive.org/web/20060924093142id_/http://www.punbb.org/download/museum/punbb-1.2.10.tar.bz2'
TARBALL_SHA256=6c5e1a567a1a22116f5fe159467b2139ae42c9c173fbc216f4495e1a3feb8208

mkdir -p "$WORK" && cd "$WORK"
[ -f punbb-1.2.10.tar.bz2 ] || curl -sfL --retry 5 -o punbb-1.2.10.tar.bz2 "$TARBALL_URL"
echo "$TARBALL_SHA256  punbb-1.2.10.tar.bz2" | shasum -a 256 -c -
rm -rf punbb-1.2.10 www && tar xjf punbb-1.2.10.tar.bz2 && cp -R punbb-1.2.10/upload www
# MySQL 4 table syntax -> MariaDB 10.3 (environment fix only)
sed -i.orig -e 's/TYPE=MyISAM/ENGINE=MyISAM/; s/TYPE=HEAP/ENGINE=HEAP/' www/install.php
chmod 777 www/cache www/img/avatars

# PHP 5.6 + Apache with libfaketime: the app's clock starts at 15 Jan 2006 10:12 UTC
docker build -q -t museum-punbb-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS punbb; CREATE DATABASE punbb;"
docker rm -f museum-punbb >/dev/null 2>&1 || true
docker run -d --name museum-punbb --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME='@2006-01-15 10:12:00' -e FAKETIME_DONT_RESET=1 \
  -v "$WORK/www":/var/www/html museum-punbb-faketime >/dev/null
sleep 3

# Install through PunBB's own installer. The admin password is random and thrown away.
PW=$(openssl rand -hex 12)
curl -sf -o "$WORK/install-result.html" -X POST "$BASE/install.php" \
  --data-urlencode form_sent=1 --data-urlencode req_db_type=mysql --data-urlencode req_db_host=museum-db \
  --data-urlencode req_db_name=punbb --data-urlencode db_username=root --data-urlencode db_password=museum \
  --data-urlencode db_prefix= --data-urlencode req_username=mkay --data-urlencode req_email=mkay@devnull-forum.example \
  --data-urlencode "req_password1=$PW" --data-urlencode "req_password2=$PW" --data-urlencode "req_base_url=$BASE"
grep -q 'Copy contents to config.php' "$WORK/install-result.html"
# install.php prints config.php for the admin to copy; do exactly that
python3 - "$WORK/install-result.html" "$WORK/www/config.php" <<'EOF'
import html, re, sys
src = open(sys.argv[1], encoding="latin-1").read()
m = re.search(r"<textarea[^>]*>(.*?)</textarea>", src, re.S)
open(sys.argv[2], "w", encoding="latin-1").write(html.unescape(m.group(1)))
EOF

docker exec -i museum-db mysql -uroot -pmuseum punbb < "$HERE/seed.sql"
rm -f "$WORK"/www/cache/cache_*.php

# Captured pages. Last-post links (viewtopic.php?pid=N#pN) resolve to the topic's page.
set -- --page '/=index.html' --page '/userlist.php=userlist.html' --page '/search.php=search.html' \
       --page '/register.php=register.html' --page '/login.php=login.html' \
       --page '/login.php?action=forget=login-forget.html' \
       --page '/search.php?action=show_24h=search-recent.html' --page '/search.php?action=show_unanswered=search-unanswered.html'
for f in 1 2 3; do set -- "$@" --page "/viewforum.php?id=$f=forum-$f.html"; done
for t in $(docker exec museum-db mysql -N -uroot -pmuseum punbb -e 'SELECT id FROM topics ORDER BY id'); do
  set -- "$@" --page "/viewtopic.php?id=$t=topic-$t.html"
done
for u in $(docker exec museum-db mysql -N -uroot -pmuseum punbb -e 'SELECT id FROM users WHERE id > 1 ORDER BY id'); do
  set -- "$@" --page "/profile.php?id=$u=profile-$u.html" --page "/search.php?action=show_user&user_id=$u=posts-$u.html"
done
for row in $(docker exec museum-db mysql -N -uroot -pmuseum punbb -e "SELECT CONCAT(id, ':', topic_id) FROM posts"); do
  set -- "$@" --alias "/viewtopic.php?pid=${row%%:*}=topic-${row##*:}.html"
done

cd "$ROOT"
python3 tools/capture.py --base $BASE --out exhibits/punbb "$@"

docker rm -f museum-punbb >/dev/null
