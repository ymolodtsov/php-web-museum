# PHP Web Museum

A museum of the PHP-powered web of the 2000s: the forums, portals, blogs, wikis and shops that ran on phpBB, vBulletin, PHP-Nuke, Joomla, WordPress and friends.

Every exhibit is a small fictional website built on the original software. I install a period release in an old PHP 5 environment, keep its default theme, fill it with invented content that fits the exhibit's archive date, and save the pages it produces as static HTML. The two closed-source forums (vBulletin and Invision Power Board) are built from real 2006–2007 pages saved by the Wayback Machine instead.

The result is plain static files: no PHP, no database, no build step to view it.

## Exhibits

| Exhibit | Software | Archive date |
|---|---|---|
| Pixel Arena Forums | phpBB 2.0.x (subSilver) | 17 Oct 2006 |
| Overclock Hardware Forums | vBulletin 3.6.4 | 12 Feb 2007 |
| Soundwave Music Community | Invision Power Board 2.1.5 | 4 May 2006 |
| Aperture Photography Community | Simple Machines Forum 1.1.3 | 21 Jul 2007 |
| /dev/null | PunBB 1.2.10 | 15 Jan 2006 |
| Inkwell | MyBB 1.2.3 | 27 Mar 2007 |
| Clearfix | Vanilla 1.1.5a | 16 Oct 2008 |
| Open Source Planet | PHP-Nuke 7.1 | 14 Mar 2004 |
| Northern Sky | PostNuke 0.750 (ExtraLite) | 20 Feb 2005 |
| Riverside Linux User Group | Mambo 4.5.1a (solarflare) | 14 Oct 2004 |
| Orbital Design Studio | Joomla 1.5.3 | 9 Jun 2008 |
| Open Computing History Project | Drupal 6.14 | 3 Nov 2009 |
| signal & noise | WordPress 2.2.1 (Kubrick) | 2 Aug 2007 |
| Nexus Gaming Portal | XOOPS 2.0.6 | 5 Apr 2004 |
| Clan Obsidian | e107 0.617 | 30 Jan 2005 |
| Retrocomputing Wiki | MediaWiki 1.10.2 (MonoBook) | 11 Sep 2007 |
| Wanderlens Travel Gallery | Coppermine 1.3.3 | 8 Jun 2005 |
| TechBits Computer Accessories | osCommerce 2.2 MS2 | 19 Nov 2004 |

A phpBB 3 exhibit is on the way.

## Viewing it locally

```sh
python3 tools/serve.py
```

Then open http://127.0.0.1:8842/. Any static web server works; `serve.py` just turns off browser caching while you edit.

The guestbook is the only dynamic part: two small Vercel functions in `api/` (a server-drawn captcha and the entry list) with entries stored in Vercel Blob. Run `vercel dev` to try it locally; under a plain static server the guestbook shows an error.

## How the exhibits are built

`tools/METHOD.md` describes the method. `tools/shell.py` applies the shared navigation, breadcrumbs and footer to the museum pages. Each exhibit has its own folder in `tools/` with a `build.sh` (or `build.py`) that downloads the original release, installs it in Docker, loads the content, and captures the pages with `tools/capture.py`. Rebuilding needs Docker; the base PHP 5.6 images are in `tools/docker/`.

## Credits and licences

The museum pages and build scripts are mine. The exhibits contain the original software's own templates, stylesheets, scripts and images, which belong to their authors and remain under their own licences (GPL for most of the open-source packages). vBulletin and Invision Power Board assets belong to their owners and are included for historical preservation.

Photos in the Coppermine and osCommerce exhibits are public domain or CC0 images from Wikimedia Commons; sources and authors are listed in `tools/coppermine/CREDITS.txt` and `tools/oscommerce22/CREDITS.txt`.

Made by Yury Molodtsov — [molodtsov.me](https://molodtsov.me/)
