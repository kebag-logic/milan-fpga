#!/bin/sh
# R457-2: the sound design's --law-boundary leg in the three histories the
# executor measured W from, at both processors, keeping every leg's own output
# (the campaign runner keeps only its verdict lines). Clean binaries from the
# suite's own default build.
#
#   PKT  the review packet; scratch/head and scratch/c4 already built
#   JOBS parallel legs (default 12)
#
# Ascending: the leg's own located scan. Descending: --law-boundary=2066..1986.
# Alone: each phase within 12 cycles of the boundary (+2014..+2038) on its own.
set -eu
: "${PKT:?}"
JOBS=${JOBS:-12}
R="$PKT/receipts/hist"
mkdir -p "$R"
{
  for t in head c4; do
    echo "$t asc --law-boundary"
    echo "$t desc --law-boundary=2066..1986"
  done
  for t in head c4; do
    p=2014; while [ $p -le 2038 ]; do echo "$t alone-$p --law-boundary=$p"; p=$((p + 1)); done
  done
} | xargs -P "$JOBS" -L 1 sh -c '
  d="$0/scratch/$1/tb/verilator/milan_dp_render"; o="$0/receipts/hist/$1-$2"
  [ -e "$o.log" ] && exit 0   # a leg already started by an earlier driver
  rc=0; ( cd "$d" && ./obj_tdm8r/Vmilan_dp_tdm8r "$3" ) > "$o.log" 2>&1 || rc=$?
  echo $rc > "$o.rc"' "$PKT"
