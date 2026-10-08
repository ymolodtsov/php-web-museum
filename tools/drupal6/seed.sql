-- Open Computing History Project: back-date the nodes created by drupal_ui.py, tag
-- them, add comments and set up blocks. Times are US Eastern (UTC-5 in November).
-- Archive date: Tuesday 3 November 2009.

-- nid, author uid, created (unix time)
CREATE TEMPORARY TABLE seed_dates (nid INT PRIMARY KEY, uid INT, created INT);
INSERT INTO seed_dates VALUES
 (1, 1, UNIX_TIMESTAMP('2009-03-09 17:05:00')),  -- About the Project   Mon 03/09/2009 - 12:05
 (2, 1, UNIX_TIMESTAMP('2009-09-14 15:20:00')),  -- ARPANET host tables Mon 09/14/2009 - 10:20
 (3, 1, UNIX_TIMESTAMP('2009-09-30 13:40:00')),  -- magazine donation   Wed 09/30/2009 - 08:40
 (4, 1, UNIX_TIMESTAMP('2009-10-12 15:05:00')),  -- keyboard notes      Mon 10/12/2009 - 10:05
 (5, 1, UNIX_TIMESTAMP('2009-10-22 18:50:00')),  -- benchmarking        Thu 10/22/2009 - 13:50
 (6, 1, UNIX_TIMESTAMP('2009-10-26 16:30:00')),  -- core memory         Mon 10/26/2009 - 11:30
 (7, 1, UNIX_TIMESTAMP('2009-10-28 21:05:00')),  -- rate card           Wed 10/28/2009 - 16:05
 (8, 1, UNIX_TIMESTAMP('2009-10-31 14:47:00')),  -- PDP-11/70 panel     Sat 10/31/2009 - 09:47
 (9, 1, UNIX_TIMESTAMP('2009-11-03 19:22:00')),  -- BBS oral history    Tue 11/03/2009 - 14:22
 (10, 1, UNIX_TIMESTAMP('2009-10-27 21:30:00')), -- forum: lab sessions
 (11, 4, UNIX_TIMESTAMP('2009-10-30 00:41:00')), -- forum: RL02 belt
 (12, 6, UNIX_TIMESTAMP('2009-11-01 18:02:00')); -- forum: paper tape emulators
-- The database session runs in UTC (museum-db default), so UNIX_TIMESTAMP above takes UTC wall times.

UPDATE node n JOIN seed_dates d USING (nid) SET n.uid = d.uid, n.created = d.created, n.changed = d.created;
UPDATE node_revisions r JOIN seed_dates d USING (nid) SET r.uid = d.uid, r.timestamp = d.created;

-- Topics
DELETE FROM term_node WHERE tid BETWEEN 1 AND 4;
INSERT INTO term_node (nid, vid, tid) VALUES
 (2, 2, 3),
 (3, 3, 2), (3, 3, 4),
 (4, 4, 2),
 (5, 5, 2), (5, 5, 4),
 (6, 6, 1),
 (7, 7, 1),
 (8, 8, 1),
 (9, 9, 2), (9, 9, 3);

-- Comments (status 0 = published, format 1 = Filtered HTML)
DELETE FROM comments;
INSERT INTO comments (cid, pid, nid, uid, subject, comment, hostname, timestamp, status, format, thread, name, mail, homepage) VALUES
 (1, 0, 2, 3, 'Host types', 'Very useful. Is the spreadsheet going to include the machine type column as well? Watching the PDP-10s give way to VAXen over those ten years would make a nice chart.', '10.1.4.22', UNIX_TIMESTAMP('2009-09-15 01:12:00'), 0, 1, '01/', 'k.ostrander', '', ''),
 (2, 0, 4, 6, 'Conductive paint', 'We had good results with a silver conductive pen on two cracked ribbon tails last year. It is not pretty but it has held up so far. Happy to write up what we did if it helps.', '10.1.7.140', UNIX_TIMESTAMP('2009-10-13 22:48:00'), 0, 1, '01/', 'pdunleavy', '', ''),
 (3, 0, 5, 2, 'Display on or off', 'The display point is a good one. A lot of the magazine reviews never said which way they ran the tests, so some of the old comparisons were never really fair.', '10.1.3.9', UNIX_TIMESTAMP('2009-10-22 23:15:00'), 0, 1, '01/', 'modem_mike', '', ''),
 (4, 0, 5, 3, 'Listings', 'Are the listings exactly as printed, or did you have to fix typos to get them running? It would be good to note which ones needed changes.', '10.1.4.22', UNIX_TIMESTAMP('2009-10-23 14:30:00'), 0, 1, '02/', 'k.ostrander', '', ''),
 (5, 0, 6, 5, 'Count me in', 'I can come to the next two sessions. I have a decent camera and a copy stand if that helps with the photography.', '10.1.9.51', UNIX_TIMESTAMP('2009-10-26 19:05:00'), 0, 1, '01/', 'rgattis', '', ''),
 (6, 0, 6, 6, 'Saturdays only', 'I can help on Saturdays. Weekdays are difficult for me this term.', '10.1.7.140', UNIX_TIMESTAMP('2009-10-27 14:12:00'), 0, 1, '02/', 'pdunleavy', '', ''),
 (7, 0, 10, 6, 'November 7', 'I will be there on the 7th.', '10.1.7.140', UNIX_TIMESTAMP('2009-10-28 13:20:00'), 0, 1, '01/', 'pdunleavy', '', ''),
 (8, 0, 11, 2, 'Belts', 'I have seen people use a flat belt from a sewing machine supply shop. Measure the old one flat and take it with you. No idea how well it holds up though.', '10.1.3.9', UNIX_TIMESTAMP('2009-10-30 13:10:00'), 0, 1, '01/', 'modem_mike', '', ''),
 (9, 0, 11, 5, 'Re: Belts', 'There is a man on one of the PDP-11 mailing lists who still sells new old stock. I will dig out his address and send it to you.', '10.1.9.51', UNIX_TIMESTAMP('2009-10-31 16:45:00'), 0, 1, '02/', 'rgattis', '', ''),
 (10, 0, 8, 4, 'Lamp part numbers', 'For anyone else doing this: we listed the lamp part numbers and the replacements we used in the photo notes. Check the voltage rating before you order a bag of them.', '10.1.2.77', UNIX_TIMESTAMP('2009-11-01 15:30:00'), 0, 1, '01/', 'jhalvorsen', '', ''),
 (11, 0, 12, 4, 'SIMH', 'SIMH works well for this. Load the image with the RIM loader first and then the BIN loader. If a tape will not load, try reading it again before assuming the tape itself is bad. We had a few bad reads from the old reader.', '10.1.2.77', UNIX_TIMESTAMP('2009-11-02 02:30:00'), 0, 1, '01/', 'jhalvorsen', '', ''),
 (12, 0, 9, 2, 'Great interview', 'This brought back a lot of memories. I called a very similar board in the Midwest around the same time, with the same door games and the same arguments about hardware. I would love to see more of these collected before the people who ran them are gone.', '10.1.3.9', UNIX_TIMESTAMP('2009-11-03 21:08:00'), 0, 1, '01/', 'modem_mike', '', ''),
 (13, 0, 9, 3, 'Echomail archives', 'Fascinating. Does the project have plans to digitize the FidoNet echomail archives mentioned in the interview? That would be a great resource.', '10.1.4.22', UNIX_TIMESTAMP('2009-11-04 00:41:00'), 0, 1, '02/', 'k.ostrander', '', ''),
 (14, 13, 9, 1, 'Re: Echomail archives', 'We have some of them on floppies that came with the interview material. They are in the imaging queue, but it will be a while before we get to them.', '10.1.1.5', UNIX_TIMESTAMP('2009-11-04 01:15:00'), 0, 1, '02.00/', 'admin', '', ''),
 (15, 0, 9, 5, 'Modems', 'Good read. A small note: the 1200 baud modems were more likely Hayes-compatible external units than internal cards, going by the timeline. Might be worth checking with the interviewee for the record.', '10.1.9.51', UNIX_TIMESTAMP('2009-11-04 02:02:00'), 0, 1, '03/', 'rgattis', '', '');

-- Comment statistics
UPDATE node_comment_statistics s JOIN node n USING (nid)
   SET s.comment_count = 0, s.last_comment_timestamp = n.created, s.last_comment_uid = n.uid, s.last_comment_name = NULL;
UPDATE node_comment_statistics s
  JOIN (SELECT nid, COUNT(*) c, MAX(timestamp) t FROM comments GROUP BY nid) c USING (nid)
  JOIN comments last ON last.nid = s.nid AND last.timestamp = c.t
   SET s.comment_count = c.c, s.last_comment_timestamp = c.t, s.last_comment_uid = last.uid, s.last_comment_name = last.name;

-- Blocks for Garland (its own search box sits above them): navigation and login on the left; recent comments
-- and active forum topics on the right; "Powered by Drupal" in the footer.
DELETE FROM blocks WHERE theme = 'garland';
INSERT INTO blocks (module, delta, theme, status, weight, region, custom, throttle, visibility, pages, title, cache) VALUES
 ('user', '1', 'garland', 1, -5, 'left', 0, 0, 0, '', '', -1),
 ('user', '0', 'garland', 1, 0, 'left', 0, 0, 0, '', '', -1),
 ('comment', '0', 'garland', 1, 0, 'right', 0, 0, 0, '', '', -1),
 ('forum', '0', 'garland', 1, 5, 'right', 0, 0, 0, '', '', -1),
 ('system', '0', 'garland', 1, 10, 'footer', 0, 0, 0, '', '', -1);

-- Clear caches and the install-time log so nothing from 2026 lingers
DELETE FROM cache; DELETE FROM cache_page; DELETE FROM cache_filter; DELETE FROM cache_menu; DELETE FROM cache_block;
DELETE FROM watchdog; DELETE FROM sessions; DELETE FROM history; DELETE FROM flood;
