# museum-php56 plus libfaketime, so SMF's "now" (header date, "Today at", posts per day,
# calendar month) reads as the exhibit's archive date.
FROM museum-php56
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends libfaketime \
 && ln -s /usr/lib/*-linux-gnu/faketime/libfaketime.so.1 /usr/local/lib/libfaketime.so.1 \
 && rm -rf /var/lib/apt/lists/*
# SMF appends PHPSESSID to every link for visitors that send no cookies (like the capture
# tool). Give every request a harmless cookie, as a normal browser would have.
RUN a2enmod headers \
 && echo 'RequestHeader setifempty Cookie "cookies=1"' > /etc/apache2/conf-enabled/museum-cookie.conf
