#!/bin/sh
# Reviewer control: the WAITING latch skips the one cycle in which the
# IDENT-BURST expiry arrives (gap_r still 1). Runs section ID (the lane's
# suite) and the reviewer probes on the planted copy.
# Usage: boundary_control.sh HEAD_EXPORT WORK_DIR
set -eu
here=$(cd "$(dirname "$0")" && pwd)
src=$1
work=$2
rm -rf "$work"
mkdir -p "$work"
cp -a "$src/hdl" "$src/tb" "$src/scripts" "$work/"
rm -rf "$work/tb/pp_top/obj_dir" "$work/tb/pp_top/obj_idn" "$work/tb/pp_top/obj_vid"
python3 - "$work/hdl/aecp/KL_aecp_notify.sv" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
old = "            if (btn_q2_r && gap_r) prs_r <= 1'b1;\n"
assert s.count(old) == 1
p.write_text(s.replace(old, "            if (btn_q2_r && gap_r && !exp_b_w) prs_r <= 1'b1;\n"))
PY
echo "== section ID (the lane's suite) on the planted copy"
(cd "$work/tb/pp_top" && make identify-build VERILATOR="$here/vl8.sh" > build.log 2>&1 && ./obj_idn/Vpp_top_idn | grep -E '^FAIL|checks, [0-9]+ failures') || true
echo "== reviewer probes on the planted copy"
"$here/run_probes.sh" "$work" "$work-probes" | grep -E "^FAIL|RP3h|RP3j|checks, [0-9]+ failures" || true
