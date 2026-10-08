# museum-php56 plus libfaketime, so Vanilla's own clock (relative "x hours ago" dates,
# "Last active" on profiles) reads as the exhibit's archive date.
FROM museum-php56
RUN apt-get -o Acquire::Check-Valid-Until=false update \
 && apt-get install -y --allow-unauthenticated --no-install-recommends libfaketime \
 && ln -s /usr/lib/*-linux-gnu/faketime/libfaketime.so.1 /usr/local/lib/libfaketime.so.1 \
 && rm -rf /var/lib/apt/lists/*
