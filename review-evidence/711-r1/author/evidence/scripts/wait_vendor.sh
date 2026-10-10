#!/bin/bash
# Wait at most $1 seconds for the next line of the vendor driver log or the given rc file; print state (scratch).
root=$SCRATCH
limit=${1:-500}; want=${2:-}
before=$(wc -l < $root/vendor/driver.log)
end=$((SECONDS+limit))
while [ $SECONDS -lt $end ]; do
  [ "$(wc -l < $root/vendor/driver.log)" != "$before" ] && break
  [ -n "$want" ] && [ -e "$root/vendor/$want" ] && break
  kill -0 483110 2>/dev/null || break
  sleep 20
done
date -Is; tail -3 $root/vendor/driver.log
kill -0 483110 2>/dev/null && echo "flock 483110 alive" || echo "flock 483110 gone"
