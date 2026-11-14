#!/bin/bash
# wait_r4.sh SECONDS: wait (at most SECONDS) until a CPU range is free, a queued part's build is ready, or a new R4
# leg exits; then run one tick. Foreground, polling every 20 s.
set -u
M=$MANAGEMENT/2026-09-23
S4=$M/895-a775/round4/scripts
T=/data-2/milan/tmp/895-a775
end=$(( $(date +%s) + $1 ))
n0=$(ls $T/legs/R4-*.rc 2>/dev/null | wc -l)
ready() { while read -r k a b c; do [ "$k" = part ] && [ -x "$T/builds/$a/native/Vsim" ] && return 0; [ "$k" = leg ] && return 1; done < $S4/legs.queue; return 1; }
while [ $(date +%s) -lt $end ]; do
  python3 $M/cpu_ranges.py show | grep -q "half8 \[\]" || break
  python3 $M/cpu_ranges.py show | grep -q "free12 \[\]" || break
  [ $(ls $T/legs/R4-*.rc 2>/dev/null | wc -l) -gt $n0 ] && break
  sleep 20
done
date +%T; python3 $M/cpu_ranges.py show | head -1
bash $S4/tick_r4.sh
