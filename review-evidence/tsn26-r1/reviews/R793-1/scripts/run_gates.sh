#!/bin/sh
# Usage: run_gates.sh <clone> <workroot> <receipts>; launches validate and baremetal concurrently, each with log and rc.
set -u
C=$1; W=$2; R=$3; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$W" "$R"
cd "$C"
( python3 scripts/validate.py --work "$W/build-validation" --jobs 16 --graphs > "$R/validate.out" 2>&1; echo $? > "$R/validate.rc" ) &
( python3 scripts/baremetal.py --work "$W/build-rv32" --jobs 16 > "$R/baremetal.out" 2>&1; echo $? > "$R/baremetal.rc" ) &
wait
