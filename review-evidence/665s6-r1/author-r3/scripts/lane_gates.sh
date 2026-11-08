#!/bin/bash
# The lane's own gates and the findings' verification steps, at the head, on the clean clone (final)
# and, for the reviewers' probes, on a byte-identical copy of it (probes). Each through gate.sh, unpiped.
export GATES=$VALIDATION_STORAGE/scratch/665s6-a745c/gates
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745c/scripts/gate.sh
F=$VALIDATION_STORAGE/scratch/665s6-a745c/final
P=$VALIDATION_STORAGE/scratch/665s6-a745c/probes
W=$VALIDATION_STORAGE/scratch/665s6-a745c/probe-work
M=$HOME/milan-fpga-management/2026-09-23
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
mkdir -p $W/tmp; export TMPDIR=$W/tmp
case "$1" in
  place)
    $G pp-placement-selftest $F python3 syn/ooc/pp_placement_selftest.py
    $G pp-baseline-selftest $F python3 syn/ooc/pp_baseline.py --selftest ;;
  leg)
    $G split-leg $F make -C tb/verilator/milan_dp split VERILATOR_JOBS=8
    $G split-cdc $F make -C tb/verilator/milan_dp split-cdc
    $G split-mutants $F make -C tb/verilator/milan_dp split-mutants ;;
  lint)
    $G lint $F python3 scripts/lint_rtl.py --check --self-test ;;
  probes)
    $G r791-2-tap-mutant-1 $P python3 -I $M/665s6-r791-2/scripts/tap_reviewer_mutants.py $P $W/tapmut 1
    $G r791-2-cdc-plants $P python3 -I $M/665s6-r791-2/scripts/cdc_plants.py $P
    $G r791-2-cdc-extra-plants $P python3 -I $M/665s6-r791-2/scripts/cdc_extra_plants.py $P
    $G r792-2-cdc-allowance-probes $P python3 -I $M/665s6-r792-2/scripts/cdc_allowance_probes.py $P
    $G r792-1-cdc-check-probes $P python3 -I $M/665s6-r792-1/scripts/cdc_check_probes.py $P ;;
esac
