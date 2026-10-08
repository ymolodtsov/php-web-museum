<?php
/**
* Seed Pixel Arena Forums into a fresh phpBB 3.0.2 install, using phpBB's own functions where
* the board has them (user_add, group_user_add, parse_message, sync, cache_moderators,
* set_config). Run from the board root inside the container: php seed.php
* Data: museum_content.php (JSON written by gen_content.py).
*/
define('IN_PHPBB', true);
$phpbb_root_path = './';
$phpEx = 'php';
$_SERVER['REMOTE_ADDR'] = '127.0.0.1';
$_SERVER['HTTP_USER_AGENT'] = 'seed';
$_SERVER['REQUEST_METHOD'] = 'GET';
include($phpbb_root_path . 'common.php');
include($phpbb_root_path . 'includes/functions_user.php');
include($phpbb_root_path . 'includes/functions_admin.php');
include($phpbb_root_path . 'includes/message_parser.php');

$user->session_begin(false);
$auth->acl($user->data);
$user->setup();
@set_time_limit(0);

$data = json_decode(file_get_contents('museum_content.php'), true);
$now = $data['now'];

function q($sql)
{
	global $db;
	return $db->sql_query($sql);
}

// Everything users type reaches phpBB through request_var(), which HTML-escapes it; do the same.
function e($s)
{
	return htmlspecialchars($s, ENT_COMPAT, 'UTF-8');
}

function parse_text($text, &$uid, &$bitfield)
{
	$mp = new parse_message(e($text));
	// bbcode, magic urls, smilies, [img], [flash], [quote], [url]
	$mp->parse(true, true, true, true, false, true, true);
	$uid = $mp->bbcode_uid;
	$bitfield = $mp->bbcode_bitfield;
	return $mp->message;
}

// ---- board configuration (ACP settings) -------------------------------------------
set_config('sitename', e($data['sitename']));
set_config('site_desc', e($data['site_desc']));
set_config('board_startdate', $data['board_start']);
set_config('allow_avatar_upload', 1);     // uploaded avatars came across from phpBB 2
set_config('load_user_activity', 0);      // "most active forum/topic" off, as on most big boards
set_config('record_online_users', $data['record_online'][0]);
set_config('record_online_date', $data['record_online'][1]);
// Housekeeping tasks (cron.php) all ran just now, so no page carries the 1x1 cron image.
foreach (array('cache', 'search', 'session', 'warnings', 'database', 'queue') as $gc)
{
	set_config($gc . '_last_gc', time(), true);
}

// ---- the installer's sample category, forum and topic go -------------------------
q('DELETE FROM ' . FORUMS_TABLE);
q('DELETE FROM ' . TOPICS_TABLE);
q('DELETE FROM ' . POSTS_TABLE);
q('DELETE FROM ' . ACL_GROUPS_TABLE . ' WHERE forum_id <> 0');
q('DELETE FROM ' . SEARCH_WORDMATCH_TABLE);
q('DELETE FROM ' . SEARCH_WORDLIST_TABLE);

// ---- ranks -----------------------------------------------------------------------
$rank_ids = array('Site Admin' => 1);
foreach ($data['ranks'] as $r)
{
	q('INSERT INTO ' . RANKS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
		'rank_title' => e($r[0]), 'rank_min' => $r[1], 'rank_special' => $r[2], 'rank_image' => '')));
	$rank_ids[$r[0]] = $db->sql_nextid();
}

// ---- members ---------------------------------------------------------------------
// Search-engine bots (created by the installer as users 3..52) move out of the way of the
// converted member ids; they get ids after the last member at the end, as the convertor does.
$bot_ids = array();
$result = q('SELECT user_id FROM ' . USERS_TABLE . ' WHERE user_type = ' . USER_IGNORE . ' AND user_id > 1 ORDER BY user_id');
while ($row = $db->sql_fetchrow($result))
{
	$bot_ids[] = (int) $row['user_id'];
}
function move_user($from, $to)
{
	foreach (array(USERS_TABLE, USER_GROUP_TABLE, BOTS_TABLE) as $t)
	{
		q("UPDATE $t SET user_id = $to WHERE user_id = $from");
	}
}
foreach ($bot_ids as $i => $id)
{
	move_user($id, 900000 + $i);
}

$all = array();
foreach ($data['members'] as $m)
{
	$all[$m['id']] = array('named' => $m);
}
foreach ($data['fillers'] as $f)
{
	$all[$f[0]] = array('filler' => $f);
}
ksort($all);
set_config('num_users', 1);   // Zane, the founder created by the installer

$avatar_salt = $config['avatar_salt'];
foreach ($all as $id => $entry)
{
	if (isset($entry['named']))
	{
		$m = $entry['named'];
		$name = $m['name'];
		$regdate = $m['regdate'];
		$posts = $m['posts'];
		$last = $m['last'];
		$from = '';
	}
	else
	{
		list(, $name, $regdate, $posts, $last, $from) = $entry['filler'];
	}
	if ($id != 2)
	{
		user_add(array(
			'user_id'		=> $id,
			'username'		=> $name,
			'user_password'	=> phpbb_hash(unique_id()),
			'user_email'	=> 'member' . $id . '@pixelarena.example',
			'group_id'		=> 2,   // REGISTERED
			'user_type'		=> USER_NORMAL,
			'user_ip'		=> '127.0.0.1',
			'user_regdate'	=> $regdate,
			'user_passchg'	=> $regdate,
			'user_lastmark'	=> $last,
			'user_lastvisit'	=> $last,
			'user_posts'	=> $posts,
			'user_allow_viewemail' => 0,
			'user_from'		=> isset($from) ? e($from) : '',
		));
	}
	else
	{
		q('UPDATE ' . USERS_TABLE . ' SET ' . $db->sql_build_array('UPDATE', array(
			'user_regdate' => $regdate, 'user_passchg' => $regdate, 'user_lastvisit' => $last,
			'user_lastmark' => $last, 'user_posts' => $posts, 'user_allow_viewemail' => 0)) . ' WHERE user_id = 2');
	}
	if (!isset($entry['named']))
	{
		continue;
	}

	$sig_uid = $sig_bitfield = '';
	$sig = ($m['sig'] !== '') ? parse_text($m['sig'], $sig_uid, $sig_bitfield) : '';
	$im = $m['im'];
	$row = array(
		'user_from'		=> e($m['loc']),
		'user_occ'		=> e($m['occ']),
		'user_interests'	=> e($m['interests']),
		'user_website'	=> $m['www'],
		'user_icq'		=> isset($im['icq']) ? $im['icq'] : '',
		'user_aim'		=> isset($im['aim']) ? $im['aim'] : '',
		'user_msnm'		=> isset($im['msnm']) ? $im['msnm'] : '',
		'user_yim'		=> isset($im['yim']) ? $im['yim'] : '',
		'user_jabber'	=> isset($im['jabber']) ? $im['jabber'] : '',
		'user_sig'		=> $sig,
		'user_sig_bbcode_uid'		=> $sig_uid,
		'user_sig_bbcode_bitfield'	=> $sig_bitfield,
		'user_birthday'	=> ($m['bday'] !== '') ? vsprintf('%2d-%2d-%4d', explode('-', $m['bday'])) : '',
		'user_rank'		=> ($m['rank'] !== '') ? $rank_ids[$m['rank']] : 0,
		'user_allow_viewonline' => $m['viewonline'],
	);
	if ($m['avatar'] !== '')
	{
		// an uploaded avatar, stored the way phpBB 3 stores uploads: <salt>_<user_id>.<ext>
		copy('museum_avatars/' . $m['avatar'], $config['avatar_path'] . '/' . $avatar_salt . '_' . $id . '.gif');
		$size = getimagesize('museum_avatars/' . $m['avatar']);
		$row += array('user_avatar' => $id . '_' . $regdate . '.gif', 'user_avatar_type' => AVATAR_UPLOAD,
			'user_avatar_width' => $size[0], 'user_avatar_height' => $size[1]);
	}
	q('UPDATE ' . USERS_TABLE . ' SET ' . $db->sql_build_array('UPDATE', $row) . " WHERE user_id = $id");

	if ($m['group'] == 'gmod')
	{
		group_user_add(4, array($id), false, false, true);   // GLOBAL_MODERATORS, default group
	}
}

foreach ($bot_ids as $i => $id)
{
	move_user(900000 + $i, $data['max_user_id'] + 1 + $i);
}
q('ALTER TABLE ' . USERS_TABLE . ' AUTO_INCREMENT = ' . ($data['max_user_id'] + 1 + sizeof($bot_ids)));

// ---- forums ----------------------------------------------------------------------
// Nested set in display order; categories wrap their forums.
$forums = $data['forums'];
$left = array();
$pos = 1;
$open = null;
foreach ($forums as $i => $f)
{
	if ($f['parent'] == 0)
	{
		if ($open !== null)
		{
			$forums[$open]['right'] = $pos++;
		}
		$forums[$i]['left'] = $pos++;
		$open = $i;
	}
	else
	{
		$forums[$i]['left'] = $pos++;
		$forums[$i]['right'] = $pos++;
	}
}
$forums[$open]['right'] = $pos++;

$names = array();
foreach ($forums as $f)
{
	$names[$f['id']] = e($f['name']);
}
foreach ($forums as $f)
{
	$is_cat = ($f['parent'] == 0);
	q('INSERT INTO ' . FORUMS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
		'forum_id' => $f['id'], 'parent_id' => $f['parent'], 'left_id' => $f['left'], 'right_id' => $f['right'],
		'forum_parents' => $is_cat ? '' : serialize(array($f['parent'] => array($names[$f['parent']], FORUM_CAT))),
		'forum_name' => e($f['name']), 'forum_desc' => e($f['desc']), 'forum_desc_bitfield' => '', 'forum_desc_options' => 7,
		'forum_desc_uid' => '', 'forum_link' => '', 'forum_password' => '', 'forum_image' => '', 'forum_rules' => '',
		'forum_rules_link' => '', 'forum_rules_bitfield' => '', 'forum_rules_options' => 7, 'forum_rules_uid' => '',
		'forum_type' => $is_cat ? FORUM_CAT : FORUM_POST, 'forum_status' => ITEM_UNLOCKED,
		'forum_last_post_subject' => '', 'forum_last_poster_name' => '', 'forum_last_poster_colour' => '',
		'forum_flags' => 32, 'display_subforum_list' => 1, 'display_on_index' => 1, 'enable_indexing' => 1,
		'enable_icons' => 1,
	)));

	// The installer's default permission sets: guests and bots read only, registered users post
	// (with polls), moderators/admins full.
	$sets = $is_cat
		? array(1 => array(17), 2 => array(17), 3 => array(17), 6 => array(17))
		: array(1 => array(17), 2 => array(21), 3 => array(21), 4 => array(21), 5 => array(14, 10), 6 => array(19));
	foreach ($sets as $group_id => $roles)
	{
		foreach ($roles as $role)
		{
			q('INSERT INTO ' . ACL_GROUPS_TABLE . " (group_id, forum_id, auth_option_id, auth_role_id, auth_setting) VALUES ($group_id, {$f['id']}, 0, $role, 0)");
		}
	}
	foreach ($f['mods'] as $mod_id)
	{
		q('INSERT INTO ' . ACL_USERS_TABLE . " (user_id, forum_id, auth_option_id, auth_role_id, auth_setting) VALUES ($mod_id, {$f['id']}, 0, 11, 0)");
	}
}
// Guests may view profiles and the member list (ACP: Group permissions).
foreach (array('u_viewprofile') as $opt)
{
	$result = q('SELECT auth_option_id FROM ' . ACL_OPTIONS_TABLE . " WHERE auth_option = '$opt'");
	$opt_id = (int) $db->sql_fetchfield('auth_option_id');
	q('INSERT INTO ' . ACL_GROUPS_TABLE . " (group_id, forum_id, auth_option_id, auth_role_id, auth_setting) VALUES (1, 0, $opt_id, 0, 1)");
}

// ---- topics and posts ------------------------------------------------------------
$topic_ids = array();
foreach ($data['topics'] as $t)
{
	$forum_id = ($t['type'] == POST_GLOBAL) ? 0 : $t['forum'];
	$topic = array(
		'topic_id' => $t['id'], 'forum_id' => $forum_id, 'topic_title' => e($t['title']),
		'topic_poster' => $t['posts'][0]['poster'], 'topic_time' => $t['posts'][0]['time'],
		'topic_views' => $t['views'], 'topic_type' => $t['type'],
		'topic_status' => $t['locked'] ? ITEM_LOCKED : ITEM_UNLOCKED, 'topic_approved' => 1,
		'topic_first_poster_name' => '', 'topic_last_poster_name' => '', 'topic_last_post_subject' => '',
		'topic_last_view_time' => $now - 60,
		'poll_title' => '', 'poll_start' => 0, 'poll_length' => 0, 'poll_max_options' => 1,
		'poll_last_vote' => 0, 'poll_vote_change' => 0,
	);
	if ($t['poll'])
	{
		$p = $t['poll'];
		$topic['poll_title'] = e($p['title']);
		$topic['poll_start'] = $p['start'];
		$topic['poll_length'] = $p['length'] * 86400;
		$topic['poll_max_options'] = $p['max'];
		$topic['poll_last_vote'] = $now - 2400;
		foreach ($p['options'] as $i => $o)
		{
			q('INSERT INTO ' . POLL_OPTIONS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
				'poll_option_id' => $i + 1, 'topic_id' => $t['id'], 'poll_option_text' => e($o[0]),
				'poll_option_total' => $o[1])));
		}
	}
	q('INSERT INTO ' . TOPICS_TABLE . ' ' . $db->sql_build_array('INSERT', $topic));
	$topic_ids[] = $t['id'];

	foreach ($t['posts'] as $p)
	{
		$uid = $bitfield = '';
		$text = parse_text($p['text'], $uid, $bitfield);
		q('INSERT INTO ' . POSTS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
			'post_id' => $p['id'], 'topic_id' => $t['id'], 'forum_id' => $forum_id, 'poster_id' => $p['poster'],
			'icon_id' => 0, 'poster_ip' => '127.0.0.1', 'post_time' => $p['time'], 'post_approved' => 1,
			'post_reported' => 0, 'enable_bbcode' => 1, 'enable_smilies' => 1, 'enable_magic_url' => 1,
			'enable_sig' => 1, 'post_username' => '', 'post_subject' => e($p['subject']), 'post_text' => $text,
			'post_checksum' => md5($text), 'post_attachment' => 0, 'bbcode_bitfield' => $bitfield,
			'bbcode_uid' => $uid, 'post_postcount' => 1, 'post_edit_time' => 0, 'post_edit_reason' => '',
			'post_edit_user' => 0, 'post_edit_count' => 0, 'post_edit_locked' => 0,
		)));
		q('UPDATE ' . USERS_TABLE . ' SET user_lastpost_time = GREATEST(user_lastpost_time, ' . $p['time'] . ') WHERE user_id = ' . $p['poster']);
	}
}
// Topic first/last post data, reply counts, poster names and colours from the posts.
sync('topic', 'topic_id', $topic_ids, false, true);

// Search index for the posts, through the board's own fulltext_native backend.
include($phpbb_root_path . 'includes/search/fulltext_native.php');
$error = false;
$search = new fulltext_native($error);
$result = q('SELECT post_id, post_subject, post_text, poster_id, forum_id FROM ' . POSTS_TABLE);
while ($row = $db->sql_fetchrow($result))
{
	$search->index('post', $row['post_id'], $row['post_text'], $row['post_subject'], $row['poster_id'], $row['forum_id']);
}

// The rest of each forum's first page: older topics whose posts are not part of the exhibit.
$colour = array();
$uname = array();
$result = q('SELECT user_id, username, user_colour FROM ' . USERS_TABLE . ' WHERE user_id IN (SELECT DISTINCT topic_poster FROM ' . TOPICS_TABLE . ') OR user_id < 10000');
while ($row = $db->sql_fetchrow($result))
{
	$colour[$row['user_id']] = $row['user_colour'];
	$uname[$row['user_id']] = $row['username'];
}
foreach ($data['filler_topics'] as $f)
{
	q('INSERT INTO ' . TOPICS_TABLE . ' ' . $db->sql_build_array('INSERT', array(
		'topic_id' => $f['id'], 'forum_id' => $f['forum'], 'topic_title' => e($f['title']), 'topic_poster' => $f['poster'],
		'topic_time' => $f['time'], 'topic_views' => $f['views'], 'topic_replies' => $f['replies'],
		'topic_replies_real' => $f['replies'], 'topic_status' => $f['locked'] ? ITEM_LOCKED : ITEM_UNLOCKED,
		'topic_type' => $f['type'], 'topic_approved' => 1,
		'topic_first_post_id' => $f['first_post_id'], 'topic_first_poster_name' => $uname[$f['poster']],
		'topic_first_poster_colour' => $colour[$f['poster']],
		'topic_last_post_id' => $f['last_post_id'], 'topic_last_poster_id' => $f['last_poster'],
		'topic_last_poster_name' => $uname[$f['last_poster']], 'topic_last_poster_colour' => $colour[$f['last_poster']],
		'topic_last_post_subject' => e(($f['replies'] ? 'Re: ' : '') . $f['title']),
		'topic_last_post_time' => $f['last_time'], 'topic_last_view_time' => $f['last_time'],
		'poll_title' => '',
	)));
}

// Forum statistics: the board's real totals, last post from the newest topic in each forum.
$total_posts = $total_topics = 0;
foreach ($data['forums'] as $f)
{
	if ($f['parent'] == 0)
	{
		continue;
	}
	$result = q('SELECT topic_last_post_id, topic_last_poster_id, topic_last_poster_name, topic_last_poster_colour, topic_last_post_subject, topic_last_post_time
		FROM ' . TOPICS_TABLE . " WHERE forum_id = {$f['id']} ORDER BY topic_last_post_time DESC");
	$row = $db->sql_fetchrow($result);
	$db->sql_freeresult($result);
	q('UPDATE ' . FORUMS_TABLE . ' SET ' . $db->sql_build_array('UPDATE', array(
		'forum_posts' => $f['posts'], 'forum_topics' => $f['topics'], 'forum_topics_real' => $f['topics'],
		'forum_last_post_id' => $row['topic_last_post_id'], 'forum_last_poster_id' => $row['topic_last_poster_id'],
		'forum_last_post_subject' => $row['topic_last_post_subject'], 'forum_last_post_time' => $row['topic_last_post_time'],
		'forum_last_poster_name' => $row['topic_last_poster_name'], 'forum_last_poster_colour' => $row['topic_last_poster_colour'],
	)) . " WHERE forum_id = {$f['id']}");
	$total_posts += $f['posts'];
	$total_topics += $f['topics'];
}
$result = q('SELECT COUNT(*) AS n FROM ' . POSTS_TABLE . ' WHERE forum_id = 0');
$total_posts += (int) $db->sql_fetchfield('n');
$total_topics += 1;   // the global announcement

$result = q('SELECT COUNT(*) AS n FROM ' . USERS_TABLE . ' WHERE user_type IN (' . USER_NORMAL . ', ' . USER_FOUNDER . ')');
set_config('num_users', (int) $db->sql_fetchfield('n'), true);
set_config('num_posts', $total_posts, true);
set_config('num_topics', $total_topics, true);
$result = q('SELECT user_id, username, user_colour FROM ' . USERS_TABLE . ' WHERE user_type = ' . USER_NORMAL . ' ORDER BY user_regdate DESC');
$row = $db->sql_fetchrow($result);
$db->sql_freeresult($result);
set_config('newest_user_id', $row['user_id'], true);
set_config('newest_username', $row['username'], true);
set_config('newest_user_colour', $row['user_colour'], true);

cache_moderators();
$auth->acl_clear_prefetch();
$cache->purge();
echo "seeded: {$config['num_users']} users, $total_topics topics, $total_posts posts\n";
