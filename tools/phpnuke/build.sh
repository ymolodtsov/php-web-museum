#!/bin/sh
# Rebuild exhibits/php-nuke from the real PHP-Nuke 7.1 release (January 2004). See tools/METHOD.md.
# PHP-Nuke 7.1 has no web installer: the stock install is "load sql/nuke.sql, edit config.php".
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${WORK:-/tmp/museum-phpnuke}
PORT=8904
DB=phpnuke
ZIP=PHP-Nuke-7.1.zip
MD5=72b1d4881ac04cd01c9d64e9b091fccd   # phpnuke.org/files/PHP-Nuke-7.1.zip as archived 2004-06-19
export LC_ALL=C

mkdir -p "$WORK" && cd "$WORK"
[ -f $ZIP ] || curl -sfL -o $ZIP "http://web.archive.org/web/20040619235947id_/http://phpnuke.org/files/$ZIP"
[ "$(md5 -q $ZIP 2>/dev/null || md5sum $ZIP | cut -d' ' -f1)" = $MD5 ] || { echo "checksum mismatch"; exit 1; }
rm -rf release site && mkdir release && unzip -q $ZIP -d release
cp -R release/html site
# PHP 5 compatibility, no visible change: PHP 4 accepted '' as "no file" in ImageJPEG(), PHP 5 needs NULL.
# Without it the login block's security-code image is empty.
sed -i.orig "s/ImageJPEG(\$image, '', 75);/ImageJPEG(\$image, NULL, 75);/" site/modules/Your_Account/index.php
rm site/modules/Your_Account/index.php.orig
sed -i.orig -e 's/^\$dbhost = "localhost";/$dbhost = "museum-db";/' -e 's/^\$dbpass = "";/$dbpass = "museum";/' \
    -e "s/^\\\$dbname = \"nuke\";/\$dbname = \"$DB\";/" site/config.php && rm site/config.php.orig
# 7.1 ships only phpnuke.gif as a topic icon. Sites of the era carried over the classic topic icon set
# that PHP-Nuke itself shipped up to 5.x; take those from the original 5.0 release.
[ -f PHP-Nuke-5.0.tar.gz ] || curl -sfL -o PHP-Nuke-5.0.tar.gz https://downloads.sourceforge.net/project/phpnuke/phpnuke/5.0/PHP-Nuke-5.0.tar.gz
rm -rf nuke50 && mkdir nuke50 && tar xzf PHP-Nuke-5.0.tar.gz -C nuke50
for i in linux kde gnome mozilla redhat debian x caldera microsoft gnu; do
    cp "$(find nuke50 -path "*images/topics/$i.gif")" site/images/topics/
done
chmod -R a+rwX site

# MySQL 4 -> MariaDB 10.3: TYPE= became ENGINE=
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS $DB; CREATE DATABASE $DB;"
sed 's/) TYPE=MyISAM;/) ENGINE=MyISAM;/' release/sql/nuke.sql | docker exec -i museum-db mysql -uroot -pmuseum $DB
docker exec -i museum-db mysql -uroot -pmuseum $DB < "$ROOT/tools/phpnuke/seed.sql"

docker rm -f museum-phpnuke >/dev/null 2>&1 || true
# PHP 5.6 legacy image + libfaketime: the app's clock starts at Sunday 14 March 2004 10:47 EST (15:47 UTC)
docker build -q -t museum-phpnuke-faketime "$ROOT/tools/phpnuke" >/dev/null
docker run -d --name museum-phpnuke --network museum -p 127.0.0.1:$PORT:80 \
    -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME="@2004-03-14 15:47:00" -e FAKETIME_DONT_RESET=1 \
    -v "$WORK/site":/var/www/html museum-phpnuke-faketime >/dev/null
sleep 3

[ -n "$NO_CAPTURE" ] && exit 0
cd "$ROOT"
bash tools/phpnuke/capture.sh
docker rm -f museum-phpnuke >/dev/null
