#!/bin/bash
# The final gate queue for a head: every workflow job a pull request to dev-soft-core triggers (run_wf.py, each on its
# own fresh clean clone) and the lane's own gates, one unit each, for cmdq.sh. usage: gate_queue.sh HEAD OUTDIR > QUEUE
set -u
H=$1 O=$2
T=<scratch>
W="/usr/bin/python3 $T/gates/run_wf.py"
L="WF_VENV=<home>/litex-milan/venv/bin"
echo "W-rtl-fast 10G mkdir -p $O; for j in changes verilator-lint bdd-conformance yosys-tool yosys-elaboration publication-census split-cdc rtl-fast; do $W rtl-fast.yml $H \$j $O > $O/rtl-fast-\$j.driver.log 2>&1; done"
echo "W-fw-unit 10G mkdir -p $O; $W rtl-fast.yml $H firmware-unit $O > $O/firmware-unit.driver.log 2>&1"
echo "W-fw-control 10G mkdir -p $O; $W rtl-fast.yml $H firmware-control-mutants $O > $O/firmware-control-mutants.driver.log 2>&1"
echo "W-fw-aecp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-aecp-mutants $O > $O/firmware-aecp-mutants.driver.log 2>&1"
echo "W-fw-srp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-srp-mutants $O > $O/firmware-srp-mutants.driver.log 2>&1"
echo "W-fw-boundary 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-boundary $O > $O/firmware-boundary.driver.log 2>&1"
echo "W-fw-verilator 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-verilator $O > $O/firmware-verilator.driver.log 2>&1"
echo "W-docs 10G mkdir -p $O; for j in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2 docs-check; do $W docs.yml $H \$j $O > $O/docs-\$j.driver.log 2>&1; done"
echo "W-rtl-a 10G mkdir -p $O; $W rtl.yml $H full-ci-gate $O > $O/rtl-full-ci-gate.driver.log 2>&1; $W rtl.yml $H yosys-tool $O > $O/rtl-yosys-tool.driver.log 2>&1; for k in 0 1; do $W rtl.yml $H yosys-shards $O shard=\$k total=4 > $O/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-rtl-b 10G mkdir -p $O; for k in 2 3; do $W rtl.yml $H yosys-shards $O shard=\$k total=4 > $O/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-elab-0 10G mkdir -p $O; $L $W elaborate.yml $H elaborate-gates-0 $O > $O/elaborate-gates-0.driver.log 2>&1; $W elaborate.yml $H elaborate $O > $O/elaborate-elaborate.driver.log 2>&1"
echo "W-elab-1 10G mkdir -p $O; $L $W elaborate.yml $H elaborate-gates-1 $O > $O/elaborate-gates-1.driver.log 2>&1"
echo "lane-gates 10G /bin/bash $T/scripts/lane_gates.sh $H ${H:0:8}"
