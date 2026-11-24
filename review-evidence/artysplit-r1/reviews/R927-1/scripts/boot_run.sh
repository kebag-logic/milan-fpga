#!/usr/bin/env bash
# The committed split boot simulation at the Arty shape (positive run).
# usage: boot_run.sh <head-tree> <scratch> <receipts>
set -u
H=$1 S=$2 R=$3
LITEX=$(ls -d "$HOME"/litex-milan/litex "$HOME"/litex-milan/migen "$HOME"/litex-milan/lite* "$HOME"/litex-milan/pythondata-* 2>/dev/null | sort -u | paste -sd:)
[ -n "${VERILATOR_DIR:-}" ] && export PATH="$VERILATOR_DIR:$PATH"   # the pinned Verilator 5.050
( cd "$H" && env PYTHONPATH="$LITEX" PYTHONHASHSEED=0 python3 -B tb/verilator/ctrl_split_boot/run.py \
    --shape endstation_arty_split --interfaces 1 --build-dir "$S/boot-arty" ) > "$R/boot-arty.log" 2>&1
echo $? > "$R/boot-arty.rc"
