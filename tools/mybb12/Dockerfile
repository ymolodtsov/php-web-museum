# museum-php56 plus libfaketime, so MyBB's clock reads 27 March 2007 ("Today"/"Yesterday",
# header "last visit", Who's Online cut-off, birthdays and the calendar month are computed from time()).
FROM museum-php56
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends libfaketime \
 && ln -s /usr/lib/*-linux-gnu/faketime/libfaketime.so.1 /usr/local/lib/libfaketime.so.1 \
 && rm -rf /var/lib/apt/lists/*
