#!/bin/sh
# The same reviewer probes with the BASE (c951a9ff) KL_pp_maap.sv, to tell
# pre-existing behaviour from behaviour this PR introduced. Only the RTL file
# differs; the head harness (with its kind-7 stub) is port-compatible.
set -u
. "$(dirname "$0")/00_env.sh"
BASE_SHA=c951a9ff0cb5851fb159d33e966e5a2a9a188fe3
T="$PKT/scratch/probe"
R="$PKT/receipts/probes"
"$PKT/scripts/04_probes.sh" > /dev/null
git -C "$CLONE" show "$BASE_SHA:hdl/maap/KL_pp_maap.sv" > "$T/hdl/maap/KL_pp_maap.sv"
python3 - "$T/tb/maap/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
k = "  a_release_mid_redraw_leaves_no_draw_behind();\n"
assert s.count(k) == 1
s = s.replace(k, "")                        # base RTL wedges in U17b by design
s = "#define R401_SKIP_P1 1\n" + s
open(p, "w").write(s)
PY
rm -rf "$T/tb/maap/obj_dir"
make -C "$T/tb/maap" VERILATOR="$VLT" run > "$R/probes-base-rtl.log" 2>&1
echo "probes on base RTL rc=$?" | tee "$R/rc-base-rtl.txt"
grep -E '^(OBS|FAIL)|checks:' "$R/probes-base-rtl.log"
