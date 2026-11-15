#!/bin/bash
# Round 5's full-pass queue at a head (round 4's mkqueueR4.sh), the four-shard sweep apart (native-shards.py): every hosted job's
# steps (run_wf.py), the lane gates' three parts and every image, on clean clones.
# The 1x1/1if and 8x8/2if legs carry by their images' byte identity with #902's 234bc149 images (Q-img).
# usage: mkqueueR4.sh HEAD > queue.txt
set -u
H=$1 T=/data-2/milan/tmp/894b-a781 F=/data-2/milan/tmp/894b-a781/fullR5
R=$F/wf G=$F/rgh L=$T/scripts/leg.sh
W="mkdir -p $R; /usr/bin/python3 $T/gates/run_wf.py"
V="WF_VENV=$WORKSPACE_HOME/litex-milan/venv/bin"
echo "W-fw-boundary mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-boundary $R > $R/firmware-boundary.driver.log 2>&1"
for j in control aecp srp unit; do jj=firmware-$j; [ $j != unit ] && jj=$jj-mutants; echo "W-fw-$j $W rtl-fast.yml $H $jj $R > $R/$jj.driver.log 2>&1"; done
for p in b a c; do echo "lane-$p /bin/bash $MANAGEMENT/2026-09-23/894b-a781/round5/scripts/lane_gates_r5.sh $H $p"; done
echo "W-rtl-fast mkdir -p $R; for j in changes verilator-lint bdd-conformance yosys-tool yosys-elaboration publication-census split-cdc rtl-fast; do /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H \$j $R > $R/rtl-fast-\$j.driver.log 2>&1; done"
for k in 0 1 2; do echo "W-docs-gates-$k $W docs.yml $H docs-gates-$k $R > $R/docs-docs-gates-$k.driver.log 2>&1"; done
echo "W-docs-a mkdir -p $R; for j in wire-accountability docs-check-no-git docs-check; do /usr/bin/python3 $T/gates/run_wf.py docs.yml $H \$j $R > $R/docs-\$j.driver.log 2>&1; done"
echo "W-elab-0 mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate-gates-0 $R > $R/elaborate-gates-0.driver.log 2>&1; /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate $R > $R/elaborate-elaborate.driver.log 2>&1"
echo "W-elab-1 mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py elaborate.yml $H elaborate-gates-1 $R > $R/elaborate-gates-1.driver.log 2>&1"
echo "W-rtl-a $W rtl.yml $H full-ci-gate $R > $R/rtl-full-ci-gate.driver.log 2>&1; /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-tool $R > $R/rtl-yosys-tool.driver.log 2>&1; for k in 0 1; do /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-shards $R shard=\$k total=4 > $R/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-rtl-b mkdir -p $R; for k in 2 3; do /usr/bin/python3 $T/gates/run_wf.py rtl.yml $H yosys-shards $R shard=\$k total=4 > $R/rtl-yosys-shards-\$k.driver.log 2>&1; done"
echo "W-fw-verilator mkdir -p $R; $V /usr/bin/python3 $T/gates/run_wf.py rtl-fast.yml $H firmware-verilator $R > $R/firmware-verilator.driver.log 2>&1"
echo "Q-img bash $T/scripts/qimg.sh $G $F/qimg"
