#!/bin/sh
# Rebuild exhibits/mediawiki from the real MediaWiki 1.10.2 release (MonoBook skin).
# See tools/METHOD.md. Archive date: 11 September 2007.
#
# MediaWiki 1.10 predates PHP 5.3, so a few environment fixes are applied to the
# PHP code before it runs on PHP 5.6 (none of them touch the skin or its output):
#   - class Namespace -> MWNamespace (namespace is a reserved word since PHP 5.3)
#   - dl() calls guarded (dl() does not exist under the Apache SAPI)
#   - TYPE=InnoDB/HEAP/MyISAM -> ENGINE=... (MariaDB 10.3)
#   - by-reference parameters in StubObject::_call and the XML importer
# libfaketime (from Debian stretch) sets the wiki's clock: 3 March 2007 for the
# install, 11 September 2007 18:40 UTC for the import and capture.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/mediawiki"
WORK=${WORK:-/tmp/museum-mediawiki}
PORT=8910
NAME=museum-mediawiki
MW="$WORK/mediawiki"

mkdir -p "$WORK" && cd "$WORK"
[ -f mediawiki-1.10.2.tar.gz ] || curl -sfLO https://releases.wikimedia.org/mediawiki/1.10/mediawiki-1.10.2.tar.gz
rm -rf "$MW" mediawiki-1.10.2 && tar xzf mediawiki-1.10.2.tar.gz && mv mediawiki-1.10.2 "$MW"

python3 - "$MW" <<'EOF'
import os, re, sys
mw = sys.argv[1]
def edit(rel, *pairs, regex=False):
    p = os.path.join(mw, rel); s = open(p, encoding="latin-1").read()
    for a, b in pairs:
        n = re.subn(a, b, s) if regex else (s.replace(a, b), s.count(a))
        if not n[1]: sys.exit("patch failed: %s %s" % (rel, a))
        s = n[0]
    open(p, "w", encoding="latin-1").write(s)
for d, _, files in os.walk(mw):
    for f in files:
        if f.endswith((".php", ".inc")):
            p = os.path.join(d, f); s = open(p, encoding="latin-1").read()
            t = re.sub(r"(^|[^A-Za-z_])Namespace::", r"\1MWNamespace::", s, flags=re.M)
            if t != s: open(p, "w", encoding="latin-1").write(t)
edit("includes/Namespace.php", ("class Namespace {", "class MWNamespace {"))
edit("includes/AutoLoader.php", ("'Namespace' => 'includes/Namespace.php'", "'MWNamespace' => 'includes/Namespace.php'"))
edit("config/index.php", ("or dl($compname . '.' . PHP_SHLIB_SUFFIX))", "or (function_exists('dl') && dl($compname . '.' . PHP_SHLIB_SUFFIX)))"),
     ("'TYPE=InnoDB'", "'ENGINE=InnoDB'"))
edit("includes/MimeMagic.php", ("if(!extension_loaded('fileinfo')) dl(", "if(!extension_loaded('fileinfo') && function_exists('dl')) dl("))
edit("includes/DefaultSettings.php", ("'TYPE=InnoDB'", "'ENGINE=InnoDB'"))
edit("maintenance/tables.sql", (") TYPE=HEAP", ") ENGINE=MEMORY"), (") TYPE=MyISAM;", ") ENGINE=MyISAM;"))
edit("includes/SpecialImport.php", ("function importRevision( &$revision )", "function importRevision( $revision )"),
     ("function debugRevisionHandler( &$revision )", "function debugRevisionHandler( $revision )"))
edit("includes/StubObject.php", ("return call_user_func_array( array( $GLOBALS[$this->mGlobal], $name ), $args );",
     "$refs = array(); foreach ( $args as $k => &$v ) { $refs[$k] = &$v; } # PHP 5.3+ by-reference parameters\n"
     "\t\treturn call_user_func_array( array( $GLOBALS[$this->mGlobal], $name ), $refs );"))
EOF
chmod -R a+rwX "$MW/config" "$MW/images"

# libfaketime from the Debian archive the image already uses
if [ ! -d faketime ]; then
  docker run --rm -v "$WORK":/out museum-php56 sh -c 'apt-get -o Acquire::Check-Valid-Until=false update >/dev/null 2>&1;
    cd /tmp && apt-get download --allow-unauthenticated libfaketime >/dev/null 2>&1 && dpkg -x libfaketime_*.deb /out/faketime'
fi
FT=$(cd faketime && find . -name libfaketime.so.1 | sed 's|^\.|/opt/faketime|')

python3 "$HERE/seed.py" "$WORK/seed"

run_app() {  # $1 = wiki clock
  docker rm -f $NAME >/dev/null 2>&1 || true
  docker run -d --name $NAME --hostname www --network museum -p 127.0.0.1:$PORT:80 \
    -v "$MW":/var/www/html -v "$WORK/faketime":/opt/faketime:ro -v "$WORK/seed":/seed:ro \
    -e LD_PRELOAD=$FT -e "FAKETIME=@$1" museum-php56 >/dev/null
  sleep 3
}
sql() { docker exec -i museum-db mysql -uroot -pmuseum mediawiki "$@"; }

docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS mediawiki; CREATE DATABASE mediawiki;"
run_app "2007-03-03 14:20:00"
PW=$(openssl rand -hex 12)   # throwaway; the admin account is never used
curl -sf -o /dev/null -X POST http://127.0.0.1:$PORT/config/index.php \
 --data-urlencode "Sitename=Retrocomputing Wiki" --data-urlencode "EmergencyContact=webmaster@localhost" \
 --data-urlencode "LanguageCode=en" --data-urlencode "License=gfdl" --data-urlencode "SysopName=WikiSysop" \
 --data-urlencode "SysopPass=$PW" --data-urlencode "SysopPass2=$PW" --data-urlencode "Shm=none" \
 --data-urlencode "Email=email_enabled" --data-urlencode "Emailuser=emailuser_enabled" \
 --data-urlencode "Enotif=enotif_disabled" --data-urlencode "Eauthent=eauthent_enabled" \
 --data-urlencode "DBtype=mysql" --data-urlencode "DBserver=museum-db" --data-urlencode "DBname=mediawiki" \
 --data-urlencode "DBuser=root" --data-urlencode "DBpassword=museum" --data-urlencode "DBpassword2=museum" \
 --data-urlencode "DBprefix=" --data-urlencode "DBschema=mysql4" --data-urlencode "RootUser=root" --data-urlencode "RootPW=museum"
mv "$MW/config/LocalSettings.php" "$MW/LocalSettings.php"
cp "$HERE/logo.png" "$MW/images/retrowiki.png"
printf '\n# Retrocomputing Wiki\n$wgLogo = "$wgScriptPath/images/retrowiki.png";\n' >> "$MW/LocalSettings.php"

sql < "$WORK/seed/users.sql"
run_app "2007-09-11 18:40:00"
docker exec -w /var/www/html/maintenance $NAME php importDump.php /seed/pages.xml >/dev/null
docker exec -w /var/www/html/maintenance $NAME php rebuildrecentchanges.php >/dev/null
sql < "$HERE/post.sql"
docker exec -w /var/www/html/maintenance $NAME php initStats.php --noviews >/dev/null

# the clock keeps running from 18:40; restart it so the capture happens at that time
run_app "2007-09-11 18:40:00"
C64=$(sql -N -e "SELECT page_id FROM page WHERE page_namespace = 0 AND page_title = 'Commodore_64'")
LAST=$(sql -N -e "SELECT MAX(rev_id) FROM revision WHERE rev_page = $C64")
PREV=$(sql -N -e "SELECT MAX(rev_id) FROM revision WHERE rev_page = $C64 AND rev_id < $LAST")
DIFF="$LAST&oldid=$PREV"

OUT="$ROOT/exhibits/mediawiki"
rm -rf "$OUT" && mkdir -p "$OUT"
cd "$ROOT"
# Pages are fetched as /index.php?title=X because capture.py resolves inline <style>
# URLs against the page's directory, which breaks for /index.php/X. The /index.php/X
# links the wiki prints are mapped to the same files with --alias.
set --
for pair in Main_Page:index.html Commodore_64:commodore-64.html Talk:Commodore_64:talk-commodore-64.html \
    Apple_II:apple-ii.html Altair_8800:altair-8800.html IBM_Personal_Computer:ibm-pc.html \
    ZX_Spectrum:zx-spectrum.html Talk:ZX_Spectrum:talk-zx-spectrum.html Amiga_500:amiga-500.html \
    BBC_Micro:bbc-micro.html TRS-80:trs-80.html VIC-20:vic-20.html MOS_Technology_6502:mos-6502.html \
    Category:8-bit_computers:category-8-bit-computers.html Category:16-bit_computers:category-16-bit-computers.html \
    Category:Commodore_hardware:category-commodore-hardware.html Special:Recentchanges:recent-changes.html \
    Retrocomputing_Wiki:Community_Portal:community-portal.html Retrocomputing_Wiki:About:about.html \
    User:Datasette_Dave:user-datasette-dave.html; do
  title=${pair%:*}; file=${pair##*:}
  set -- "$@" --page "/index.php?title=$title=$file" --alias "/index.php/$title=$file"
done
python3 tools/capture.py --bar-bottom --base http://127.0.0.1:$PORT --out exhibits/mediawiki "$@" \
 --page '/index.php?title=Commodore_64&action=history=commodore-64-history.html' \
 --page "/index.php?title=Commodore_64&diff=$DIFF=commodore-64-diff.html" \
 --alias '/index.php/C64=commodore-64.html' --alias '/index.php/IBM_PC=ibm-pc.html' \
 --alias '/index.php/6502=mos-6502.html' --alias '/=index.html'

python3 "$HERE/postprocess.py" "$OUT" http://127.0.0.1:$PORT
docker rm -f $NAME >/dev/null
