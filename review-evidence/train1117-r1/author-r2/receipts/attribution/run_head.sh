#!/bin/bash
# run_head.sh REV LABEL: decision 3's attribution legs at one head, 1x1/1if: a clone at REV with the scratch
# instruction-count aid (patch_sim.py), arm A's aecp-largest-notice, acmp-notk and datapath-events and the
# answering-every-port arm's notice-burst-5, notice-burst-7 and notice-every-7 (round 1's probe: where the largest
# record, event.MAAP, the datapath events and event.AECP were dearest), built as run.py builds by default.
set -u
REV=$1 L=$2
T=<scratch>
. $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1 BUDGET_INSTR=1
C=$T/attr/clones/$L B=$T/attr/b/$L
mkdir -p $B
[ -d $C ] || $T/bin/clone.sh $REV $C || exit 2
python3 -I $T/attr/patch_sim.py $C/tb/verilator/ctrl_service_budget/sim_main.cpp || exit 2
echo "HEAD $(git -C $C rev-parse HEAD) diff $(git -C $C diff --stat | tail -1) start $(date +%T)"
leg() {  # variant dir groups
  python3 -B $T/tools/legs.py build $C $B/$2 1x1 $1 1 $3 > $B/$2.build.log 2>&1 || { echo "build $2 rc=$?"; return 1; }
  python3 -B $T/tools/legs.py run $C $B/$2 1x1 $1 0 3 > $B/$2.run.log 2>&1; echo "run $2 rc=$? $(date +%T)"
}
leg none none aecp-largest-notice,acmp-notk,datapath-events &
leg answering-every-port aep notice-burst-5,notice-burst-7,notice-every-7 &
wait
echo "END $(date +%T)"
