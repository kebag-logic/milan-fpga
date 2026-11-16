#!/bin/bash
# Lane 897 round 7's clean-clone pass at a head (round 5's gate_queue5.sh without the sweep, which runs in the
# manager's merge candidate): every rtl-fast job (the firmware units, campaigns, coverage, boundary and Verilator jobs
# among them) and the docs jobs (run_wf.py, each on its own fresh clean clone), the lane's own gates in three parts, the
# Verilator suites that build the split firmware (mbx, milan_dp, milan_dp_gm_steps), each alone as run_all_suites.sh
# runs it, and one group of every harness arm at each point (fresh builds, whose ELFs show the measured images'
# identity). usage: gate_queue7.sh HEAD OUTDIR > QUEUE
set -u
H=$1 O=$2
T=/data-2/milan/tmp/897-a776
W="/usr/bin/python3 $T/gates/run_wf.py"
L="WF_VENV=$WORKSPACE_HOME/litex-milan/venv/bin"
C=$T/r4/cl-final-${H:0:8}
echo "W-fw-control 10G mkdir -p $O; $W rtl-fast.yml $H firmware-control-mutants $O > $O/firmware-control-mutants.driver.log 2>&1"
echo "W-fw-aecp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-aecp-mutants $O > $O/firmware-aecp-mutants.driver.log 2>&1"
echo "W-fw-unit 10G mkdir -p $O; $W rtl-fast.yml $H firmware-unit $O > $O/firmware-unit.driver.log 2>&1"
echo "W-fw-srp 10G mkdir -p $O; $W rtl-fast.yml $H firmware-srp-mutants $O > $O/firmware-srp-mutants.driver.log 2>&1"
echo "W-fw-boundary 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-boundary $O > $O/firmware-boundary.driver.log 2>&1"
echo "W-fw-verilator 10G mkdir -p $O; $L $W rtl-fast.yml $H firmware-verilator $O > $O/firmware-verilator.driver.log 2>&1"
for p in b c a; do echo "lane-$p 10G /bin/bash $T/scripts/r4/lane_gates7.sh $H ${H:0:8} $p"; done
for s in "milan_dp 4800" "mbx 1800" "milan_dp_gm_steps 1800"; do set -- $s
  echo "suite-$1 12G /bin/bash $T/scripts/r4/rerun_suite.sh $H $1 $2"; done
G16=$(python3 -c "print(','.join([f'notice-every-{k}' for k in range(8)] + [f'notice-burst-{k}' for k in range(8)]))")
for spec in "B1 1x1 aecp,aecp-fanout,aecp-largest-notice --variant answering-ports" \
            "B8 8x8 aecp,aecp-largest-notice,aecp-fanout --variant answering-ports" \
            "A1 1x1 aecp" "A8 8x8 aecp" "E1 1x1 notice-every-0 --variant answering-every-port" \
            "E8 8x8 notice-every-0 --variant answering-every-port" \
            "V1 1x1 srp-talker --variant valid-destinations" "V8 8x8 srp-talker --variant valid-destinations"; do
  set -- $spec; n=$1; shift
  echo "hs-h$n 10G /bin/bash $T/scripts/r4/hs3.sh $C h$n $* > $T/r4/logs/hs-h$n.log 2>&1"
done
echo "W-rtl-fast 10G mkdir -p $O; for j in changes verilator-lint bdd-conformance yosys-tool yosys-elaboration publication-census split-cdc rtl-fast; do $W rtl-fast.yml $H \$j $O > $O/rtl-fast-\$j.driver.log 2>&1; done"
echo "W-docs-a 10G mkdir -p $O; for j in wire-accountability docs-check-no-git docs-check; do $W docs.yml $H \$j $O > $O/docs-\$j.driver.log 2>&1; done"
for j in docs-gates-0 docs-gates-1 docs-gates-2; do echo "W-$j 10G mkdir -p $O; $W docs.yml $H $j $O > $O/docs-$j.driver.log 2>&1"; done
