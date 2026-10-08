#!/bin/sh
# Rebuild exhibits/mambo from the real Mambo 4.5.1a Stable release. See tools/METHOD.md.
#
# Archive date: Thursday 14 October 2004. 4.5.1a ("Three For Rum", RELDATE 05/10/2004) was the current
# stable release then (4.5.1 shipped 23 Sep 2004, 4.5.1a on 6 Oct; 4.5.2 came in February 2005).
# The tarball is the one MamboForge served (1.21 MB), preserved by the Wayback Machine; its contents are
# identical to Debian's mambo_4.5.1a.orig.tar.gz (snapshot.debian.org).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
WORK=${WORK:-/tmp/museum-mambo}
PORT=8905
BASE=http://127.0.0.1:$PORT
TARBALL=MamboV4.5.1a-Stable.tar.gz
TARBALL_URL="https://web.archive.org/web/20051124162030id_/http://mamboforge.net/frs/download.php/2151/$TARBALL"
TARBALL_SHA256=6e1e40f40a7886f605cd687f22227e490892a12e2c9aef5bd2a3abe9e02afefa

mkdir -p "$WORK" && cd "$WORK"
[ -f $TARBALL ] || curl -sfL --retry 5 -o $TARBALL "$TARBALL_URL"
echo "$TARBALL_SHA256  $TARBALL" | shasum -a 256 -c -
rm -rf www && mkdir www && tar xzf $TARBALL -C www
# MySQL 4 table syntax -> MariaDB 10.3 (environment fixes only)
perl -pi.orig -e 's/TYPE=MyISAM/ENGINE=MyISAM/; s/(`rating_sum` int\(11\) unsigned NOT NULL default )\x27\x27/$1\x270\x27/' \
  www/installation/sql/mambo.sql
# PHP 5 compatibility (environment fix only): Cache_Lite_Function::call() passes arguments to
# call_user_func_array() by value, which PHP 4 accepted for by-reference parameters (frontpage(),
# showSection(), ... take &$access) and PHP 5 refuses, leaving those pages blank. Pass references.
perl -pi -e 's/(\$target = array_shift\(\$arguments\);)/$1 \$museum_args = \$arguments; \$arguments = array(); foreach (array_keys(\$museum_args) as \$k) { \$arguments[\$k] = &\$museum_args[\$k]; } \/\/ museum: PHP 5 needs references for by-ref parameters/' \
  www/includes/Cache/Lite/Function.php
grep -q "museum: PHP 5" www/includes/Cache/Lite/Function.php
chmod -R a+rwX www

# PHP 5.6 (register_globals shim) + Apache with libfaketime: the clock starts at 14 Oct 2004 09:40 UTC
docker build -q -t museum-mambo-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS mambo; CREATE DATABASE mambo;"
docker rm -f museum-mambo >/dev/null 2>&1 || true
docker run -d --name museum-mambo --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME='@2004-10-14 09:40:00' -e FAKETIME_DONT_RESET=1 \
  -v "$WORK/www":/var/www/html museum-mambo-faketime >/dev/null
sleep 3

# Install through Mambo's own installer (steps 2 and 4; 1 and 3 only display forms). No sample data.
# The admin password is random and thrown away.
PW=$(openssl rand -hex 8)
DB="-d DBhostname=museum-db -d DBuserName=root -d DBpassword=museum -d DBname=mambo -d DBPrefix=mos_"
curl -sf -o /dev/null -X POST "$BASE/installation/install2.php" $DB -d DBDel=1 -d DBBackup=0
curl -sf -o "$WORK/install-result.html" -X POST "$BASE/installation/install4.php" $DB \
  --data-urlencode "sitename=Riverside Linux User Group" --data-urlencode "siteUrl=$BASE" \
  -d absolutePath=/var/www/html --data-urlencode "adminEmail=webmaster@riversidelug.org" -d adminPassword=$PW
grep -q "Congratulations" "$WORK/install-result.html"
rm -rf www/installation   # Mambo refuses to run while the installer is present

# Global Configuration fields the site owner fills in (what the admin form writes to configuration.php)
perl -pi -e 's/^(\$mosConfig_MetaDesc) = .*/$1 = '"'"'Riverside Linux User Group: monthly meetings, install-fests and help with Linux and free software'"'"';/;
              s/^(\$mosConfig_MetaKeys) = .*/$1 = '"'"'linux, lug, riverside, free software, install-fest, open source'"'"';/' www/configuration.php

docker exec -i museum-db mysql -uroot -pmuseum mambo < "$HERE/seed.sql"
[ -n "$SKIP_CAPTURE" ] && exit 0

# Capture as one visitor (cookie jar), so the Who's Online count stays the same on every page.
# Mambo links the same article with different Itemids depending on where the link appears;
# the variants are captured once and aliased.
set -- --page '/=index.html' --alias '/index.php?option=com_frontpage&Itemid=1=index.html' \
  --alias '/index.php?option=com_frontpage&Itemid=1&limit=4&limitstart=0=index.html' \
  --page '/index.php?option=com_frontpage&Itemid=1&limit=4&limitstart=4=index-2.html' \
  --alias '/index.php?option=com_frontpage&Itemid=1&limit=4&limitstart=4 =index-2.html'
for spec in 1:installfest-notes:40 2:openoffice-library:2 3:firefox-preview:2 4:xp-sp2-drivers:2 5:mailing-list-archive:2 \
            6:knoppix-36:2 7:meeting-schedule:40 8:october-meeting:40 9:spring-installfest:40 10:faq-dual-boot:41 \
            11:faq-distribution:41 12:faq-samba:41 13:faq-k3b:41 14:faq-wireless:41 15:about:42 16:kiosk-trial:2 \
            17:newsflash-next-meeting:2 18:newsflash-cd-table:2 19:newsflash-mailing-list:2; do
  id=${spec%%:*}; rest=${spec#*:}; name=${rest%%:*}; item=${rest#*:}
  set -- "$@" --page "/index.php?option=com_content&task=view&id=$id&Itemid=$item=$name.html"
  for alt in "" "&Itemid=" "&Itemid=1" "&Itemid=2" "&Itemid=4" "&Itemid=40" "&Itemid=41" "&Itemid=42"; do
    [ "$alt" = "&Itemid=$item" ] || set -- "$@" --alias "/index.php?option=com_content&task=view&id=$id$alt=$name.html"
  done
done
set -- "$@" \
 --page '/index.php?option=com_content&task=section&id=1&Itemid=2=news.html' \
 --page '/index.php?option=com_content&task=category&sectionid=1&id=7&Itemid=2=news-group.html' \
 --page '/index.php?option=com_content&task=category&sectionid=1&id=8&Itemid=2=news-software.html' \
 --page '/index.php?option=com_content&task=category&sectionid=2&id=3&Itemid=2=newsflashes.html' \
 --page '/index.php?option=com_content&task=blogsection&id=3&Itemid=40=meetings.html' \
 --page '/index.php?option=com_content&task=section&id=4&Itemid=41=faq.html' \
 --page '/index.php?option=com_content&task=category&sectionid=4&id=11&Itemid=41=faq-getting-started.html' \
 --page '/index.php?option=com_content&task=category&sectionid=4&id=12&Itemid=41=faq-hardware.html' \
 --page '/index.php?option=com_weblinks&Itemid=4=links.html' \
 --page '/index.php?option=com_weblinks&catid=13&Itemid=4=links-distributions.html' \
 --page '/index.php?option=com_weblinks&catid=14&Itemid=4=links-software.html' \
 --page '/index.php?option=com_weblinks&catid=15&Itemid=4=links-help.html' \
 --page '/index.php?option=com_contact&Itemid=3=contact.html' \
 --page '/index.php?option=com_poll&task=results&id=14=poll-results.html'

cd "$ROOT"
rm -rf exhibits/mambo && mkdir exhibits/mambo
python3 "$HERE/capture_session.py" --base $BASE --out exhibits/mambo "$@"
# The poll module's Results button navigates from an onclick handler, which capture.py does not see.
perl -pi -e "s/document\.location\.href='index\.php\?option=com_poll&amp;task=results&amp;id=14'/document.location.href='poll-results.html'/" exhibits/mambo/*.html
# com_poll writes src=".../poll.png " (trailing space); browsers trim it, capture.py kept it in the filename.
[ -f "exhibits/mambo/components/com_poll/images/poll.png " ] && mv "exhibits/mambo/components/com_poll/images/poll.png " exhibits/mambo/components/com_poll/images/poll.png
# poll.html.php adds components/com_poll/poll_bars.css from JavaScript (the result bar colours).
cp "$WORK/www/components/com_poll/poll_bars.css" exhibits/mambo/components/com_poll/
# PDF / print / e-mail icons open index2.php popups from javascript: links; there is nothing to open.
perl -pi -e "s/href=\"javascript:void window\.open\('index2\.php[^\"]*\"/href=\"#\"/g" exhibits/mambo/*.html

docker rm -f museum-mambo >/dev/null
