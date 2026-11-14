#!/bin/bash
# Lane 897 round 3's clean-clone pass for a head (round 2's gate_queue2.sh): every workflow job a pull request to
# dev-soft-core triggers (run_wf.py, each on its own fresh clean clone), the lane's own gates in three parts and the
# CPU budget harness's legs at both points (fresh builds), one unit each, for dispatch3.py. The full Verilator sweep runs
# beside it as four native-shards units (launch_sweep3.sh). usage: gate_queue3.sh HEAD OUTDIR > QUEUE
set -u
H=$1 O=$2
T=/data-2/milan/tmp/897-a776
W="/usr/bin/python3 $T/gates/run_wf.py"
L="WF_VENV=$WORKSPACE_HOME/litex-milan/venv/bin"
C=$T/r3/cl-final-${H:0:8}
echo "W-fw-control 10G mkdir -p $O; $W rtl-fast.yml $H firmware-control-mutants $O > $O/firmware-control-mutants.driver.log 2>&1"
echo "W-fw-aecp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-aecp-mutants $O > $O/firmware-aecp-mutants.driver.log 2>&1"
echo "W-fw-unit 10G mkdir -p $O; $W rtl-fast.yml $H firmware-unit $O > $O/firmware-unit.driver.log 2>&1"
echo "W-fw-srp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-srp-mutants $O > $O/firmware-srp-mutants.driver.log 2>&1"
echo "W-fw-boundary 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-boundary $O > $O/firmware-boundary.driver.log 2>&1"
echo "W-fw-verilator 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-verilator $O > $O/firmware-verilator.driver.log 2>&1"
for p in b c a; do echo "lane-$p 10G /bin/bash $T/scripts/r3/lane_gates3.sh $H ${H:0:8} $p"; done
for spec in "A1 1x1 datapath-events,aecp-largest-notice,backlog-owed,srp,aecp,aecp-fanout,acmp-cmd" \
            "N1 1x1 notice-every-0,notice-burst-0 --variant answering-every-port" "B1 1x1 aecp --variant answering-ports" \
            "A8 8x8 datapath-events,backlog-owed,aecp,aecp-fanout,acmp-cmd" "S8 8x8 srp" \
            "N8 8x8 notice-every-0,notice-burst-0 --variant answering-every-port" \
            "B8 8x8 aecp,aecp-largest-notice --variant answering-ports"; do
  set -- $spec; n=$1; shift
  echo "hs-f$n 10G /bin/bash $T/scripts/r3/hs3.sh $C f$n $* > $T/r3/logs/hs-f$n.log 2>&1"
done
echo "W-rtl-fast 10G mkdir -p $O; for j in changes verilator-lint bdd-conformance yosys-tool yosys-elaboration publication-census split-cdc rtl-fast; do $W rtl-fast.yml $H \$j $O > $O/rtl-fast-\$j.driver.log 2>&1; done"
echo "W-docs-a 10G mkdir -p $O; for j in wire-accountability docs-check-no-git docs-check; do $W docs.yml $H \$j $O > $O/docs-\$j.driver.log 2>&1; done"
for j in docs-gates-0 docs-gates-1 docs-gates-2; do echo "W-$j 10G mkdir -p $O; $W docs.yml $H $j $O > $O/docs-$j.driver.log 2>&1"; done
echo "W-elab-0 10G mkdir -p $O; $L $W elaborate.yml $H elaborate-gates-0 $O > $O/elaborate-gates-0.driver.log 2>&1; $W elaborate.yml $H elaborate $O > $O/elaborate-elaborate.driver.log 2>&1"
echo "W-elab-1 10G mkdir -p $O; $L $W elaborate.yml $H elaborate-gates-1 $O > $O/elaborate-gates-1.driver.log 2>&1"
echo "W-rtl-a 10G mkdir -p $O; $W rtl.yml $H full-ci-gate $O > $O/rtl-full-ci-gate.driver.log 2>&1; $W rtl.yml $H yosys-tool $O > $O/rtl-yosys-tool.driver.log 2>&1; for k in 0 1; do $W rtl.yml $H yosys-shards $O shard=\$k total=4 > $O/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-rtl-b 10G mkdir -p $O; for k in 2 3; do $W rtl.yml $H yosys-shards $O shard=\$k total=4 > $O/rtl-yosys-shards-\$k.driver.log 2>&1; done"
