#!/usr/bin/env bash
# Run the gate list (gates/gates.tsv: stream, name, command) from the lane's physical path,
# one sequential stream per stream id, each gate's output to its own log (never piped),
# and its rc and seconds to gates/summary-<stream>.txt.
#   run_gates.sh <cpus>
set -u
cpus=$1
LANE=$LANES/617-capture-frame-atomic
G=$VALIDATION_STORAGE/617-a434-work/gates
export PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$PATH
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
mkdir -p "$G/logs"
stream() {
  local s=$1
  : > "$G/summary-$s.txt"
  while IFS=$'\t' read -r id name cmd; do
    [ "$id" = "$s" ] || continue
    local t0 t1 rc
    t0=$(date +%s)
    ( cd "$LANE" && taskset -c "$cpus" bash -c "$cmd" ) > "$G/logs/$name.log" 2>&1
    rc=$?
    t1=$(date +%s)
    printf '%s %s :: %s (%s s)\n' "$rc" "$name" "$cmd" "$((t1 - t0))" >> "$G/summary-$s.txt"
  done < "$G/gates.tsv"
  echo "stream $s done" >> "$G/summary-$s.txt"
}
for s in 0 1 2 3; do stream "$s" & done
wait
echo "all streams done"
