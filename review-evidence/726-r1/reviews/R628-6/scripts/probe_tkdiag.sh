#!/bin/sh
# probe_tkdiag.sh REPO WORK VARIANT
# Builds tb/verilator/tkdiag from REPO with KL_talker_diag_ctx.sv either
# unchanged (VARIANT=clean) or with one disposable plant staged under WORK,
# then runs the bench and prints its summary. Nothing in REPO is written.
set -u
REPO=$(cd "$1" && pwd); WORK=$2; VARIANT=$3
mkdir -p "$WORK"; WORK=$(cd "$WORK" && pwd)
SRC="$REPO/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv"
DST="$WORK/KL_talker_diag_ctx.sv"
cp "$SRC" "$DST"
case "$VARIANT" in
  clean) ;;
  tx-start-drop)
    # a PDU completing in the start-edge cycle is not counted
    python3 -I - "$DST" <<'EOF'
import sys
p = sys.argv[1]; t = open(p).read()
old = "ftx_r[c]    <= {31'd0, ev_f_w[c]};"
assert t.count(old) == 1, "anchor"
open(p, "w").write(t.replace(old, "ftx_r[c]    <= '0;"))
EOF
    ;;
  tx-saturate)
    python3 -I - "$DST" <<'EOF'
import sys
p = sys.argv[1]; t = open(p).read()
old = "ftx_r[c] <= ftx_r[c] + 32'd1;"
assert t.count(old) == 1, "anchor"
open(p, "w").write(t.replace(old, "if (ftx_r[c] != 32'hFFFFFFFF) ftx_r[c] <= ftx_r[c] + 32'd1;"))
EOF
    ;;
  *) echo "unknown variant"; exit 2;;
esac
B="$REPO/tb/verilator/tkdiag"
sed 's|"../../common/|"'"$REPO"'/tb/common/|' "$B/sim_main.cpp" > "$WORK/sim_main.cpp"
"${VERILATOR:-verilator}" --cc --exe --build -j 2 --top-module tkdiag_tb_top \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-GENUNNAMED \
  -CFLAGS "-std=c++17 -O2 -I$REPO/tb/verilator/tkdiag" --Mdir "$WORK/obj" \
  "$DST" "$REPO/hdl/ieee1722/avtp/KL_media_clock_restart.sv" "$B/tkdiag_tb_top.sv" \
  "$WORK/sim_main.cpp" -o Vtkdiag_sim > "$WORK/build.log" 2>&1 || { echo "BUILD FAILED"; tail -20 "$WORK/build.log"; exit 3; }
( cd "$B" && "$WORK/obj/Vtkdiag_sim" ) > "$WORK/run.log" 2>&1
rc=$?
echo "tkdiag $VARIANT rc=$rc"
grep -E "FAIL|checks|RESULT|passed|failed" "$WORK/run.log" | tail -8
exit 0
