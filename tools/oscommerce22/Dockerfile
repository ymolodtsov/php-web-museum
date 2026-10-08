# museum-php56-legacy plus libfaketime, so osCommerce's clock reads 19 November 2004
# (footer date, "New Products For November", review/order timestamps written at runtime).
# default_charset is cleared so PHP sends no charset header, as PHP 4 did; osCommerce's
# own <meta> tag (iso-8859-1) then decides the encoding.
FROM museum-php56-legacy
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends faketime \
 && rm -rf /var/lib/apt/lists/* \
 && ln -s "$(dirname "$(find /usr/lib -name libfaketime.so.1 | head -1)")/libfaketime.so.1" /usr/local/lib/libfaketime.so.1 \
 && echo 'default_charset = ""' > /usr/local/etc/php/conf.d/zz-oscommerce.ini
