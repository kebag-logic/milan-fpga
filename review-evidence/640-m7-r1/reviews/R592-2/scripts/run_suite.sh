#!/bin/sh
# run_suite.sh TREE SUITE TARGET LOGDIR TAG
# Runs `make -C TREE/tb/verilator/SUITE TARGET` with the pinned simulator,
# writing LOGDIR/TAG.log and LOGDIR/TAG.rc (exit status).
TREE=$1; SUITE=$2; TARGET=$3; LOGDIR=$4; TAG=$5
: "${PINNED_VERILATOR:?set PINNED_VERILATOR to the pinned verilator}"
: "${PKT_TMP:?set PKT_TMP to a scratch temp dir}"
VDIR=$(dirname "$PINNED_VERILATOR")
start=$(date +%s)
env TMPDIR="$PKT_TMP" PATH="$VDIR:$PATH" VERILATOR="$PINNED_VERILATOR" \
    make -C "$TREE/tb/verilator/$SUITE" $TARGET > "$LOGDIR/$TAG.log" 2>&1
rc=$?
echo "$rc" > "$LOGDIR/$TAG.rc"
echo "elapsed_s=$(( $(date +%s) - start ))" >> "$LOGDIR/$TAG.rc"
