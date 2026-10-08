-- signal & noise: WordPress 2.2.1 seed content (archive date 2 August 2007)
UPDATE wp_options SET option_value = 'signal & noise' WHERE option_name = 'blogname';
UPDATE wp_options SET option_value = '5' WHERE option_name = 'posts_per_page';
UPDATE wp_users SET display_name = 'Dave', user_nicename = 'admin', user_registered = '2007-05-28 21:40:00' WHERE ID = 1;

DELETE FROM wp_posts; DELETE FROM wp_post2cat; DELETE FROM wp_comments; DELETE FROM wp_postmeta;
DELETE FROM wp_categories; DELETE FROM wp_links; DELETE FROM wp_link2cat;

INSERT INTO wp_categories (cat_ID, cat_name, category_nicename, category_description, category_parent, category_count, link_count) VALUES
 (1, 'Uncategorized', 'uncategorized', '', 0, 1, 0),
 (2, 'Blogroll', 'blogroll', '', 0, 0, 6),
 (3, 'Hardware', 'hardware', '', 0, 1, 0),
 (4, 'Software', 'software', '', 0, 2, 0),
 (5, 'Gadgets', 'gadgets', '', 0, 2, 0),
 (6, 'Reviews', 'reviews', '', 0, 2, 0),
 (7, 'Rants', 'rants', '', 0, 2, 0);

INSERT INTO wp_links (link_id, link_url, link_name, link_category, link_visible, link_owner, link_rating) VALUES
 (1, 'http://arstechnica.com/', 'Ars Technica', 2, 'Y', 1, 0),
 (2, 'http://www.codinghorror.com/blog/', 'Coding Horror', 2, 'Y', 1, 0),
 (3, 'http://kottke.org/', 'kottke.org', 2, 'Y', 1, 0),
 (4, 'http://mikes-photos.example/', 'Mike''s photoblog', 2, 'Y', 1, 0),
 (5, 'http://www.joelonsoftware.com/', 'Joel on Software', 2, 'Y', 1, 0),
 (6, 'http://lifehacker.com/', 'Lifehacker', 2, 'Y', 1, 0);
INSERT INTO wp_link2cat (link_id, category_id) VALUES (1,2),(2,2),(3,2),(4,2),(5,2),(6,2);

INSERT INTO wp_posts (ID, post_author, post_date, post_date_gmt, post_modified, post_modified_gmt, post_content, post_title, post_excerpt, post_status, comment_status, ping_status, post_name, to_ping, pinged, post_content_filtered, post_parent, guid, menu_order, post_type, comment_count) VALUES
(7, 1, '2007-08-02 09:14:00', '2007-08-02 09:14:00', '2007-08-02 09:14:00', '2007-08-02 09:14:00',
'I held out for about four weeks. Then the AT&T store near work had them in stock on a Tuesday afternoon with nobody in line, and that was that. Eight gigs, black, $599 plus the two-year contract I swore I''d never sign.

<!--more-->

A week in, the short version: the screen and the browser are as good as everybody said, and the phone part is fine but nothing special.

Safari is the reason to own it. Pages load as real pages, not the stripped "mobile" versions, and pinch-zooming into a column of text on the train still feels slightly ridiculous in a good way. On EDGE it is slow. On my home WiFi it is genuinely usable, which is not something I have ever said about a phone browser.

The keyboard took about three days. I was hitting the wrong letters constantly for the first two, and then one morning it just stopped being a problem. Trusting the autocorrect is most of the trick.

Things I don''t love:

<ul>
<li>No copy and paste. I keep reaching for it.</li>
<li>No third-party apps. Apple says web apps are the answer. We''ll see.</li>
<li>The battery is fine for a phone and terrible for a phone you use as a computer.</li>
<li>I have already dropped it once. It survived. My heart barely did.</li>
</ul>

Would I tell someone to buy one? If they were already thinking about an iPod and a new phone at the same time, probably. If they need a phone that types email all day, the BlackBerry people are not wrong yet.',
'First impressions: a week with the iPhone', '', 'publish', 'open', 'open', 'first-impressions-a-week-with-the-iphone', '', '', '', 0, 'http://127.0.0.1:8901/?p=7', 0, 'post', 3),

(6, 1, '2007-07-26 22:41:00', '2007-07-26 22:41:00', '2007-07-26 22:41:00', '2007-07-26 22:41:00',
'Six months ago I put Vista Home Premium on the main machine, partly because the new PC came with it and partly because I wanted to know whether the complaining was fair.

<!--more-->

Mostly fair, it turns out, though not for the reasons people say.

The look is fine. I like the Aero glass more than I expected to, and the search box in the Start menu is the single best thing Microsoft has added since XP. I type three letters and the program opens. I don''t remember the last time I clicked through All Programs.

UAC is annoying but I''ve made my peace with it. The real problem is drivers. My scanner has no Vista driver and the manufacturer has "no plans" to release one. My TV tuner card works, but only with software that crashes once a day. The printer driver is a 140MB download for a printer.

The other thing nobody warned me about is how much memory it wants. With 1GB it was sluggish; with 2GB it''s fine. If you''re buying a machine with Vista on it this year, do not let them sell you 1GB.

Would I go back to XP? On the laptop, I never left. On the desktop, no. But I understand why people are asking for downgrades.',
'Vista, six months in', '', 'publish', 'open', 'open', 'vista-six-months-in', '', '', '', 0, 'http://127.0.0.1:8901/?p=6', 0, 'post', 2),

(5, 1, '2007-07-18 20:05:00', '2007-07-18 20:05:00', '2007-07-18 20:05:00', '2007-07-18 20:05:00',
'The old Athlon XP finally retired this weekend. Parts list for anyone curious:

<!--more-->

<ul>
<li>Intel Core 2 Duo E6600</li>
<li>Gigabyte P965 board</li>
<li>2GB of Corsair DDR2-800</li>
<li>eVGA GeForce 8800 GTS 320MB</li>
<li>Seagate 320GB SATA</li>
<li>Antec Sonata case, because it was on sale and it is quiet</li>
</ul>

Total was a little under $1,100 with shipping. Build took one evening, most of which was spent finding out that the front panel connectors are labelled for ants.

First boot: nothing. Second boot after reseating the RAM: fine. It always seems to be the RAM.

I haven''t overclocked it yet and I''m not sure I will. Everything I play runs at 1680x1050 with the settings turned up, and the case is quiet enough that I can hear the hard drive again, which I''d forgotten was a sound computers make.',
'Finally built the new box', '', 'publish', 'open', 'open', 'finally-built-the-new-box', '', '', '', 0, 'http://127.0.0.1:8901/?p=5', 0, 'post', 4),

(4, 1, '2007-07-05 13:30:00', '2007-07-05 13:30:00', '2007-07-05 13:30:00', '2007-07-05 13:30:00',
'Every few months somebody at work asks what I have installed, so here is the list, mostly so I can send them a link.

<!--more-->

<ul>
<li><strong>Adblock Plus</strong> plus the Filterset.G updater. Obviously.</li>
<li><strong>Firebug.</strong> If you write any HTML at all this is not optional.</li>
<li><strong>Foxmarks</strong> to keep bookmarks the same at home and at work.</li>
<li><strong>Tab Mix Plus</strong>, mostly for the session saving.</li>
<li><strong>Greasemonkey</strong>, with exactly two scripts that I wrote myself and am slightly embarrassed by.</li>
</ul>

I''ve tried to stop at five. It never lasts.',
'Firefox extensions I can''t live without', '', 'publish', 'open', 'open', 'firefox-extensions', '', '', '', 0, 'http://127.0.0.1:8901/?p=4', 0, 'post', 1),

(3, 1, '2007-06-21 23:12:00', '2007-06-21 23:12:00', '2007-06-21 23:12:00', '2007-06-21 23:12:00',
'Bloglines tells me I have 1,412 unread items. I am subscribed to 96 feeds. I would like to know when that happened.

<!--more-->

Tonight I went through and unsubscribed from everything I hadn''t clicked on in a month. That got me down to 41, which still feels like a lot, but at least I recognise all of them.

If you are one of the 55, it''s not personal.',
'My feed reader is out of control', '', 'publish', 'open', 'open', 'my-feed-reader-is-out-of-control', '', '', '', 0, 'http://127.0.0.1:8901/?p=3', 0, 'post', 0),

(1, 1, '2007-06-08 18:44:00', '2007-06-08 18:44:00', '2007-06-08 18:44:00', '2007-06-08 18:44:00',
'Seven months after launch, the GameStop down the road had three of them sitting on a shelf on a Friday afternoon. I didn''t ask questions.

<!--more-->

Wii Sports bowling is exactly as much fun as everyone says, and my arm hurts.',
'Bought a Wii. Finally.', '', 'publish', 'open', 'open', 'bought-a-wii-finally', '', '', '', 0, 'http://127.0.0.1:8901/?p=1', 0, 'post', 2),

(8, 1, '2007-05-30 21:02:00', '2007-05-30 21:02:00', '2007-05-30 21:02:00', '2007-05-30 21:02:00',
'After three years on Blogger I''ve moved everything over to WordPress on my own hosting. The old posts are still over there for now; I''ll bring the good ones across when I get a weekend.

Yes, I know the theme is the default one. I''ll get to it.',
'Moving to WordPress', '', 'publish', 'open', 'open', 'moving-to-wordpress', '', '', '', 0, 'http://127.0.0.1:8901/?p=8', 0, 'post', 1),

(2, 1, '2007-05-28 21:45:00', '2007-05-28 21:45:00', '2007-06-02 10:10:00', '2007-06-02 10:10:00',
'I''m Dave. I write software for an insurance company during the day, which is less interesting than it sounds, and I spend too much of the rest of my time reading about computers and occasionally building them.

This blog is mostly hardware, software and gadgets, plus whatever I''m annoyed about that week. It moved here from Blogger in May 2007.

You can reach me at dave at this domain.',
'About', '', 'publish', 'open', 'open', 'about', '', '', '', 0, 'http://127.0.0.1:8901/?page_id=2', 0, 'page', 0),

(9, 1, '2007-05-28 21:50:00', '2007-05-28 21:50:00', '2007-05-28 21:50:00', '2007-05-28 21:50:00',
'', 'Archives', '', 'publish', 'closed', 'closed', 'archives', '', '', '', 0, 'http://127.0.0.1:8901/?page_id=9', 0, 'page', 0);

INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (9, '_wp_page_template', 'archives.php'), (2, '_wp_page_template', 'default');

INSERT INTO wp_post2cat (post_id, category_id) VALUES
 (7, 5), (7, 6), (6, 4), (6, 7), (5, 3), (4, 4), (3, 7), (1, 5), (8, 1);
UPDATE wp_categories c SET category_count = (SELECT COUNT(*) FROM wp_post2cat p WHERE p.category_id = c.cat_ID) WHERE cat_ID <> 2;

INSERT INTO wp_comments (comment_post_ID, comment_author, comment_author_email, comment_author_url, comment_author_IP, comment_date, comment_date_gmt, comment_content, comment_karma, comment_approved, comment_agent, comment_type, comment_parent, user_id) VALUES
 (7, 'Mike', 'mike@example.com', 'http://mikes-photos.example/', '127.0.0.1', '2007-08-02 11:02:00', '2007-08-02 11:02:00', 'Told you you''d cave. How''s the camera? Mine takes everything slightly yellow indoors.', 0, '1', '', '', 0, 0),
 (7, 'Jen K.', 'jen@example.com', '', '127.0.0.1', '2007-08-02 13:47:00', '2007-08-02 13:47:00', 'The no copy and paste thing would drive me insane. I''m waiting for version 2.', 0, '1', '', '', 0, 0),
 (7, 'Dave', 'dave@example.com', '', '127.0.0.1', '2007-08-02 14:20:00', '2007-08-02 14:20:00', 'Mike: indoors it''s pretty bad, outdoors it''s fine. It''s a 2 megapixel camera on a phone, I''m keeping my expectations low.', 0, '1', '', '', 0, 1),
 (6, 'Rob', 'rob@example.com', 'http://robsblog.example/', '127.0.0.1', '2007-07-27 08:15:00', '2007-07-27 08:15:00', 'Same story with my scanner. Ended up buying a new one rather than keep an XP box around just for it.', 0, '1', '', '', 0, 0),
 (6, 'Sam', 'sam@example.com', '', '127.0.0.1', '2007-07-27 19:31:00', '2007-07-27 19:31:00', 'Agree on the Start menu search. I can''t go back to XP at work now without missing it.', 0, '1', '', '', 0, 0),
 (5, 'Mike', 'mike@example.com', 'http://mikes-photos.example/', '127.0.0.1', '2007-07-18 21:10:00', '2007-07-18 21:10:00', 'Nice. What are you doing with the old Athlon?', 0, '1', '', '', 0, 0),
 (5, 'Dave', 'dave@example.com', '', '127.0.0.1', '2007-07-18 21:34:00', '2007-07-18 21:34:00', 'File server, probably. Or it sits in the closet for two years like the last one.', 0, '1', '', '', 0, 1),
 (5, 'tk421', 'tk@example.com', '', '127.0.0.1', '2007-07-19 10:02:00', '2007-07-19 10:02:00', 'E6600 will do 3GHz on the stock cooler without trying. Just saying.', 0, '1', '', '', 0, 0),
 (5, 'Jen K.', 'jen@example.com', '', '127.0.0.1', '2007-07-19 12:40:00', '2007-07-19 12:40:00', '"labelled for ants" made my morning.', 0, '1', '', '', 0, 0),
 (4, 'Rob', 'rob@example.com', 'http://robsblog.example/', '127.0.0.1', '2007-07-05 16:22:00', '2007-07-05 16:22:00', 'Add the Web Developer toolbar to that list.', 0, '1', '', '', 0, 0),
 (1, 'Sam', 'sam@example.com', '', '127.0.0.1', '2007-06-08 19:30:00', '2007-06-08 19:30:00', 'Strap. Use the strap.', 0, '1', '', '', 0, 0),
 (1, 'Mike', 'mike@example.com', 'http://mikes-photos.example/', '127.0.0.1', '2007-06-09 09:12:00', '2007-06-09 09:12:00', 'Bring it over Saturday, I''ve been practising.', 0, '1', '', '', 0, 0),
 (8, 'Jen K.', 'jen@example.com', '', '127.0.0.1', '2007-05-31 08:50:00', '2007-05-31 08:50:00', 'Welcome to the club. The default theme is fine, everyone has it.', 0, '1', '', '', 0, 0);
