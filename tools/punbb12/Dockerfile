# museum-php56 plus libfaketime, so PunBB's clock reads 15 January 2006
# ("Today"/"Yesterday" labels and the users-online list are computed from time()).
FROM museum-php56
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1
