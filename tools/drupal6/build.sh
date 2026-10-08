#!/bin/sh
# Rebuild exhibits/drupal-6 from the real Drupal 6.14 release (Garland, default blue
# colour scheme). See tools/METHOD.md. Archive date 3 November 2009.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/drupal6"
WORK=${WORK:-/tmp/museum-drupal}
PORT=8907
BASE=http://127.0.0.1:$PORT
SQL="docker exec -i museum-db mysql -uroot -pmuseum drupal6"

mkdir -p "$WORK" && cd "$WORK"
rm -rf drupal
[ -f drupal-6.14.tar.gz ] || curl -sfLO https://ftp.drupal.org/files/projects/drupal-6.14.tar.gz
tar xzf drupal-6.14.tar.gz && mv drupal-6.14 drupal
sed "s#^\$db_url = .*#\$db_url = 'mysqli://root:museum@museum-db/drupal6';#" \
    drupal/sites/default/default.settings.php > drupal/sites/default/settings.php
mkdir -p drupal/sites/default/files && chmod 777 drupal/sites/default/files

# Local-only admin password for this throwaway install
[ -f admin-pass.txt ] || openssl rand -hex 8 > admin-pass.txt
PW=$(cat admin-pass.txt)

docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS drupal6; CREATE DATABASE drupal6 CHARACTER SET utf8;"
docker rm -f museum-drupal >/dev/null 2>&1 || true
docker run -d --name museum-drupal --network museum -p 127.0.0.1:$PORT:80 -v "$WORK/drupal":/var/www/html museum-php56 >/dev/null
sleep 3

python3 "$HERE/drupal_ui.py" $BASE "$PW" install
python3 "$HERE/drupal_ui.py" $BASE "$PW" modules     # + forum, search, contact
$SQL < "$HERE/structure.sql"                          # settings, permissions, terms, users
python3 "$HERE/drupal_ui.py" $BASE "$PW" content     # 1 page, 8 stories, 3 forum topics
python3 "$HERE/drupal_ui.py" $BASE "$PW" menu        # primary links
$SQL < "$HERE/seed.sql"                               # dates, tags, comments, blocks

# Stop the container's clock at Tue 3 Nov 2009, 22:30 EST so "n days ago" strings
# (recent comments, forum listings) are computed against the archive date.
docker exec museum-drupal sh -c 'apt-get -o Acquire::Check-Valid-Until=false update -qq >/dev/null 2>&1;
  apt-get install -y -qq --allow-unauthenticated faketime >/dev/null 2>&1;
  echo "@2009-11-04 03:30:00" > /etc/faketimerc;
  ls /usr/lib/*/faketime/libfaketime.so.1 > /etc/ld.so.preload'
docker restart museum-drupal >/dev/null
sleep 3

cd "$ROOT"
OUT=exhibits/drupal-6
python3 tools/capture.py --base $BASE --out $OUT \
 --page '/=index.html' \
 --page '/?q=node/1=about.html' \
 --page '/?q=node/2=node-2.html' --page '/?q=node/3=node-3.html' --page '/?q=node/4=node-4.html' \
 --page '/?q=node/5=node-5.html' --page '/?q=node/6=node-6.html' --page '/?q=node/7=node-7.html' \
 --page '/?q=node/8=node-8.html' --page '/?q=node/9=node-9.html' \
 --page '/?q=node/10=node-10.html' --page '/?q=node/11=node-11.html' --page '/?q=node/12=node-12.html' \
 --page '/?q=taxonomy/term/1=term-1.html' --page '/?q=taxonomy/term/2=term-2.html' \
 --page '/?q=taxonomy/term/3=term-3.html' --page '/?q=taxonomy/term/4=term-4.html' \
 --page '/?q=forum=forum.html' --page '/?q=forum/5=forum-5.html' --page '/?q=forum/6=forum-6.html' \
 --page '/?q=forum/7=forum-7.html' \
 --page '/?q=search=search.html' --page '/?q=contact=contact.html' \
 --page '/?q=user/register=user-register.html' --page '/?q=user/password=user-password.html' \
 --alias '/?q=node=index.html' --alias '/?q=search/node=search.html'

[ -n "$KEEP" ] || docker rm -f museum-drupal >/dev/null
