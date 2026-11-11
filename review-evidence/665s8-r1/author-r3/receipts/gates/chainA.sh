#!/bin/bash
# chainA: rtl-fast's census, boundary and short jobs, each on its own fresh clone of the gate head, in turn
G=<scratch>/gates; export CPUS=20-23
$G/wf_jobs.sh rtl-fast $G/rtl-fast publication-census firmware-boundary:litex changes split-cdc yosys-tool yosys-elaboration verilator-lint bdd-conformance rtl-fast ci-manifest ci-fail-fast ci-cancel-tail
echo done > $G/chainA.done
