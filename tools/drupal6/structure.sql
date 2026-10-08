-- Open Computing History Project: Drupal 6.14 site structure (run after enabling
-- forum/search/contact, before drupal_ui.py content). Archive date 3 November 2009.

-- Site settings
REPLACE INTO variable (name, value) VALUES
 ('site_slogan', 's:51:"Documenting and preserving the history of computing";'),
 ('site_mission', 's:230:"The Open Computing History Project is an open-source research project at the Department of Computer Science. We collect, catalogue and publish primary sources on computing hardware, software, networks and the people who used them.";'),
 ('site_footer', 's:94:"Open Computing History Project, Department of Computer Science. Content licensed CC BY-SA 3.0.";'),
 ('site_mail', 's:19:"ochp@cs.example.edu";'),
 ('anonymous', 's:9:"Anonymous";'),
 ('user_register', 's:1:"1";'),
 ('error_level', 's:1:"0";'),  -- log PHP warnings instead of printing them (PHP 5.6 warns where 5.2 did not)
 ('cron_last', 'i:1257265800;'),
 ('install_time', 'i:1236617400;');
DELETE FROM cache;

-- Anonymous visitors can read comments, search and use the contact form
UPDATE permission SET perm = 'access comments, access content, access site-wide contact form, search content' WHERE rid = 1;
UPDATE permission SET perm = 'access comments, access content, access site-wide contact form, create forum topics, edit own forum topics, post comments, post comments without approval, search content' WHERE rid = 2;

-- Contact form category
DELETE FROM contact;
INSERT INTO contact (cid, category, recipients, reply, weight, selected) VALUES
 (1, 'General enquiries', 'ochp@cs.example.edu', '', 0, 1),
 (2, 'Donations', 'ochp-donations@cs.example.edu', '', 1, 0);

-- Topics vocabulary for stories (vid 1 is the forum module's Forums vocabulary)
DELETE FROM vocabulary WHERE vid = 2;
INSERT INTO vocabulary (vid, name, description, help, relations, hierarchy, multiple, required, tags, module, weight) VALUES
 (2, 'Topics', 'Subject areas covered by the project.', '', 1, 0, 1, 0, 0, 'taxonomy', 0);
DELETE FROM vocabulary_node_types WHERE vid = 2;
INSERT INTO vocabulary_node_types (vid, type) VALUES (2, 'story');

DELETE FROM term_data; DELETE FROM term_hierarchy;
INSERT INTO term_data (tid, vid, name, description, weight) VALUES
 (1, 2, 'Mainframes', 'Mainframe and minicomputer systems, timesharing, and the institutions that ran them.', 0),
 (2, 2, 'Early Microcomputers', 'Home and personal computers from the 1970s and 1980s.', 0),
 (3, 2, 'Networking History', 'ARPANET, bulletin board systems, FidoNet and other early networks.', 0),
 (4, 2, 'Software Preservation', 'Imaging, describing and running historical software.', 0),
 (5, 1, 'Announcements', 'Lab sessions, events and project news.', 0),
 (6, 1, 'Hardware lab', 'Restoration, repair and parts.', 1),
 (7, 1, 'Software and emulation', 'Media imaging, emulators and software archaeology.', 2);
INSERT INTO term_hierarchy (tid, parent) VALUES (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0);

-- Users (password hashes are random; nobody logs in as them)
UPDATE users SET created = 1236617400, access = 1257264000, login = 1257264000, mail = 'ochp-admin@cs.example.edu' WHERE uid = 1;
DELETE FROM users WHERE uid > 1; DELETE FROM users_roles WHERE uid > 1;
INSERT INTO users (uid, name, pass, mail, mode, sort, threshold, theme, signature, signature_format, created, access, login, status, timezone, language, picture, init, data) VALUES
 (2, 'modem_mike', MD5(RAND()), 'mike@example.net', 0, 0, 0, '', '', 0, 1237995000, 1257260000, 1257260000, 1, NULL, '', '', 'mike@example.net', 'a:0:{}'),
 (3, 'k.ostrander', MD5(RAND()), 'kostrander@example.edu', 0, 0, 0, '', '', 0, 1239802000, 1257262000, 1257262000, 1, NULL, '', '', 'kostrander@example.edu', 'a:0:{}'),
 (4, 'jhalvorsen', MD5(RAND()), 'jhalvorsen@cs.example.edu', 0, 0, 0, '', '', 0, 1238410000, 1257250000, 1257250000, 1, NULL, '', '', 'jhalvorsen@cs.example.edu', 'a:0:{}'),
 (5, 'rgattis', MD5(RAND()), 'rgattis@example.com', 0, 0, 0, '', '', 0, 1246035000, 1257240000, 1257240000, 1, NULL, '', '', 'rgattis@example.com', 'a:0:{}'),
 (6, 'pdunleavy', MD5(RAND()), 'pdunleavy@example.org', 0, 0, 0, '', '', 0, 1251205000, 1257100000, 1257100000, 1, NULL, '', '', 'pdunleavy@example.org', 'a:0:{}');
