#!/bin/bash
# wait.sh SECONDS FILE...: return when every FILE exists, or after SECONDS.
t=$1; shift; end=$((SECONDS + t))
while [ $SECONDS -lt $end ]; do
  all=1; for f in "$@"; do [ -e "$f" ] || all=0; done
  [ $all = 1 ] && exit 0
  sleep 20
done
exit 1
