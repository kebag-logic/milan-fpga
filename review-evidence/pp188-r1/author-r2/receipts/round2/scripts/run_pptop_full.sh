#!/usr/bin/env bash
# usage: run_pptop_full.sh <rev> <dir>: export <rev> of the lane, run tb/pp_top's
# default make (what scripts/run_suites.sh runs) and keep its whole log.
set -u
. <scratch>/scripts/env.sh
rev=$1; d=$2
rm -rf "$d"; mkdir -p "$d"
git -C <lane> archive "$rev" | tar -x -C "$d"
cd "$d/tb/pp_top" || exit 2
t0=$(date +%s)
make VERILATOR="$VERILATOR" > "$d.log" 2>&1; echo $? > "$d.rc"
echo $(( $(date +%s) - t0 )) > "$d.sec"
