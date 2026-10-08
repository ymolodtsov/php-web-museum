<?php
/**
* "Who is online" at capture time: sessions for the members, guests and crawlers that are on
* the board. Fetched over HTTP right before the capture (so time() is the web server's faked
* clock), then deleted. Data: museum_content.php (JSON written by gen_content.py).
*/
define('IN_PHPBB', true);
$phpbb_root_path = './';
$phpEx = 'php';
include($phpbb_root_path . 'common.php');

$data = json_decode(file_get_contents('museum_content.php'), true);
$now = time();

$db->sql_query('DELETE FROM ' . SESSIONS_TABLE);

// what people are looking at: the board index, a few forums and the busiest topics
$pages = array('index.php', 'viewforum.php?f=5', 'memberlist.php', 'viewforum.php?f=4', 'search.php', 'faq.php');
foreach ($data['topics'] as $t)
{
	if (in_array($t['key'], array('fallout', 'lbp', 'gpu', 'fable', 'poll', 'gears', 'intro')))
	{
		$pages[] = 'viewtopic.php?f=' . $t['forum'] . '&t=' . $t['id'];
	}
}

function add_session($user_id, $ip, $age, $page, $viewonline, $browser)
{
	global $db, $now;
	$forum_id = preg_match('/f=(\d+)/', $page, $m) ? (int) $m[1] : 0;
	$db->sql_query('INSERT INTO ' . SESSIONS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
		'session_id' => md5(unique_id()), 'session_user_id' => $user_id, 'session_forum_id' => $forum_id,
		'session_last_visit' => $now - $age - 3600, 'session_start' => $now - $age - 600, 'session_time' => $now - $age,
		'session_ip' => $ip, 'session_browser' => $browser, 'session_forwarded_for' => '', 'session_page' => $page,
		'session_viewonline' => $viewonline, 'session_autologin' => 1, 'session_admin' => 0,
	)));
}

$ff = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3';
foreach ($data['online'] as $i => $user_id)
{
	$result = $db->sql_query('SELECT user_allow_viewonline FROM ' . USERS_TABLE . " WHERE user_id = $user_id");
	$viewonline = (int) $db->sql_fetchfield('user_allow_viewonline');
	add_session($user_id, '10.20.' . $i . '.' . (40 + $i), 20 + $i * 37, $pages[$i % sizeof($pages)], $viewonline, $ff);
	$db->sql_query('UPDATE ' . USERS_TABLE . ' SET user_lastvisit = ' . ($now - 20 - $i * 37) . " WHERE user_id = $user_id");
}
for ($g = 0; $g < $data['guests_online']; $g++)
{
	add_session(ANONYMOUS, '10.40.' . $g . '.' . (11 + 7 * $g), 5 + $g * 17, $pages[($g + 3) % sizeof($pages)], 1, $ff);
}
foreach ($data['bots_online'] as $b => $bot)
{
	$result = $db->sql_query('SELECT user_id FROM ' . USERS_TABLE . " WHERE username = '" . $db->sql_escape($bot) . "'");
	$bot_id = (int) $db->sql_fetchfield('user_id');
	add_session($bot_id, '66.249.71.' . (20 + $b), 50 + $b * 60, 'viewtopic.php?f=8&t=64963', 1, 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)');
}
echo 'ok';
