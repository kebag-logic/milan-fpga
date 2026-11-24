#!/usr/bin/env bash
# Run the committed region-decode self-test at the Arty shape and at the
# harness's default (AX7101 1x1) shape, each with its own build dir, log, rc.
# usage: region_runs.sh <head-tree> <scratch> <receipts>
set -u
H=$1 S=$2 R=$3
LITEX=$(ls -d "$HOME"/litex-milan/litex "$HOME"/litex-milan/migen "$HOME"/litex-milan/lite* "$HOME"/litex-milan/pythondata-* 2>/dev/null | sort -u | paste -sd:)
[ -n "${VERILATOR_DIR:-}" ] && export PATH="$VERILATOR_DIR:$PATH"   # the pinned Verilator 5.050
run() { local name=$1; shift; ( cd "$H" && env PYTHONPATH="$LITEX" PYTHONHASHSEED=0 "$@" ) > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
run region-arty python3 -B tb/verilator/ctrl_region_decode/run.py --shape endstation_arty_split --self-test --build-dir "$S/region-arty" &
run region-ax python3 -B tb/verilator/ctrl_region_decode/run.py --self-test --build-dir "$S/region-ax" &
wait
