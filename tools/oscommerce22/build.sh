#!/bin/sh
# Rebuild exhibits/oscommerce from the real osCommerce 2.2 Milestone 2 release. See tools/METHOD.md.
#
# Version: 2.2 MS2 (released 12 July 2003) was the current osCommerce release on 19 November 2004;
# the next package, 2.2 MS2-051112, came out in November 2005. The tarball is the one on the
# project's SourceForge file area (project "tep"); its MD5 matches the .md5sum file published
# alongside it in 2003 and SourceForge's own SHA-1/SHA-256.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/../.." && pwd)
WORK=${WORK:-/tmp/museum-oscommerce}
PORT=8912
BASE=http://127.0.0.1:$PORT
TARBALL=oscommerce-2.2ms2.tar.gz
TARBALL_URL=https://downloads.sourceforge.net/project/tep/osCommerce/2.2-MS2/$TARBALL
TARBALL_SHA256=e27621e556f97d0c0604a055f033064d37987374d09cde5eef1b3cdb7381a531   # md5 2dee2756a27ab86561645a4141499795

mkdir -p "$WORK" && cd "$WORK"
[ -f $TARBALL ] || curl -sfL --retry 5 -o $TARBALL "$TARBALL_URL"
echo "$TARBALL_SHA256  $TARBALL" | shasum -a 256 -c -
rm -rf oscommerce-2.2ms2 catalog && tar xzf $TARBALL && mv oscommerce-2.2ms2/catalog catalog
"$HERE/compat.sh" catalog                      # PHP 5.6 environment fixes only
chmod -R a+rwX catalog

# Product photos (public domain / CC0, see CREDITS.txt), cropped to osCommerce's 5:4 image box
cp -R "$HERE/images/" catalog/images/

# PHP 5.6 + register_globals shim + libfaketime: the clock starts at 19 Nov 2004 10:20 UTC
docker build -q -t museum-oscommerce-faketime "$HERE" >/dev/null
docker exec museum-db mysql -uroot -pmuseum -e "DROP DATABASE IF EXISTS oscommerce; CREATE DATABASE oscommerce;"
run() {
  docker rm -f museum-oscommerce >/dev/null 2>&1 || true
  docker run -d --name museum-oscommerce --network museum -p 127.0.0.1:$PORT:80 \
    -e LD_PRELOAD=/usr/local/lib/libfaketime.so.1 -e FAKETIME='@2004-11-19 10:20:00' -e FAKETIME_DONT_RESET=1 \
    -v "$WORK/catalog":/var/www/html "$@" museum-oscommerce-faketime >/dev/null
  sleep 3
}
run

# osCommerce's own installer: step 3 imports install/oscommerce.sql (with sample data), step 7 writes configure.php
I="-d install[]=database -d install[]=configure -d DB_SERVER=museum-db -d DB_SERVER_USERNAME=root -d DB_SERVER_PASSWORD=museum -d DB_DATABASE=oscommerce"
curl -sf $I "$BASE/install/install.php?step=3" | grep -q "database import was <b>successful"
curl -sf $I -d STORE_SESSIONS=files -d HTTP_WWW_ADDRESS=$BASE/ -d DIR_FS_DOCUMENT_ROOT=/var/www/html/ \
     -d HTTP_COOKIE_DOMAIN= -d HTTP_COOKIE_PATH=/ "$BASE/install/install.php?step=7" | grep -q "configuration was successful"
# what the installer's final page tells the shop owner to do (the storefront warns until it's done)
# (Docker Desktop's bind mount reports every file writable, so configure.php is mounted read-only instead of chmod 644)
rm -rf catalog/install
run -v "$WORK/catalog/includes/configure.php":/var/www/html/includes/configure.php:ro

# Store content: catalogue/orders in the database, texts via the language files (Define Languages)
docker exec -i museum-db mysql -uroot -pmuseum oscommerce < "$HERE/seed.sql"
python3 "$HERE/texts.py" catalog
[ -n "$SKIP_CAPTURE" ] && exit 0

PRODUCTS="1 25 26 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45"
set -- --page '/=index.html'
for c in 1 1_4 1_6 1_7 1_8 1_9 1_16 1_17 1_23 1_24 21 22; do set -- "$@" --page "/index.php?cPath=$c=cat-$c.html"; done
for m in 1 2 5 10 11 12 13 14 15 16 17 18 19 20 21; do set -- "$@" --page "/index.php?manufacturers_id=$m=manufacturer-$m.html"; done
for p in $PRODUCTS; do
  set -- "$@" --page "/product_info.php?products_id=$p=product-$p.html" --page "/product_reviews.php?products_id=$p=product-$p-reviews.html" \
              --page "/popup_image.php?pID=$p=popup-$p.html" --alias "/product_reviews_write.php?products_id=$p=login.html"
done
for r in 1:26 2:37 3:26 4:39 5:33 6:42 7:28 8:28 9:41; do
  set -- "$@" --page "/product_reviews_info.php?products_id=${r#*:}&reviews_id=${r%%:*}=review-${r%%:*}.html"
done
set -- "$@" \
 --page '/shopping_cart.php=shopping_cart.html' \
 --page '/specials.php=specials.html' \
 --page '/products_new.php=products_new.html' --alias '/products_new.php?page=1=products_new.html' \
 --page '/products_new.php?page=2=products_new-2.html' --page '/products_new.php?page=3=products_new-3.html' \
 --page '/reviews.php=reviews.html' --alias '/reviews.php?page=1=reviews.html' --page '/reviews.php?page=2=reviews-2.html' \
 --page '/advanced_search.php=advanced_search.html' \
 --page '/shipping.php=shipping.html' --page '/privacy.php=privacy.html' --page '/conditions.php=conditions.html' \
 --page '/contact_us.php=contact_us.html' \
 --page '/login.php=login.html' --alias '/account.php=login.html' --alias '/checkout_shipping.php=login.html' \
 --page '/create_account.php=create_account.html' --page '/password_forgotten.php=password_forgotten.html'

cd "$ROOT"
rm -rf exhibits/oscommerce && mkdir exhibits/oscommerce
# the visitor has a Logitech MX518 and a SanDisk CompactFlash card in the cart
python3 "$HERE/capture_session.py" --cart 28 --cart 42 --base $BASE --out exhibits/oscommerce "$@"
# "Click to enlarge" opens popup_image.php from a document.write() javascript: link, which capture.py does not see
perl -pi -e "s/popupWindow\(\\\\'popup_image\.php\?pID=(\d+)\\\\'\)/popupWindow(\\\\'popup-\$1.html\\\\')/g" exhibits/oscommerce/product-*.html exhibits/oscommerce/review-*.html

docker rm -f museum-oscommerce >/dev/null
