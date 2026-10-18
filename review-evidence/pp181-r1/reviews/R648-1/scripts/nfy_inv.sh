#!/usr/bin/env bash
# Temporal induction of the occupancy invariant of KL_aecp_notify:
#   cmdq_nempty_r == (cmdq_count_r != 0) in every cycle after the reset cycle.
# A probe copy gets one kept internal wire inv_ok_w after the amap_busy_o
# assign; nothing else changes.
# usage: nfy_inv.sh <tree> <workdir> [chparam assignments...]
set -u
tree=$1; wd=$2; shift 2
SV2V=${SV2V:-$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v}
YOSYS=${YOSYS:-yosys}
mkdir -p "$wd"
python3 -I - "$tree/hdl/aecp/KL_aecp_notify.sv" "$wd/notify_probe.sv" <<'EOF' || exit 3
import sys
src = open(sys.argv[1]).read()
anchor = "  assign prng_draw_kind_o = 3'd4;"
assert src.count(anchor) == 1
src = src.replace(anchor, "  (* keep *) wire inv_ok_w = (cmdq_nempty_r == (cmdq_count_r != 5'd0));\n" + anchor)
open(sys.argv[2], "w").write(src)
EOF
"$SV2V" "$tree/hdl/common/pp_pkg.sv" "$wd/notify_probe.sv" >"$wd/notify.v" || exit 3
set_params=""
[ $# -gt 0 ] && set_params="chparam $(printf -- '-set %s ' "$@" | sed 's/=/ /g') KL_aecp_notify"
cat >"$wd/inv.ys" <<EOF
read_verilog $wd/notify.v
$set_params
hierarchy -top KL_aecp_notify
proc; flatten; memory; opt -fast
sat -tempinduct -prove inv_ok_w 1 -set-at 1 rst_n 0 -seq 1 -maxsteps 1 -verify
EOF
"$YOSYS" -q -l "$wd/inv.log" "$wd/inv.ys" >/dev/null 2>&1; rc=$?
v=$(grep -E "Induction step proven|Induction step failed|proof did fail|ERROR" "$wd/inv.log" | tail -1)
echo "params=[$*] rc=$rc [$v]"
exit $rc
