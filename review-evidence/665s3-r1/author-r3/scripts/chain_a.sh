#!/bin/bash
# Chain A at one head: the docs gates (gates_s3.py, one at a time), the end-station builder, the TSN stack boundary
# without Verilator, the CPU budget harness at 1x1; each step its own unit and clone.
# usage: chain_a.sh COMMIT CPUS
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697d/scripts
C=$1 CPUS=$2 W=$VALIDATION_STORAGE/665s3-a697d/$1 R=$MANAGEMENT/2026-09-23/665s3-a697d/receipts/gates-at-$1
mkdir -p "$W" "$R"
for d in docs bld bnd s2a; do [ -e "$W/$d" ] || bash $S/clone.sh "$W/$d" "$C" > "$R/clone-$d.txt" 2>&1; done
bash $S/unitw.sh docs-$C "$CPUS" "$W/docs" "$R/docs-runner.log" . /bin/bash $S/docs_gates.sh "$W/docs" "$R/docs"
bash $S/unitw.sh bld-$C "$CPUS" "$W/bld" "$R/builder_require_rv32.log" . python3 sw/builder/test_builder.py --require-rv32
bash $S/unitw.sh bnd-$C "$CPUS" "$W/bnd" "$R/ctrl_boundary-without-verilator.log" . python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
bash $S/unitw.sh s2a-$C "$CPUS" "$W/s2a" "$R/s2_harness-1x1.log" . python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$W/s2build/budget-1x1" --record-budget-findings --jobs 4
echo "chain A done $(date)" > "$R/chain_a.done"
