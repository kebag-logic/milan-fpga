#!/bin/bash
# Batch 1: exact-head standalone checks of the lane's harness and builder outputs, run concurrently.
# usage: batch1.sh CLONE PACKET   (each job writes PACKET/receipts/b1-<name>.log and .rc)
set -u
CLONE=$1; PKT=$2
R=$PKT/receipts; S=$PKT/scratch/b1
mkdir -p "$R" "$S"
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
export PATH=${PINNED_VERILATOR_DIR:?set PINNED_VERILATOR_DIR to the pinned Verilator 5.050 directory}:$PATH
cd "$CLONE" || exit 2
H=tb/verilator/ctrl_service_budget
job() { local name=$1; shift; ( "$@" > "$R/b1-$name.log" 2>&1; echo $? > "$R/b1-$name.rc" ) & }
job ledger-selftest python3 -I -B $H/egress_ledger.py --selftest
job arty-selftest python3 -I -B $H/arty_grade.py --selftest
job arty-4x4 python3 -B $H/arty_grade.py --point arty-4x4
job arty-1x1 python3 -B $H/arty_grade.py --point arty-1x1
job arty-badpoint python3 -B $H/arty_grade.py --point arty-9x9
job shape-check python3 -I -B $H/shape_costs.py --check
job shape-selftest python3 -I -B $H/shape_costs.py --selftest
job load-check python3 -I -B $H/load_grade.py --check
job load-selftest python3 -I -B $H/load_grade.py --selftest
job rows-selftest python3 -I -B $H/rows_tiers.py --selftest
job record-selftest python3 -I -B $H/record_classes.py --selftest
job mii-selftest python3 -I -B $H/egress_mii.py --selftest
job mii-structural python3 -I -B $H/egress_mii.py --structural
# egress_fixed.py imports egress_mii from its own directory, so it runs without -I (its usage line says -I; at the
# base as at the head, -I fails that import).
job fixed-100 python3 -B $H/egress_fixed.py "$S/fixed100" 100000000
job fixed-80 python3 -B $H/egress_fixed.py "$S/fixed80"
job fixed-125 python3 -B $H/egress_fixed.py "$S/fixed125" 125000000
job builder-4x4 python3 -B sw/builder/endstation_builder.py configs/endstation_arty_split_4x4.yaml -o "$S/builder-4x4"
wait
# A build directory reused at another clock: the 80 MHz build measured again at 100 MHz must read 100 MHz's figure.
cp -a "$S/fixed80" "$S/fixed-reuse"
python3 -B $H/egress_fixed.py "$S/fixed-reuse" 100000000 > "$R/b1-fixed-reuse-80then100.log" 2>&1
echo $? > "$R/b1-fixed-reuse-80then100.rc"
cmp -s "$S/builder-4x4/endstation_arty_split_4x4/adp_shape_defaults.svh" \
    configs/generated/endstation_arty_split_4x4/gen/adp_shape_defaults.svh
echo $? > "$R/b1-builder-4x4-include-cmp.rc"
for f in "$R"/b1-*.rc; do echo "$(basename "$f" .rc) $(cat "$f")"; done | sort > "$R/b1-summary.txt"
cat "$R/b1-summary.txt"
