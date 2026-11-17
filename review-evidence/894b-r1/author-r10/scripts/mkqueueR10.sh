#!/bin/bash
# Round 10's final gates at a head, the ones round 8's STOP left (#894's ruling of 2026-11-16, round 9), each its own
# unit on clean clones: every firmware job of rtl-fast (firmware-unit carries fw_coverage --check), every docs job,
# the lane gates' three parts, rtl.yml's verilator shards 1, 3, 4, 6, 10 and 17 of 19 (the suites that build the split
# firmware: milan_dp's pieces, fw_service_budget, milan_dp_gm_steps, mbx), and every image (Q-img).
# usage: mkqueueR10.sh HEAD > queue.txt
set -u
H=$1 T=/data-2/milan/tmp/894b-a781 F=/data-2/milan/tmp/894b-a781/fullR10
R=$F/wf G=$F/rgh S=$MANAGEMENT/2026-09-23/894b-a781/round10/scripts
W="mkdir -p $R; /usr/bin/python3 $T/gates/run_wf.py"
V="WF_VENV=$WORKSPACE_HOME/litex-milan/venv/bin"
echo "W-fw-boundary mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-boundary $R > $R/firmware-boundary.driver.log 2>&1"
for j in control aecp srp unit; do jj=firmware-$j; [ $j != unit ] && jj=$jj-mutants; echo "W-fw-$j $W rtl-fast.yml $H $jj $R > $R/$jj.driver.log 2>&1"; done
echo "W-fw-verilator mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-verilator $R > $R/firmware-verilator.driver.log 2>&1"
for p in b a c; do echo "lane-$p /bin/bash $S/lane_gates_r10.sh $H $p"; done
for k in 0 1 2; do echo "W-docs-gates-$k $W docs.yml $H docs-gates-$k $R > $R/docs-docs-gates-$k.driver.log 2>&1"; done
echo "W-docs-a mkdir -p $R; for j in wire-accountability docs-check-no-git docs-check; do /usr/bin/python3 $T/gates/run_wf.py docs.yml $H \$j $R > $R/docs-\$j.driver.log 2>&1; done"
for k in 1 3 4 6 10 17; do echo "W-vshard-$k bash $S/vshard.sh $H $k"; done
echo "Q-img bash $T/scripts/qimg.sh $G $F/qimg"
