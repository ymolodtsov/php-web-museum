# museum-php56-legacy plus libfaketime, so PHP-Nuke's clock reads Sunday 14 March 2004
# (header date, Who's Online, "Big Story of Today", forum times are all computed from time()),
# plus import_request_variables() which PHP-Nuke 7.1's mainfile.php needs and PHP 5.4 removed.
FROM museum-php56-legacy
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1
COPY shim.php /usr/local/lib/phpnuke-shim.php
COPY zz-phpnuke.ini /usr/local/etc/php/conf.d/zz-phpnuke.ini
