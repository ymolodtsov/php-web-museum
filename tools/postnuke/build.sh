#!/bin/bash
# Rebuild exhibits/postnuke from the real PostNuke 0.750 "Gold" release (September 2004) with the
# PNphpBB2 1.2g forum module (November 2004). See tools/METHOD.md.
# Fictional site: Northern Sky, an amateur astronomy club in Duluth, MN, archived Sunday 20 February 2005.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/postnuke"
WORK=${WORK:-/tmp/museum-postnuke}
PORT=8914
DB=postnuke
B=http://127.0.0.1:$PORT
# Local-only test credentials for the throwaway install. make_seed.py replaces the admin's password
# hash with an unusable one, so nothing can sign in to the captured site.
ADMIN=dhalvorsen
ADMINPW=nsky-admin-2005
export LC_ALL=C

md5of() { md5 -q "$1" 2>/dev/null || md5sum "$1" | cut -d' ' -f1; }
fetch() {  # url file md5
  [ -f "$2" ] || curl -sfL -o "$2" "$1"
  [ "$(md5of "$2")" = "$3" ] || { echo "checksum mismatch: $2"; exit 1; }
}

mkdir -p "$WORK/dl" && cd "$WORK"
# PostNuke-0.750.tar.gz: the original download.hostnuke.com/sf/postnuke/ URL is gone. The checksum is the one
# PLD Linux published in its postnuke.spec when packaging 0.750 GOLD (2004-09-15, github.com/pld-linux/postnuke,
# commit a58d3172); the file comes from PLD's by-md5 distfiles mirror.
fetch http://distfiles.pld-linux.org/distfiles/by-md5/2/3/237975777086466ced38e55321981274/PostNuke-0.750.tar.gz \
      dl/PostNuke-0.750.tar.gz 237975777086466ced38e55321981274
# PNphpBB2 1.2g, the first release that runs on PostNuke .75x; md5s as published on SourceForge
SF=https://downloads.sourceforge.net/project/pnphpbb2/pnphpbb2/PNphpBB2%2012g
fetch $SF/PNphpBB2_12g.tar.gz dl/PNphpBB2_12g.tar.gz e9670be9e73d25c8362e6690d9441b9a
fetch $SF/lang_english_12g.tar.gz dl/lang_english_12g.tar.gz 7c6990a71bb599c17dd34845bddb4046

rm -rf release pnbb site && mkdir release pnbb
tar xzf dl/PostNuke-0.750.tar.gz -C release
tar xzf dl/PNphpBB2_12g.tar.gz -C pnbb && tar xzf dl/lang_english_12g.tar.gz -C pnbb
cp -R release/PostNuke-0.750/html site
cp -R pnbb/PNphpBB2 site/modules/   # "upload the PNphpBB2 folder to your modules directory"
# MySQL 4 -> MariaDB 10.3 in the installer's CREATE TABLEs: TYPE= became ENGINE=, TIMESTAMP(14) lost its width
sed -i.orig -E -e 's/\) TYPE ?= " \. \$dbtabletype/) ENGINE = " . $dbtabletype/' -e 's/timestamp\(14\)/timestamp/g' \
    site/install/newtables.php && rm site/install/newtables.php.orig
sed -i.orig -E 's/timestamp\(14\)/timestamp/g' site/modules/Xanthia/pninit.php && rm site/modules/Xanthia/pninit.php.orig
chmod -R a+rwX site

docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS $DB; CREATE DATABASE $DB;"
docker build -q -t museum-postnuke-faketime "$HERE" >/dev/null
run() {  # start the app with its clock at the given UTC time
  docker rm -f museum-postnuke >/dev/null 2>&1 || true
  docker run -d --name museum-postnuke --network museum -p 127.0.0.1:$PORT:80 \
      -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME="@$1" -e FAKETIME_DONT_RESET=1 \
      -v "$WORK/site":/var/www/html museum-postnuke-faketime >/dev/null
  sleep 3
}

# 1. the site went up in June 2003 (PostNuke records the install month as the site's start date)
run "2003-06-14 16:20:00"
C="currentlang=eng&dbhost=museum-db&dbuname=root&dbpass=museum&dbname=$DB&prefix=nuke&dbtype=mysql&dbtabletype=myisam&intranet=0"
curl -sf -d "op=Start&$C" $B/install.php >/dev/null
curl -sf --data-urlencode "op=Set Login" --data-urlencode "aid=$ADMIN" --data-urlencode "name=Dave Halvorsen" \
     --data-urlencode "pwd=$ADMINPW" --data-urlencode "repeatpwd=$ADMINPW" \
     --data-urlencode "email=webmaster@northernsky.example" --data-urlencode "url=http://www.northernsky.example/" \
     -d "$C" $B/install.php >/dev/null
curl -sf -d "op=Finish&currentlang=eng" $B/install.php >/dev/null
rm -rf site/install.php site/install   # the installer's own instruction

# 2. PNphpBB2's installer, run from Admin > Modules > Initialise; then remove its install directory as told
python3 "$HERE/pnbb_install.py" $B $ADMIN $ADMINPW >/dev/null
rm -rf site/modules/PNphpBB2/install

# 3. content (see make_seed.py), then restart the clock at the archive date: Sunday 20 February 2005, 2:40 PM CST
python3 "$HERE/make_seed.py" >/dev/null
docker exec -i museum-db mysql -uroot -pmuseum $DB < "$HERE/seed.sql"
run "2005-02-20 20:40:00"

[ -n "$NO_CAPTURE" ] && exit 0
rm -rf "$ROOT/exhibits/postnuke" && mkdir -p "$ROOT/exhibits/postnuke"
bash "$HERE/capture.sh"
docker rm -f museum-postnuke >/dev/null
