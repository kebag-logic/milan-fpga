#!/bin/bash
# repeat_control.sh TREE CONTROL WORKERS RUNS_PER_WORKER OUTDIR
# Runs one owner control WORKERS-at-once, RUNS_PER_WORKER times each, recording every rc and red output.
tree=$1 control=$2 workers=$3 runs=$4 out=$5
mkdir -p "$out"
worker() {
  local w=$1 i
  for ((i = 0; i < runs; i++)); do
    o=$(python3 -B "$tree/scripts/test_suite_cancellation.py" --control "$control" 2>&1); rc=$?
    echo "$w $i $rc $(cut -d' ' -f1-3 /proc/loadavg)" >> "$out/rc.$w"
    [ "$rc" = 0 ] || printf '=== worker %s run %s rc %s\n%s\n' "$w" "$i" "$rc" "$(tail -4 <<<"$o")" >> "$out/red.$w"
  done
}
for ((w = 0; w < workers; w++)); do worker $w & done
wait
cat "$out"/rc.* | awk '{n++; if ($3 != 0) r++; l += $4} END {printf "runs %d red %d mean_load1 %.1f\n", n, r, l / n}'
