-- Retrocomputing Wiki: things the XML import cannot carry (run after importDump.php
-- and rebuildrecentchanges.php, before initStats.php).

-- Main Page protected by the founder the day after the install
DELETE FROM page_restrictions;
DELETE FROM logging WHERE log_type = 'protect';
INSERT INTO page_restrictions (pr_page, pr_type, pr_level, pr_cascade, pr_expiry)
  SELECT page_id, 'edit', 'sysop', 0, 'infinity' FROM page WHERE page_namespace = 0 AND page_title = 'Main_Page';
INSERT INTO page_restrictions (pr_page, pr_type, pr_level, pr_cascade, pr_expiry)
  SELECT page_id, 'move', 'sysop', 0, 'infinity' FROM page WHERE page_namespace = 0 AND page_title = 'Main_Page';
INSERT INTO logging (log_type, log_action, log_timestamp, log_user, log_namespace, log_title, log_comment, log_params)
  VALUES ('protect', 'protect', '20070304190540', 2, 0, 'Main_Page', 'main page [edit=sysop:move=sysop]', '');

-- Page view counters (shown as "This page has been accessed N times.")
UPDATE page SET page_counter = CASE page_title
  WHEN 'Main_Page' THEN 4211
  WHEN 'Commodore_64' THEN 1388
  WHEN 'ZX_Spectrum' THEN 702
  WHEN 'Amiga_500' THEN 655
  WHEN 'Apple_II' THEN 574
  WHEN 'Altair_8800' THEN 491
  WHEN 'BBC_Micro' THEN 463
  WHEN 'IBM_Personal_Computer' THEN 318
  WHEN 'VIC-20' THEN 297
  WHEN 'TRS-80' THEN 251
  WHEN 'MOS_Technology_6502' THEN 244
  WHEN 'Community_Portal' THEN 186
  WHEN 'About' THEN 97
  WHEN '8-bit_computers' THEN 133
  ELSE 20 + (page_id * 7) % 40 END;

-- Recent changes: mark page creations as new and fill in the byte counts
UPDATE recentchanges rc JOIN revision r ON r.rev_id = rc.rc_this_oldid SET rc.rc_new_len = r.rev_len;
UPDATE recentchanges rc JOIN revision r ON r.rev_id = rc.rc_last_oldid SET rc.rc_old_len = r.rev_len;
UPDATE recentchanges rc JOIN (SELECT rev_page, MIN(rev_id) AS first FROM revision GROUP BY rev_page) f
  ON rc.rc_this_oldid = f.first SET rc.rc_new = 1, rc.rc_type = 1, rc.rc_last_oldid = 0, rc.rc_old_len = 0;
UPDATE recentchanges SET rc_new = 0, rc_type = 0 WHERE rc_last_oldid <> 0;
UPDATE recentchanges SET rc_ip = rc_user_text WHERE rc_user = 0;
UPDATE recentchanges SET rc_patrolled = 1;

-- Invalidate parser cache so every page renders with the final templates
DELETE FROM objectcache;
UPDATE page SET page_touched = '20070911184000';
