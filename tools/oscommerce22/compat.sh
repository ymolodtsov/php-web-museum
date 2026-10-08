#!/bin/sh
# PHP 5.6 compatibility for osCommerce 2.2 MS2 (environment only; no template/visual change).
# 1. PHP >= 5.4 has no register_globals ini switch, so the hard-coded ini_get() check always fails.
#    museum-php56-legacy emulates register_globals and sets MUSEUM_REGISTER_GLOBALS=1; accept that.
# 2. PHP 4 register_globals imported session variables into the global scope on session_start();
#    osCommerce relies on that for $cart, $language, $currency, $navigation. Re-create it.
set -e
CAT=$1
for f in "$CAT/install/includes/application.php" "$CAT/includes/application_top.php" "$CAT/admin/includes/application_top.php"; do
  perl -pi -e "s/ini_get\('register_globals'\) or exit/(ini_get('register_globals') || getenv('MUSEUM_REGISTER_GLOBALS')) or exit/" "$f"
done
for f in "$CAT/includes/functions/sessions.php" "$CAT/admin/includes/functions/sessions.php"; do
  perl -0pi -e 's/function tep_session_start\(\) \{\n    return session_start\(\);/function tep_session_start() {\n    \$r = session_start(); foreach (array_keys(\$_SESSION) as \$k) { \$GLOBALS[\$k] = &\$_SESSION[\$k]; } \/\/ museum: PHP 4 register_globals session import\n    return \$r;/' "$f"
done
# 3. MySQL >= 5.0.12 gives JOIN higher precedence than the comma operator, so the product listing
#    queries in index.php fail with "1054 Unknown column 'p.products_id' in 'on clause'". Bracket the
#    comma-joined tables, the same change osCommerce itself shipped in 2.2 MS2-051112.
perl -pi -e '
  s/from " \. TABLE_PRODUCTS \. " p, " \. TABLE_PRODUCTS_DESCRIPTION \. " pd, /from (" . TABLE_PRODUCTS . " p, " . TABLE_PRODUCTS_DESCRIPTION . " pd, /;
  s/from " \. TABLE_PRODUCTS_DESCRIPTION \. " pd, " \. TABLE_PRODUCTS \. " p left join /from (" . TABLE_PRODUCTS_DESCRIPTION . " pd, " . TABLE_PRODUCTS . " p left join /;
  s/ p2c left join " \. TABLE_SPECIALS/ p2c) left join " . TABLE_SPECIALS/;
  s/ m left join " \. TABLE_SPECIALS/ m) left join " . TABLE_SPECIALS/;
' "$CAT/index.php"
