#!/usr/bin/env bash
# At the final head: R763-9's stress_owner_report.py (3000, 8 at once) beside R764-9's repeat_control.sh (16 x 200),
# with BURNERS busy loops of this unit's own, on its own CPUs, ended through their own PIDs.
set -u
S=$VALIDATION_STORAGE/833-a726j
R=$MANAGEMENT/2026-09-23/833-a726j/receipts/final
B=${1:-16}
export TMPDIR=$S/tmp
grep SigIgn /proc/self/status > "$R/head-stress.sigign"
pids=()
for _ in $(seq "$B"); do python3 -c "while True: pass" & pids+=($!); done
sleep 60
cat /proc/loadavg > "$R/head-stress.load"
( while sleep 10; do cat /proc/loadavg; done ) > "$R/head-stress.loadsamples" & sampler=$!
rm -rf "$S/repeat-final"
( python3 -I "$S/probes/833-r763-9/stress_owner_report.py" "$S/wt-head" 3000 8 > "$R/r763-9-stress-final-head.log" 2>&1
  echo $? > "$R/r763-9-stress-final-head.rc" ) &
one=$!
( bash "$S/probes/833-r764-9/scripts/repeat_control.sh" "$S/wt-head" owner_report 16 200 "$S/repeat-final" \
    > "$R/r764-9-repeat-final-head.log" 2>&1; echo $? > "$R/r764-9-repeat-final-head.rc" ) &
two=$!
wait "$one" "$two"
kill "$sampler" "${pids[@]}"
wait 2>/dev/null
cat /proc/loadavg >> "$R/head-stress.load"
cat "$S"/repeat-final/red.* > "$R/r764-9-repeat-final-head.red" 2>/dev/null
head -3 "$R/r763-9-stress-final-head.log"; cat "$R/r764-9-repeat-final-head.log"
awk '{print $1}' "$R/head-stress.loadsamples" | sort -n | sed -n '1p;$p'
