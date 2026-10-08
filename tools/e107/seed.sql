-- Clan Obsidian: e107 v0.617 seed content (archive date Sunday 30 January 2005)
-- Loaded after the stock installer has run. Text is stored the way e107 stores it
-- (apostrophes and double quotes as entities, see the normalisation pass at the end).
SET time_zone = '+00:00';

-- ---------------------------------------------------------------- users
UPDATE e107_user SET user_customtitle = 'Clan Leader', user_email = 'revenant@clanobsidian.net',
  user_homepage = 'http://www.clanobsidian.net', user_msn = 'revenant_obs@hotmail.com', user_location = 'Columbus, OH',
  user_birthday = '1981-06-12', user_signature = '[OBS]Revenant - if it ain''t broke, I haven''t played on it yet',
  user_join = UNIX_TIMESTAMP('2002-03-14 20:11:00'), user_lastvisit = UNIX_TIMESTAMP('2005-01-30 18:52:00'),
  user_currentvisit = UNIX_TIMESTAMP('2005-01-30 21:20:00'), user_ip = '24.95.112.40', user_visits = 1412,
  user_pwchange = UNIX_TIMESTAMP('2004-09-19 11:30:00'), user_class = '1.'
WHERE user_id = 1;

INSERT INTO e107_user (user_id, user_name, user_customtitle, user_password, user_email, user_homepage, user_icq, user_aim, user_msn,
  user_location, user_birthday, user_signature, user_image, user_hideemail, user_join, user_lastvisit, user_currentvisit,
  user_ip, user_prefs, user_new, user_viewed, user_visits, user_admin, user_class, user_perms, user_realm) VALUES
 (2, 'ShadowFang', 'Co-Leader', MD5('x-shadowfang'), 'shadowfang@clanobsidian.net', '', '', 'ShadowFangOBS', '', 'Dayton, OH', '1983-02-03',
  'Halo 2 LAN Feb 5th - bring a controller', '', 1, UNIX_TIMESTAMP('2002-06-02 17:40:00'), UNIX_TIMESTAMP('2005-01-29 23:10:00'), UNIX_TIMESTAMP('2005-01-30 16:05:00'),
  '68.40.17.201', '', '', '', 988, 0, '1.', '', ''),
 (3, 'Kryton', 'Officer - Server Admin', MD5('x-kryton'), 'kryton@clanobsidian.net', '', '183049921', '', 'kryton_cs@hotmail.com', 'Pittsburgh, PA', '1979-10-27',
  'Server: 66.150.164.12:27015 | Vent: vent.clanobsidian.net:3784', '', 1, UNIX_TIMESTAMP('2002-11-19 21:02:00'), UNIX_TIMESTAMP('2005-01-30 12:44:00'), UNIX_TIMESTAMP('2005-01-30 20:58:00'),
  '71.192.4.88', '', '', '', 1203, 0, '1.', '', ''),
 (4, 'NullPointer', 'Officer - Forum Admin', MD5('x-nullpointer'), 'nullpointer@clanobsidian.net', 'http://www.geocities.com/nullptr_obs/', '', 'nullptr42', '', 'Toronto, ON', '1984-08-08',
  'Segmentation fault (core dumped)', '', 1, UNIX_TIMESTAMP('2003-01-05 14:15:00'), UNIX_TIMESTAMP('2005-01-29 20:30:00'), UNIX_TIMESTAMP('2005-01-30 11:12:00'),
  '65.92.200.14', '', '', '', 840, 0, '1.', '', ''),
 (5, 'Vortex_', 'Member', MD5('x-vortex'), 'vortex_cs@hotmail.com', '', '', '', 'vortex_cs@hotmail.com', 'Louisville, KY', '1987-04-30',
  'AWP or go home', '', 1, UNIX_TIMESTAMP('2003-07-22 19:33:00'), UNIX_TIMESTAMP('2005-01-30 17:41:00'), UNIX_TIMESTAMP('2005-01-30 21:02:00'),
  '74.128.33.9', '', '', '', 1120, 0, '1.', '', ''),
 (6, 'Hollowpoint', 'Member', MD5('x-hollowpoint'), 'hollowpoint@earthlink.net', '', '', 'hollowpt77', '', 'Indianapolis, IN', '1977-12-02',
  '', '', 1, UNIX_TIMESTAMP('2004-02-11 22:08:00'), UNIX_TIMESTAMP('2005-01-30 09:15:00'), UNIX_TIMESTAMP('2005-01-30 19:47:00'),
  '24.13.77.120', '', '', '', 503, 0, '1.', '', ''),
 (8, 'Static_Wolf', 'Member', MD5('x-staticwolf'), 'static_wolf@yahoo.com', '', '', '', '', 'Cincinnati, OH', '1986-09-15',
  'WoW: Wolfstatic, 47 Night Elf Hunter (Mal''Ganis)', '', 1, UNIX_TIMESTAMP('2004-09-03 16:20:00'), UNIX_TIMESTAMP('2005-01-29 01:12:00'), UNIX_TIMESTAMP('2005-01-30 13:30:00'),
  '69.133.8.51', '', '', '', 344, 0, '1.', '', ''),
 (10, 'Recruit_Dex', 'Recruit (trial)', MD5('x-dex'), 'dexter.h@comcast.net', '', '', 'dexplays', '', 'Ann Arbor, MI', '1988-01-19',
  '', '', 1, UNIX_TIMESTAMP('2005-01-20 18:44:00'), UNIX_TIMESTAMP('2005-01-29 21:00:00'), UNIX_TIMESTAMP('2005-01-30 15:21:00'),
  '68.41.140.2', '', '', '', 37, 0, '', '', ''),
 (11, 'm0nk3y', '', MD5('x-monkey'), 'm0nk3y_cs@hotmail.com', '', '', '', 'm0nk3y_cs@hotmail.com', 'Erie, PA', '0000-00-00',
  '', '', 1, UNIX_TIMESTAMP('2005-01-27 16:58:00'), UNIX_TIMESTAMP('2005-01-28 22:40:00'), UNIX_TIMESTAMP('2005-01-29 19:05:00'),
  '70.21.15.180', '', '', '', 6, 0, '', '', ''),
 (7, '[FURY]Blitz', '', MD5('x-blitz'), 'blitz@furyclan.org', 'http://www.furyclan.org', '', '', '', 'Chicago, IL', '0000-00-00',
  'www.furyclan.org - always recruiting', '', 1, UNIX_TIMESTAMP('2004-08-14 20:05:00'), UNIX_TIMESTAMP('2005-01-26 18:17:00'), UNIX_TIMESTAMP('2005-01-29 23:50:00'),
  '67.167.92.30', '', '', '', 41, 0, '', '', ''),
 (9, 'TomH', '', MD5('x-tomh'), 'tomh2000@aol.com', '', '', 'TomH2000', '', 'Columbus, OH', '0000-00-00',
  '', '', 1, UNIX_TIMESTAMP('2004-11-17 08:12:00'), UNIX_TIMESTAMP('2004-12-28 14:02:00'), UNIX_TIMESTAMP('2005-01-11 10:30:00'),
  '152.163.100.6', '', '', '', 12, 0, '', '', '');

INSERT INTO e107_userclass_classes (userclass_id, userclass_name, userclass_description, userclass_editclass) VALUES
 (1, 'Clan Members', 'Full members of [OBS]', 0);

-- ---------------------------------------------------------------- site links (Admin > Links)
DELETE FROM e107_links;
INSERT INTO e107_links (link_id, link_name, link_url, link_description, link_button, link_category, link_order, link_refer, link_open, link_class) VALUES
 (1, 'Home', 'index.php', '', '', 1, 1, 0, 0, 0),
 (2, 'Forum', 'forum.php', '', '', 1, 2, 0, 0, 0),
 (3, 'Roster', 'content.php?content.1', '', '', 1, 3, 0, 0, 0),
 (4, 'Downloads', 'download.php', '', '', 1, 4, 0, 0, 0),
 (5, 'Members', 'user.php', '', '', 1, 5, 0, 0, 0),
 (6, 'Links', 'links.php', '', '', 1, 6, 0, 0, 0),
 (7, 'Submit News', 'submitnews.php', '', '', 1, 7, 0, 0, 0),
 (8, 'Site Map', 'sitemap.php', '', '', 1, 8, 0, 0, 0),
 (20, 'e107.org', 'http://e107.org', 'Home of the e107 website script', 'e107_images/button.png', 2, 0, 0, 0, 0),
 (21, 'Steam', 'http://www.steampowered.com', 'Valve''s content delivery system. Updates, news and server browser.', '', 3, 1, 14, 1, 0),
 (22, 'Cyberathlete Amateur League', 'http://www.caleague.com', 'CAL - where we play our league matches. CS 1.6 Main division.', '', 3, 2, 22, 1, 0),
 (23, 'GotFrag', 'http://www.gotfrag.com', 'Pro Counter-Strike news, demos and match coverage.', '', 3, 3, 9, 1, 0),
 (24, 'Steam Powered Forums', 'http://forums.steampowered.com', 'Official forums, for when Steam is down again.', '', 3, 4, 5, 1, 0),
 (25, 'Ventrilo', 'http://www.ventrilo.com', 'Get the client here. Our server info is in the forum.', '', 3, 5, 17, 1, 0),
 (26, '[FURY] Clan', 'http://www.furyclan.org', 'Our regular scrim partners out of Chicago.', '', 4, 1, 6, 1, 0),
 (27, 'Midwest LAN Coalition', 'http://www.midwestlan.net', 'Bring-your-own-computer LAN parties around Ohio and Indiana.', '', 4, 2, 3, 1, 0);
INSERT INTO e107_link_category (link_category_id, link_category_name, link_category_description, link_category_icon) VALUES
 (3, 'Gaming', 'Sites we use every day', ''),
 (4, 'Friends', 'Clans and LAN groups we play with', '');

-- ---------------------------------------------------------------- roster page (Admin > Content > custom page)
INSERT INTO e107_content (content_id, content_heading, content_subheading, content_content, content_parent, content_datestamp, content_author, content_comment, content_summary, content_type, content_review_score, content_pe_icon, content_class) VALUES
 (1, 'Clan Obsidian Roster', 'Who we are and who to bug', '[b]Leaders[/b]
Revenant - Clan Leader, founder (March 2002)
ShadowFang - Co-Leader, match scheduling

[b]Officers[/b]
Kryton - Server Admin, CS 1.6 and Source servers, Ventrilo
NullPointer - Forum Admin, recruitment

[b]Members[/b]
Vortex_ - since July 2003
Hollowpoint - since February 2004
Static_Wolf - since September 2004

[b]On trial[/b]
Recruit_Dex - since January 2005

Interested in joining? Post an application in the Recruitment forum and play on the public server for a couple of weeks so we know who you are. We run scrims most weekends and a CAL match every Wednesday night.', 1, UNIX_TIMESTAMP('2004-03-02 19:30:00'), '1', 0, '', 1, 0, 0, 0);

-- ---------------------------------------------------------------- news
-- news_allow_comments: 0 = comments open (e107 0.6 stores the 'disable comments' flag)
DELETE FROM e107_news; DELETE FROM e107_news_category;
INSERT INTO e107_news_category (category_id, category_name, category_icon) VALUES
 (1, 'Clan News', 'icon1.png'),
 (2, 'Matches', 'icon2.png'),
 (3, 'Gaming', 'icon3.png'),
 (4, 'Misc', 'icon5.png');

INSERT INTO e107_news (news_id, news_title, news_body, news_extended, news_datestamp, news_author, news_category, news_allow_comments, news_start, news_end, news_class, news_render_type) VALUES
 (1, 'Half-Life 2 is finally out', 'Steam unlocked Half-Life 2 a little after midnight and judging by Vent last night about half of you were up until 4am playing it. Steam itself has been falling over all day so if you are stuck on "connecting to Steam network" just keep trying.

Kryton is putting up a Counter-Strike: Source server alongside the 1.6 box. League matches stay on 1.6 for now.', '', UNIX_TIMESTAMP('2004-11-16 18:22:00'), 1, 3, 0, 0, 0, 0, 0),
 (2, 'Welcome Static_Wolf', 'Static_Wolf has finished his trial and is now a full member. He has been on the public server most nights since the summer and carried us through the second half against [eVo] last week, so it was an easy vote. Welcome aboard.', '', UNIX_TIMESTAMP('2004-10-02 21:05:00'), 4, 1, 0, 0, 0, 0, 0),
 (3, 'Merry Christmas from [OBS]', 'No scrims this week or next, CAL is on break until January 5th. The servers stay up the whole time so feel free to hop on if you get bored of the relatives.

Have a good one everybody.', '', UNIX_TIMESTAMP('2004-12-23 15:40:00'), 1, 1, 0, 0, 0, 0, 0),
 (4, 'New recruit: Recruit_Dex', 'Please welcome Recruit_Dex, who starts his trial period today. He is in the Michigan area and plays rifle mostly. Trial is the usual three weeks: show up to practice, play in at least one scrim and be nice on the server.

NullPointer has given him access to the recruits forum.', '', UNIX_TIMESTAMP('2005-01-20 20:15:00'), 4, 1, 0, 0, 0, 0, 0),
 (5, 'Halo 2 LAN night Saturday the 5th', 'Hosting a small LAN at my place Saturday evening, February 5th, for anyone with an Xbox and a copy of Halo 2. Bring your own controller and a TV if you have a spare one to lend. Should be room for six or seven consoles linked up if people show.

Reply on the forum thread so I know how many pizzas to order.', '', UNIX_TIMESTAMP('2005-01-24 19:48:00'), 2, 3, 0, 0, 0, 0, 0),
 (6, 'A few of us are hooked on World of Warcraft', 'Noticed half the roster has been quiet on Counter-Strike the last couple weeks. Turns out most of you have been off levelling in World of Warcraft instead. Nothing wrong with that, a few of us started an informal guild on Mal''Ganis (Horde side is full of 12 year olds, so we went Alliance).

Just don''t forget we''ve still got scrims booked, people.', '', UNIX_TIMESTAMP('2005-01-26 22:31:00'), 1, 3, 0, 0, 0, 0, 0),
 (7, 'This weekend''s scrim results', 'Played a best-of-three against [FURY] on de_dust2 and de_inferno Saturday afternoon and came out 2-1. Close second map, we were down 3 rounds at half before the eco strats started working. Good match overall, GG to their guys.

Demo is up in the downloads section if anyone wants to watch the clutch on map three.', '[b]de_dust2[/b] - OBS 16, FURY 9
[b]de_inferno[/b] - OBS 13, FURY 16
[b]de_dust2[/b] (decider) - OBS 16, FURY 14

Lineup: Kryton, Vortex_, Hollowpoint, Static_Wolf, ShadowFang. Recruit_Dex subbed in for the last six rounds of map two.

Inferno is still our weak map. We keep losing banana control on the T side and then there is nothing to do but rush B. Practice Wednesday will be all Inferno, no complaining.', UNIX_TIMESTAMP('2005-01-29 22:40:00'), 3, 2, 0, 0, 0, 0, 0),
 (8, 'Server move this Friday - expect downtime', 'We''re moving the game servers and the website to the new host this Friday night. Figure on a few hours of downtime starting around 9pm while DNS catches up. Sorry for the short notice, but the old box has been flaking out all week and we didn''t want to risk losing anything.', 'The current box has been dropping connections on and off for about two weeks now, and after a long chat with the hosting company we''ve decided it''s not worth waiting for them to sort out whatever''s wrong with it on their end.

Expect the Counter-Strike and Half-Life 2 servers to go down around 9pm and stay down for a few hours while the files copy over and DNS updates propagate. The forum will be read-only for roughly the same window, so if you need to post something urgent, do it before then. Everyone''s accounts, stats and forum history are being carried over, so there''s nothing you need to do on your end.

If things aren''t back up by Saturday morning, post in the General Discussion forum rather than emailing me directly. I''ll be checking that first. Thanks for bearing with us, the new host should be considerably more stable going forward.', UNIX_TIMESTAMP('2005-01-30 19:12:00'), 1, 1, 0, 0, 0, 0, 0);

-- ---------------------------------------------------------------- news comments (comment_type 0 = news)
INSERT INTO e107_comments (comment_id, comment_pid, comment_item_id, comment_subject, comment_author, comment_author_email, comment_datestamp, comment_comment, comment_blocked, comment_ip, comment_type) VALUES
 (1, 0, 8, 'Re: Server move this Friday - expect downtime', '5.Vortex_', '', UNIX_TIMESTAMP('2005-01-30 19:31:00'), 'About time, that server''s been lagging out every scrim for two weeks straight. Good riddance.', 0, '74.128.33.9', 0),
 (2, 0, 8, 'Re: Server move this Friday - expect downtime', '6.Hollowpoint', '', UNIX_TIMESTAMP('2005-01-30 19:47:00'), 'As long as it''s back up before Saturday I don''t care. Hope the stats carry over properly this time, last move we lost about a month of frag counts.', 0, '24.13.77.120', 0),
 (3, 0, 8, 'Re: Server move this Friday - expect downtime', '3.Kryton', '', UNIX_TIMESTAMP('2005-01-30 20:58:00'), 'Stats are just a MySQL dump this time, I''ll copy them over myself. New box is a P4 2.8 with a gig of RAM on a 10 megabit line, so both servers should be fine running at once.', 0, '71.192.4.88', 0),
 (4, 0, 8, 'Re: Server move this Friday - expect downtime', 'Darkfire', '', UNIX_TIMESTAMP('2005-01-30 21:14:00'), 'will the new IP be posted somewhere? I have the old one saved in my favorites', 0, '68.58.140.77', 0),
 (5, 0, 7, 'Re: This weekend''s scrim results', '7.[FURY]Blitz', '', UNIX_TIMESTAMP('2005-01-29 23:52:00'), 'gg guys. we want a rematch on nuke next month.', 0, '67.167.92.30', 0),
 (6, 0, 7, 'Re: This weekend''s scrim results', '5.Vortex_', '', UNIX_TIMESTAMP('2005-01-30 10:05:00'), 'That 1v3 on the last round was all luck and I''ll admit it. Still counts though.', 0, '74.128.33.9', 0),
 (7, 0, 6, 'Re: A few of us are hooked on World of Warcraft', '8.Static_Wolf', '', UNIX_TIMESTAMP('2005-01-26 23:02:00'), 'In my defence the servers were down for half of last week so I did play CS. Some.', 0, '69.133.8.51', 0),
 (8, 0, 5, 'Re: Halo 2 LAN night Saturday the 5th', '6.Hollowpoint', '', UNIX_TIMESTAMP('2005-01-24 21:40:00'), 'I can bring my 27 inch and the system link cable.', 0, '24.13.77.120', 0);

-- ---------------------------------------------------------------- forums
DELETE FROM e107_forum; DELETE FROM e107_forum_t;
INSERT INTO e107_forum (forum_id, forum_name, forum_description, forum_parent, forum_datestamp, forum_moderators, forum_threads, forum_replies, forum_lastpost, forum_class, forum_order) VALUES
 (1, 'Clan Obsidian', '', 0, UNIX_TIMESTAMP('2004-03-02 19:00:00'), '', 0, 0, '', '0', 1),
 (2, 'Announcements', 'Server news and anything the leaders need everybody to read.', 1, UNIX_TIMESTAMP('2004-03-02 19:01:00'), 'Revenant, ShadowFang', 0, 0, '', '0', 2),
 (3, 'General Discussion', 'Clan business, scheduling, complaints.', 1, UNIX_TIMESTAMP('2004-03-02 19:02:00'), 'Revenant, NullPointer', 0, 0, '', '0', 3),
 (4, 'Recruitment', 'Want to join [OBS]? Read the sticky, then post your application here.', 1, UNIX_TIMESTAMP('2004-03-02 19:03:00'), 'NullPointer', 0, 0, '', '0', 4),
 (5, 'Games', '', 0, UNIX_TIMESTAMP('2004-03-02 19:04:00'), '', 0, 0, '', '0', 5),
 (6, 'Counter-Strike', '1.6 and Source. Strats, configs, scrims and demos.', 5, UNIX_TIMESTAMP('2004-03-02 19:05:00'), 'Kryton', 0, 0, '', '0', 6),
 (7, 'Half-Life 2', 'Single player, Deathmatch and mods.', 5, UNIX_TIMESTAMP('2004-11-16 18:30:00'), 'Kryton', 0, 0, '', '0', 7),
 (8, 'Other Games', 'WoW, Halo 2, whatever else is eating your time.', 5, UNIX_TIMESTAMP('2004-03-02 19:06:00'), 'NullPointer', 0, 0, '', '0', 8),
 (9, 'Off Topic', '', 0, UNIX_TIMESTAMP('2004-03-02 19:07:00'), '', 0, 0, '', '0', 9),
 (10, 'The Lounge', 'Anything goes, within reason.', 9, UNIX_TIMESTAMP('2004-03-02 19:08:00'), 'NullPointer', 0, 0, '', '0', 10),
 (11, 'Tech Help', 'Hardware, drivers, connection problems.', 9, UNIX_TIMESTAMP('2004-03-02 19:09:00'), 'Kryton', 0, 0, '', '0', 11);

-- thread_parent = 0 for the opening post; replies carry the opening post's id
-- thread_user = 'userid.username'; thread_active 1 = open; thread_s 1 = sticky
INSERT INTO e107_forum_t (thread_id, thread_name, thread_thread, thread_forum_id, thread_datestamp, thread_parent, thread_user, thread_views, thread_active, thread_lastpost, thread_s) VALUES
-- Announcements
 (1, 'Server move - any objections?', 'The hosting company still can''t tell us why the box keeps dropping connections, so I''m thinking we move everything (CS 1.6, Source, the website and Vent) to a new host next Friday the 4th, starting around 9pm.

Kryton found a place with a P4 2.8 and a 10 megabit line for about the same money we pay now. If anybody has a reason we shouldn''t do it that weekend, speak up now.', 2, UNIX_TIMESTAMP('2005-01-28 21:05:00'), 0, '1.Revenant', 87, 1, UNIX_TIMESTAMP('2005-01-30 20:41:00'), 0),
 (2, '', 'Fine by me. I''ll take a backup of the stats database and the server configs on Thursday night so we have something to roll back to.', 2, UNIX_TIMESTAMP('2005-01-28 21:30:00'), 1, '3.Kryton', 0, 1, 0, 0),
 (3, '', 'We have a scrim booked Saturday at 3. As long as the server is back by then I don''t care what you do to it.', 2, UNIX_TIMESTAMP('2005-01-28 22:12:00'), 1, '5.Vortex_', 0, 1, 0, 0),
 (4, '', 'If DNS is slow we can always post the new IP in here and on the front page. People can connect by IP until it catches up.', 2, UNIX_TIMESTAMP('2005-01-29 11:20:00'), 1, '4.NullPointer', 0, 1, 0, 0),
 (5, '', 'Ok, sounds like nobody minds. I''ll put it on the front page tonight. Kryton, can you sort out the Vent server too?', 2, UNIX_TIMESTAMP('2005-01-30 18:58:00'), 1, '1.Revenant', 0, 1, 0, 0),
 (6, '', 'Yep, Vent moves with everything else. Same password. Port stays 3784.', 2, UNIX_TIMESTAMP('2005-01-30 20:41:00'), 1, '3.Kryton', 0, 1, 0, 0),
-- General Discussion
 (7, 'Ventrilo server info', 'Server: vent.clanobsidian.net
Port: 3784
Password: ask in Vent or PM me, it is not going on a public forum.

Please set up push-to-talk. Nobody wants to hear your mom yelling about dinner during a scrim.', 3, UNIX_TIMESTAMP('2004-10-10 15:30:00'), 0, '3.Kryton', 412, 1, UNIX_TIMESTAMP('2004-10-10 15:30:00'), 1),
 (8, 'Wednesday practice times', 'Since CAL moved our match night, practice is now Wednesday 8pm Eastern on the private server. If you can''t make it let ShadowFang know before 6.', 3, UNIX_TIMESTAMP('2005-01-06 19:15:00'), 0, '2.ShadowFang', 64, 1, UNIX_TIMESTAMP('2005-01-07 08:40:00'), 0),
 (9, '', 'Works for me. 8 Eastern is 7 for me so I can actually eat first.', 3, UNIX_TIMESTAMP('2005-01-07 08:40:00'), 8, '6.Hollowpoint', 0, 1, 0, 0),
-- Recruitment
 (10, 'How to apply - read this first', 'Post a new thread with:

- In-game name and Steam ID
- Age and location
- Which games you play and how long
- Previous clans, if any, and why you left
- When you can usually play

Then spend some time on the public server so we get to know you. Trial period is three weeks. Don''t PM the leaders asking for a decision, we will reply in your thread.', 4, UNIX_TIMESTAMP('2004-03-02 20:00:00'), 0, '4.NullPointer', 530, 1, UNIX_TIMESTAMP('2004-03-02 20:00:00'), 1),
 (11, 'Application - m0nk3y', 'Name: m0nk3y
Steam ID: STEAM_0:1:4410273
Age: 17, Erie PA
Playing CS since beta 6.5, mostly rifle, can AWP if I have to
Was in [k9] until they broke up in December
Can play most nights after 7 and weekends

I''m on your public server a lot, usually on dust2 and office.', 4, UNIX_TIMESTAMP('2005-01-27 17:10:00'), 0, '11.m0nk3y', 58, 1, UNIX_TIMESTAMP('2005-01-28 22:15:00'), 0),
 (12, '', 'Thanks for applying. You''ve been seen on the server and nobody has complained, which is a good start. Come to practice on Wednesday and we''ll go from there.', 4, UNIX_TIMESTAMP('2005-01-28 22:15:00'), 11, '4.NullPointer', 0, 1, 0, 0),
-- Counter-Strike
 (13, 'LF scrim partners this weekend', 'We have Saturday afternoon free. 5v5, CS 1.6, our server or yours. de_dust2, de_inferno, de_nuke or de_train. Anybody?', 6, UNIX_TIMESTAMP('2005-01-25 20:20:00'), 0, '3.Kryton', 104, 1, UNIX_TIMESTAMP('2005-01-30 11:02:00'), 0),
 (14, '', '[FURY] is up for it. 3pm Eastern, best of three, dust2 and inferno and the decider is dust2 again if it comes to that. Your server is fine.', 6, UNIX_TIMESTAMP('2005-01-25 23:05:00'), 13, '7.[FURY]Blitz', 0, 1, 0, 0),
 (15, '', 'Done. See you Saturday. Server info is in your PM.', 6, UNIX_TIMESTAMP('2005-01-26 07:50:00'), 13, '3.Kryton', 0, 1, 0, 0),
 (16, '', 'gg. Anybody free next Saturday as well? Server should be back up by then.', 6, UNIX_TIMESTAMP('2005-01-30 11:02:00'), 13, '5.Vortex_', 0, 1, 0, 0),
 (17, 'Source vs 1.6 for league?', 'CAL is running a Source ladder now. Do we want to put a team in or stay on 1.6 until the netcode gets fixed?', 6, UNIX_TIMESTAMP('2004-12-14 21:40:00'), 0, '2.ShadowFang', 156, 1, UNIX_TIMESTAMP('2004-12-15 19:22:00'), 0),
 (18, '', 'Stay on 1.6. Hitboxes in Source are still all over the place. Wait for a few more patches.', 6, UNIX_TIMESTAMP('2004-12-14 22:03:00'), 17, '5.Vortex_', 0, 1, 0, 0),
 (19, '', 'Agree with Vortex. Also half of us would need new video cards to get a decent framerate.', 6, UNIX_TIMESTAMP('2004-12-15 19:22:00'), 17, '6.Hollowpoint', 0, 1, 0, 0),
-- Half-Life 2
 (20, 'Ravenholm', 'Just got through Ravenholm. I am not ashamed to say I played that whole chapter with the lights on. The gravity gun and the saw blades never stop being funny though.', 7, UNIX_TIMESTAMP('2004-11-20 01:14:00'), 0, '6.Hollowpoint', 77, 1, UNIX_TIMESTAMP('2004-11-20 13:30:00'), 0),
 (21, '', 'Wait until you get to the coast. The buggy section goes on way too long but the antlion part after it makes up for it.', 7, UNIX_TIMESTAMP('2004-11-20 13:30:00'), 20, '4.NullPointer', 0, 1, 0, 0),
 (22, 'HL2 Deathmatch server?', 'Valve put out HL2 Deathmatch today for free if you have the Silver or Gold pack. Can we get a server up? Physics kills with toilets are the best thing ever.', 7, UNIX_TIMESTAMP('2004-12-01 17:45:00'), 0, '5.Vortex_', 92, 1, UNIX_TIMESTAMP('2004-12-02 09:10:00'), 0),
 (23, '', 'It''s up on port 27025, 16 slots, dm_lockdown and dm_overwatch. Might add more maps later.', 7, UNIX_TIMESTAMP('2004-12-02 09:10:00'), 22, '3.Kryton', 0, 1, 0, 0),
-- Other Games
 (24, 'Anyone else hooked on WoW now?', 'Rolled a Night Elf hunter on Mal''Ganis last week and I think I have slept about 20 hours total since. Who else is playing? We should get a guild together.', 8, UNIX_TIMESTAMP('2005-01-22 02:30:00'), 0, '8.Static_Wolf', 133, 1, UNIX_TIMESTAMP('2005-01-29 16:12:00'), 0),
 (25, '', 'I''m on Mal''Ganis too, a dwarf priest. Level 31. Send me a whisper, same name as here.', 8, UNIX_TIMESTAMP('2005-01-22 11:15:00'), 24, '1.Revenant', 0, 1, 0, 0),
 (26, '', 'Not paying 15 bucks a month to stand in line for a quest mob. I''ll stick with CS.', 8, UNIX_TIMESTAMP('2005-01-23 20:40:00'), 24, '5.Vortex_', 0, 1, 0, 0),
 (27, '', 'Picked it up Thursday. Vortex will cave within a month, mark my words.', 8, UNIX_TIMESTAMP('2005-01-29 16:12:00'), 24, '6.Hollowpoint', 0, 1, 0, 0),
 (28, 'Halo 2 LAN - who''s in?', 'Saturday Feb 5th at my place, starting around 6. I have two Xboxes and a hub. Need people to bring consoles, TVs and controllers. Post here if you''re coming so I can figure out food.', 8, UNIX_TIMESTAMP('2005-01-24 19:52:00'), 0, '2.ShadowFang', 71, 1, UNIX_TIMESTAMP('2005-01-29 20:37:00'), 0),
 (29, '', 'In. Bringing my Xbox and the 27 inch.', 8, UNIX_TIMESTAMP('2005-01-24 21:38:00'), 28, '6.Hollowpoint', 0, 1, 0, 0),
 (30, '', 'Can I come? I only have a controller but I can bring a second one.', 8, UNIX_TIMESTAMP('2005-01-27 18:02:00'), 28, '10.Recruit_Dex', 0, 1, 0, 0),
 (31, '', 'I''ll be there. Pepperoni please, no mushrooms.', 8, UNIX_TIMESTAMP('2005-01-29 20:37:00'), 28, '8.Static_Wolf', 0, 1, 0, 0),
-- The Lounge
 (32, 'What did you get for Christmas?', 'Got a 6800 GT, finally. Half-Life 2 at 1280x1024 with everything turned up. Also socks.', 10, UNIX_TIMESTAMP('2004-12-26 14:20:00'), 0, '8.Static_Wolf', 118, 1, UNIX_TIMESTAMP('2004-12-27 10:44:00'), 0),
 (33, '', 'An iPod. The 20 gig one. Already filled about half of it.', 10, UNIX_TIMESTAMP('2004-12-26 18:05:00'), 32, '4.NullPointer', 0, 1, 0, 0),
 (34, '', 'Halo 2 and a gift card for Best Buy that I already spent on a new headset.', 10, UNIX_TIMESTAMP('2004-12-27 10:44:00'), 32, '2.ShadowFang', 0, 1, 0, 0),
-- Tech Help
 (35, 'Steam says the servers are too busy', 'Bought HL2 on Steam last night and it has been "decrypting" for six hours and now says the servers are too busy. Anyone else?', 11, UNIX_TIMESTAMP('2004-11-16 20:15:00'), 0, '6.Hollowpoint', 96, 1, UNIX_TIMESTAMP('2004-11-16 21:02:00'), 0),
 (36, '', 'Everybody has that today. Leave it running overnight and it will usually go through by morning. Don''t delete the GCF files whatever you do.', 11, UNIX_TIMESTAMP('2004-11-16 21:02:00'), 35, '3.Kryton', 0, 1, 0, 0),
 (37, 'Choppy sound in Source with Audigy 2', 'Sound cuts in and out in CS:Source but 1.6 is fine. Creative drivers are the newest ones off their site. Any ideas?', 11, UNIX_TIMESTAMP('2005-01-18 22:50:00'), 0, '10.Recruit_Dex', 41, 1, UNIX_TIMESTAMP('2005-01-19 07:35:00'), 0),
 (38, '', 'Try snd_mixahead 0.1 in the console, and turn off hardware acceleration in dxdiag if that doesn''t help. Fixed it for me.', 11, UNIX_TIMESTAMP('2005-01-19 07:35:00'), 37, '4.NullPointer', 0, 1, 0, 0);

-- forum counters and "last post" columns, as forum_post.php maintains them
UPDATE e107_forum f SET
  forum_threads = (SELECT COUNT(*) FROM e107_forum_t t WHERE t.thread_forum_id = f.forum_id AND t.thread_parent = 0),
  forum_replies = (SELECT COUNT(*) FROM e107_forum_t t WHERE t.thread_forum_id = f.forum_id AND t.thread_parent <> 0)
WHERE forum_parent <> 0;
UPDATE e107_forum f SET forum_lastpost = (
  SELECT CONCAT(t.thread_user, '.', t.thread_datestamp) FROM e107_forum_t t
  WHERE t.thread_forum_id = f.forum_id ORDER BY t.thread_datestamp DESC LIMIT 1)
WHERE forum_parent <> 0;

-- ---------------------------------------------------------------- chatbox (newest last)
DELETE FROM e107_chatbox;
INSERT INTO e107_chatbox (cb_id, cb_nick, cb_message, cb_datestamp, cb_blocked, cb_ip) VALUES
 (1, '2.ShadowFang', 'Halo night is on, thread is in Other Games', UNIX_TIMESTAMP('2005-01-29 20:40:00'), 0, '68.40.17.201'),
 (2, '8.Static_Wolf', 'gg today guys', UNIX_TIMESTAMP('2005-01-29 21:12:00'), 0, '69.133.8.51'),
 (3, '7.[FURY]Blitz', 'gg OBS, rematch on nuke soon', UNIX_TIMESTAMP('2005-01-29 23:50:00'), 0, '67.167.92.30'),
 (4, '10.Recruit_Dex', 'anyone on vent?', UNIX_TIMESTAMP('2005-01-30 15:21:00'), 0, '68.41.140.2'),
 (5, '6.Hollowpoint', 'dex im on in 10', UNIX_TIMESTAMP('2005-01-30 15:29:00'), 0, '24.13.77.120'),
 (6, 'Darkfire', 'is the server down? cant connect', UNIX_TIMESTAMP('2005-01-30 17:02:00'), 0, '68.58.140.77'),
 (7, '3.Kryton', 'Darkfire: restarting it, give it 5 min', UNIX_TIMESTAMP('2005-01-30 17:06:00'), 0, '71.192.4.88'),
 (8, '1.Revenant', 'server move news is up, read it', UNIX_TIMESTAMP('2005-01-30 19:14:00'), 0, '24.95.112.40'),
 (9, '5.Vortex_', 'finally', UNIX_TIMESTAMP('2005-01-30 19:30:00'), 0, '74.128.33.9'),
 (10, '3.Kryton', 'pub is back up, 66.150.164.12:27015', UNIX_TIMESTAMP('2005-01-30 21:03:00'), 0, '71.192.4.88');

-- ---------------------------------------------------------------- poll (poll_active 1 = anyone can vote)
DELETE FROM e107_poll;
INSERT INTO e107_poll VALUES (1, UNIX_TIMESTAMP('2005-01-17 18:00:00'), 0, 1, 'Which map should we practice for the CAL playoffs?',
 'de_dust2', 'de_inferno', 'de_nuke', 'de_train', 'de_cbble', 'I&#39;m playing WoW, leave me alone', '', '', '', '',
 4, 7, 5, 2, 1, 3, 0, 0, 0, 0, '', 1, 1);

-- ---------------------------------------------------------------- downloads
DELETE FROM e107_download; DELETE FROM e107_download_category;
INSERT INTO e107_download_category (download_category_id, download_category_name, download_category_description, download_category_icon, download_category_parent, download_category_class) VALUES
 (1, 'Counter-Strike', 'Files for CS 1.6 and Source', 'icon1.png', 0, '0'),
 (2, 'Demos', 'HLTV and POV demos of our matches', 'icon2.png', 1, '0'),
 (3, 'Configs and Scripts', 'Clan config, buy binds, net settings', 'icon3.png', 1, '0'),
 (4, 'Maps', 'Custom maps that run on our server', 'icon4.png', 1, '0'),
 (5, 'Utilities', 'Voice chat and tools', 'icon5.png', 0, '0'),
 (6, 'Voice and Tools', 'Everything you need to get on Vent', 'icon5.png', 5, '0');
INSERT INTO e107_download (download_id, download_name, download_url, download_author, download_author_email, download_author_website, download_description, download_filesize, download_requested, download_category, download_active, download_datestamp, download_thumb, download_image, download_comment) VALUES
 (1, 'OBS vs FURY - de_dust2 decider (HLTV)', 'obs_vs_fury_dust2_0129.zip', 'Kryton', 'kryton@clanobsidian.net', '', 'HLTV demo of the third map against [FURY] on 29 January 2005. The 1v3 clutch is round 29. Record with CS 1.6, play back with viewdemo.', '14823190', 23, 2, 1, UNIX_TIMESTAMP('2005-01-30 12:40:00'), '', '', 1),
 (2, 'OBS vs eVo - de_train (HLTV)', 'obs_vs_evo_train_1124.zip', 'Kryton', 'kryton@clanobsidian.net', '', 'CAL match, week 7. We lost 11-16, watch it and learn from our mistakes on the T side.', '12207733', 31, 2, 1, UNIX_TIMESTAMP('2004-11-25 10:15:00'), '', '', 1),
 (3, 'Obsidian clan config pack', 'obs_cfg_v3.zip', 'NullPointer', 'nullpointer@clanobsidian.net', '', 'autoexec.cfg, buy binds, the jump-throw script and net settings for cable connections. Unzip into your cstrike folder. Read the readme before you overwrite your own config.', '8417', 112, 3, 1, UNIX_TIMESTAMP('2004-12-04 18:30:00'), '', '', 1),
 (4, 'Rate settings for DSL and cable', 'netsettings.txt', 'Kryton', 'kryton@clanobsidian.net', '', 'rate, cl_updaterate and cl_cmdrate values that work on our server. Text file, copy into your console.', '1210', 67, 3, 1, UNIX_TIMESTAMP('2004-10-20 21:00:00'), '', '', 0),
 (5, 'aim_ag_texture2', 'aim_ag_texture2.zip', 'unknown', '', '', 'The aim map we run on Friday fun nights. Goes in cstrike/maps.', '402113', 58, 4, 1, UNIX_TIMESTAMP('2004-07-09 20:45:00'), '', '', 0),
 (6, 'fy_iceworld', 'fy_iceworld.zip', 'unknown', '', '', 'Classic. Also for Friday fun nights.', '611090', 74, 4, 1, UNIX_TIMESTAMP('2004-07-09 20:47:00'), '', '', 0),
 (7, 'Ventrilo client 2.1.4 (Windows)', 'ventrilo-2.1.4-Windows-i386.exe', 'Flagship Industries', '', 'http://www.ventrilo.com', 'Ventrilo voice client. Server details are in the Ventrilo sticky in General Discussion.', '1573102', 89, 6, 1, UNIX_TIMESTAMP('2004-10-10 15:40:00'), '', '', 0);

-- ---------------------------------------------------------------- menus (Admin > Menus)
UPDATE e107_menus SET menu_location = 1, menu_order = 1 WHERE menu_name = 'login_menu';
UPDATE e107_menus SET menu_location = 1, menu_order = 2 WHERE menu_name = 'chatbox_menu';
UPDATE e107_menus SET menu_location = 1, menu_order = 3 WHERE menu_name = 'online_menu';
UPDATE e107_menus SET menu_location = 1, menu_order = 4 WHERE menu_name = 'sitebutton_menu';
UPDATE e107_menus SET menu_location = 1, menu_order = 5 WHERE menu_name = 'compliance_menu';
UPDATE e107_menus SET menu_location = 2, menu_order = 1 WHERE menu_name = 'newforumposts_menu';
UPDATE e107_menus SET menu_location = 2, menu_order = 2 WHERE menu_name = 'poll_menu';
UPDATE e107_menus SET menu_location = 2, menu_order = 3 WHERE menu_name = 'powered_by_menu';
UPDATE e107_menus SET menu_location = 2, menu_order = 4 WHERE menu_name = 'backend_menu';
UPDATE e107_menus SET menu_location = 0, menu_order = 0 WHERE menu_name IN ('clock_menu', 'articles_menu', 'review_menu', 'headlines_menu', 'counter_menu');

-- ---------------------------------------------------------------- who is online
-- online.php deletes rows older than 5 minutes on every request, so these rows carry a
-- timestamp far in the future. The timestamp itself is never displayed.
DELETE FROM e107_online;
INSERT INTO e107_online (online_timestamp, online_flag, online_user_id, online_ip, online_location, online_pagecount) VALUES
 (2145916800, 0, '1.Revenant', '24.95.112.40', 'http://127.0.0.1:8909/news.php', 4),
 (2145916800, 0, '3.Kryton', '71.192.4.88', 'http://127.0.0.1:8909/forum_viewtopic.php.1', 2),
 (2145916800, 0, '5.Vortex_', '74.128.33.9', 'http://127.0.0.1:8909/forum.php', 3),
 (2145916800, 0, '0', '68.58.140.77', 'http://127.0.0.1:8909/news.php', 2),
 (2145916800, 0, '0', '207.46.98.35', 'http://127.0.0.1:8909/user.php', 1),
 (2145916800, 0, '0', '66.249.65.12', 'http://127.0.0.1:8909/download.php', 1),
 (2145916800, 0, '0', '82.35.17.90', 'http://127.0.0.1:8909/forum.php', 1);

-- ---------------------------------------------------------------- per-user counters
UPDATE e107_user u SET
  user_forums = (SELECT COUNT(*) FROM e107_forum_t t WHERE t.thread_user = CONCAT(u.user_id, '.', u.user_name)),
  user_comments = (SELECT COUNT(*) FROM e107_comments c WHERE c.comment_author = CONCAT(u.user_id, '.', u.user_name)),
  user_chats = 40 + u.user_id * 7,
  user_lastpost = GREATEST(
    IFNULL((SELECT MAX(thread_datestamp) FROM e107_forum_t t WHERE t.thread_user = CONCAT(u.user_id, '.', u.user_name)), 0),
    IFNULL((SELECT MAX(cb_datestamp) FROM e107_chatbox c WHERE c.cb_nick = CONCAT(u.user_id, '.', u.user_name)), 0));

-- ---------------------------------------------------------------- banner stats and cache
UPDATE e107_banner SET banner_impressions = 18342, banner_clicks = 41;
DELETE FROM e107_cache;

-- ---------------------------------------------------------------- store text the way e107's formtpa() does
UPDATE e107_news SET news_title = REPLACE(news_title, '''', '&#39;'), news_body = REPLACE(REPLACE(news_body, '''', '&#39;'), '"', '&quot;'),
  news_extended = REPLACE(REPLACE(news_extended, '''', '&#39;'), '"', '&quot;');
UPDATE e107_comments SET comment_subject = REPLACE(comment_subject, '''', '&#39;'), comment_comment = REPLACE(REPLACE(comment_comment, '''', '&#39;'), '"', '&quot;');
UPDATE e107_forum_t SET thread_name = REPLACE(thread_name, '''', '&#39;'), thread_thread = REPLACE(REPLACE(thread_thread, '''', '&#39;'), '"', '&quot;');
UPDATE e107_chatbox SET cb_message = REPLACE(cb_message, '''', '&#39;');
UPDATE e107_content SET content_content = REPLACE(content_content, '''', '&#39;');
UPDATE e107_download SET download_description = REPLACE(download_description, '''', '&#39;');
UPDATE e107_links SET link_description = REPLACE(link_description, '''', '&#39;'), link_name = REPLACE(link_name, '''', '&#39;');
UPDATE e107_user SET user_signature = REPLACE(user_signature, '''', '&#39;');
