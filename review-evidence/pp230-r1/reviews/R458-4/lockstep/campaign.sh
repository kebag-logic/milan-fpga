#!/usr/bin/env bash
# R458-4 lockstep campaign. Usage: campaign.sh <head checkout> <base checkout> <work dir> <jobs>
# Positive: base against head at 1/1, 2/2, 3/5, 5/3, 8/8, 9/9, three seeds x
# 1,000,000 clocks each, 0 mismatching clocks required. Controls: each planted
# head edit (a checked-in campaign patch of the head) must mismatch at the
# shapes listed. Writes <work>/RESULTS.txt; exit 0 = all as required.
set -u
here=$(cd "$(dirname "$0")" && pwd)
head=$1 base=$2 work=$3 jobs=$4
mkdir -p "$work"
pos() { "$here/run_lockstep.sh" "$head" "$base" "$work/pos-$1x$2" "$1" "$2" 1000000 11 22 33 > "$work/pos-$1x$2.log" 2>&1; echo "positive $1/$2 rc=$?" > "$work/pos-$1x$2.rc"; }
ctl() { # label shape-m shape-n
  local t="$work/ctl-$1-$2x$3"; rm -rf "$t"; mkdir -p "$t/tree"; cp -r "$head/hdl" "$t/tree/hdl"
  (cd "$t/tree" && git apply "$head/tb/srp_top/mutations/$1.patch") || { echo "control $1 $2/$3 PATCH-FAILED" > "$t.rc"; return; }
  "$here/run_lockstep.sh" "$t/tree" "$base" "$t/work" "$2" "$3" 300000 44 > "$t.log" 2>&1
  local rc=$?
  if [ $rc -eq 1 ]; then echo "control $1 $2/$3 CAUGHT" > "$t.rc"; else echo "control $1 $2/$3 NOT-CAUGHT rc=$rc" > "$t.rc"; fi
}
export -f pos ctl; export here head base work
{
  for s in "1 1" "2 2" "3 5" "5 3" "8 8" "9 9"; do echo "pos $s"; done
  for c in "wtsp-read-at-gate-source 2 2" "wtsp-write-ignores-ready 2 2" "wid-flops-da-of-gate-source 2 2" \
           "wid-ram-read-neighbour 3 5" "wid-ram-first-open-only 3 5" "wsid-ram-first-settle-only 3 5" \
           "wsid-write-ignores-ready 3 5" "wsid-ram-written-on-teardown 3 5" "talker-vid-unreset 2 2" \
           "slope-stored-at-source-0 3 5" "slope-read-source-0 3 5" "slope-store-source-0-only 8 8"; do echo "ctl $c"; done
} | xargs -P "$jobs" -I{} bash -c '{}'
cat "$work"/*.rc | sort > "$work/RESULTS.txt"
for f in "$work"/pos-*.log; do grep -h "^shape\|^activity" "$f"; done >> "$work/RESULTS.txt"
cat "$work/RESULTS.txt"
! grep -qE "rc=[^0]|NOT-CAUGHT|PATCH-FAILED" "$work/RESULTS.txt"
