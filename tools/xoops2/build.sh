#!/bin/bash
# Rebuild exhibits/xoops from the real XOOPS 2.0.6 release (6 Feb 2004). See tools/METHOD.md.
# Archive date 5 April 2004: the app runs under libfaketime so every "now" it prints is that day.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/xoops2"
WORK=${WORK:-/tmp/museum-xoops}
PORT=8908
U=http://127.0.0.1:$PORT
ZIP_MD5=02b5289a7759346907146060045379af   # xoops-2.0.6.zip from SourceForge OldFiles; identical content to xoops-2.0.6.tgz there

mkdir -p "$WORK" && cd "$WORK"
[ -f xoops-2.0.6.zip ] || curl -sfL -A Wget/1.21 -o xoops-2.0.6.zip https://downloads.sourceforge.net/project/xoops/OldFiles/xoops-2.0.6.zip
[ "$( (md5sum xoops-2.0.6.zip 2>/dev/null || md5 -r xoops-2.0.6.zip) | cut -c1-32)" = "$ZIP_MD5" ] || { echo "checksum mismatch"; exit 1; }
rm -rf z src && mkdir z && (cd z && unzip -q ../xoops-2.0.6.zip) && cp -R z/html src

# --- environment fixes only (PHP 4 / MySQL 4 code on PHP 5.6 / MariaDB 10.3); nothing visual is touched
cd src
grep -rl "TYPE=MyISAM" . | xargs perl -pi -e 's/TYPE=MyISAM/ENGINE=MyISAM/g'
# "clone" became a reserved word in PHP 5 (later XOOPS releases renamed the method the same way)
perl -pi -e 's/function &clone\(\)/function &xoopsClone()/' kernel/object.php
perl -pi -e 's/->clone\(\)/->xoopsClone()/g' modules/system/admin/blocksadmin/blocksadmin.php modules/system/admin/tplsets/main.php
# PHP 5 forbids "$this =& ..."
perl -0pi -e 's/\$this =& \$blkhandler->get\(\$id\);/\$obj =& \$blkhandler->get(\$id); foreach (\$obj->vars as \$k => \$v) { \$this->assignVar(\$k, \$v["value"]); } \/\/ PHP 5 compat (museum)/' kernel/block.php
# PHP 4 returned lower-case class names from get_class()
grep -rlE "get_class\([^)]*\) *(==|!=) *['\"]" . | xargs perl -pi -e 's/(?<!strtolower\()get_class\(([^()]*)\)(\s*(?:==|!=)\s*[\x27"][a-z_]+[\x27"])/strtolower(get_class($1))$2/g'
# PHP 4 kept $HTTP_SESSION_VARS bound to $_SESSION
perl -pi -e 's/^(\s*)session_start\(\);\s*$/$1session_start();\n$1\$HTTP_SESSION_VARS =& \$_SESSION; \/\/ PHP 5 compat (museum): PHP 4 linked these arrays\n/' include/common.php
chmod -R a+rwX cache templates_c uploads && chmod a+rw mainfile.php
cd "$WORK"

docker image inspect museum-xoops-faketime >/dev/null 2>&1 || docker build -q -t museum-xoops-faketime "$HERE"
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS xoops; CREATE DATABASE xoops;"
docker rm -f museum-xoops >/dev/null 2>&1 || true
docker run -d --name museum-xoops --network museum -p 127.0.0.1:$PORT:80 -v "$WORK/src":/var/www/html \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME="@2004-04-05 21:40:00" -e FAKETIME_DONT_RESET=1 \
  museum-xoops-faketime >/dev/null
sleep 4

# --- XOOPS's own web installer
I=$U/install/index.php; C="-s -b $WORK/cj -c $WORK/cj -e $U/ -o /dev/null"
rm -f "$WORK/cj"
curl $C $I -d "op=start&lang=english"
curl $C $I -d "op=dbsave&lang=english&database=mysql&dbhost=museum-db&dbuname=root&dbpass=museum&dbname=xoops&prefix=xoops&db_pconnect=0&root_path=/var/www/html&xoops_url=$U"
for op in mainfile initial checkDB createTables siteInit; do curl $C $I -d "op=$op&lang=english"; done
curl $C $I -d "op=insertData&lang=english&adminname=admin&adminmail=admin@example.com&adminpass=museum2004&adminpass2=museum2004"
curl $C $I -d "op=finish&lang=english"

# --- System Admin > Modules: install the bundled modules a 2004 portal used
rm -f "$WORK/cj"
curl $C $U/user.php -d "op=login&uname=admin&pass=museum2004"
for m in news newbb mydownloads mylinks xoopspoll xoopsmembers; do
  curl $C "$U/modules/system/admin.php" -d "fct=modulesadmin&op=install_ok&module=$m"
done
curl $C "$U/user.php?op=logout"

python3 "$HERE/make_seed.py" >/dev/null
docker exec -i museum-db mysql -uroot -pmuseum xoops < "$HERE/seed.sql"
docker exec museum-xoops sh -c 'rm -f /var/www/html/templates_c/*.php /var/www/html/cache/*.php'

# --- capture (NOCAPTURE=1 leaves the app running for inspection)
[ -n "$NOCAPTURE" ] && exit 0
capture() {
  cd "$ROOT"
  local P=(--page '/modules/news/=index.html' --alias '/=index.html' --alias '/index.php=index.html'
    --page '/modules/news/?start=5=news-page-2.html' --page '/modules/news/archive.php=news-archive.html'
    --page '/modules/newbb/=forum.html' --alias '/modules/newbb/index.php=forum.html'
    --page '/modules/mydownloads/=downloads.html' --alias '/modules/mydownloads/index.php=downloads.html'
    --page '/modules/mydownloads/topten.php?hit=1=downloads-popular.html' --page '/modules/mydownloads/topten.php?rate=1=downloads-toprated.html'
    --page '/modules/mylinks/=links.html' --alias '/modules/mylinks/index.php=links.html'
    --page '/modules/mylinks/topten.php?hit=1=links-popular.html' --page '/modules/mylinks/topten.php?rate=1=links-toprated.html'
    --page '/modules/xoopspoll/=polls.html' --alias '/modules/xoopspoll/index.php=polls.html'
    --page '/modules/xoopsmembers/=members.html'
    --page '/register.php=register.html' --page '/user.php=login.html'
    --alias '/modules/news/?start=0&storytopic=0=index.html' --alias '/modules/news/?start=5&storytopic=0=news-page-2.html'
    --page '/modules/news/archive.php?month=4&year=2004=news-archive-2004-04.html'
    --page '/modules/news/archive.php?month=3&year=2004=news-archive-2004-03.html'
    --page '/modules/xoopspoll/?poll_id=1=poll-1.html')
  P+=(--page '/modules/news/article.php?storyid=6=article.html')
  for i in 1 2 3 4 5; do P+=(--page "/modules/news/article.php?storyid=$i=article-$i.html" --page "/modules/news/?storytopic=$i=news-topic-$i.html"); done
  for i in 1 2 3 4 5 6; do P+=(--page "/modules/newbb/viewforum.php?forum=$i=forum-$i.html"); done
  for i in 1 2; do P+=(--alias "/modules/newbb/index.php?cat=$i=forum.html"); done
  while read -r t f last; do
    P+=(--page "/modules/newbb/viewtopic.php?topic_id=$t&forum=$f=topic-$t.html" --alias "/modules/newbb/viewtopic.php?topic_id=$t&forum=$f&post_id=$last=topic-$t.html"
        --alias "/modules/newbb/viewtopic.php?topic_id=$t&forum=$f&viewmode=flat=topic-$t.html")
  done < <(docker exec museum-db mysql -N -uroot -pmuseum xoops -e "SELECT topic_id, forum_id, topic_last_post_id FROM xoops_bb_topics")
  for i in 1 2 3 4; do P+=(--page "/modules/mydownloads/viewcat.php?cid=$i=downloads-cat-$i.html" --alias "/modules/mydownloads/viewcat.php?cid=$i&op==downloads-cat-$i.html"); done
  while read -r l c; do P+=(--page "/modules/mydownloads/singlefile.php?cid=$c&lid=$l=download-$l.html"); done \
    < <(docker exec museum-db mysql -N -uroot -pmuseum xoops -e "SELECT lid, cid FROM xoops_mydownloads_downloads")
  for i in 1 2 3; do P+=(--page "/modules/mylinks/viewcat.php?cid=$i=links-cat-$i.html" --alias "/modules/mylinks/viewcat.php?cid=$i&op==links-cat-$i.html"); done
  while read -r l c; do P+=(--page "/modules/mylinks/singlelink.php?cid=$c&lid=$l=link-$l.html"); done \
    < <(docker exec museum-db mysql -N -uroot -pmuseum xoops -e "SELECT lid, cid FROM xoops_mylinks_links")
  for i in 1 2; do P+=(--page "/modules/xoopspoll/pollresults.php?poll_id=$i=poll-results-$i.html"); done
  for i in $(seq 1 12); do P+=(--page "/userinfo.php?uid=$i=user-$i.html"); done
  rm -rf exhibits/xoops
  python3 tools/capture.py --base $U --out exhibits/xoops "${P[@]}"
  # "Tell a Friend" mailto bodies carry the app's URL-encoded address
  perl -pi -e 's/http%3A%2F%2F127\.0\.0\.1%3A8908/http%3A%2F%2Fwww.nexusgaming.example/g' exhibits/xoops/*.html
}
capture
[ -n "$KEEP" ] || docker rm -f museum-xoops >/dev/null
