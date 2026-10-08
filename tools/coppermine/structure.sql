-- Wanderlens Travel Gallery: categories and albums (Coppermine 1.3.3 tables)
UPDATE cpg133_config SET value='Wanderlens Travel Gallery' WHERE name='gallery_name';
UPDATE cpg133_config SET value='photographs from wherever the cheap flights go' WHERE name='gallery_description';
UPDATE cpg133_config SET value='dan@wanderlens.co.uk' WHERE name='gallery_admin_email';
UPDATE cpg133_config SET value='1' WHERE name='read_exif_data';
UPDATE cpg133_config SET value='1' WHERE name='display_pic_info';
UPDATE cpg133_config SET value='1' WHERE name='subcat_level';
UPDATE cpg133_config SET value='http://www.wanderlens.co.uk/gallery/' WHERE name='ecards_more_pic_target';
UPDATE cpg133_usergroups SET can_post_comments=1 WHERE group_id=3;
UPDATE cpg133_users SET user_regdate='2004-09-02 20:11:42', user_lastvisit='2005-06-07 22:41:05', user_email='dan@wanderlens.co.uk' WHERE user_id=1;

DELETE FROM cpg133_categories WHERE cid > 1;
INSERT INTO cpg133_categories (cid, owner_id, name, description, pos, parent, thumb) VALUES
 (2, 0, 'Asia', 'Thailand, Laos, Cambodia, Vietnam and a long weekend in Tokyo', 1, 0, 0),
 (3, 0, 'Europe', 'Walking in the Alps and a week on the Portuguese coast', 2, 0, 0),
 (4, 0, 'North Africa & the Americas', 'Morocco over New Year and a road trip through New England', 3, 0, 0);

DELETE FROM cpg133_albums;
INSERT INTO cpg133_albums (aid, title, description, visibility, uploads, comments, votes, pos, category, keyword) VALUES
 (1, 'Southeast Asia - Spring 2005', 'Three and a half weeks from Bangkok to Halong Bay, mostly by bus, slow boat and the occasional terrifying minivan.', 0, 'NO', 'YES', 'YES', 1, 2, ''),
 (2, 'City Lights: Tokyo at Night', 'Four nights in Tokyo on the way back from a work trip, with a borrowed Nikon D70 and tripod.', 0, 'NO', 'YES', 'YES', 2, 2, ''),
 (3, 'Alpine Hiking Trip', 'A week of day hikes out of Zermatt, then over to Austria for the last few days. August 2004.', 0, 'NO', 'YES', 'YES', 3, 3, ''),
 (4, 'Coastal Portugal', 'Porto, Lisbon and Sintra, then down to the Algarve in February. Cold water, empty beaches.', 0, 'NO', 'YES', 'YES', 4, 3, ''),
 (5, 'Moroccan Markets', 'Marrakech, Chefchaouen and Fes over Christmas and New Year. Bargained badly, ate very well.', 0, 'NO', 'YES', 'YES', 5, 4, ''),
 (6, 'New England Autumn', 'Leaf-peeping road trip through Vermont, New Hampshire and Maine, October 2004.', 0, 'NO', 'YES', 'YES', 6, 4, '');
