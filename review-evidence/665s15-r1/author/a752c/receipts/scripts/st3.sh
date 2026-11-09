#!/bin/bash
# One compact status block for round 3 resume at 7aa6ef0c.
T=$SCRATCH
echo "$(date +%T) units: $(systemctl --user list-units 'milan-665s15-a752c-*' --no-legend --state=active --plain | awk '{print $1}' | sed 's/milan-665s15-a752c-//; s/.service//' | tr '\n' ' ')"
echo "queue left: $(wc -l < $T/queue-3.txt); wf rc files: $(ls $T/gates-out/wf3/logs/*.rc 2>/dev/null | wc -l), nonzero: $(for f in $T/gates-out/wf3/logs/*.rc; do [ "$(cat $f)" != 0 ] && basename $f .rc; done 2>/dev/null | tr '\n' ' ')"
echo "lane: $(tail -n 1 $T/gates-out/lane-7aa6r/summary.txt 2>/dev/null); nonzero: $(grep -v 'rc=0\|start\|done' $T/gates-out/lane-7aa6r/summary.txt 2>/dev/null | tr '\n' ' ')"
for p in M32 M8 M1; do [ -f $T/runs/$p.head ] && echo "$p: $(grep -h -- '-rc' $T/runs/$p-build.time $T/runs/$p-run.time 2>/dev/null | tr '\n' ' ') $(tail -n 1 $T/runs/$p-run.log 2>/dev/null | cut -c1-110)"; done
[ -f $T/runs/twin.head ] && echo "twin: $(grep -h twin-rc $T/runs/twin-twin.time 2>/dev/null) $(tail -n 1 $T/runs/twin-twin.log | cut -c1-100)"
for k in 0 1 2 3; do f=$T/sweep3/shard-$k; [ -d $f ] && echo "shard$k: $(ls $f/logs 2>/dev/null | wc -l) logs $(cat $f/complete.json 2>/dev/null | head -c 100)"; done
grep MemAvailable /proc/meminfo
tail -n 3 $T/logs/665s15-a752c-sw3.txt
