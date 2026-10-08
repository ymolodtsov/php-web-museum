<?php
// Set the site preferences an admin would change in Admin > Preferences / Menus.
// Run inside the app container: php /var/www/html/museum_prefs.php
// Stores prefs the way e107 0.617's save_prefs() does: addslashes(serialize($pref)).
mysql_connect('museum-db', 'root', 'museum') or die(mysql_error());
mysql_select_db('e107');

function load($name) {
    $r = mysql_fetch_row(mysql_query("SELECT e107_value FROM e107_core WHERE e107_name='$name'"));
    return unserialize($r[0]);
}
function save($name, $v) {
    mysql_query("UPDATE e107_core SET e107_value='" . addslashes(serialize($v)) . "' WHERE e107_name='$name'") or die(mysql_error());
}

$pref = load('pref');
$pref['sitename'] = 'Clan Obsidian';
$pref['sitetag'] = 'Counter-Strike and Half-Life 2 since 2002';
$pref['sitedescription'] = 'Clan Obsidian [OBS] - Counter-Strike 1.6, Source and Half-Life 2 Deathmatch. Public server, scrims, forums.';
$pref['siteadmin'] = 'Revenant';
$pref['siteadminemail'] = 'revenant@clanobsidian.net';
$pref['sitedisclaimer'] = 'All trademarks are &copy; their respective owners, all other content is &copy; Clan Obsidian.<br />e107 is &copy; e107.org 2002/2003 and is released under the <a href=&#39;http://www.gnu.org/&#39;>GNU GPL license</a>.';
$pref['smiley_activate'] = '1';
$pref['autoban'] = '0';           // the capture run would otherwise trip the hit counter
$pref['forum_title'] = 'Forums';
$pref['newsposts'] = '10';
save('pref', $pref);

$menu = load('menu_pref');
$menu['newforumposts_caption'] = 'Latest Forum Posts';
$menu['newforumposts_display'] = '6';
$menu['newforumposts_characters'] = '50';
save('menu_pref', $menu);
echo "prefs saved\n";
