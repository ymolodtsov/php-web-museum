# museum-php56-legacy plus libfaketime, so PostNuke's clock reads Sunday 20 February 2005
# (header date, Who's Online, "Today's Big Story", forum times are all computed from time()).
FROM museum-php56-legacy
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1
COPY zz-postnuke.ini /usr/local/etc/php/conf.d/zz-postnuke.ini
COPY shim.php /usr/local/lib/postnuke-shim.php
