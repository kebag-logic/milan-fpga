#!/bin/sh
# Usage: run_gates.sh <clone> <work>. Runs validate.py (--jobs 3, with graphs) and baremetal.py (--jobs 4) concurrently,
# at most 16 parallel jobs in total; each writes <work>/<name>.log and <work>/<name>.rc.
set -u
CLONE=$1; WORK=$2; mkdir -p "$WORK"
. "$(dirname "$0")/env.sh"
cd "$CLONE" || exit 2
( python3 scripts/validate.py --work "$WORK/validate" --jobs 3 --graphs > "$WORK/validate.log" 2>&1; echo $? > "$WORK/validate.rc" ) &
( python3 scripts/baremetal.py --work "$WORK/rv32" --jobs 4 > "$WORK/baremetal.log" 2>&1; echo $? > "$WORK/baremetal.rc" ) &
wait
