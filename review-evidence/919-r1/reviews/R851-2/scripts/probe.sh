#!/bin/sh
# Insert reviewer_probes.cpp into a disposable copy's test_plat_phy.cpp before its closing namespace brace.
# usage: probe.sh <copy-root> <reviewer_probes.cpp>
set -eu
t="$1/sw/firmware/ctrl/test/test_plat_phy.cpp"
grep -q '^}  // namespace$' "$t"
python3 -I - "$t" "$2" <<'PY'
import sys
t, p = sys.argv[1], sys.argv[2]
s = open(t).read(); i = s.rindex("}  // namespace")
s = s[:i] + open(p).read() + "\n" + s[i:]
if "#include <cstdio>" not in s: s = "#include <cstdio>\n" + s
open(t, "w").write(s)
PY
