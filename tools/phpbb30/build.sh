#!/bin/sh
# Rebuild exhibits/phpbb3 from the real phpBB 3.0.2 release (10 July 2008), stock prosilver.
# See tools/METHOD.md. 3.0.2 is the newest 3.0.x before the archive date (3.0.3 was tagged
# on 12 November 2008). The tarball is phpBB's own, from download.phpbb.com; its files are
# identical to the release-3.0.2 tag of github.com/phpbb/phpbb apart from expanded $Id$ lines.
#
# Pixel Arena Forums, Friday 17 October 2008 -- two years after the phpBB 2 exhibit.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/phpbb30"
WORK=${WORK:-/tmp/museum-phpbb3}
PORT=8916
BASE=http://127.0.0.1:$PORT
NOW="2008-10-17 15:22:00"   # archive date (UTC); the app clock is faked with libfaketime
TARBALL_URL=https://download.phpbb.com/pub/release/3.0/3.0.2/phpBB-3.0.2.tar.bz2
TARBALL_SHA256=b2dca82175fa316e2c822aee1cd324bca07a4640ad130f02311fe6558eb08993

mkdir -p "$WORK" && cd "$WORK"
[ -f phpBB-3.0.2.tar.bz2 ] || curl -sfL --retry 5 -o phpBB-3.0.2.tar.bz2 "$TARBALL_URL"
echo "$TARBALL_SHA256  phpBB-3.0.2.tar.bz2" | shasum -a 256 -c -
rm -rf phpBB3 www && tar xjf phpBB-3.0.2.tar.bz2 && mv phpBB3 www
chmod 666 www/config.php
chmod -R a+rwX www/cache www/store www/files www/images/avatars/upload

docker build -q -t museum-phpbb3-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS phpbb3; CREATE DATABASE phpbb3 CHARACTER SET utf8 COLLATE utf8_bin;"
docker rm -f museum-phpbb3 >/dev/null 2>&1 || true
docker run -d --name museum-phpbb3 --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e "FAKETIME=@$NOW" -e FAKETIME_DONT_RESET=1 \
  -e FAKETIME_DONT_FAKE_MONOTONIC=1 -v "$WORK/www":/var/www/html museum-phpbb3-faketime >/dev/null
sleep 3

# phpBB's own installer, step by step, as the install wizard posts it. The founder
# account is renamed and given a random password; nobody logs in to the exhibit.
PW=$(openssl rand -hex 12)
install_step() {
  sub=$1; shift
  curl -sf -o "$WORK/install-$sub.html" -X POST "$BASE/install/index.php?mode=install&sub=$sub" \
    -d language=en -d dbms=mysqli -d dbhost=museum-db -d dbport= -d dbuser=root -d dbpasswd=museum \
    -d dbname=phpbb3 -d table_prefix=phpbb_ -d default_lang=en -d admin_name=Zane \
    -d "admin_pass1=$PW" -d "admin_pass2=$PW" -d board_email1=zane@pixelarena.example \
    -d board_email2=zane@pixelarena.example -d img_imagick= -d email_enable=0 -d smtp_delivery=0 \
    -d cookie_secure=0 -d force_server_vars=0 -d server_protocol=http:// -d server_name=127.0.0.1 \
    -d server_port=$PORT -d script_path=/ -d testdb=true -d submit=1 "$@"
}
for s in requirements database administrator config_file advanced create_table final; do install_step $s; done
grep -q 'Congratulations' "$WORK/install-final.html"
rm -rf www/install

# Content: members, ranks, forums, permissions, topics and polls (tools/phpbb30/seed.php,
# which uses phpBB's own functions -- user_add, group_user_add, parse_message, sync).
python3 "$HERE/gen_content.py" > "$WORK/www/museum_content.php"
cp "$HERE/seed.php" "$WORK/www/"
mkdir -p "$WORK/www/museum_avatars" && cp "$HERE"/avatars/*.gif "$WORK/www/museum_avatars/"
docker exec -w /var/www/html museum-phpbb3 php seed.php 2>&1 | grep -v '^PHP Deprecated'
rm -rf "$WORK/www/seed.php" "$WORK/www/museum_avatars"

# Capture as a guest. online.php fills "Who is online" right before; both helper files go after.
cp "$HERE/online.php" "$WORK/www/"
cd "$ROOT"
rm -rf exhibits/phpbb3 && mkdir exhibits/phpbb3
WWW="$WORK/www" python3 "$HERE/capture_phpbb3.py" "$BASE"
rm -f "$WORK/www/online.php" "$WORK/www/museum_content.php"
[ -n "$KEEP" ] || docker rm -f museum-phpbb3 >/dev/null   # KEEP=1 leaves the board running
