-- Orbital Design Studio: Joomla! 1.5.3 seed content (archive date 9 June 2008)
-- Loaded after a clean install without sample data. Table prefix jos_.

-- Users: the installer creates 62 (admin). A second author writes the tech notes.
UPDATE jos_users SET name = 'Helen Marsh', email = 'helen@orbitaldesignstudio.example',
  registerDate = '2007-06-04 09:30:00', lastvisitDate = '2008-06-09 08:41:00' WHERE id = 62;
UPDATE jos_core_acl_aro SET name = 'Helen Marsh' WHERE value = '62';
DELETE FROM jos_users WHERE id > 62;
DELETE FROM jos_core_acl_aro WHERE id > 10;
DELETE FROM jos_core_acl_groups_aro_map WHERE aro_id > 10;
INSERT INTO jos_users (id, name, username, email, password, usertype, block, sendEmail, gid, registerDate, lastvisitDate, activation, params) VALUES
 (63, 'Tom Bradley', 'tbradley', 'tom@orbitaldesignstudio.example', 'c1a5e1cb21b0a2f5cbbd3d4bf7d5d1d6:Qe3uR8kZtYw0pVb2mXnL4cJsHg7aD9fE', 'Author', 0, 0, 19, '2007-06-04 09:42:00', '2008-06-06 17:12:00', '', 'admin_language=\nlanguage=\neditor=\nhelpsite=\ntimezone=0\n\n');
INSERT INTO jos_core_acl_aro (id, section_value, value, order_value, name, hidden) VALUES (11, 'users', '63', 0, 'Tom Bradley', 0);
INSERT INTO jos_core_acl_groups_aro_map (group_id, section_value, aro_id) VALUES (19, '', 11);

-- Sections and categories
DELETE FROM jos_sections; DELETE FROM jos_categories;
INSERT INTO jos_sections (id, title, name, alias, image, scope, image_position, description, published, checked_out, checked_out_time, ordering, access, count, params) VALUES
 (1, 'News', '', 'news', '', 'content', 'left', 'Studio news, notes from client work and the occasional opinion about the web. Choose a topic below.', 1, 0, '0000-00-00 00:00:00', 1, 0, 3, ''),
 (2, 'Portfolio', '', 'portfolio', '', 'content', 'left', 'A selection of recent sites we have designed and built.', 1, 0, '0000-00-00 00:00:00', 2, 0, 1, ''),
 (3, 'Company', '', 'company', '', 'content', 'left', '', 1, 0, '0000-00-00 00:00:00', 3, 0, 1, '');

INSERT INTO jos_categories (id, parent_id, title, name, alias, image, section, image_position, description, published, checked_out, checked_out_time, editor, ordering, access, count, params) VALUES
 (1, 0, 'Studio News', '', 'studio-news', '', '1', 'left', 'What is going on at the studio: launches, opening hours and the odd staff change.', 1, 0, '0000-00-00 00:00:00', NULL, 1, 0, 0, ''),
 (2, 0, 'Technology Notes', '', 'technology-notes', '', '1', 'left', 'Browsers, hosting, software and the questions clients ask us most often.', 1, 0, '0000-00-00 00:00:00', NULL, 2, 0, 0, ''),
 (3, 0, 'Web Design', '', 'web-design', '', '1', 'left', 'Notes on design, usability and what we have learned from client projects.', 1, 0, '0000-00-00 00:00:00', NULL, 3, 0, 0, ''),
 (4, 0, 'Client Websites', '', 'client-websites', '', '2', 'left', '', 1, 0, '0000-00-00 00:00:00', NULL, 1, 0, 0, ''),
 (5, 0, 'Company Information', '', 'company-information', '', '3', 'left', '', 1, 0, '0000-00-00 00:00:00', NULL, 1, 0, 0, ''),
 (6, 0, 'Contacts', '', 'contacts', '', 'com_contact_details', 'left', 'Contact details for Orbital Design Studio', 1, 0, '0000-00-00 00:00:00', NULL, 1, 0, 0, ''),
 (7, 0, 'Newsflash', '', 'newsflash', '', '3', 'left', '', 1, 0, '0000-00-00 00:00:00', NULL, 2, 0, 0, '');

-- Articles
DELETE FROM jos_content; DELETE FROM jos_content_frontpage;
INSERT INTO jos_content (id, title, alias, title_alias, introtext, `fulltext`, state, sectionid, mask, catid, created, created_by, created_by_alias, modified, modified_by, checked_out, checked_out_time, publish_up, publish_down, images, urls, attribs, version, parentid, ordering, metakey, metadesc, access, hits, metadata) VALUES
(1, 'Five Things We Learned Redesigning a Restaurant Site This Year', 'five-things-we-learned-redesigning-a-restaurant-site-this-year', '',
'<p>We just wrapped up a redesign for a local restaurant client who was still running a site built entirely in Flash back in 2004. Menus that never got updated, no way for search engines to read the text, and a splash screen nobody had the patience to sit through twice. Here is what we took away from the project, including a few arguments we had internally about whether to keep any Flash at all.</p>',
'<p><strong>1. Clients want to edit the menu themselves.</strong><br />Every restaurant owner we have worked with eventually wants to change a price or add a dish without calling us. Building the menu as plain content rather than a baked-in image or Flash movie saved everyone a lot of phone calls.</p>
<p><strong>2. Search engines still can''t read Flash text.</strong><br />The old site never showed up for the restaurant''s own name in search results. Within two weeks of launch, the new HTML version was already outranking three directory listings the client didn''t even know existed.</p>
<p><strong>3. Not every visitor has a fast connection.</strong><br />We tested the site on an older laptop over a hotel wireless connection and the difference was obvious. Not everyone has broadband at home yet, and plenty of people still check a restaurant''s hours from a work computer that locks down browser plugins entirely.</p>
<p><strong>4. A simple RSS feed for specials was an easy win.</strong><br />We added a small feed so regular customers could subscribe to the weekly specials. Explaining what RSS actually does took longer than building it, but a few customers have already told us they use it.</p>
<p><strong>5. Mobile matters more than clients think.</strong><br />With the iPhone now in enough pockets around town, we made sure the hours, address and phone number were usable without a mouse. It''s a small thing, but it is the first part of the site some visitors will ever see.</p>
<p>In the end we kept one small piece of Flash: the slideshow of the dining room on the About page, with a plain photo underneath for anyone without the plugin.</p>
<p>If your business is still running a Flash-only site, get in touch through our <a href="index.php?option=com_contact&amp;view=contact&amp;id=1&amp;Itemid=6">contact page</a> and we''ll take a look at what a redesign might involve.</p>',
1, 1, 0, 3, '2008-06-02 10:12:00', 62, '', '2008-06-02 10:31:00', 62, 0, '0000-00-00 00:00:00', '2008-06-02 10:12:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 3, 0, 1, 'restaurant, redesign, flash, rss', '', 0, 341, 'robots=\nauthor='),

(2, 'Why We''re Still Recommending Firefox to Clients', 'why-were-still-recommending-firefox-to-clients', '',
'<p>With Vista''s compatibility headaches still fresh for a lot of our clients and a new Firefox release expected any day now, we keep getting asked which browser to standardise on for the office. Short answer: it depends what you''re testing, but we still install Firefox 2 on every new machine we set up, alongside whatever came in the box.</p>',
'<p>Here is the longer answer we have been giving people.</p>
<p><strong>It is free and it keeps itself up to date.</strong> Most of our clients are offices of three to ten people with nobody in charge of IT. Firefox checks for security updates on its own and asks once before installing them. That alone is worth a lot.</p>
<p><strong>Tabs and the pop-up blocker.</strong> Internet Explorer 7 finally has both, but plenty of our clients are still on Windows XP machines with IE6, and we would rather not push a big upgrade on a machine that is otherwise working.</p>
<p><strong>It behaves the same on the Mac.</strong> Two of our clients have a mix of Macs and PCs in the office. Using the same browser on both cuts down on the &quot;it looks different on my computer&quot; phone calls.</p>
<p><strong>Add-ons.</strong> For us the Web Developer toolbar and Firebug are the reason we live in Firefox all day. Most clients won''t need them, but a good ad blocker and a spell checker in web forms are popular.</p>
<p>We don''t tell anyone to remove Internet Explorer. Online banking, the VAT returns site and a few older intranets still expect it, so we leave it on the desktop for those.</p>
<p>As for the new version: Firefox 3 has been in release candidate testing since May and it looks noticeably faster with less memory use. We will wait for the final release and probably the first point update before rolling it out on client machines. If you would like us to set it up for your office, give Tom a call.</p>',
1, 1, 0, 2, '2008-05-29 14:30:00', 63, '', '2008-05-30 09:02:00', 63, 0, '0000-00-00 00:00:00', '2008-05-29 14:30:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 2, 0, 1, 'firefox, browsers, internet explorer', '', 0, 412, 'robots=\nauthor='),

(3, 'Portfolio Update: Riverside Dental Launches New Site', 'portfolio-update-riverside-dental-launches-new-site', '',
'<p>Riverside Dental''s new site went live last week, including an online appointment request form and a staff page their receptionist has already asked us to update twice. Full case notes are up in the portfolio section.</p>',
'<p>The practice had been using a single page with their phone number and a map for about five years. The new site has a page for each treatment, opening hours, a team page with photos and a short form for appointment requests that goes straight to the front desk email.</p>
<p>The practice manager can now change the opening hours and holiday notices herself, which was the main thing she asked for in our first meeting.</p>',
1, 1, 0, 1, '2008-05-22 09:05:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-05-22 09:05:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 2, '', '', 0, 198, 'robots=\nauthor='),

(4, 'Notes from a Client Meeting: Explaining RSS to a Restaurant Owner', 'notes-from-a-client-meeting-explaining-rss-to-a-restaurant-owner', '',
'<p>&quot;So it''s like a newsletter, but they don''t give you their email address?&quot; That was the closest we got in the first ten minutes. A few notes on how we ended up explaining feeds to a client who has never used one.</p>',
'<p>What finally worked was skipping the technology entirely. We opened the BBC News site, clicked the orange icon, added the feed to the client''s own Outlook and showed her the headlines turning up next to her email. Then we did the same with a test feed of her own specials.</p>
<p>A few things we will do differently next time:</p>
<ul>
<li>Don''t say &quot;XML&quot;. Ever.</li>
<li>Show the orange icon early, because they have seen it before and wondered what it was.</li>
<li>Point out that subscribers can leave whenever they like, with no unsubscribe link to manage.</li>
<li>Offer an email newsletter as well. Most of her regulars will still prefer that.</li>
</ul>',
1, 1, 0, 2, '2008-05-14 16:40:00', 63, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-05-14 16:40:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 2, '', '', 0, 187, 'robots=\nauthor='),

(5, 'Studio Closed Monday 16 June for Staff Training', 'studio-closed-monday-16-june-for-staff-training', '',
'<p>The studio will be closed all day on Monday 16 June while the whole team is away at a one-day course on accessibility and web standards in Manchester. Phones will go to voicemail and we will reply to email on Tuesday 17 June.</p><p>Hosting customers with an urgent problem can still use the support number printed on their welcome letter.</p>',
'',
1, 1, 0, 1, '2008-06-06 11:20:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-06-06 11:20:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 1, '', '', 0, 64, 'robots=\nauthor='),

(6, 'Why Flash Intros Still Won''t Die', 'why-flash-intros-still-wont-die', '',
'<p>Every few months a new client asks us for an animated intro page with a &quot;Skip Intro&quot; button. We usually talk them out of it. Here is the speech.</p>',
'<p>An intro page is the one page on your site that every new visitor has to get past and that nobody comes to see. Search engines see a page with no text. Visitors on a slow connection see a loading bar. Regular customers see the same animation every single time.</p>
<p>The reasons clients give for wanting one are almost always good ones: they want the site to feel professional, or they want to show off a product. Both are better done with a strong home page and good photography.</p>
<p>If you really want movement, put a short slideshow on the home page itself, keep it under a few seconds and make sure the phone number is visible before it finishes loading.</p>',
1, 1, 0, 3, '2007-11-20 12:00:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2007-11-20 12:00:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 3, '', '', 0, 1042, 'robots=\nauthor='),

(7, 'Should You Redesign for Internet Explorer 7?', 'should-you-redesign-for-internet-explorer-7', '',
'<p>Internet Explorer 7 has been out for almost a year and Windows Update is now pushing it to most XP machines. Do you need to change your site? Probably not, but it is worth an afternoon of testing.</p>',
'<p>Most of the problems we have seen fall into three groups: layouts that relied on IE6 bugs to line up, PNG images with transparency that were hacked around for IE6, and old &quot;best viewed in&quot; scripts that sniff the browser version and send IE7 users to an error page.</p>
<p>Our advice: open your site in IE7, Firefox and Safari side by side, check the forms and the checkout if you have one, and fix what is broken. A full redesign is only worth it if the site needed one anyway.</p>',
1, 1, 0, 2, '2007-09-12 15:10:00', 63, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2007-09-12 15:10:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 4, '', '', 0, 871, 'robots=\nauthor='),

(8, 'A Short Guide to Favicon Design', 'a-short-guide-to-favicon-design', '',
'<p>The little icon in the address bar and the bookmarks menu is sixteen pixels square, and most companies use a shrunken copy of their full logo. It rarely works. A few tips from the last dozen we have drawn.</p>',
'<ul>
<li>Use one letter or one shape from the logo, not the whole thing.</li>
<li>Draw it at 16 by 16 pixels, pixel by pixel. Don''t just resize.</li>
<li>Check it on a white and a grey background, since browsers show both.</li>
<li>Save it as a real .ico file in the root of the site so older browsers find it.</li>
</ul>',
1, 1, 0, 3, '2008-01-24 10:25:00', 63, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-01-24 10:25:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 2, '', '', 0, 298, 'robots=\nauthor='),

(9, 'Choosing Between Joomla and WordPress for Clients', 'choosing-between-joomla-and-wordpress-for-clients', '',
'<p>We build on both, and clients often ask why one site got Joomla and another got WordPress. Our rough rule: if it is mostly a blog, WordPress. If it is a company site with sections, a contact form, members or more than one person editing, Joomla.</p>',
'<p>Joomla 1.5 came out in January and it has made the decision easier. The new version is cleaner to work with, the administrator screens are easier to explain to clients, and we can set up sections and categories that match how a business already thinks about its information.</p>
<p>WordPress is still quicker to learn for someone who only wants to post news, and the editing screen is friendlier. For a dentist who wants to update holiday hours twice a year, either will do the job.</p>',
1, 1, 0, 2, '2008-03-04 13:45:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-03-04 13:45:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 3, '', '', 0, 256, 'robots=\nauthor='),

(10, 'New Server for Our Hosting Customers', 'new-server-for-our-hosting-customers', '',
'<p>Over the weekend of 9 and 10 February we moved all hosted sites and mailboxes to a new server with more memory and faster disks. If you notice anything not working as it did, please let Tom know.</p>',
'',
1, 1, 0, 1, '2008-02-11 09:00:00', 63, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-02-11 09:00:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 3, '', '', 0, 143, 'robots=\nauthor='),

(11, 'Riverside Dental Practice', 'riverside-dental-practice', '',
'<p>A new site for a three-dentist practice on Riverside Road, with a page for each treatment, an appointment request form and a team page that the practice manager keeps up to date herself.</p>',
'<p><strong>Client:</strong> Riverside Dental Practice, Northbridge<br /><strong>Launched:</strong> May 2008<br /><strong>Built with:</strong> Joomla 1.5</p>
<p>The brief was simple: patients kept phoning to ask about opening hours and whether the practice took new NHS patients. Both answers are now on the home page. The appointment request form sends an email to the front desk, who phone the patient back to confirm a time.</p>
<p>We also set up the practice''s first proper email addresses and trained two members of staff to edit the site.</p>',
1, 2, 0, 4, '2008-05-22 08:50:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-05-22 08:50:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 1, '', '', 0, 133, 'robots=\nauthor='),

(12, 'Maple & Vine Restaurant', 'maple-vine-restaurant', '',
'<p>Replacing a Flash-only site with a searchable, editable menu section and a weekly specials feed. The write-up of what changed and why is in our news section.</p>',
'<p><strong>Client:</strong> Maple &amp; Vine, Combe Street<br /><strong>Launched:</strong> May 2008<br /><strong>Built with:</strong> Joomla 1.5</p>
<p>The restaurant''s old site was a single Flash movie made in 2004. The new site keeps the same colours and photography, but the menu, opening hours and directions are now ordinary pages the owner can edit. Weekly specials are published as news items with an RSS feed.</p>',
1, 2, 0, 4, '2008-05-09 11:15:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-05-09 11:15:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 2, '', '', 0, 276, 'robots=\nauthor='),

(13, 'Hartley & Combe Solicitors', 'hartley-combe-solicitors', '',
'<p>A straightforward six-page brochure site for a local firm of solicitors, with a staff directory and a downloadable PDF of their client information leaflet.</p>',
'<p><strong>Client:</strong> Hartley &amp; Combe Solicitors<br /><strong>Launched:</strong> April 2008<br /><strong>Built with:</strong> hand-coded HTML and CSS</p>
<p>The partners wanted something quiet and easy to read, with no news section to keep up to date. We designed it around their existing letterhead and kept every page printable.</p>',
1, 2, 0, 4, '2008-04-18 14:00:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-04-18 14:00:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 3, '', '', 0, 164, 'robots=\nauthor='),

(14, 'Northbridge Running Club', 'northbridge-running-club', '',
'<p>A small pilot project adding a members-only events calendar for a local running club, built around the same login module we use on our own site.</p>',
'<p><strong>Client:</strong> Northbridge Running Club<br /><strong>Launched:</strong> April 2008<br /><strong>Built with:</strong> Joomla 1.5</p>
<p>The club has around 120 members and used to send race dates round by email. Members now log in to see the calendar, results and the committee minutes. Public pages cover how to join and where the Tuesday and Thursday runs start.</p>',
1, 2, 0, 4, '2008-04-02 10:30:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-04-02 10:30:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 4, '', '', 0, 211, 'robots=\nauthor='),

(15, 'Combe Street Gallery', 'combe-street-gallery', '',
'<p>An online catalogue for a small art gallery, with Flickr used for the image galleries rather than a custom upload system, to keep hosting costs down.</p>',
'<p><strong>Client:</strong> Combe Street Gallery<br /><strong>Launched:</strong> March 2008<br /><strong>Built with:</strong> Joomla 1.5 and Flickr</p>
<p>The gallery changes its exhibition every six weeks. The owner uploads photos of the new work to Flickr from her own computer, and the site shows the current set alongside the artist''s notes and prices.</p>',
1, 2, 0, 4, '2008-03-14 16:20:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-03-14 16:20:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 5, '', '', 0, 189, 'robots=\nauthor='),

(16, 'About Us', 'about-us', '',
'<p>Orbital Design Studio is a small web design company based at 14 Combe Street in Northbridge. We have been designing, building and looking after websites for local businesses, charities and clubs since 2001.</p>
<p>There are four of us:</p>
<ul>
<li><strong>Helen Marsh</strong> started the studio and still does most of the design work and client meetings.</li>
<li><strong>Tom Bradley</strong> looks after development, hosting and email, and answers the support phone.</li>
<li><strong>Priya Shah</strong> joined in 2006 and works on design, print and photography.</li>
<li><strong>Gareth Lowe</strong> works part time on project planning and accounts.</li>
</ul>
<p>Most of our clients are within twenty miles of the studio, and we prefer to meet in person at the start of a project. We are happy to work with businesses further away too.</p>
<p>We are members of the Northbridge Chamber of Commerce and have sponsored the Northbridge Running Club 10k since 2005.</p>',
'',
1, 3, 0, 5, '2007-06-11 10:00:00', 62, '', '2008-03-10 15:22:00', 62, 0, '0000-00-00 00:00:00', '2007-06-11 10:00:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=0\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 4, 0, 1, '', '', 0, 512, 'robots=\nauthor='),

(17, 'Services', 'services', '',
'<p>We keep things simple: a fixed quote before we start, and one person you can phone who knows your site. All prices exclude VAT.</p>
<h3>Website design</h3>
<p>Brochure sites from &pound;950 for five pages, including a contact form and a site map. Larger sites with news, a members area or an online catalogue are quoted individually.</p>
<h3>Content management</h3>
<p>We set up sites on Joomla so you can edit your own pages, add news and change opening hours without calling us. Every site includes a half-day training session at your office.</p>
<h3>Hosting and email</h3>
<p>Hosting on our own server from &pound;60 a year, with up to ten email addresses on your own domain name. We also register and renew domain names.</p>
<h3>Search engines</h3>
<p>Every site we build is written so that Google, Yahoo! and Live Search can read it. We also offer a one-off review of an existing site from &pound;150.</p>
<h3>Maintenance</h3>
<p>Monthly maintenance contracts cover updates, backups and up to two hours of changes a month.</p>
<h3>Print</h3>
<p>Logos, business cards, letterheads and leaflets, designed to match your website.</p>',
'',
1, 3, 0, 5, '2007-06-11 10:20:00', 62, '', '2008-04-02 11:05:00', 62, 0, '0000-00-00 00:00:00', '2007-06-11 10:20:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=0\nshow_create_date=0\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 6, 0, 2, '', '', 0, 389, 'robots=\nauthor='),

(18, 'Summer bookings', 'summer-bookings', '',
'<p>We are now booking website projects for July and August. Call the studio on 01632 960 118 or use our <a href="index.php?option=com_contact&amp;view=contact&amp;id=1&amp;Itemid=6">contact form</a> for a free quote.</p>',
'',
1, 3, 0, 7, '2008-05-27 09:15:00', 62, '', '0000-00-00 00:00:00', 0, 0, '0000-00-00 00:00:00', '2008-05-27 09:15:00', '0000-00-00 00:00:00', '', '', 'show_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_vote=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nlanguage=\nkeyref=\nreadmore=', 1, 0, 1, '', '', 0, 0, 'robots=\nauthor=');

INSERT INTO jos_content_frontpage (content_id, ordering) VALUES (1, 1), (5, 2), (2, 3), (3, 4), (4, 5);

-- Contact
DELETE FROM jos_contact_details;
INSERT INTO jos_contact_details (id, name, alias, con_position, address, suburb, state, country, postcode, telephone, fax, misc, image, imagepos, email_to, default_con, published, checked_out, checked_out_time, ordering, params, user_id, catid, access, mobile, webpage) VALUES
(1, 'Orbital Design Studio', 'orbital-design-studio', 'Studio Office', '14 Combe Street', 'Northbridge', '', 'United Kingdom', 'NB1 4QJ', '01632 960 118', '01632 960 119',
 'We are usually in the office Monday to Friday, 9am to 5:30pm, and we try to return calls and emails the same working day. Prefer not to call? Send us a message using the form below.',
 '', 'top', 'info@orbitaldesignstudio.example', 1, 1, 0, '0000-00-00 00:00:00', 1,
 'show_name=1\r\nshow_position=1\r\nshow_email=0\r\nshow_street_address=1\r\nshow_suburb=1\r\nshow_state=1\r\nshow_postcode=1\r\nshow_country=1\r\nshow_telephone=1\r\nshow_mobile=1\r\nshow_fax=1\r\nshow_webpage=1\r\nshow_misc=1\r\nshow_image=1\r\nallow_vcard=0\r\ncontact_icons=0\r\nicon_address=\r\nicon_email=\r\nicon_telephone=\r\nicon_fax=\r\nicon_misc=\r\nshow_email_form=1\r\nemail_description=1\r\nshow_email_copy=1\r\nbanned_email=\r\nbanned_subject=\r\nbanned_text=',
 0, 6, 0, '', '');

-- Poll
DELETE FROM jos_polls; DELETE FROM jos_poll_data; DELETE FROM jos_poll_date; DELETE FROM jos_poll_menu;
INSERT INTO jos_polls (id, title, alias, voters, checked_out, checked_out_time, published, access, lag) VALUES
 (1, 'Which browser do you use most?', 'which-browser-do-you-use-most', 145, 0, '0000-00-00 00:00:00', 1, 0, 86400);
INSERT INTO jos_poll_data (id, pollid, text, hits) VALUES
 (1, 1, 'Internet Explorer 7', 48), (2, 1, 'Internet Explorer 6', 31), (3, 1, 'Firefox 2', 52), (4, 1, 'Safari 3', 10),
 (5, 1, 'Opera 9', 4), (6, 1, '', 0), (7, 1, '', 0), (8, 1, '', 0), (9, 1, '', 0), (10, 1, '', 0), (11, 1, '', 0), (12, 1, '', 0);
INSERT INTO jos_poll_date (id, date, vote_id, poll_id) VALUES
 (1, '2008-06-08 19:42:11', 3, 1), (2, '2008-06-08 21:05:37', 1, 1), (3, '2008-06-09 07:58:02', 2, 1);

-- Menus: Main Menu (left) plus the same menu as pills in the header
DELETE FROM jos_menu WHERE id > 1;
UPDATE jos_menu SET params = 'num_leading_articles=1\nnum_intro_articles=4\nnum_columns=2\nnum_links=4\norderby_pri=\norderby_sec=front\nshow_pagination=2\nshow_pagination_results=1\nshow_feed_link=1\nshow_noauth=\nshow_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_item_navigation=\nshow_readmore=\nshow_vote=\nshow_icons=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nshow_hits=\nfeed_summary=\npage_title=Welcome to Orbital Design Studio\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n' WHERE id = 1;
INSERT INTO jos_menu (id, menutype, name, alias, link, type, published, parent, componentid, sublevel, ordering, checked_out, checked_out_time, pollid, browserNav, access, utaccess, params, lft, rgt, home) VALUES
(2, 'mainmenu', 'About Us', 'about-us', 'index.php?option=com_content&view=article&id=16', 'component', 1, 0, 20, 0, 2, 0, '0000-00-00 00:00:00', 0, 0, 0, 0, 'show_noauth=\nshow_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_item_navigation=\nshow_readmore=\nshow_vote=\nshow_icons=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nshow_hits=\nfeed_summary=\npage_title=\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n', 0, 0, 0),
(3, 'mainmenu', 'Services', 'services', 'index.php?option=com_content&view=article&id=17', 'component', 1, 0, 20, 0, 3, 0, '0000-00-00 00:00:00', 0, 0, 0, 0, 'show_noauth=\nshow_title=\nlink_titles=\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_item_navigation=\nshow_readmore=\nshow_vote=\nshow_icons=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nshow_hits=\nfeed_summary=\npage_title=\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n', 0, 0, 0),
(4, 'mainmenu', 'Portfolio', 'portfolio', 'index.php?option=com_content&view=section&layout=blog&id=2', 'component', 1, 0, 20, 0, 4, 0, '0000-00-00 00:00:00', 0, 0, 0, 0, 'show_description=1\nshow_description_image=0\nnum_leading_articles=0\nnum_intro_articles=6\nnum_columns=1\nnum_links=4\norderby_pri=\norderby_sec=rdate\nshow_pagination=2\nshow_pagination_results=1\nshow_feed_link=1\nshow_noauth=\nshow_title=\nlink_titles=1\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_author=0\nshow_create_date=0\nshow_modify_date=0\nshow_item_navigation=\nshow_readmore=\nshow_vote=\nshow_icons=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nshow_hits=\nfeed_summary=\npage_title=Our Recent Work\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n', 0, 0, 0),
(5, 'mainmenu', 'News', 'news', 'index.php?option=com_content&view=section&id=1', 'component', 1, 0, 20, 0, 5, 0, '0000-00-00 00:00:00', 0, 0, 0, 0, 'show_description=1\nshow_description_image=0\nshow_categories=1\nshow_empty_categories=0\nshow_cat_num_articles=1\nshow_category_description=1\norderby=\norderby_sec=rdate\nshow_feed_link=1\nshow_noauth=\nshow_title=\nlink_titles=1\nshow_intro=\nshow_section=\nlink_section=\nshow_category=\nlink_category=\nshow_author=\nshow_create_date=\nshow_modify_date=\nshow_item_navigation=\nshow_readmore=\nshow_vote=\nshow_icons=\nshow_pdf_icon=\nshow_print_icon=\nshow_email_icon=\nshow_hits=\nfeed_summary=\npage_title=\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n', 0, 0, 0),
(6, 'mainmenu', 'Contact Us', 'contact-us', 'index.php?option=com_contact&view=contact&id=1', 'component', 1, 0, 7, 0, 6, 0, '0000-00-00 00:00:00', 0, 0, 0, 0, 'show_contact_list=0\nshow_category_crumb=0\ncontact_icons=\nicon_address=\nicon_email=\nicon_telephone=\nicon_mobile=\nicon_fax=\nicon_misc=\nshow_headings=\nshow_position=\nshow_email=\nshow_telephone=\nshow_mobile=\nshow_fax=\nallow_vcard=\nbanned_email=\nbanned_subject=\nbanned_text=\nvalidate_session=\ncustom_reply=\npage_title=\nshow_page_title=1\npageclass_sfx=\nmenu_image=-1\nsecure=0\n\n', 0, 0, 0);

-- Front-end modules (the installer only adds Main Menu)
DELETE FROM jos_modules WHERE client_id = 0 AND id > 1;
UPDATE jos_modules SET ordering = 1 WHERE id = 1;
INSERT INTO jos_modules (id, title, content, ordering, position, checked_out, checked_out_time, published, module, numnews, access, showtitle, params, iscore, client_id, control) VALUES
(25, 'Newsflash', '', 1, 'top', 0, '0000-00-00 00:00:00', 1, 'mod_newsflash', 0, 0, 1, 'catid=7\nlayout=default\nimage=0\nlink_titles=\nshowLastSeparator=1\nreadmore=0\nitem_title=0\nitems=1\nmoduleclass_sfx=\ncache=0\n\n', 0, 0, ''),
(16, 'Polls', '', 1, 'right', 0, '0000-00-00 00:00:00', 1, 'mod_poll', 0, 0, 1, 'id=1\ncache=1', 0, 0, ''),
(18, 'Login Form', '', 2, 'left', 0, '0000-00-00 00:00:00', 1, 'mod_login', 0, 0, 1, 'greeting=1\nname=0', 1, 0, ''),
(19, 'Latest News', '', 1, 'user1', 0, '0000-00-00 00:00:00', 1, 'mod_latestnews', 0, 0, 1, 'count=5\nordering=c_dsc\nuser_id=0\nshow_front=1\nsecid=1\ncatid=\nmoduleclass_sfx=\ncache=1\ncache_time=900\n\n', 1, 0, ''),
(21, 'Who''s Online', '', 2, 'right', 0, '0000-00-00 00:00:00', 1, 'mod_whosonline', 0, 0, 1, 'online=1\nusers=1\nmoduleclass_sfx=', 0, 0, ''),
(22, 'Popular', '', 1, 'user2', 0, '0000-00-00 00:00:00', 1, 'mod_mostread', 0, 0, 1, 'count=5\nshow_front=1\nsecid=1\ncatid=\nmoduleclass_sfx=\ncache=1\n\n', 0, 0, ''),
(27, 'Search', '', 1, 'user4', 0, '0000-00-00 00:00:00', 1, 'mod_search', 0, 0, 0, 'cache=1', 0, 0, ''),
(29, 'Top Menu', '', 1, 'user3', 0, '0000-00-00 00:00:00', 1, 'mod_mainmenu', 0, 0, 0, 'cache=1\nmenutype=mainmenu\nmenu_style=list_flat\nmenu_images=n\nmenu_images_align=left\nexpand_menu=n\nclass_sfx=-nav\nmoduleclass_sfx=\nindent_image1=0\nindent_image2=0\nindent_image3=0\nindent_image4=0\nindent_image5=0\nindent_image6=0', 1, 0, ''),
(33, 'Footer', '', 2, 'footer', 0, '0000-00-00 00:00:00', 1, 'mod_footer', 0, 0, 0, 'cache=1\n\n', 1, 0, ''),
(35, 'Breadcrumbs', '', 1, 'breadcrumb', 0, '0000-00-00 00:00:00', 1, 'mod_breadcrumbs', 0, 0, 1, 'moduleclass_sfx=\ncache=0\nshowHome=1\nhomeText=Home\nshowComponent=1\nseparator=\n\n', 1, 0, ''),
(36, 'Syndication', '', 3, 'syndicate', 0, '0000-00-00 00:00:00', 1, 'mod_syndicate', 0, 0, 0, '', 1, 0, '');

DELETE FROM jos_modules_menu WHERE moduleid > 1;
INSERT INTO jos_modules_menu (moduleid, menuid) VALUES
 (16, 1), (18, 0), (25, 0), (19, 1), (19, 5), (21, 1), (22, 1), (22, 5), (27, 0), (29, 0), (33, 0), (35, 0), (36, 0);

-- Session table: one other guest browsing when the snapshot was taken
DELETE FROM jos_session;
