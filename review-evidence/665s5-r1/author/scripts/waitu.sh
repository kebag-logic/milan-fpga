#!/bin/bash
# Wait up to SECONDS (default 540) for the named units to finish; print each one's state and its log's tail.
# usage: waitu.sh SECONDS NAME...
T=$1; shift
end=$(( $(date +%s) + T ))
while [ "$(date +%s)" -lt "$end" ]; do
  busy=0
  for n in "$@"; do systemctl --user is-active -q "milan-665s5-a702-$n" && busy=1; done
  [ $busy = 0 ] && break
  read -t 15 < /dev/zero 2>/dev/null || true
  timeout 15 tail -f /dev/null 2>/dev/null
done
for n in "$@"; do echo "$n: $(systemctl --user is-active "milan-665s5-a702-$n" 2>/dev/null)"; done
grep MemAvailable /proc/meminfo
