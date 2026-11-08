#!/bin/sh
# Usage: run_gates.sh <clone> <workroot> <receipts>; launches validate (12 jobs) and baremetal (4 jobs)
# concurrently, each with its own log and rc file, so at most 16 jobs run at once.
set -u
C=$1; W=$2; R=$3; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$W" "$R"
cd "$C"
( python3 scripts/validate.py --work "$W/build-validation" --jobs 12 --graphs > "$R/validate.out" 2>&1; echo $? > "$R/validate.rc" ) &
( python3 scripts/baremetal.py --work "$W/build-rv32" --jobs 4 > "$R/baremetal.out" 2>&1; echo $? > "$R/baremetal.rc" ) &
wait
