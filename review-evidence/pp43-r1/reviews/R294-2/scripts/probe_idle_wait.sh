#!/usr/bin/env bash
# R294 round-2 probe W (disposable): the harness integrator keeps gsi_wait_i
# HIGH whenever gsi_req_o is LOW (the engine documents wait as "HOLD the beat
# (not a ready)", qualified by the request, so a registered-busy integrator
# may leave it high between beats). Runs the GI phase on an extracted tree,
# optionally with the top's internal-selector wait mask removed.
# Usage: probe_idle_wait.sh <extracted-tree> <log> [mutate]
set -euo pipefail
tree=$1; log=$2; mode=${3:-}
here=$(cd "$(dirname "$0")" && pwd)
python3 - "$tree" "$mode" <<'PY'
import sys
from pathlib import Path
tree, mode = Path(sys.argv[1]), sys.argv[2]
sm = tree / "tb/pp_top/sim_main.cpp"
s = sm.read_text()
old = ("  void serve_milan_info_face() {\n"
       "    d->gsi_wait_i = 0;\n")
new = ("  void serve_milan_info_face() {\n"
       "    d->gsi_wait_i = gsi_retired_stuck && !d->gsi_req_o;  // R294 probe W\n")
assert s.count(old) == 1
sm.write_text(s.replace(old, new))
if mode == "mutate":
    top = tree / "hdl/top/protocol_processor_top.sv"
    t = top.read_text()
    o = "assign aecp_gsi_wait_w = !gsi_internal_w && gsi_wait_i;"
    assert t.count(o) == 1
    top.write_text(t.replace(o, "assign aecp_gsi_wait_w = gsi_wait_i;"))
print("patched", tree, mode or "head")
PY
cd "$tree/tb/pp_top"
rm -rf obj_dir
make gsi-build VERILATOR="$here/verilator8" > "$log.build" 2>&1
./obj_dir/Vpp_top_sim --gsi-internal-only > "$log" 2>&1 || true
grep -m4 '^FAIL' "$log" || true
grep -E 'checks, ' "$log"
