#!/usr/bin/env bash
# Run one Verilator suite of a tree copy with the pinned Verilator and record
# its log and rc.  usage: run_suite.sh <tree> <suite-dir> <make-target|-> <logdir> <tag>
set -u
tree=$1; suite=$2; target=$3; logdir=$4; tag=$5
VER=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
mkdir -p "$logdir"
log="$logdir/$tag.log"
[ "$target" = "-" ] && target=""
( cd "$tree/tb/$suite" && make VERILATOR="$VER" $target ) >"$log" 2>&1
rc=$?
echo "$rc" >"$logdir/$tag.rc"
tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$log" | tail -1)
echo "$tag rc=$rc ${tally:-no-tally}"
exit 0
