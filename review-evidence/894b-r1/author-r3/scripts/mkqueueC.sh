#!/bin/bash
# Round 3's full-pass dispatcher queue at a head (round 2 phase B's mkqueueB.sh): every hosted job's
# steps (run_wf.py), the lane gates' three parts, the harness legs at 1x1 and 8x8/2if on one clean clone as #902's pass
# runs them, and every image. 8x8/1if is measured once (the measurement legs C-*), so no 8x8-1if leg is here.
# usage: mkqueueB.sh HEAD > queue.txt
set -u
H=$1 T=/data-2/milan/tmp/894b-a781 F=/data-2/milan/tmp/894b-a781/fullC
R=$F/wf G=$F/rgh L=$T/scripts/leg.sh
W="mkdir -p $R; /usr/bin/python3 $T/gates/run_wf.py"
V="WF_VENV=$WORKSPACE_HOME/litex-milan/venv/bin"
echo "W-fw-boundary mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-boundary $R > $R/firmware-boundary.driver.log 2>&1"
for j in control aecp srp unit; do jj=firmware-$j; [ $j != unit ] && jj=$jj-mutants; echo "W-fw-$j $W rtl-fast.yml $H $jj $R > $R/$jj.driver.log 2>&1"; done
for p in b a c; do echo "lane-$p /bin/bash $T/scripts/lane_gates_r3.sh $H $p"; done
echo "W-rtl-fast mkdir -p $R; for j in changes verilator-lint bdd-conformance yosys-tool yosys-elaboration publication-census split-cdc rtl-fast; do /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H \$j $R > $R/rtl-fast-\$j.driver.log 2>&1; done"
for k in 0 1 2; do echo "W-docs-gates-$k $W docs.yml $H docs-gates-$k $R > $R/docs-docs-gates-$k.driver.log 2>&1"; done
echo "W-docs-a mkdir -p $R; for j in wire-accountability docs-check-no-git docs-check; do /usr/bin/python3 $T/gates/run_wf.py docs.yml $H \$j $R > $R/docs-\$j.driver.log 2>&1; done"
echo "W-elab-0 mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate-gates-0 $R > $R/elaborate-gates-0.driver.log 2>&1; /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate $R > $R/elaborate-elaborate.driver.log 2>&1"
echo "W-elab-1 mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate-gates-1 $R > $R/elaborate-gates-1.driver.log 2>&1"
echo "W-rtl-a $W rtl.yml $H full-ci-gate $R > $R/rtl-full-ci-gate.driver.log 2>&1; /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-tool $R > $R/rtl-yosys-tool.driver.log 2>&1; for k in 0 1; do /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-shards $R shard=\$k total=4 > $R/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-rtl-b mkdir -p $R; for k in 2 3; do /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-shards $R shard=\$k total=4 > $R/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-fw-verilator mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-verilator $R > $R/firmware-verilator.driver.log 2>&1"
leg() { echo "$1 $L $G $F/builds/$1 $2 1 ${*:3}"; }
leg H-L1A 1x1 --groups datapath-events; leg H-L1N 1x1 --variant answering-every-port --groups notice-every-0
leg H-L8A 8x8 --groups datapath-events; leg H-L8N 8x8 --variant answering-every-port --groups notice-every-0
leg H-L1L 1x1 --groups aecp-largest-notice; leg H-L8L 8x8 --variant answering-ports --groups aecp-largest-notice
leg H-L1O 1x1 --groups backlog-owed; leg H-L8O 8x8 --groups backlog-owed
leg C-R1 1x1 --mutation acmp-redelivered-every-poll
leg H-J1 1x1 --groups srp; leg H-J8 8x8 --groups srp
echo "Q-img bash $T/scripts/qimg.sh $G $F/qimg"
