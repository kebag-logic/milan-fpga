#!/bin/sh
# Append reviewer probes to a scratch copy of the head tb/maap suite and run it.
#   r1: the R401-1 probes P1, P1c, P2, P3 (P3 re-graded by the #66 ruling)
#   r2: the R401-2 probes Q1 to Q4
# Optional: PROBE_HDL=<dir> runs the same probes against another hdl/ tree.
set -u
. "$(dirname "$0")/00_env.sh"
S="$PKT/scratch/head"
R="$PKT/receipts/probes"
mkdir -p "$R"
for set in r1 r2; do
  T="$PKT/scratch/probe-$set${PROBE_TAG:-}"
  rm -rf "$T"; mkdir -p "$T/tb"
  cp -r "${PROBE_HDL:-$S/hdl}" "$T/hdl"; cp -r "$S/tb/maap" "$S/tb/common" "$T/tb/"
  rm -rf "$T/tb/maap/obj_dir"
  python3 - "$T/tb/maap/sim_main.cpp" "$PKT/scripts/${set}_probe_scenarios.inc" <<'PY'
import sys
p, inc = sys.argv[1], open(sys.argv[2]).read()
s = open(p).read()
a = "  void announce_during_probe_yields_without_tie_break();\n"
b = "int MaapAnnexBSuite::run() {"
c = "  announce_during_probe_yields_without_tie_break();\n\n  printf("
for k in (a, b, c):
    assert s.count(k) == 1, k
s = s.replace(a, a + "  void r401_probes();\n  void r401_fall_sweep(int source);\n")
s = s.replace(b, inc + "\n" + b)
s = s.replace(c, "  announce_during_probe_yields_without_tie_break();\n  r401_probes();\n\n  printf(")
open(p, "w").write(s)
PY
  make -C "$T/tb/maap" VERILATOR="$VLT" run > "$R/probes-$set${PROBE_TAG:-}.log" 2>&1
  echo "probes $set${PROBE_TAG:-} rc=$?" | tee -a "$R/summary${PROBE_TAG:-}.txt"
  grep -E '^(OBS: [PQ]|FAIL)|checks:' "$R/probes-$set${PROBE_TAG:-}.log" | tee -a "$R/summary${PROBE_TAG:-}.txt"
done
