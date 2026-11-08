#!/bin/bash
# usage: run_gates.sh CLONE WORKROOT RECEIPTS JOBS
# Runs the repository's own validation kit and bare-metal gate concurrently, one log and rc file each.
set -u
clone=$1; work=$2; rec=$3; jobs=${4:-8}
. "$(dirname "$0")/env.sh"
cd "$clone"
( python3 scripts/validate.py --work "$work/validation" --jobs "$jobs" > "$rec/validate.log" 2>&1; echo $? > "$rec/validate.rc" ) &
( python3 scripts/baremetal.py --work "$work/rv32" --jobs "$jobs" > "$rec/baremetal.log" 2>&1; echo $? > "$rec/baremetal.rc" ) &
wait
