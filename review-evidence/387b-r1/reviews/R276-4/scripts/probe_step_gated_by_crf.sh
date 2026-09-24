#!/bin/sh
# Probe: is "a PHC step toggles mr whatever the clock source" graded outside
# the CRF-selected gmstep leg? Plants the step's mr term gated by CRF selection
# into a COPY of milan_datapath.sv and builds the default milan_dp 1x1 leg
# (sim_main.cpp, the obj_dir recipe line of `make -n run`) against it.
# Usage: probe_step_gated_by_crf.sh <repo-at-head> <work-dir> build|run
# Requires Verilator 5.050 first on PATH; run after `make gmstep` (generated
# headers and hex images). Never edits the repository.
set -eu
REPO=$1; WORK=$2; STEP=$3
D=$REPO/tb/verilator/milan_dp
mkdir -p "$WORK"
MUT=$WORK/milan_datapath_step_gated.sv
if [ "$STEP" = build ]; then
  python3 - "$REPO/hdl/milan/milan_datapath.sv" "$MUT" <<'PY'
import sys
s = open(sys.argv[1]).read()
old = "                       | media_rebase_p_w;"
new = "                       | (media_rebase_p_w & crf_clk_selected_r);"
assert s.count(old) == 1, "anchor moved"
open(sys.argv[2], "w").write(s.replace(old, new))
PY
  cd "$D"
  CMD=$(make -n run DP_SRC="$MUT" VERILATOR=verilator VERILATOR_JOBS=8 2>/dev/null | grep -- '-o Vmilan_dp_sim$')
  [ -n "$CMD" ] || { echo "recipe line not found"; exit 2; }
  echo "$CMD" | grep -q "$MUT" || { echo "mutated datapath not in recipe"; exit 2; }
  eval "$CMD --Mdir $WORK/obj_step_gated"
else
  cd "$D" && "$WORK/obj_step_gated/Vmilan_dp_sim" || true
fi
