#!/usr/bin/env bash
# status.sh: one look at this round's drivers, extras, sweep and resources.
S=<scratch>
date +%T; uptime | sed 's/.*load/load/'; grep MemAvailable /proc/meminfo
echo "unit memory.current $(( $(cat /sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-823-a753f.service/memory.current) / 1048576 )) MiB"
python3 <management>/2026-09-23/cpu_ranges.py show 2>&1 | tail -1
for f in $S/drive-*.log; do echo "== $(basename $f): $(grep -c 'rc=' $f) steps, $(grep -c 'rc=[1-9]' $f) nonzero; last: $(tail -n 1 $f)"; grep 'rc=[1-9]' $f; done
for f in $S/gates/run/logs/extra.*.rc; do [ -f "$f" ] && echo "$(basename $f): $(cat $f)"; done
ls $S/gates/run/logs/ 2>/dev/null | grep -v '\.rc$\|tree-after' | sed 's/^/  present: /'
tail -n 3 $S/sweep_waiter.log
systemctl --user list-units 'milan-823-a753f-*' --no-legend --plain | awk '{print "  unit", $1, $3, $4}'
for k in 0 1 2 3; do d=$S/sweep/shard-$k/logs; [ -d $d ] && echo "shard $k: $(ls $d | grep -c '\.log$') logs"; done
