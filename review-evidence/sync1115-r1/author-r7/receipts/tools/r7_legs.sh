#!/bin/bash
# r7_legs.sh SPEC...: each SPEC "name;clone;build;point;jobs;run.py args", one leg.sh run. Each starts once the one
# before it has built its native model (its log shows the model's COMMAND line) or ended, so one build runs at a time
# in the unit. A leg's precompiled headers (a compiler cache --reuse-build never reads) are dropped once its model is
# built. Logs: r7/logs/<name>.log and <name>.log.rc.
set -u
S=<scratch>; mkdir -p $S/r7/logs
for spec in "$@"; do
  IFS=';' read -r n c b p j a <<< "$spec"
  log=$S/r7/logs/$n.log; rm -f "$log.rc"
  # shellcheck disable=SC2086  # a: the leg's run.py arguments, split on spaces
  ( bash $S/bin/leg.sh "$c" "$b" "$p" "$j" $a > "$log" 2>&1; echo $? > "$log.rc" ) &
  until grep -q '^COMMAND .*native/Vsim ' "$log" 2>/dev/null || [ -f "$log.rc" ]; do sleep 20; done
  /usr/bin/find "$b/native" -maxdepth 1 -name 'Vsim__pch.h.*.gch' -delete 2>/dev/null
  echo "$n built $(date +%FT%T)"
done
wait
echo "DONE $(date +%FT%T)"
