#!/bin/sh
# Run one pp_shadow CRF arm in a disposable tree and keep a receipt.
# usage: run_arm.sh <tree> <label> [sim-arg]
# Environment: VERILATOR (pinned 5.050 wrapper), RECEIPTS (output directory).
set -u
tree=$1
label=$2
arg=${3-}
log="$RECEIPTS/$label.log"
{
    echo "tree=$tree"
    echo "parent=$(git -C "$tree" rev-parse HEAD)"
    echo "processor=$(git -C "$tree/protocol-processor" rev-parse HEAD)"
    echo "sim_arg=${arg:-<none>}"
    "$VERILATOR" --version
} > "$log"
make -C "$tree/tb/verilator/pp_shadow" run-crf VERILATOR="$VERILATOR" \
    SIM_ARGS="$arg" >> "$log" 2>&1
rc=$?
echo "make_rc=$rc" >> "$log"
grep -E "^pp_shadow: |FIRST_PROBE|CRF_STOP|FAIL|make_rc" "$log" | tail -n 60
exit 0
