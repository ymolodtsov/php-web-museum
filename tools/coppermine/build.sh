#!/bin/sh
# Rebuild exhibits/coppermine from the real Coppermine 1.3.3 release (SourceForge,
# 20 April 2005). See tools/METHOD.md. Archive date: 8 June 2005.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
WORK=${WORK:-/tmp/museum-coppermine}
PORT=8911
NAME=museum-coppermine
IMAGE=museum-coppermine-faketime
SHA1=4229fb86db4a37d9f6ff89f497234a722b5c983e
ADMIN_USER=danwalsh
ADMIN_PASS=wander05     # local test value for this throwaway install

docker build -q -t $IMAGE "$HERE" >/dev/null
mkdir -p "$WORK" && cd "$WORK"
[ -f cpg1.3.3.zip ] || curl -sfL -o cpg1.3.3.zip "https://downloads.sourceforge.net/project/coppermine/Coppermine/1.3.x%20%28outdated%29/cpg1.3.3.zip"
echo "$SHA1  cpg1.3.3.zip" | shasum -c -
rm -rf src cpg133 && unzip -q cpg1.3.3.zip && mv cpg133 src
# MySQL 4.0 syntax that MariaDB 10.3 rejects (environment fix, not a theme change)
sed -i.orig -e 's/) *TYPE *= *[Mm][Yy][Ii][Ss][Aa][Mm]/) ENGINE=MyISAM/' -e 's/timestamp(14)/timestamp/' src/sql/schema.sql
chmod -R a+rwX src/albums src/include

# Coppermine's clock (PHP time()) follows libfaketime; each album is added on its own date.
start() {
  docker rm -f $NAME >/dev/null 2>&1 || true
  docker run -d --name $NAME --network museum -p 127.0.0.1:$PORT:80 -v "$WORK/src":/var/www/html \
    -e MUSEUM_REGISTER_GLOBALS=0 -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME="@$1" -e FAKETIME_DONT_RESET=1 \
    $IMAGE >/dev/null
  until curl -s -o /dev/null http://127.0.0.1:$PORT/; do sleep 1; done
}

docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS coppermine; CREATE DATABASE coppermine;"
start "2004-09-02 20:05:00"
curl -sf -o /dev/null -X POST http://127.0.0.1:$PORT/install.php \
  -d "admin_username=$ADMIN_USER&admin_password=$ADMIN_PASS&dbserver=museum-db&dbname=coppermine&dbuser=root&dbpass=museum&table_prefix=cpg133_&impath=&thumb_method=gd2&submitted=Let%27s+continue+%21"
docker exec -i museum-db mysql -uroot -pmuseum coppermine < "$HERE/structure.sql"

# Photos: public-domain / CC0 originals (CREDITS.txt) -> camera-sized JPEGs -> 2004-05 camera EXIF
python3 "$HERE/photos.py" "$HERE/photos.json" "$WORK/prepared" "$WORK/orig"
rm -rf "$WORK/exif" && python3 "$HERE/exif.py" "$HERE/photos.json" "$WORK/prepared" "$WORK/exif"

# "FTP" each trip's folder into albums/ and add it with Coppermine's Batch add files, on the upload day
for spec in "alps=3=2004-09-05 10:12:00" "newengland=6=2004-10-19 21:03:00" "morocco=5=2005-01-30 11:40:00" \
            "portugal=4=2005-02-14 20:18:00" "tokyo=2=2005-03-02 22:47:00" "seasia=1=2005-05-28 18:25:00"; do
  folder=${spec%%=*}; rest=${spec#*=}; aid=${rest%%=*}; when=${rest#*=}
  cp -Rp "$WORK/exif/$folder" "$WORK/src/albums/$folder" && chmod -R a+rwX "$WORK/src/albums/$folder"
  start "$when"
  python3 "$HERE/upload.py" http://127.0.0.1:$PORT $ADMIN_USER $ADMIN_PASS "$folder=$aid"
done

docker exec -i museum-db mysql -uroot -pmuseum coppermine < "$HERE/seed.sql"

# Capture as a guest on the evening of 8 June 2005
start "2005-06-08 20:35:00"
cd "$ROOT"
[ -d exhibits/coppermine ] && rm -rf exhibits/coppermine
python3 "$HERE/pages.py" http://127.0.0.1:$PORT > "$WORK/pages.args"
tr '\n' '\0' < "$WORK/pages.args" | xargs -0 python3 tools/capture.py --base http://127.0.0.1:$PORT --out exhibits/coppermine
python3 "$HERE/fixup.py" exhibits/coppermine

docker rm -f $NAME >/dev/null
