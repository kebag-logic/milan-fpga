#!/usr/bin/env bash
# Run one suite exactly as scripts/run_all_suites.sh does (`make -C <suite>`, log captured,
# no -j), pinned to a CPU set, from a clean suite directory, and record the wall time.
#   timed_suite.sh <tree> <suite> <cpus> <make-bin-dir|system> <label>
# Output: logs/<label>.log (suite log), logs/<label>.time (summary)
set -uo pipefail
tree=$1; suite=$2; cpus=$3; makedir=$4; label=$5
W=$VALIDATION_STORAGE/617-a434-work
d="$tree/tb/verilator/$suite"
path=$VALIDATION_TOOLS/verilator-v5.050/bin:$PATH
[ "$makedir" != system ] && path="$makedir:$path"
make -s -C "$d" clean >/dev/null 2>&1
rm -rf "$d/obj_dir" "$d/obj_dp"
{
  echo "label: $label"
  echo "tree: $tree ($(git -C "$tree" rev-parse HEAD 2>/dev/null || echo export))"
  echo "suite: $suite"
  echo "cpus: $cpus (nproc under taskset: $(taskset -c "$cpus" nproc))"
  echo "make: $(env PATH="$path" make --version | head -1)"
  echo "verilator: $(env PATH="$path" verilator --version)"
  echo "loadavg at start: $(cat /proc/loadavg)"
  echo "start: $(date -Is)"
} > "$W/logs/$label.time"
t0=$(date +%s.%N)
env PATH="$path" taskset -c "$cpus" /usr/bin/time -v -o "$W/logs/$label.rusage" \
  make -C "$d" > "$W/logs/$label.log" 2>&1
rc=$?
t1=$(date +%s.%N)
{
  echo "end: $(date -Is)"
  echo "loadavg at end: $(cat /proc/loadavg)"
  echo "rc: $rc"
  printf 'wall_s: %.1f\n' "$(echo "$t1 - $t0" | bc)"
  grep -E 'Maximum resident|Percent of CPU|User time|System time' "$W/logs/$label.rusage"
} >> "$W/logs/$label.time"
echo "$label done rc=$rc"
