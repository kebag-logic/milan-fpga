#!/bin/sh
# Run probe.sh jobs from a job file, at most 8 in parallel, in the foreground.
# job line: <name> <src-tree> <mutant|none> <harness>
# Receipt: receipts/probes/<name>.log, with the exit status as its last line.
set -eu
JOBS=$1
PKT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$PKT/receipts/probes"
export PKT
grep -v '^#' "$JOBS" | grep -v '^$' | xargs -P 8 -L 1 sh -c '
  name=$0; src=$1; mut=$2; h=$3
  case "$src" in /*) ;; *) src="$PKT/$src" ;; esac
  log="$PKT/receipts/probes/$name.log"
  echo "probe $name src=$(basename "$src") mutant=$mut harness=$h" >"$log"
  set +e
  sh "$PKT/scripts/${PROBE:-probe.sh}" "$src" "$PKT/scratch/work/$name" "$mut" "$h" >>"$log" 2>&1
  rc=$?
  if [ $rc -ne 0 ] && [ -f "$PKT/scratch/work/$name/tb/verilator/mmcm_servo/build.log" ]; then
    tail -n 20 "$PKT/scratch/work/$name/tb/verilator/mmcm_servo/build.log" >>"$log"
  fi
  echo "EXIT $rc" >>"$log"
'
for f in "$PKT"/receipts/probes/*.log; do printf '%s %s\n' "$(basename "$f" .log)" "$(tail -n 1 "$f")"; done
