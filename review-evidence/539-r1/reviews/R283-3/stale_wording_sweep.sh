#!/bin/sh
# Sweep tb/ docs/ hdl/ at the exact head for #539 wording that still states
# an open step-guard gap, and compare README:388 against GM_LOSS_RECOVERY:181.
# Usage: stale_wording_sweep.sh <repo>
set -u
REPO=${1:?repo}
H=324eb343a870973b64706779d0183ae342dcb3d7
cd "$REPO"
run() { echo "== git grep $*"; git grep -n "$@" "$H" -- tb docs hdl; echo "rc=$?"; }
run -i -e "step guard gap"
run -i -e "guard gap"
run -e "108 to 524" -e "108-524" -e "108 and 524"
run -i -e "integrates a locked" -e "integrated as a rate" -e "integrates the step" -e "integrates it"
run -i -e "#539"
run -i -e "issues/539"
echo "== README:388 vs GM_LOSS_RECOVERY:181"
git show "$H:tb/verilator/milan_dp/README.md" | sed -n 388p
git show "$H:docs/design/GM_LOSS_RECOVERY.md" | sed -n 181p
echo "== sim_gmstep.cpp:14-18"
git show "$H:tb/verilator/milan_dp/sim_gmstep.cpp" | sed -n 14,18p
echo "== Vphc_step target exists"
git show "$H:tb/verilator/mmcm_servo/Makefile" | grep -n "Vphc_step"
echo "== margin arithmetic (4096/384, 20000/4096)"
python3 -I -c "print(round(4096/384,3), round(20000/4096,3))"
echo "SWEEP_DONE"
