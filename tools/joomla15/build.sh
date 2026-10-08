#!/bin/sh
# Rebuild exhibits/joomla-15 from the real Joomla! 1.5.3 release (22 April 2008). See tools/METHOD.md.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
WORK=${WORK:-/tmp/museum-joomla}
PORT=8906
J=http://127.0.0.1:$PORT
DB="docker exec -i museum-db mysql -uroot -pmuseum"

mkdir -p "$WORK" && cd "$WORK"
if [ ! -d joomla ]; then
  curl -sfL -o joomla.tar.gz "https://downloads.joomla.org/cms/joomla15/1-5-3/joomla_1-5-3-stable-full_package-tar-gz?format=gz"
  mkdir joomla && tar xzf joomla.tar.gz -C joomla
  # Environment fixes for MariaDB 10.3 / PHP 5.6 (output unchanged):
  # MySQL 4 table syntax in the installer SQL
  sed -i.bak 's/TYPE=MyISAM/ENGINE=MyISAM/g' joomla/installation/sql/mysql/*.sql
  # PHP >= 5.3 refuses by-reference args through call_user_func_array, which left
  # every mod_mainmenu module empty. Same change Joomla itself shipped in 1.5.15.
  sed -i.bak 's/function buildXML(&\$params)/function buildXML($params)/' joomla/modules/mod_mainmenu/helper.php
  rm -f joomla/installation/sql/mysql/*.bak joomla/modules/mod_mainmenu/helper.php.bak
fi
[ -d joomla/installation ] || { rm -rf joomla/installation; cp -R installation.removed joomla/installation; }
rm -f joomla/configuration.php

$DB -e "DROP DATABASE IF EXISTS joomla15; CREATE DATABASE joomla15 CHARACTER SET utf8;"
docker rm -f museum-joomla >/dev/null 2>&1 || true
docker run -d --name museum-joomla --network museum -p 127.0.0.1:$PORT:80 -v "$WORK/joomla":/var/www/html museum-php56 >/dev/null
sleep 3

# The web installer, driven step by step (no sample data)
rm -f cj
curl -sf -c cj -b cj "$J/installation/index.php" -o /dev/null
curl -sf -c cj -b cj "$J/installation/index.php" -o /dev/null -d task=makedb \
  -d 'vars[DBtype]=mysql' -d 'vars[DBhostname]=museum-db' -d 'vars[DBuserName]=root' -d 'vars[DBpassword]=museum' \
  -d 'vars[DBname]=joomla15' -d 'vars[DBPrefix]=jos_' -d 'vars[DBOld]=rm' -d 'vars[lang]=en-GB'
PW=$(openssl rand -hex 12)
curl -sf -c cj -b cj "$J/installation/index.php" -o /dev/null -d task=saveconfig \
  -d 'vars[siteName]=Orbital Design Studio' -d 'vars[adminEmail]=webmaster@orbitaldesignstudio.example' \
  -d "vars[adminPassword]=$PW" -d "vars[confirmAdminPassword]=$PW" -d 'vars[ftpEnable]=0'
rm -f cj
test -f joomla/configuration.php
rm -rf installation.removed && mv joomla/installation installation.removed

# Global Configuration > Site: metadata
sed -i.bak -e "s/^var \$MetaDesc = .*/var \$MetaDesc = 'Orbital Design Studio - web design, hosting and Joomla websites for small businesses in Northbridge.';/" \
           -e "s/^var \$MetaKeys = .*/var \$MetaKeys = 'web design, Northbridge, website hosting, Joomla, small business websites';/" joomla/configuration.php
rm -f joomla/configuration.php.bak

$DB joomla15 < "$ROOT/tools/joomla15/seed.sql"

# Discover pages, then reseed so crawl hits don't count, and leave two other guests online
python3 "$ROOT/tools/joomla15/pages.py" $J > pages.txt
$DB joomla15 < "$ROOT/tools/joomla15/seed.sql"
NOW=$(date +%s)
$DB joomla15 -e "INSERT INTO jos_session (username, time, session_id, guest, userid, usertype, gid, client_id, data) VALUES
  ('', '$NOW', 'a3f9c1e07b5d2846e1c0f7a9b2d4e6f1', 1, 0, '', 0, 0, ''),
  ('', '$NOW', 'c81e728d9d4c2f636f067f89cc14862c', 1, 0, '', 0, 0, '');"

cd "$ROOT"
OUT=exhibits/joomla-15
find "$OUT" -mindepth 1 -delete 2>/dev/null || true
python3 tools/capture.py --base $J --out $OUT $(cat "$WORK/pages.txt")

# The archive date is 9 June 2008: mod_footer prints the server's current year.
# The poll's Results button navigates from an onclick, which capture.py doesn't rewrite.
for f in $OUT/*.html; do
  sed -i.bak -e "s/Copyright &#169; [0-9]\{4\} Orbital/Copyright \&#169; 2008 Orbital/" \
             -e "s#document.location.href='/index.php?option=com_poll&amp;id=1:which-browser-do-you-use-most'#document.location.href='poll-results.html'#" "$f"
  rm -f "$f.bak"
done

docker rm -f museum-joomla >/dev/null
