#!/usr/bin/env bash
S=<scratch>
echo "$(date +%H:%M) $(tail -1 $S/rec/memwatch.log | cut -d' ' -f2-)"
for d in base-camps head-camps head-cons head-ooc; do
  printf "%s: " $d
  for f in $S/rec/$d/*.rc; do [ -f "$f" ] && printf "%s=%s " $(basename $f .rc) $(cat $f); done 2>/dev/null
  echo
done
for d in base-camps head-camps; do
  for l in $S/rec/$d/*.log; do
    c=$(basename $l .log); [ -f $S/rec/$d/$c.rc ] && continue
    printf "%s %s running: %s arms\n" $d $c $(grep -cE ": rc=-?[0-9]+ failures=" $l)
  done
done
