#!/bin/bash
# The service self-test in a disposable copy of the reviewed tree, its mutants split over 8 concurrent partitions.
# usage: service_selftest.sh CLONE PACKET
CLONE=$1; PKT=$2; T=$PKT/scratch/st-tree; R=$PKT/receipts
rm -rf "$T"; mkdir -p "$T"; (cd "$CLONE" && tar --exclude=.git -cf - .) | (cd "$T" && tar -xf -)
cd "$T" || exit 2
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PATH=${PINNED_VERILATOR_DIR:?set PINNED_VERILATOR_DIR to the pinned Verilator 5.050 directory}:$PATH
code="import sys; sys.path.insert(0,'tb/verilator/ctrl_service_budget'); import selftest; n=int(sys.argv[1]); selected=list(selftest.selftest_mutants.MUTANTS.items())[n::8]; print('PARTITION',n,'OF 8',len(selected),flush=True); selftest.selftest_mutants.MUTANTS=dict(selected); raise SystemExit(selftest.main([]))"
for n in 0 1 2 3 4 5 6 7; do ( python3 -B -c "$code" $n > "$R/st-$n.log" 2>&1; echo $? > "$R/st-$n.rc" ) & done
wait
for n in 0 1 2 3 4 5 6 7; do echo "partition $n rc=$(cat $R/st-$n.rc)"; done | tee "$R/st-summary.txt"
