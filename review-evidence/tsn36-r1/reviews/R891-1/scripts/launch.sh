#!/bin/bash
# launch.sh PACKET: start the three independent campaigns detached, each with its own log and rc file.
set -u
P=$1 S=$P/scratch R=$P/receipts
. "$P/scripts/env.sh"
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR" "$R/validate" "$R/rv32"
( cd "$S/head-validate" && s=$(date +%s); python3 scripts/validate.py --work "$S/build-validation" --jobs 8 --graphs > "$R/validate/validate.log" 2>&1; echo $? > "$R/validate/validate.rc"; echo "$(( $(date +%s) - s ))s" > "$R/validate/time.txt" ) &
( cd "$S/head-rv32" && s=$(date +%s); python3 scripts/baremetal.py --work "$S/build-rv32" --jobs 4 > "$R/rv32/baremetal.log" 2>&1; echo $? > "$R/rv32/baremetal.rc"; echo "$(( $(date +%s) - s ))s" > "$R/rv32/time.txt" ) &
( s=$(date +%s); python3 -I "$P/scripts/probes.py" "$S/head-probe" "$S/base-probe" "$S/probes" "$R/probes.json" --jobs 4 > "$R/probes.log" 2>&1; echo $? > "$R/probes.rc"; echo "$(( $(date +%s) - s ))s" > "$R/probes-time.txt" ) &
wait
