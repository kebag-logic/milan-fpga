#!/usr/bin/env bash
# status.sh: one look at every unit of this round, the drivers' failures and the sweep's suites.
S=<scratch>
date +%T; uptime | sed 's/.*load/load/'; grep MemAvailable /proc/meminfo
python3 <management>/2026-09-23/cpu_ranges.py show 2>&1 | tail -1
systemctl --user list-units 'milan-823-a753d-*' --no-legend --plain | awk '{print $1, $3, $4}'
for f in $S/drive-*.log; do echo "== $(basename $f): $(grep -c 'rc=' $f) steps, $(grep -c 'rc=[1-9]' $f) nonzero; last: $(tail -n 1 $f)"; grep 'rc=[1-9]' $f; done
for k in 0 1 2 3; do d=$S/sweep/shard-$k/logs; n=$(ls $d 2>/dev/null | grep -c '\.log$'); echo "shard $k: $n logs; $(ls -t $d 2>/dev/null | head -n 2 | tr '\n' ' ')"; done
for f in $S/gates/run/logs/extra.*.rc; do [ -f "$f" ] && echo "$(basename $f): $(cat $f)"; done 2>/dev/null
