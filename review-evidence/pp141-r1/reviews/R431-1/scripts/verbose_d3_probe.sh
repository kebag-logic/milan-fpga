#!/bin/sh
# Disposable probe: export a revision's tree, make CHECK print passing checks
# too ("PASS: ..."), and run section D3 alone. Usage:
#   verbose_d3_probe.sh REPO REV WORKDIR VERILATOR
set -eu
REPO="$1"; REV="$2"; W="$3"; V="$4"
rm -rf "$W"; mkdir -p "$W"
git -C "$REPO" archive "$REV" | tar -x -C "$W"
python3 - "$W/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '  if (!(cond)) { ++h.fails; printf("FAIL: " __VA_ARGS__); printf("\\n"); } \\\n'
new = ('  if (!(cond)) { ++h.fails; printf("FAIL: " __VA_ARGS__); printf("\\n"); } \\\n'
       '  else { printf("PASS: " __VA_ARGS__); printf("\\n"); } \\\n')
assert s.count(old) == 1, "CHECK macro text not found exactly once"
open(p, 'w').write(s.replace(old, new))
PY
make -C "$W/tb/pp_top" d3 VERILATOR="$V"
