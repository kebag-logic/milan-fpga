#!/usr/bin/env bash
# Re-measure the srp_top README's slope-control table: each slope patch at each
# admission shape alone (the suite's `make` stops at the first failing shape).
# Usage: slope_shapes.sh <head checkout> <work dir> <jobs>; VERILATOR exported.
set -u
head=$1 work=$2 jobs=$3
mkdir -p "$work"
one() { # label N
  local t="$work/$1-N$2"; rm -rf "$t"; mkdir -p "$t/tb"
  cp -r "$head/hdl" "$t/hdl"; cp -r "$head/tb/srp_admission" "$t/tb/srp_admission"; cp -r "$head/tb/common" "$t/tb/common"; rm -rf "$t"/tb/srp_admission/obj_*
  (cd "$t" && git apply "$head/tb/srp_top/mutations/$1.patch") || { echo "$1 N=$2 PATCH-FAILED"; return; }
  make -C "$t/tb/srp_admission" run N="$2" > "$t.log" 2>&1
  echo "$1 N=$2 rc=$? $(grep -h 'checks:' "$t.log" | tail -1)"
}
export -f one; export head work
for l in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  for n in 1 2 3 5 8; do echo "$l $n"; done
done | xargs -P "$jobs" -n 2 bash -c 'one "$0" "$1"' | sort
