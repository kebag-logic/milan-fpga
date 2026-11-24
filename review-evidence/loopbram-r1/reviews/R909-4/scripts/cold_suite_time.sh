#!/usr/bin/env bash
# Time one Verilator suite's sweep command cold on four pinned CPUs.
# Usage: cold_suite_time.sh <repo> <scratch-dir> <suite> <cpu-list> <receipt-dir>
# Exports the repo's HEAD into a fresh copy (submodules symlinked from <repo>),
# records the load average, then runs `make -C tb/verilator/<suite>` under taskset.
set -u
repo=$1; scratch=$2; suite=$3; cpus=$4; out=$5
d="$scratch/cold-$suite"
rm -rf "$d"; mkdir -p "$d"
git -C "$repo" archive HEAD | tar -x -C "$d"
git -C "$repo" config -f .gitmodules --get-regexp '\.path$' 2>/dev/null | awk '{print $2}' |
while read -r m; do rmdir "$d/$m" 2>/dev/null; ln -sfn "$repo/$m" "$d/$m"; done
log="$out/cold-$suite.log"
{
  echo "head $(git -C "$repo" rev-parse HEAD) suite $suite cpus $cpus verilator $(verilator --version)"
  echo "loadavg-before $(cat /proc/loadavg)"
  start=$(date +%s.%N)
  taskset -c "$cpus" make -C "$d/tb/verilator/$suite" > "$out/cold-$suite.make.log" 2>&1
  rc=$?
  end=$(date +%s.%N)
  echo "loadavg-after $(cat /proc/loadavg)"
  echo "rc=$rc wall_s=$(echo "$end - $start" | bc)"
  grep -E 'PASS|FAIL|RESULT|checks' "$out/cold-$suite.make.log" | tail -4
} > "$log" 2>&1
cat "$log"
