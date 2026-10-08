-- Riverside Linux User Group: Mambo 4.5.1a seed content (archive date Thursday 14 October 2004).
-- Applied after a clean install without sample data. The default template (rhuk_solarflare) and the
-- stock module positions are kept; only content, menus and the poll are the group's own.

-- People ---------------------------------------------------------------------------------------
UPDATE mos_users SET name = 'Dave Reyes', registerDate = '2004-02-29 16:20:00', lastvisitDate = '2004-10-13 21:52:00' WHERE id = 62;
UPDATE mos_core_acl_aro SET name = 'Dave Reyes' WHERE value = '62';
INSERT INTO mos_users (id, name, username, email, password, usertype, block, sendEmail, gid, registerDate, lastvisitDate, activation, params) VALUES
 (63, 'Maria Lindqvist', 'mlindqvist', 'maria@riversidelug.org', MD5(RAND()), 'Author', 0, 0, 19, '2004-03-06 11:02:00', '2004-10-14 08:57:00', '', ''),
 (64, 'Tom Becker', 'tbecker', 'tbecker@riversidelug.org', MD5(RAND()), 'Registered', 0, 0, 18, '2004-04-18 17:45:00', '2004-10-12 19:20:00', '', '');
INSERT INTO mos_core_acl_aro (aro_id, section_value, value, order_value, name, hidden) VALUES
 (11, 'users', '63', 0, 'Maria Lindqvist', 0), (12, 'users', '64', 0, 'Tom Becker', 0);
INSERT INTO mos_core_acl_groups_aro_map (group_id, section_value, aro_id) VALUES (19, '', 11), (18, '', 12);

-- Stock content a real group would have deleted ---------------------------------------------------
DELETE FROM mos_content;               -- Welcome to Mambo, the three sample newsflashes, Mambo License
DELETE FROM mos_content_frontpage;
DELETE FROM mos_weblinks;              -- link to mamboserver.com
DELETE FROM mos_categories WHERE id IN (1, 2);          -- 'Latest' (News) and 'Mambo' (web links)
DELETE FROM mos_menu WHERE id IN (6, 27, 33, 37, 38, 39); -- Administrator, Search, Mambo License, News Feeds, Wrapper, Blog
DELETE FROM mos_modules_menu WHERE menuid IN (27, 36);

-- Sections and categories ------------------------------------------------------------------------
INSERT INTO mos_sections (id, title, name, image, scope, image_position, description, published, ordering, access, count, params) VALUES
 (3, 'Meetings', 'Meetings', 'taking_notes.jpg', 'content', 'right', 'We meet on the third Saturday of every month at the Riverside Public Library. Meeting announcements, write-ups and install-fest notes are filed here.', 1, 3, 0, 2, ''),
 (4, 'FAQ', 'Frequently Asked Questions', 'pastarchives.jpg', 'content', 'left', 'Answers to the questions that come up at almost every meeting. If yours is not here, ask on the mailing list.', 1, 4, 0, 2, '');
UPDATE mos_sections SET count = 2 WHERE id = 1;

INSERT INTO mos_categories (id, parent_id, title, name, image, section, image_position, description, published, ordering, access, count, params) VALUES
 (7, 0, 'Group News', 'Group News', '', '1', 'left', 'News about the group, the web site and the mailing list.', 1, 1, 0, 0, ''),
 (8, 0, 'Linux & Free Software', 'Linux & Free Software', '', '1', 'left', 'New releases and things members have been trying out.', 1, 2, 0, 0, ''),
 (9, 0, 'Schedule', 'Meeting Schedule', '', '3', 'left', 'Where and when we meet, and what is coming up.', 1, 1, 0, 0, ''),
 (10, 0, 'Install-fests', 'Install-fests', '', '3', 'left', 'Notes from our quarterly install-fests.', 1, 2, 0, 0, ''),
 (11, 0, 'Getting Started', 'Getting Started', '', '4', 'left', 'First steps with Linux.', 1, 1, 0, 0, ''),
 (12, 0, 'Hardware & Networking', 'Hardware & Networking', '', '4', 'left', 'Drivers, home networks and burning CDs.', 1, 2, 0, 0, ''),
 (13, 0, 'Distributions', 'Linux Distributions', '', 'com_weblinks', 'left', 'Where to download the distributions our members use. If you do not have a fast connection, pick up a CD at the next meeting.', 1, 1, 0, 0, ''),
 (14, 0, 'Software', 'Free Software Downloads', '', 'com_weblinks', 'left', 'Free software that also runs on Windows. A good way to start switching before you switch.', 1, 2, 0, 0, ''),
 (15, 0, 'Help & Resources', 'Help & Resources', '', 'com_weblinks', 'left', 'Documentation, forums and other places to look for help.', 1, 3, 0, 0, '');
UPDATE mos_categories SET description = 'How to reach the Riverside Linux User Group.' WHERE id = 4;

-- Articles ---------------------------------------------------------------------------------------
INSERT INTO mos_content (id, title, title_alias, introtext, `fulltext`, state, sectionid, mask, catid, created, created_by, created_by_alias, modified, modified_by, publish_up, publish_down, images, urls, attribs, version, parentid, ordering, metakey, metadesc, access, hits) VALUES
(1, 'Notes from last week''s install-fest', 'Install-fest notes',
'Eleven members turned out to the library meeting room on Saturday the 11th for our quarterly install-fest, and by the end of the afternoon we''d gotten three laptops dual-booting, one desktop fully converted, and talked one fellow out of wiping his only Windows partition without a backup first.',
'<p>Most of the burned CDs in circulation were Fedora Core 2 and Mandrake 10.0, a few point releases newer than what most of us were running back in the spring. Partitioning was the main sticking point of the day. Two of the laptops had unusual disk geometries that confused the installer''s automatic resizing, and we ended up doing the partition table by hand for both of them. If you''re planning to dual-boot an older laptop, check the install notes for known issues with your particular model before you start, and always, always back up first.</p>\r\n<p>On the desktop side, the conversion went smoothly once we''d confirmed the network card was supported out of the box. The owner had been putting off the switch for months after hearing stories about driver trouble, but in the end the only real hiccup was getting the monitor''s native resolution detected correctly, which took a quick edit to XF86Config.</p>\r\n<p>Thanks to everyone who brought burned CDs, extra RAM sticks, and patience. A few members mentioned wanting a repeat session focused on wireless cards, so we''ll likely schedule a follow-up before the end of the year. Details will be posted here and brought up at the next regular meeting.</p>',
1, 3, 0, 10, '2004-09-18 21:12:00', 62, '', '2004-09-19 10:03:00', 62, '2004-09-18 21:12:00', '0000-00-00 00:00:00', '', '', '', 2, 0, 1, '', '', 0, 214),

(2, 'Why we''re trying OpenOffice.org 1.1 at the library kiosk', 'OpenOffice.org at the library',
'The Riverside Public Library has agreed to let us set up OpenOffice.org 1.1 on the two public-access kiosk machines for a three month trial, replacing the aging word processor currently installed. We''ll be collecting feedback from patrons at the front desk and reporting back at the October meeting.',
'<p>The kiosks are two Pentium III machines running Windows 98, so for now this is OpenOffice.org on Windows, not Linux. The library''s IT person was happy to try it because the licences for the old word processor ran out last year and nobody wants to pay for an upgrade on hardware that old.</p>\r\n<p>Maria and Tom did the install last Tuesday evening. We set the default save format to Microsoft Word, since most patrons are printing resumes or taking files home on a floppy, and we left a one-page cheat sheet by each machine explaining where Save As and Print Preview live.</p>\r\n<p>If you use the kiosks, tell the front desk what you think, good or bad. If the trial goes well the library may let us try a Linux install on one of them next year.</p>',
1, 1, 0, 7, '2004-09-10 19:40:00', 63, '', '0000-00-00 00:00:00', 0, '2004-09-10 19:40:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 1, '', '', 0, 167),

(3, 'Firefox Preview Release: worth a look', 'Firefox Preview Release',
'Mozilla''s Firefox Preview Release came out on Tuesday and has been making the rounds of the mailing list all week. It''s still pre-1.0 and rough around a few edges, but tabbed browsing and the built-in popup blocker have already won over a few of our Internet Explorer holdouts.',
'<p>The Preview Release is version 0.10 and runs on Linux, Windows and Mac OS X. On Linux it installs into your home directory from a tarball, so you don''t need root to try it, and it can import your bookmarks from Mozilla or Netscape the first time it starts.</p>\r\n<p>Things people on the list have liked so far: the Live Bookmarks feature for RSS feeds, the find bar that appears at the bottom of the window instead of a dialog box, and the fact that it starts noticeably faster than the full Mozilla suite. Things they haven''t: a few extensions written for 0.9 don''t work yet, and the Windows installer still asks a couple of confusing questions.</p>\r\n<p>A full 1.0 release is expected before the end of the year. We''ll have it on the CD table at the October meeting for anyone without broadband.</p>',
1, 1, 0, 8, '2004-09-16 08:25:00', 62, '', '0000-00-00 00:00:00', 0, '2004-09-16 08:25:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 1, '', '', 0, 298),

(4, 'SP2 rollout causing driver headaches for some members', 'XP SP2 problems',
'With Windows XP Service Pack 2 now going out through Automatic Updates, a couple of members have reported network card and firewall conflicts after installing it on older hardware. If you''re planning to upgrade, check your device vendor''s site for updated drivers first, and back up before you start.',
'<p>Yes, this is a Linux group, but most of us still have a Windows machine somewhere in the house, and the dual-boot boxes from the install-fests are affected too. The two problems we''ve heard about most:</p>\r\n<ul>\r\n<li>An older 3Com PCI network card that stopped working until the driver was updated.</li>\r\n<li>The new Windows Firewall blocking file sharing to a Samba server on the home network. Turning on the File and Printer Sharing exception in the firewall settings fixed it.</li>\r\n</ul>\r\n<p>If SP2 has broken something on your machine, bring it to the next meeting and we''ll take a look.</p>',
1, 1, 0, 7, '2004-08-28 14:03:00', 62, '', '0000-00-00 00:00:00', 0, '2004-08-28 14:03:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 188),

(5, 'New mailing list archive now online', 'Mailing list archive',
'The riverside-lug mailing list now has a searchable web archive going back to March 2001, when we moved the list off the old Majordomo server. Thanks to Tom for setting it up on his spare box.',
'<p>The archive is updated every hour. Messages from before March 2001 are on a CD-R somewhere and will be added if we find it. Email addresses in the archive are partly hidden to keep the spammers away.</p>\r\n<p>The list itself hasn''t changed: same address, same rules. Keep it friendly, no HTML mail please, and put [OT] in the subject line if it''s off topic.</p>',
1, 1, 0, 7, '2004-08-16 21:47:00', 62, '', '0000-00-00 00:00:00', 0, '2004-08-16 21:47:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 3, '', '', 0, 141),

(6, 'Knoppix 3.6 is on the CD table', 'Knoppix 3.6',
'Klaus Knopper released Knoppix 3.6 last week, and we''ve burned a stack of copies for the September meeting. If you''ve never tried Linux, this is the easiest way: boot from the CD, nothing gets installed on your hard drive.',
'<p>Version 3.6 comes with kernel 2.6.7 and KDE 3.2.3, and hardware detection is better than in 3.4. It found the sound and network cards on every machine we tried it on, including a two-year-old Dell laptop that Fedora had trouble with.</p>\r\n<p>The CD is also handy as a rescue disk. You can use it to copy files off a Windows machine that won''t boot, or to check a hard drive before you repartition it.</p>',
1, 1, 0, 8, '2004-08-24 20:15:00', 63, '', '0000-00-00 00:00:00', 0, '2004-08-24 20:15:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 236),

(7, 'Meeting schedule', 'Meeting schedule',
'The Riverside Linux User Group meets on the third Saturday of every month. Meetings are free and open to anyone interested in Linux or free software. No membership is required and beginners are welcome.',
'<table cellpadding="3" cellspacing="0" border="0">\r\n<tr><td valign="top"><b>When</b></td><td>Third Saturday of each month, 1:00 PM to 4:00 PM</td></tr>\r\n<tr><td valign="top"><b>Where</b></td><td>Riverside Public Library, Meeting Room B, 2nd Floor</td></tr>\r\n<tr><td valign="top"><b>Next meeting</b></td><td>Saturday, 16 October 2004</td></tr>\r\n<tr><td valign="top"><b>Format</b></td><td>Short presentation, open Q&amp;A, informal install help afterward</td></tr>\r\n<tr><td valign="top"><b>Contact</b></td><td>Dave Reyes, group coordinator, through the Contact Us page</td></tr>\r\n</table>\r\n<p>Bring a laptop if you want help installing or configuring anything. We usually have two or three members on hand with spare burned CDs and an Ethernet hub for the afternoon. The library does not provide wireless access in the meeting room, so plan accordingly.</p>\r\n<p>Upcoming topics include a wireless card compatibility session (see the install-fest write-up for background) and a talk on setting up a home file server with Samba.</p>',
1, 3, 0, 9, '2004-03-02 20:30:00', 62, '', '2004-09-20 19:55:00', 62, '2004-03-02 20:30:00', '0000-00-00 00:00:00', '', '', '', 6, 0, 1, '', '', 0, 402),

(8, 'October meeting: a home file server with Samba', 'October meeting',
'Our October meeting is on Saturday, 16 October, 1:00 to 4:00 PM in Meeting Room B at the library. Tom Becker will show how he turned an old Pentium II into a file and print server for his family''s three Windows PCs using Samba 3.',
'<p>Tom will cover installing Samba, sharing a folder and a printer, setting up user accounts so everyone gets their own home share, and making the Windows XP SP2 firewall play along. Bring questions about your own setup.</p>\r\n<p>As usual, the second half of the afternoon is open for install help. We''ll have Fedora Core 2, Mandrake 10.0 and Knoppix 3.6 CDs on the table.</p>',
1, 3, 0, 9, '2004-09-21 18:30:00', 62, '', '0000-00-00 00:00:00', 0, '2004-09-21 18:30:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 96),

(9, 'Spring install-fest wrap-up', 'Spring install-fest',
'Thanks to the fourteen people who came to the spring install-fest on April 17th. We installed Linux on six machines, set up two dual-boot systems, and got one very old ThinkPad running Debian with 64 MB of RAM.',
'<p>The library gave us both meeting rooms this time, which helped a lot. We''ll ask for the same arrangement in the fall.</p>\r\n<p>Lessons learned: label the CDs, bring a power strip for every table, and have a sign-up sheet at the door so people don''t wait an hour for help with a five-minute question.</p>',
1, 3, 0, 10, '2004-04-19 21:05:00', 62, '', '0000-00-00 00:00:00', 0, '2004-04-19 21:05:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 173),

(10, 'How do I set up a dual-boot XP/Linux system?', 'Dual-boot XP and Linux',
'This is the question we get most often. The short answer: defragment Windows, shrink the Windows partition, install Linux into the free space, and let the Linux installer set up the boot loader.',
'<p><b>1. Back up.</b> Resizing partitions is usually safe, but not always. Copy anything you care about to CD or another drive first.</p>\r\n<p><b>2. Defragment.</b> Run Disk Defragmenter in Windows so the data is packed at the start of the partition. If your drive is NTFS, run chkdsk as well.</p>\r\n<p><b>3. Make room.</b> Mandrake 10.0 and Fedora Core 2 can both shrink a Windows partition during the install. PartitionMagic or qtparted on a Knoppix CD also work. Leave at least 5 GB for Linux.</p>\r\n<p><b>4. Install Linux.</b> Create a swap partition (twice your RAM is fine) and a root partition in the free space. Let the installer put GRUB in the master boot record.</p>\r\n<p><b>5. Reboot.</b> You should see a menu offering Linux and Windows. If Windows is missing, ask on the mailing list. It''s usually a one-line fix in /boot/grub/grub.conf.</p>',
1, 4, 0, 11, '2004-03-08 22:10:00', 62, '', '2004-06-02 19:30:00', 62, '2004-03-08 22:10:00', '0000-00-00 00:00:00', '', '', '', 3, 0, 1, '', '', 0, 1842),

(11, 'Which distribution should I start with?', 'Which distribution',
'There is no single right answer, but most members recommend Mandrake or Fedora Core for a first install. Both have graphical installers, detect most hardware and come with everything you need on a few CDs.',
'<p>If you just want to look around without installing anything, start with a Knoppix CD. If you have an old machine with little memory, try Debian or Slackware with a light window manager. SUSE is popular too, and the Personal edition is a free download.</p>\r\n<p>Whatever you pick, pick the one your friends use. Help from someone who runs the same thing is worth more than any feature list.</p>',
1, 4, 0, 11, '2004-03-08 22:40:00', 62, '', '0000-00-00 00:00:00', 0, '2004-03-08 22:40:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 642),

(12, 'Setting up Samba for a home network', 'Samba at home',
'Samba lets a Linux machine share files and printers with Windows PCs. For a small home network you only need a few lines in /etc/samba/smb.conf.',
'<p>Set the workgroup to match your Windows machines (usually WORKGROUP or MSHOME), add a share for a folder, and give each user a Samba password with smbpasswd -a. Restart Samba and the share should appear in My Network Places.</p>\r\n<p>If Windows XP can''t see the server after Service Pack 2, check that File and Printer Sharing is allowed in the Windows Firewall. Tom''s talk at the October meeting will go through the whole setup.</p>',
1, 4, 0, 12, '2004-04-02 21:00:00', 64, '', '2004-08-29 11:20:00', 64, '2004-04-02 21:00:00', '0000-00-00 00:00:00', '', '', '', 2, 0, 1, '', '', 0, 1203),

(13, 'Burning ISOs with K3b', 'Burning ISOs with K3b',
'Downloaded an ISO image and not sure what to do with it? Don''t copy the file onto a CD. It has to be burned as an image. On Linux, K3b makes this easy.',
'<p>Open K3b, choose Tools, then Burn CD Image, and select the .iso file. Check the MD5 sum that K3b shows against the one on the download site, then click Start. Burn at a lower speed if your drive is old; it saves a lot of coasters.</p>\r\n<p>On Windows, Nero and Easy CD Creator both have a "burn image" option. Look for it in the File or Recorder menu.</p>',
1, 4, 0, 12, '2004-05-11 20:20:00', 63, '', '0000-00-00 00:00:00', 0, '2004-05-11 20:20:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 781),

(14, 'Will my wireless card work under Linux?', 'Wireless cards',
'Maybe. Cards based on the Prism2 and Orinoco chipsets work out of the box with most distributions. Many newer 802.11g cards do not have Linux drivers yet.',
'<p>Before you buy, find out which chipset the card uses, not just the brand name. The same model number can ship with different chips. For cards with only Windows drivers, the NdisWrapper project can load the Windows driver under Linux. It works for a lot of people but takes some patience.</p>\r\n<p>We''re planning an install-fest session on wireless cards later this year. Bring yours.</p>',
1, 4, 0, 12, '2004-06-14 21:30:00', 62, '', '0000-00-00 00:00:00', 0, '2004-06-14 21:30:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 3, '', '', 0, 512),

(15, 'About the Riverside Linux User Group', 'About Us',
'<p>The Riverside Linux User Group started in the fall of 1998, when five people who had met on a Usenet newsgroup got together at a coffee shop to swap Red Hat 5.1 CDs. We''ve met every month since, first at the coffee shop, then at the community college, and since 2001 at the Riverside Public Library.</p>\r\n<p>We are an informal group. There are no dues and no officers apart from a coordinator who books the room and keeps this web site running. Our members include students, retirees, programmers, a few system administrators and a lot of people who just want their computer to work.</p>\r\n<p>What we do:</p>\r\n<ul>\r\n<li>A monthly meeting with a short talk and open Q&amp;A</li>\r\n<li>Install-fests four times a year</li>\r\n<li>A mailing list for help between meetings</li>\r\n<li>Free install CDs for anyone who asks</li>\r\n</ul>\r\n<p>This site moved to Mambo in March 2004. The old pages from 1999 to 2003 are gone, but the mailing list archive goes back to 2001.</p>',
'', 1, 0, 0, 0, '2004-03-01 21:00:00', 62, '', '2004-07-12 20:10:00', 62, '2004-03-01 21:00:00', '0000-00-00 00:00:00', '', '', '', 2, 0, 1, '', '', 0, 956);
INSERT INTO mos_content (id, title, title_alias, introtext, `fulltext`, state, sectionid, mask, catid, created, created_by, created_by_alias, modified, modified_by, publish_up, publish_down, images, urls, attribs, version, parentid, ordering, metakey, metadesc, access, hits) VALUES
(16, 'Library kiosk trial: three weeks in', 'Kiosk trial update',
'Three weeks into the OpenOffice.org trial on the library''s public kiosks, the front desk has collected 23 comment cards. Most are positive, a few are confused, and one patron wants to know why the paperclip is gone.',
'<p>The most common complaint is that documents saved on the kiosks open with slightly different spacing in Word at home. That''s a known issue with fonts, and we''ve asked the library to install the free Microsoft core fonts on both machines, which should help.</p>\r\n<p>The most common compliment is that saving as PDF is built in. Several patrons have been using it to send resumes by email.</p>\r\n<p>We''ll go through all the cards at Saturday''s meeting. If you''ve used the kiosks yourself, come and tell us how it went.</p>',
1, 1, 0, 7, '2004-10-11 20:05:00', 63, '', '0000-00-00 00:00:00', 0, '2004-10-11 20:05:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 0, '', '', 0, 58),
-- Newsflashes (section 'Newsflashes', category 'Newsflash' as installed; the Newsflash module shows one at random)
(17, 'Next meeting', '', 'Next meeting: Saturday, 16 October, 1:00 PM in Meeting Room B, Riverside Public Library. Tom Becker on building a home file server with Samba.', '',
1, 2, 0, 3, '2004-09-21 18:35:00', 62, '', '0000-00-00 00:00:00', 0, '2004-09-21 18:35:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 1, '', '', 0, 0),
(18, 'CD table', '', 'Free install CDs at every meeting: Fedora Core 2, Mandrake 10.0 and Knoppix 3.6. Take one, and bring it back when you''re done if you can.', '',
1, 2, 0, 3, '2004-08-24 20:20:00', 62, '', '0000-00-00 00:00:00', 0, '2004-08-24 20:20:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 2, '', '', 0, 0),
(19, 'Mailing list', '', 'Stuck between meetings? Ask on the riverside-lug mailing list. Most questions get an answer the same day.', '',
1, 2, 0, 3, '2004-08-16 21:50:00', 62, '', '0000-00-00 00:00:00', 0, '2004-08-16 21:50:00', '0000-00-00 00:00:00', '', '', '', 1, 0, 3, '', '', 0, 0);

INSERT INTO mos_content_frontpage (content_id, ordering) VALUES (16, 1), (8, 2), (1, 3), (3, 4), (2, 5), (4, 6), (6, 7);

-- Menus ------------------------------------------------------------------------------------------
UPDATE mos_menu SET name = 'Links & Downloads', ordering = 6 WHERE id = 4;
UPDATE mos_menu SET ordering = 8 WHERE id = 3;
INSERT INTO mos_menu (id, menutype, name, link, type, published, parent, componentid, sublevel, ordering, checked_out, checked_out_time, pollid, browserNav, access, utaccess, params) VALUES
 (40, 'mainmenu', 'Meetings', 'index.php?option=com_content&task=blogsection&id=3', 'content_blog_section', 1, 0, 3, 0, 4, 0, '0000-00-00 00:00:00', 0, 0, 0, 3, ''),
 (41, 'mainmenu', 'FAQ', 'index.php?option=com_content&task=section&id=4', 'content_section', 1, 0, 4, 0, 5, 0, '0000-00-00 00:00:00', 0, 0, 0, 3, ''),
 (42, 'mainmenu', 'About Us', 'index.php?option=com_content&task=view&id=15', 'content_typed', 1, 0, 15, 0, 7, 0, '0000-00-00 00:00:00', 0, 0, 0, 3, '');

-- Poll (the stock install has the Polls module but no poll) -----------------------------------------
INSERT INTO mos_polls (id, title, voters, checked_out, checked_out_time, published, access, lag) VALUES
 (14, 'Which desktop do you use most at home?', 132, 0, '0000-00-00 00:00:00', 1, 0, 86400);
INSERT INTO mos_poll_data (id, pollid, text, hits) VALUES
 (1, 14, 'GNOME', 41), (2, 14, 'KDE', 47), (3, 14, 'Xfce', 9),
 (4, 14, 'A window manager (Fluxbox, IceWM, ...)', 12), (5, 14, 'Still mostly Windows', 23),
 (6, 14, '', 0), (7, 14, '', 0), (8, 14, '', 0), (9, 14, '', 0), (10, 14, '', 0), (11, 14, '', 0), (12, 14, '', 0);
INSERT INTO mos_poll_menu (pollid, menuid) VALUES (14, 1);
-- one mos_poll_date row per vote, spread over 2 August - 13 October 2004
INSERT INTO mos_poll_date (date, vote_id, poll_id)
WITH RECURSIVE n AS (SELECT 1 AS i UNION ALL SELECT i + 1 FROM n WHERE i < 132)
SELECT DATE_ADD('2004-08-02 08:00:00', INTERVAL (i * 48437) MOD 6271200 SECOND),
       CASE WHEN i <= 41 THEN 1 WHEN i <= 88 THEN 2 WHEN i <= 97 THEN 3 WHEN i <= 109 THEN 4 ELSE 5 END,
       14
FROM n;

-- Contact (stock placeholder row, filled in) --------------------------------------------------------
UPDATE mos_contact_details SET name = 'Dave Reyes', con_position = 'Group Coordinator',
  address = 'Riverside Linux User Group\r\nc/o Riverside Public Library', suburb = 'Riverside', state = '', country = '',
  postcode = '', telephone = '', fax = '',
  misc = 'The quickest way to reach us is the mailing list or the monthly meeting. Use this form for anything else, such as booking a speaker or asking about install-fests. It goes straight to the group coordinator.',
  image = '', email_to = 'coordinator@riversidelug.org', user_id = 62
WHERE id = 1;

-- Web links ----------------------------------------------------------------------------------------
INSERT INTO mos_weblinks (id, catid, sid, title, url, description, date, hits, published, ordering, archived, approved, params) VALUES
 (1, 13, 0, 'Fedora Core', 'http://fedora.redhat.com/', 'The free community version of Red Hat Linux. Core 2 is current.', '2004-03-04 20:00:00', 187, 1, 1, 0, 1, ''),
 (2, 13, 0, 'Mandrakelinux', 'http://www.mandrakelinux.com/', 'Friendly installer and good hardware detection. Our most common pick for first-timers.', '2004-03-04 20:01:00', 203, 1, 2, 0, 1, ''),
 (3, 13, 0, 'Debian GNU/Linux', 'http://www.debian.org/', 'Stable, huge package archive, runs on old hardware.', '2004-03-04 20:02:00', 96, 1, 3, 0, 1, ''),
 (4, 13, 0, 'SUSE Linux', 'http://www.suse.com/', 'SUSE 9.1 Personal is a free download.', '2004-03-04 20:03:00', 71, 1, 4, 0, 1, ''),
 (5, 13, 0, 'Slackware Linux', 'http://www.slackware.com/', 'The oldest surviving distribution. Simple and fast.', '2004-03-04 20:04:00', 44, 1, 5, 0, 1, ''),
 (6, 13, 0, 'Knoppix', 'http://www.knoppix.net/', 'Runs straight from the CD without installing anything.', '2004-03-04 20:05:00', 152, 1, 6, 0, 1, ''),
 (7, 14, 0, 'OpenOffice.org', 'http://www.openoffice.org/', 'Word processor, spreadsheet and presentations. Opens Microsoft Office files.', '2004-03-05 21:00:00', 164, 1, 1, 0, 1, ''),
 (8, 14, 0, 'Mozilla Firefox', 'http://www.mozilla.org/products/firefox/', 'Web browser with tabs and a popup blocker.', '2004-03-05 21:01:00', 211, 1, 2, 0, 1, ''),
 (9, 14, 0, 'The GIMP', 'http://www.gimp.org/', 'Image editor.', '2004-03-05 21:02:00', 58, 1, 3, 0, 1, ''),
 (10, 14, 0, 'Samba', 'http://www.samba.org/', 'File and print sharing with Windows.', '2004-04-02 21:05:00', 47, 1, 4, 0, 1, ''),
 (11, 15, 0, 'The Linux Documentation Project', 'http://www.tldp.org/', 'HOWTOs and guides for almost everything.', '2004-03-05 21:10:00', 66, 1, 1, 0, 1, ''),
 (12, 15, 0, 'LinuxQuestions.org', 'http://www.linuxquestions.org/', 'Large and friendly help forum.', '2004-03-05 21:11:00', 59, 1, 2, 0, 1, ''),
 (13, 15, 0, 'DistroWatch', 'http://www.distrowatch.com/', 'News about new distribution releases.', '2004-03-05 21:12:00', 38, 1, 3, 0, 1, ''),
 (14, 15, 0, 'Freshmeat', 'http://freshmeat.net/', 'Announcements of new free software releases.', '2004-03-05 21:13:00', 22, 1, 4, 0, 1, '');

-- Who's Online: other visitors on the morning of 14 October 2004 (Maria is logged in) ---------------
DELETE FROM mos_session;
INSERT INTO mos_session (username, time, session_id, guest, userid, usertype, gid) VALUES
 ('', '1097749500', 'a1f0c3e9b27d4c58e6f1a0b2c3d4e5f6', 1, 0, '', 0),
 ('', '1097749500', 'b2e1d4f0c38e5d69f702b1c3d4e5f6a7', 1, 0, '', 0),
 ('', '1097749500', 'c3f2e5a1d49f6e7a0813c2d4e5f6a7b8', 1, 0, '', 0),
 ('', '1097749500', 'd4a3f6b2e5a07f8b1924d3e5f6a7b8c9', 1, 0, '', 0),
 ('mlindqvist', '1097749500', 'e5b4a7c3f6b18a9c2a35e4f6a7b8c9d0', 0, 63, 'Author', 19);
