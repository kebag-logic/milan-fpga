#!/usr/bin/env bash
# status.sh: one look at this round's running gates.
S=<scratch>
date +%T
for d in a b c agg; do
  f=$S/drive-$d.log; [ -f "$f" ] || continue
  printf 'driver %s: %s steps rc=0, bad: %s | %s\n' "$d" "$(grep -c 'rc=0$' "$f")" \
    "$(grep -E 'rc=[1-9]' "$f" | tr '\n' ' ')" "$(grep '^== ' "$f" | tail -1)"
done
tail -1 $S/waiter.log
for n in ctrl_nvm_selftest twin; do
  r=$S/gates/run/logs/extra.$n.rc; [ -f "$r" ] && echo "extra $n rc=$(cat $r)"
done
for k in 0 1 2 3; do
  printf 'shard %s: %s logs\n' $k "$(ls $S/sweep/shard-$k/logs/*.log 2>/dev/null | wc -l)"
done
systemctl --user list-units 'milan-823-a753e*' --no-legend --plain | awk '{print $1, $4}' | tr '\n' ' '; echo
grep MemAvailable /proc/meminfo
