<?php
// Run inside the container after seeding: MyBB's own code rebuilds inc/settings.php and the
// data caches (board stats, forums, moderators, user titles, groups, permissions) from the tables.
define("IN_MYBB", 1);
chdir("/var/www/html");
require "./inc/init.php";
rebuildsettings();
$cache->updatestats();
$cache->updateforums();
$cache->updatemoderators();
$cache->updateusertitles();
$cache->updateusergroups();
$cache->updateforumpermissions();
echo "rebuilt\n";
