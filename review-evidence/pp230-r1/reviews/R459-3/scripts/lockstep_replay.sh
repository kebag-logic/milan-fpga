#!/usr/bin/env bash
# Replay the published round-1 lockstep bench (base c4cb84ff KL_srp_top vs the
# head's) with reviewer-chosen shapes and seeds, unmodified bench files, laid
# out under $VALIDATION_STORAGE as its build.sh expects.
# usage: lockstep_replay.sh <hdl/srp under test> <tag> <cycles> <out log> "<shape>"...
#   shape = "name NS NK SLOT_AW JOIN PERIODIC LEAVE"
set -u
NEW=$1; TAG=$2; CYC=$3; LOG=$4; shift 4
L=$VALIDATION_STORAGE/pp230-a523/lockstep
: > "$LOG"; bad=0
for shape in "$@"; do
  set -- $shape
  o=$L/rv-$TAG/$1
  "$L/build.sh" "$NEW" "$o" $2 $3 $4 $5 $6 $7 > /dev/null 2>&1 || { echo "BUILD-FAIL $1" >> "$LOG"; bad=1; continue; }
  for sd in 459301 459302 459303 459304; do
    "$o/obj/Vlockstep" $((sd * 7 + ${#1})) "$CYC" $((sd % 3)) >> "$LOG" 2>&1 || bad=1
  done
  rm -rf "$o/obj"
done
echo "replay-rc=$bad" >> "$LOG"; exit $bad
