#!/bin/bash
# The split leg, its mutants and CDC check, and the reviewers' probes, on the probes clone at the head.
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745b/scripts/gate.sh
P=$VALIDATION_STORAGE/scratch/665s6-a745b/probes
R791=$HOME/milan-fpga-management/2026-09-23/665s6-r791-1/scripts
W=$VALIDATION_STORAGE/scratch/665s6-a745b/probe-work
mkdir -p $W
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$W/tmp; mkdir -p $TMPDIR
$G split-leg $P make -C tb/verilator/milan_dp split VERILATOR_JOBS=8
$G split-mutants $P make -C tb/verilator/milan_dp split-mutants
$G split-cdc $P make -C tb/verilator/milan_dp split-cdc
$G r791-split-reviewer-mutants $P python3 $R791/split_reviewer_mutants.py $P $W/revmut --jobs 4
$G r791-ctrl-boundary-probe $P python3 $R791/ctrl_boundary_probe.py $P $W/cbprobe
