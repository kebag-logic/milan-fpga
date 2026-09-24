#!/bin/sh
# R277-4 reviewer probe: plant reviewer-chosen engine defects and run the
# committed tkdiag harness (make build with MCR_SRC/TKDIAG_MDIR overridden).
#   usage: tkdiag_extra_mutants.sh <repo-root> <work-dir>
set -u
ROOT=$1; WORK=$2; mkdir -p "$WORK"
E=$ROOT/hdl/ieee1722/avtp/KL_media_clock_restart.sv
plant() { # name, python replace expression
  f=$WORK/$1.sv
  python3 - "$E" "$f" "$2" "$3" <<'PY'
import sys
src=open(sys.argv[1]).read(); a=sys.argv[3]; b=sys.argv[4]
assert src.count(a)==1, "anchor"
open(sys.argv[2],"w").write(src.replace(a,b))
PY
  make -s -C "$ROOT/tb/verilator/tkdiag" build MCR_SRC="$f" TKDIAG_MDIR="$WORK/obj_$1" >/dev/null 2>&1 || { echo "$1: BUILD FAIL"; return; }
  out=$(cd "$ROOT/tb/verilator/tkdiag" && "$WORK/obj_$1/Vtkdiag_sim")
  echo "$1: $(echo "$out" | grep -c '\[FAIL\]') failed checks; $(echo "$out" | grep 'checks:')"
  echo "$out" | grep '\[FAIL\]' | sed 's/^/    /'
}
plant window_plus_one "        if ((restart_p_i | src_change_w) && streaming_i[t] && (hold_r[t] == '0))" "        if ((restart_p_i | src_change_w) && streaming_i[t] && (hold_r[t] <= HOLDW_C'(1)))"
plant no_streaming_term "        if ((restart_p_i | src_change_w) && streaming_i[t] && (hold_r[t] == '0))" "        if ((restart_p_i | src_change_w) && (hold_r[t] == '0))"
plant src_not_request "      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;" "      if (restart_p_i) tgt_r <= ~mr_o;"
plant hold_seven "hold_r[t] == HOLDW_C'(HOLD_PDU_P))) begin : g_adopt" "hold_r[t] >= HOLDW_C'(HOLD_PDU_P - 1))) begin : g_adopt"
