FROM php:5.6-apache
RUN sed -i 's|deb.debian.org|archive.debian.org|g; s|security.debian.org|archive.debian.org|g; /stretch-updates/d' /etc/apt/sources.list \
 && apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends libpng-dev libjpeg-dev libfreetype6-dev wget \
 && docker-php-ext-configure gd --with-jpeg-dir=/usr --with-png-dir=/usr --with-freetype-dir=/usr \
 && docker-php-ext-install mysql mysqli gd \
 && a2enmod rewrite \
 && rm -rf /var/lib/apt/lists/*
RUN { echo 'error_reporting = E_ALL & ~E_NOTICE & ~E_STRICT & ~E_DEPRECATED'; echo 'display_errors = Off'; echo 'short_open_tag = On'; echo 'date.timezone = UTC'; echo 'magic_quotes_gpc = Off'; } > /usr/local/etc/php/conf.d/museum.ini
COPY legacy-shim.php /usr/local/lib/php-legacy-shim.php
