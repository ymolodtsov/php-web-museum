# How exhibits are built

Exhibits are snapshots of the original software, not lookalikes. Never hand-write
HTML/CSS that imitates a system, never replace its images with CSS boxes, and never
invent its colours. Everything visual must come from the real release (or, for
closed-source systems, from real archived pages).

## Open-source systems: run the real release, then capture

1. Download the original release that matches the exhibit's era from an official
   or long-standing archive (project download site, SourceForge, GitHub tags,
   ftp.drupal.org, releases.wikimedia.org, wordpress.org/download/release-archive).
   Prefer the newest point release of the target branch that predates the
   exhibit's archive date.
2. Run it in Docker, localhost only:
   - images: `museum-php56` (PHP 5.6 + Apache, mysql/mysqli/gd) and
     `museum-php56-legacy` (same, plus register_globals / `$HTTP_*_VARS` /
     `session_register()` emulation for 2002-2005 code). Dockerfiles in tools/docker.
   - database: the shared `museum-db` container (MariaDB 10.3, sql_mode='',
     root password `museum`) on docker network `museum`. Create your own database
     named after the exhibit. Never stop, restart or remove `museum-db`, the
     `museum` network, or containers you didn't create.
   - `docker run -d --name museum-<slug> --network museum -p 127.0.0.1:<port>:80 -v <src>:/var/www/html <image>`
     Always bind to 127.0.0.1.
   - Old schemas may need `TYPE=MyISAM` -> `ENGINE=MyISAM` and similar
     MySQL-4-isms fixed in the install SQL. Fix the environment, not the theme.
3. Install through the software's own installer, keep the default theme/skin.
4. Seed content through the app's own admin UI or its own tables (SQL). Content
   must be period-correct for the exhibit's archive date (dates, versions,
   hardware, games, prices). Write mundane, believable text. ASCII or the app's
   native encoding.
5. Make the app's clock match the archive date: run the container under
   libfaketime (examples: tools/punbb12/Dockerfile, tools/xoops2/Dockerfile) so
   "Today", "x hours ago", header dates and online lists are the software's own
   output. Post-process only what the browser computes (e.g. a JS clock).
6. Capture: `python3 tools/capture.py --base http://127.0.0.1:<port> --out exhibits/<slug> --page '/<url>=<file>.html' ...`
   It downloads same-origin assets with their original paths, rewrites links
   between captured pages, turns every other link into `#`, makes forms inert,
   and adds the museum return bar. Capture enough pages that the main navigation
   leads somewhere real (front page, a listing, a detail page, a profile/about).
7. Back up the previous exhibit folder to the scratchpad before overwriting, and
   remove files from the old hand-built version that are no longer referenced.
8. Keep the seed script/SQL in `tools/<slug>/` so the exhibit can be rebuilt.
9. Stop and remove your app container when done (keep the database).

## Closed-source systems (vBulletin, IPB): real archived pages

Use the Wayback Machine's raw mode (`https://web.archive.org/web/<timestamp>id_/<url>`)
to fetch original HTML, CSS and images from a real forum of the right era that ran
the stock default style. Use that markup as the page, and replace the community's
content (names, threads, posts, stats) with the exhibit's fictional content. Keep
the software's own logo/branding as shipped in the default style; remove the host
site's own branding.

## Verification

Open the exhibit via the local static server (http://127.0.0.1:8842/exhibits/<slug>/)
at 1024x768 and 800x600 and compare against a real archived screenshot/page of the
same software version. If anything is missing (images, CSS) the capture is wrong.
