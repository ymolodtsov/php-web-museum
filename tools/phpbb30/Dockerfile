# museum-php56 plus libfaketime, so phpBB's clock (header date, "Who is online", birthdays,
# "Last visit", relative join dates) reads as the exhibit's archive date.
FROM museum-php56
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends libfaketime \
 && ln -s /usr/lib/*-linux-gnu/faketime/libfaketime.so.1 /usr/local/lib/libfaketime.so.1 \
 && rm -rf /var/lib/apt/lists/*
# phpBB 3.0.2's installer probes for missing extensions with dl(), which PHP 5.3+ removed from
# the Apache SAPI (a fatal error); with enable_dl off it skips the probe, as on most 2008 hosts.
RUN echo 'enable_dl = Off' > /usr/local/etc/php/conf.d/museum-phpbb3.ini
