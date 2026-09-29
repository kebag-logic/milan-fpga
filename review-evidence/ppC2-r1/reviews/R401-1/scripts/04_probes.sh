#!/bin/sh
# Append the reviewer probes to a scratch copy of the head tb/maap suite and run it.
set -u
. "$(dirname "$0")/00_env.sh"
S="$PKT/scratch/head"
T="$PKT/scratch/probe"
R="$PKT/receipts/probes"
mkdir -p "$R"
rm -rf "$T"; mkdir -p "$T/tb"
cp -r "$S/hdl" "$T/hdl"; cp -r "$S/tb/maap" "$S/tb/common" "$T/tb/"
rm -rf "$T/tb/maap/obj_dir"
python3 - "$T/tb/maap/sim_main.cpp" "$PKT/scripts/probe_scenarios.inc" <<'PY'
import sys
p, inc = sys.argv[1], open(sys.argv[2]).read()
s = open(p).read()
a = "  void announce_during_probe_yields_without_tie_break();\n"
b = "int MaapAnnexBSuite::run() {"
c = "  announce_during_probe_yields_without_tie_break();\n\n  printf("
for k in (a, b, c):
    assert s.count(k) == 1, k
s = s.replace(a, a + "  void r401_probes();\n")
s = s.replace(b, inc + "\n" + b)
s = s.replace(c, "  announce_during_probe_yields_without_tie_break();\n  r401_probes();\n\n  printf(")
open(p, "w").write(s)
PY
make -C "$T/tb/maap" VERILATOR="$VLT" run > "$R/probes.log" 2>&1
echo "probes rc=$?" | tee "$R/rc.txt"
grep -E '^(OBS|FAIL)|checks:' "$R/probes.log"
