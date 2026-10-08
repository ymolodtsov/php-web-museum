# museum-php56-legacy plus libfaketime, so the app's clock reads 5 April 2004.
FROM museum-php56-legacy
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1
