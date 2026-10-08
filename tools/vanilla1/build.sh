#!/bin/sh
# Rebuild exhibits/vanilla from the real Vanilla 1.1.5a release (Lussumo, 24 September 2008),
# stock "vanilla" theme with its default style. See tools/METHOD.md.
# Archive date: Thursday 16 October 2008, 15:42 UTC. Community: "Clearfix" (content.py).
#
# Source: the Lussumo maintainers' own Google Code project (lussumo-vanilla), preserved by Google's
# code archive. Its download listing publishes SHA-1 b0125cd7454a6f85ddf79cfcd8b0e3c89d5b6a0a for
# Vanilla-1.1.5a.zip; every file inside is dated 2008-09-24, the release date getvanilla.com gave
# ("Latest version: 1.1.5a; Released: Sep 24, 2008"). The default style's CSS matches the copy
# lussumo.com/community itself served (Wayback, Oct 2007) apart from whitespace and zero units.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/tools/vanilla1"
WORK=${WORK:-/tmp/museum-vanilla}
PORT=8915
BASE=http://127.0.0.1:$PORT
NOW="2008-10-16 15:42:00"
ZIP_URL='https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/lussumo-vanilla/Vanilla-1.1.5a.zip'
ZIP_SHA1=b0125cd7454a6f85ddf79cfcd8b0e3c89d5b6a0a
ZIP_SHA256=4e7a9ac9b6e07b9fed3bb41776003cd1851cee98a2101cec1febfd937b3b741c

mkdir -p "$WORK/dl" && cd "$WORK"
[ -f dl/Vanilla-1.1.5a.zip ] || curl -sfL --retry 5 -o dl/Vanilla-1.1.5a.zip "$ZIP_URL"
echo "$ZIP_SHA1  dl/Vanilla-1.1.5a.zip" | shasum -a 1 -c -
echo "$ZIP_SHA256  dl/Vanilla-1.1.5a.zip" | shasum -a 256 -c -
rm -rf src www && mkdir src && unzip -q dl/Vanilla-1.1.5a.zip -d src && cp -R src/vanilla-1.1.5a www
chmod -R a+rwX www   # the installer writes conf/*.php

# PHP 5.6 + Apache with libfaketime: Vanilla's clock is frozen at the archive date, so
# "x minutes ago", "Last Active" and "Account Created" are the software's own output.
docker build -q -t museum-vanilla-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS vanilla; CREATE DATABASE vanilla;"
docker rm -f museum-vanilla >/dev/null 2>&1 || true
docker run -d --name museum-vanilla --network museum -p 127.0.0.1:$PORT:80 \
  -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e "FAKETIME=$NOW" -e FAKETIME_DONT_FAKE_MONOTONIC=1 \
  -v "$WORK/www":/var/www/html museum-vanilla-faketime >/dev/null
sleep 3

# Vanilla's own installer, all three steps. The admin password is random and thrown away.
PW=$(openssl rand -hex 10)
J="$WORK/install-cookies.txt"; rm -f "$J"
inst() { curl -sf -c "$J" -b "$J" -o /dev/null -w '%{redirect_url}\n' -X POST "$BASE/setup/installer.php" "$@"; }
inst -d PostBackAction=Permissions | grep -q 'Step=2'
inst -d PostBackAction=Database -d DBHost=museum-db -d DBName=vanilla -d DBUser=root -d DBPass=museum \
     -d DBTablePrefix=LUM_ | grep -q 'Step=3'
inst -d PostBackAction=User -d Username=dmitri -d "Password=$PW" -d "ConfirmPassword=$PW" -d SupportName=dmitri \
     -d SupportEmail=dmitri@clearfix.example -d ApplicationTitle=Clearfix -d CookieDomain= -d CookiePath=/ | grep -q 'Step=4'

python3 "$HERE/gen_seed.py"
docker exec -i museum-db mysql -uroot -pmuseum vanilla < "$HERE/seed.sql"

# Pages. Discussion and sign-in link variants are mapped by capture_vanilla.py.
set -- --page '/=index.html' --page '/?page=2=index-2.html' --alias '/?page=1=index.html' --page '/categories.php=categories.html' \
       --page '/search.php=search.html' --page '/people.php=signin.html' \
       --page '/people.php?PostBackAction=ApplyForm=apply.html' \
       --page '/people.php?PostBackAction=PasswordRequestForm=password.html' \
       --page '/termsofservice.php=terms.html'
for c in $(docker exec museum-db mysql -N -uroot -pmuseum vanilla -e 'SELECT CategoryID FROM LUM_Category ORDER BY CategoryID'); do
  set -- "$@" --page "/?CategoryID=$c=category-$c.html"
done
for d in $(docker exec museum-db mysql -N -uroot -pmuseum vanilla -e 'SELECT DiscussionID FROM LUM_Discussion ORDER BY DiscussionID'); do
  set -- "$@" --page "/comments.php?DiscussionID=$d=discussion-$d.html"
done
for u in $(docker exec museum-db mysql -N -uroot -pmuseum vanilla -e 'SELECT UserID FROM LUM_User ORDER BY UserID'); do
  set -- "$@" --page "/account.php?u=$u=account-$u.html"
done

OUT="$ROOT/exhibits/vanilla"
rm -rf "$OUT" && mkdir -p "$OUT"
cd "$ROOT"
python3 "$HERE/capture_vanilla.py" --base "$BASE" --out exhibits/vanilla "$@"
# Images the default style only uses from JavaScript or for states a guest never sees.
for f in progress.gif hprogress.gif ico.check.gif ico.alert.gif ico.unknown.gif; do
  [ -f "$OUT/themes/vanilla/styles/default/$f" ] || cp "$WORK/www/themes/vanilla/styles/default/$f" "$OUT/themes/vanilla/styles/default/"
done

[ -n "$KEEP" ] || docker rm -f museum-vanilla >/dev/null
