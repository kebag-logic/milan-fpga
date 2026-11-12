#!/bin/bash
# Each leg's groups with a finished log (SUMMARY in its tail) over its list, and the save groups' log sizes.
T=<scratch>
for n in GA8 GA1 GN8 GN1 D1; do
  total=$(tr ',' '\n' < $T/groups-$n.txt | grep -c .)
  done_=0
  for g in $(tr ',' ' ' < $T/groups-$n.txt); do
    for f in $T/builds/$n/results-*/$g.log; do [ -f "$f" ] && tail -c 3000 "$f" | grep -q SUMMARY && { done_=$((done_+1)); break; }; done
  done
  echo "$n $done_/$total $(cat $T/logs/$n.log.rc 2>/dev/null)"
done
ls -la $T/builds/GA8/results-save-*/save-*.log $T/builds/GA1/results-save-second/save-second.log 2>/dev/null | awk '{print $5, $9}' | sed 's#.*/builds/##'
