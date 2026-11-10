#!/bin/bash
# chainB: rtl-fast's wire-timing and firmware jobs, each on its own fresh clone of the gate head, in turn
G=$VALIDATION_STORAGE/665s8-a758b/gates; export CPUS=108-111
$G/wf_jobs.sh rtl-fast $G/rtl-fast wire-timing:litex firmware-verilator firmware-unit firmware-control-mutants firmware-aecp-mutants firmware-srp-mutants
echo done > $G/chainB.done
