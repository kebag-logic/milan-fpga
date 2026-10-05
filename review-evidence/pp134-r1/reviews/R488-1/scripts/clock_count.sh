#!/bin/sh
# R488-1: measure the complete default srp_top run in DUT clocks at a tree.
# Usage: clock_count.sh <tree> <log>   (tree = git-archive extraction, scratch only)
set -eu
T=$1; L=$2
python3 - "$T/tb/srp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '    printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n    return fails ? 1 : 0;'
assert s.count(old) == 1
s = s.replace(old, '    printf("R488_TOTAL_CLOCKS %llu\\n", (unsigned long long)h.t);\n' + old)
open(p, "w").write(s)
PY
make -C "$T/tb/srp_top" VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator run > "$L" 2>&1
