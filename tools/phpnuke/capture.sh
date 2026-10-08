#!/bin/bash
# Capture the running PHP-Nuke 7.1 site (see build.sh) into exhibits/php-nuke.
set -e
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
PORT=8904
M='/modules.php?name='
P=()
page() { P+=(--page "$1=$2"); }
alias_() { P+=(--alias "$1=$2"); }

# forums first: the forum's who-is-online list only counts sessions from the last five minutes
page "${M}Forums" forums.html
alias_ "${M}Forums&file=index" forums.html
for f in 1 2 3 4 5 6; do page "${M}Forums&file=viewforum&f=$f" forum-$f.html; done
for t in 1 2 3 4 5 6 7 8 9; do page "${M}Forums&file=viewtopic&t=$t" forum-topic-$t.html; done
# "last post" links point at a post id; map each post to its topic page
while read -r p t; do alias_ "${M}Forums&file=viewtopic&p=$p" forum-topic-$t.html; done \
  < <(docker exec museum-db mysql -uroot -pmuseum phpnuke -N -e "SELECT post_id, topic_id FROM nuke_bbposts")

page / index.html
for s in $(seq 1 14); do page "${M}News&file=article&sid=$s" article-$s.html; done
for t in $(seq 1 11); do page "${M}News&new_topic=$t" topic-$t.html; done
page "${M}Topics" topics.html
page "${M}Downloads" downloads.html
for c in 1 2 3 4; do page "${M}Downloads&d_op=viewdownload&cid=$c" downloads-cat-$c.html; done
for l in $(docker exec museum-db mysql -uroot -pmuseum phpnuke -N -e "SELECT CONCAT(lid,'|',REPLACE(title,' ','_')) FROM nuke_downloads_downloads"); do
  page "${M}Downloads&d_op=viewdownloaddetails&lid=${l%%|*}&ttitle=${l#*|}" download-${l%%|*}.html
done
page "${M}Downloads&d_op=NewDownloads" downloads-new.html
page "${M}Downloads&d_op=MostPopular" downloads-popular.html
page "${M}Web_Links" links.html
for c in 1 2 3 4; do page "${M}Web_Links&l_op=viewlink&cid=$c" links-cat-$c.html; done
page "${M}Web_Links&l_op=NewLinks" links-new.html
page "${M}Web_Links&l_op=MostPopular" links-popular.html
page "${M}Surveys" surveys.html
page "${M}Surveys&op=results&pollID=2" survey-results-2.html
alias_ "${M}Surveys&op=results&pollID=2&mode=&order=&thold=" survey-results-2.html
page "${M}Surveys&op=results&pollID=1" survey-results-1.html
alias_ "${M}Surveys&op=results&pollID=1&mode=&order=&thold=" survey-results-1.html
page "${M}Surveys&pollID=2" survey-2.html
page "${M}Surveys&pollID=1" survey-1.html
page "${M}Top" top10.html
page "${M}Statistics" statistics.html
page "${M}Statistics&op=Stats" statistics-detailed.html
page "${M}Stories_Archive" archive.html
page "${M}Stories_Archive&sa=show_month&year=2004&month=03&month_l=March" archive-2004-03.html
page "${M}Stories_Archive&sa=show_month&year=2004&month=02&month_l=February" archive-2004-02.html
page "${M}Search" search.html
page "${M}Submit_News" submit-news.html
page "${M}Your_Account" account.html
page "${M}Your_Account&op=new_user" account-new.html
for u in chris deb_hacker gnomeuser2k kernel_tinkerer slackbob penguinista mwalsh tuxfan04; do
  page "${M}Your_Account&op=userinfo&username=$u" user-$u.html
done
page "${M}Recommend_Us" recommend.html
page "${M}Feedback" feedback.html
page "${M}Journal" journal.html
page "${M}Private_Messages" messages.html
page "${M}WebMail" webmail.html
page "${M}AvantGo" avantgo.html

cd "$ROOT"
python3 tools/phpnuke/capture_nuke.py --base http://127.0.0.1:$PORT --out exhibits/php-nuke "${P[@]}"
