# museum-php56-legacy plus libfaketime, so Mambo's clock reads 14 October 2004
# (the header date, Who's Online and "now" checks are computed from time()).
FROM museum-php56-legacy
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1
