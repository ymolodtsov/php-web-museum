#!/bin/bash
# Capture the running PostNuke 0.750 site (see build.sh) into exhibits/postnuke.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PORT=8914
M='/modules.php?op=modload&name='
F='/index.php?name=PNphpBB2&file='
P=()
page() { P+=(--page "$1=$2"); }
alias_() { P+=(--alias "$1=$2"); }
sqlq() { docker exec museum-db mysql -uroot -pmuseum postnuke -N -e "$1"; }

# forums first: PNphpBB2's who-is-online only counts sessions from the last five minutes
page "${F}index" forums.html
alias_ "${M}PNphpBB2&file=index" forums.html
for c in 1 2; do page "${F}index&c=$c" forums-cat-$c.html; done
for f in 1 2 3 4 5 6; do page "${F}viewforum&f=$f" forum-$f.html; done
for t in $(sqlq "SELECT topic_id FROM nuke_phpbb_topics"); do
  page "${F}viewtopic&t=$t" forum-topic-$t.html
  alias_ "${F}viewtopic&t=$t&start=0&postdays=0&postorder=asc&highlight=" forum-topic-$t.html
done
# "last post" links point at a post id; map each post to its topic page
while read -r p t; do alias_ "${F}viewtopic&p=$p" forum-topic-$t.html; done < <(sqlq "SELECT post_id, topic_id FROM nuke_phpbb_posts")
# PNphpBB2 1.2g only shows profiles and the member list to logged-in members; guests get the login form
page "${F}login" forum-login.html
for u in $(sqlq "SELECT user_id FROM nuke_phpbb_users WHERE user_id>1"); do
  alias_ "${F}profile&mode=viewprofile&u=$u" forum-login.html
done
alias_ "${F}memberlist" forum-login.html
page "${F}viewonline" forum-online.html
page "${F}faq" forum-faq.html

page / index.html
alias_ "${M}News&file=index" index.html
for s in $(sqlq "SELECT pn_sid FROM nuke_stories"); do
  page "${M}News&file=article&sid=$s&mode=thread&order=0&thold=0" article-$s.html
  alias_ "${M}News&file=article&sid=$s" article-$s.html
  page "/print.php?sid=$s" print-$s.html
done
for c in 1 2 3; do
  page "${M}News&file=index&catid=$c" category-$c.html
  alias_ "${M}News&file=index&catid=$c&topic=" category-$c.html
done
for t in $(sqlq "SELECT pn_topicid FROM nuke_topics"); do page "${M}News&file=index&catid=&topic=$t" topic-$t.html; done
page "${M}Topics&file=index" topics.html
page "${M}NS-Polls&file=index" polls.html
for p in 1 2; do
  page "${M}NS-Polls&file=index&req=results&pollID=$p&mode=thread&order=0&thold=0" poll-results-$p.html
  alias_ "${M}NS-Polls&file=index&req=results&pollID=$p" poll-results-$p.html
  page "${M}NS-Polls&file=index&pollID=$p" poll-$p.html
done
page "${M}Downloads&file=index" downloads.html
for c in 1 2 3 4; do page "${M}Downloads&file=index&req=viewdownload&cid=$c" downloads-cat-$c.html; done
for l in $(sqlq "SELECT pn_lid FROM nuke_downloads_downloads"); do
  page "${M}Downloads&file=index&req=viewdownloaddetails&lid=$l" download-$l.html
done
page "${M}Downloads&file=index&req=NewDownloads" downloads-new.html
page "${M}Downloads&file=index&req=MostPopular" downloads-popular.html
page "${M}Web_Links&file=index" links.html
for c in 1 2 3 4; do page "${M}Web_Links&file=index&req=viewlink&cid=$c" links-cat-$c.html; done
page "${M}Web_Links&file=index&req=NewLinks" links-new.html
page "${M}Web_Links&file=index&req=MostPopular" links-popular.html
page "${M}Members_List&file=index" members.html
for u in $(sqlq "SELECT pn_uname FROM nuke_users WHERE pn_uid>1"); do
  page "/user.php?op=userinfo&uname=$u" user-$u.html
  alias_ "/user.php?op=userinfo&uname=$u&module=NS-User" user-$u.html
done
page "${M}FAQ&file=index" faq.html
for c in 1 2; do page "${M}FAQ&file=index&myfaq=yes&id_cat=$c" faq-$c.html; done
page "${M}Reviews&file=index" reviews.html
page "${M}Reviews&file=index&req=All" reviews-all.html
for r in 1 2; do page "${M}Reviews&file=index&req=showcontent&id=$r" review-$r.html; done
page "${M}Stats&file=index" stats.html
page "${M}Top_List&file=index" toplist.html
page "${M}Search&file=index" search.html
page "${M}Sections&file=index" sections.html
page "${M}Recommend_Us&file=index" recommend.html
page "${M}AvantGo&file=index" avantgo.html
page "/user.php" account.html
page "/user.php?op=check_age&module=NS-NewUser" account-new.html
page "/user.php?op=loginscreen&module=NS-User" account-login.html
page "/user.php?op=lostpassscreen&module=NS-LostPassword" account-lostpass.html

cd "$ROOT"
python3 tools/postnuke/capture_pn.py --base http://127.0.0.1:$PORT --out exhibits/postnuke "${P[@]}"
