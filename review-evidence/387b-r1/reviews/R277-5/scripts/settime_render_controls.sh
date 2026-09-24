#!/bin/sh
# R277-5 reviewer probe: can RENDER-SETTIME (sim_aclk.cpp) fail?
# Plants datapath copies (never the tree file) and builds them through the
# suite's own ACLK recipe (DP_SRC and ACLK_MDIR overridden), then runs the
# true-ratio leg with --render-only (the phases that carry RENDER-SETTIME).
#   omit   - the render trigger drops the settime: media_rebase_p_w -> eff_ptp_adjust_w
#            in render_recentre_p_w only (mr still sees the settime)
#   double - the settime reaches the stage twice: a one-cycle-late copy of the
#            load strobe is ORed into the render trigger
#   usage: settime_render_controls.sh <repo-root> <work-dir>
set -eu
ROOT=$(cd "$1" && pwd); WORK=$2; mkdir -p "$WORK"
D=$ROOT/tb/verilator/milan_dp
DP=$ROOT/hdl/milan/milan_datapath.sv
ANCHOR='  wire render_recentre_p_w /* verilator public_flat_rd */ =
       media_rebase_p_w
       | src_recentre_p_r;'
python3 - "$DP" "$WORK" "$ANCHOR" <<'PY'
import sys, pathlib
dp, work, anchor = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
t = dp.read_text()
assert t.count(anchor) == 1, "anchor moved"
omit = anchor.replace("       media_rebase_p_w\n", "       eff_ptp_adjust_w\n")
double = ("  logic settime_late_r;\n"
          "  always_ff @(posedge axis_clk) settime_late_r <= cfg_ptp_cmd_load;\n"
          + anchor.replace("       media_rebase_p_w\n",
                           "       media_rebase_p_w | settime_late_r\n"))
(work / "omit_milan_datapath.sv").write_text(t.replace(anchor, omit))
(work / "double_milan_datapath.sv").write_text(t.replace(anchor, double))
PY
for c in clean omit double; do
  if [ $c = clean ]; then src=$DP; else src=$WORK/${c}_milan_datapath.sv; fi
  make -s -C "$D" aclk-build DP_SRC="$src" ACLK_MDIR="$WORK/obj_$c" >"$WORK/build_$c.log" 2>&1 \
    || { echo "$c: BUILD FAILED"; continue; }
  (cd "$D" && "$WORK/obj_$c/Vmilan_dp_aclk" --render-only >"$WORK/run_$c.log" 2>&1) && rc=0 || rc=$?
  echo "== $c: rc=$rc; $(grep -E '^media_aclk: ' "$WORK/run_$c.log")"
  grep -E 'RENDER-SETTIME|\[FAIL\]' "$WORK/run_$c.log" || true
done
