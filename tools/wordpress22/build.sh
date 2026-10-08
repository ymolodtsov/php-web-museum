#!/bin/sh
# Rebuild exhibits/wordpress from the real WordPress 2.2.1 release. See tools/METHOD.md.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${WORK:-/tmp/museum-wordpress22}
PORT=8901

mkdir -p "$WORK" && cd "$WORK"
[ -d wordpress ] || { curl -sfL -o wp.tar.gz https://wordpress.org/wordpress-2.2.1.tar.gz && tar xzf wp.tar.gz; }
sed -e "s/putyourdbnamehere/wp/; s/usernamehere/root/; s/yourpasswordhere/museum/; s/localhost/museum-db/" \
    wordpress/wp-config-sample.php > wordpress/wp-config.php

docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS wp; CREATE DATABASE wp;"
docker rm -f museum-wp >/dev/null 2>&1 || true
docker run -d --name museum-wp --network museum -p 127.0.0.1:$PORT:80 -v "$WORK/wordpress":/var/www/html museum-php56 >/dev/null
sleep 3
curl -s -o /dev/null -X POST "http://127.0.0.1:$PORT/wp-admin/install.php?step=2" \
     --data-urlencode "weblog_title=signal & noise" --data-urlencode "admin_email=dave@example.com"
docker exec -i museum-db mysql -uroot -pmuseum wp < "$ROOT/tools/wordpress22/seed.sql"

cd "$ROOT"
python3 tools/capture.py --base http://127.0.0.1:$PORT --out exhibits/wordpress \
 --page '/=index.html' \
 --page '/?p=7=post-7.html' --page '/?p=6=post-6.html' --page '/?p=5=post-5.html' --page '/?p=4=post-4.html' \
 --page '/?p=3=post-3.html' --page '/?p=1=post-1.html' --page '/?p=8=post-8.html' \
 --page '/?page_id=2=about.html' --page '/?page_id=9=archives.html' \
 --page '/?m=200708=2007-08.html' --page '/?m=200707=2007-07.html' --page '/?m=200706=2007-06.html' --page '/?m=200705=2007-05.html' \
 --page '/?cat=1=cat-uncategorized.html' --page '/?cat=3=cat-hardware.html' --page '/?cat=4=cat-software.html' \
 --page '/?cat=5=cat-gadgets.html' --page '/?cat=6=cat-reviews.html' --page '/?cat=7=cat-rants.html' \
 --page '/?paged=2=page-2.html'

docker rm -f museum-wp >/dev/null
