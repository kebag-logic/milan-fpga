#!/usr/bin/env bash
# chain_sims.sh: the serial simulation chain on the exact-head clone; each step's log and rc in receipts/.
set -u
. "${R:?packet directory}/tools/env.sh"
# The as-run chain had no generator guard (see REPORT.md, Deviations); a re-run should carry it:
export PYTHONPATH=$R/tools/noguard
C=${CLONE:?exact-head clone}; B=$R/scratch/build; O=$R/receipts/sims; mkdir -p "$B" "$O"
step() { local name=$1; shift; echo "$(date +%T) start $name" >> "$O/chain.log"; ( cd "$C" && /usr/bin/time -v "$@" ) > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc"; echo "$(date +%T) $name rc $(cat "$O/$name.rc")" >> "$O/chain.log"; }
step region-self-test "$PY" -B tb/verilator/ctrl_region_decode/run.py --build-dir "$B/region-self" --self-test
step boot-1x1 "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-1x1"
step boot-8x8 "$PY" -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B/boot-8x8" --shape endstation_ax7101_8x8
echo "$(date +%T) chain done" >> "$O/chain.log"
