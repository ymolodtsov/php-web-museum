#!/bin/sh
# Rebuild exhibits/e107 from the real e107 v0.617 release (SourceForge, 17 Sep 2004),
# default theme e107v4a. Archive date: Sunday 30 January 2005. See tools/METHOD.md.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/e107"
WORK=${WORK:-/tmp/museum-e107}
PORT=8909
OUT="$ROOT/exhibits/e107"
SHA1=3af4bdd0364691213daafad4ab3047323c3cdcb3   # published by SourceForge for e107_v0617.tar.gz

mkdir -p "$WORK" && cd "$WORK"
[ -f e107_v0617.tar.gz ] || curl -sfL -o e107_v0617.tar.gz \
  https://downloads.sourceforge.net/project/e107/e107/e107v0.617/e107_v0617.tar.gz
echo "$SHA1  e107_v0617.tar.gz" | shasum -c -

# Fresh copy of the release. Only environment fix: MySQL 4 "TYPE=MyISAM" -> "ENGINE=MyISAM".
rm -rf app && mkdir app && tar xzf e107_v0617.tar.gz -C app
LC_ALL=C sed -i '' 's/TYPE=MyISAM/ENGINE=MyISAM/' app/e107_admin/sql/core_sql.php
chmod -R a+rwX app

docker build -q -t museum-e107-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS e107; CREATE DATABASE e107;"
docker rm -f museum-e107 >/dev/null 2>&1 || true
docker run -d --name museum-e107 --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME='@2005-01-30 21:36:00' -e FAKETIME_DONT_RESET=1 \
  -v "$WORK/app":/var/www/html museum-e107-faketime >/dev/null
sleep 3

# Stock installer, final stage (writes e107_config.php, creates tables, default content).
curl -sf -o /dev/null -X POST "http://127.0.0.1:$PORT/install.php" \
  -d stage=7 -d installlanguage=English -d mysql_server=museum-db -d mysql_name=root \
  -d mysql_password=museum -d mysql_db=e107 -d mysql_prefix=e107_ \
  -d admin_name=Revenant -d admin_password1=obsidian -d admin_email=revenant@clanobsidian.net

# Admin > Preferences / Menus settings, then content.
cp "$HERE/prefs.php" app/museum_prefs.php
docker exec museum-e107 php /var/www/html/museum_prefs.php
rm app/museum_prefs.php
docker exec -i museum-db mysql -uroot -pmuseum e107 < "$HERE/seed.sql"

# Capture as TomH, a registered (non-clan) visitor: e107 0.617 shows the member list and
# profiles only to logged-in users. The cookie is the one e107's login.php would set.
COOKIE=$(docker exec museum-db mysql -uroot -pmuseum e107 -N -e \
  "SELECT CONCAT(user_id, '.', MD5(user_password)) FROM e107_user WHERE user_name = 'TomH'")
rm -rf "$OUT" && cd "$ROOT"
P=""
for f in 2 3 4 6 7 8 10 11; do P="$P --page /forum_viewforum.php?$f=forum-$f.html"; done
for t in 2.1 2.7 3.8 4.10 4.11 6.13 6.17 7.20 7.22 8.24 8.28 10.32 11.35 11.37; do
  P="$P --page /forum_viewtopic.php?$t=thread-${t#*.}.html"
done
for u in 1 2 3 4 5 6 7 8 9 10 11; do P="$P --page /user.php?id.$u=user-$u.html"; done
for n in 1 2 3 4 5 6 7 8; do P="$P --page /comment.php?comment.news.$n=comments-$n.html --page /print.php?news.$n=print-$n.html"; done
for c in 2 3 4 6; do P="$P --page /download.php?list.$c=downloads-$c.html"; done
for d in 1 2 3 4 5 6 7; do P="$P --page /download.php?view.$d=download-$d.html"; done
# newforumposts_menu builds one reply link with a stale forum id; the server answers it with thread 24
P="$P --alias /forum_viewtopic.php?2.24=thread-24.html"
# shellcheck disable=SC2086
python3 tools/e107/capture_as.py "$COOKIE" --base http://127.0.0.1:$PORT --out "$OUT" \
  --page '/news.php=index.html' --alias '/=index.html' \
  --page '/news.php?extend.8=news-8.html' --page '/news.php?extend.7=news-7.html' \
  --page '/forum.php=forum.html' \
  --page '/user.php=members.html' \
  --page '/content.php?content.1=roster.html' \
  --page '/download.php=downloads.html' \
  --page '/links.php=links.html' \
  --page '/sitemap.php=sitemap.html' \
  --page '/submitnews.php=submitnews.html' \
  --page '/oldpolls.php=oldpolls.html' \
  --page '/comment.php?comment.poll.1=poll-comments.html' \
  --page '/online.php=online.html' \
  --page '/top.php?0.top.forum.10=top-posters.html' --page '/top.php?0.active=top-active.html' \
  $P

# The header clock (clock_menu/clock.js) is written by the visitor's browser from new Date().
# Pin it to the archive date: the one string that would otherwise print today's date.
LC_ALL=C sed -i '' 's/today = new Date();/today = new Date(2005, 0, 30, 21, 41, 0);/' \
  "$OUT/e107_plugins/clock_menu/clock.js"
grep -q 'new Date(2005, 0, 30' "$OUT/e107_plugins/clock_menu/clock.js"

# The stock W3C Compliance menu hotlinks its badges from w3.org; keep local copies.
mkdir -p "$OUT/w3c"
curl -sSL -A "Mozilla/5.0" -o "$OUT/w3c/valid-xhtml11.png" https://www.w3.org/Icons/valid-xhtml11.png
curl -sSL -A "Mozilla/5.0" -o "$OUT/w3c/vcss.png" https://jigsaw.w3.org/css-validator/images/vcss
LC_ALL=C sed -i '' -e "s|src='http://www.w3.org/Icons/valid-xhtml11[^']*'|src='w3c/valid-xhtml11.png'|g" \
  -e "s|src='http://jigsaw.w3.org/css-validator/images/vcss[^']*'|src='w3c/vcss.png'|g" "$OUT"/*.html

[ -n "$KEEP" ] || docker rm -f museum-e107 >/dev/null
