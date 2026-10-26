#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probe runner (R709-1, issue #202). Builds tb/acmp_talker from a
# pristine tree with the reviewer section r709_cases.hpp added, optionally
# after one exact-text RTL edit (a planted mutant), and runs it.
#   run_talker_probe.sh SRC_TREE WORK_DIR VERILATOR [EDIT_PY]
# SRC_TREE is never modified; WORK_DIR is created fresh. EDIT_PY, when
# given, is a python file defining OLD and NEW strings for
# hdl/acmp/KL_acmp_talker.sv (OLD must occur exactly once).
# Exit status = the bench's exit status (0 = every check passed), 97 = edit refused.
set -euo pipefail
src=$1; work=$2; ver=$3; edit=${4:-}
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$work"; mkdir -p "$work"
cp -a "$src/hdl" "$src/tb" "$work/"
tal="$work/tb/acmp_talker"
cp "$here/r709_cases.hpp" "$tal/"
python3 -I - "$tal/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]
t = open(p).read()
a = '#include "sid_cases.hpp"\n'
b = '  check_sid_cases();\n'
assert t.count(a) == 1 and t.count(b) == 1
t = t.replace(a, a + '#include "r709_cases.hpp"\n').replace(b, b + '  r709_run(*this);\n')
open(p, 'w').write(t)
PY
if [ -n "$edit" ]; then
  python3 -I - "$work/hdl/acmp/KL_acmp_talker.sv" "$edit" <<'PY' || exit 97
import sys, runpy
p, e = sys.argv[1], sys.argv[2]
d = runpy.run_path(e)
t = open(p).read()
if t.count(d['OLD']) != 1:
    sys.exit(1)
open(p, 'w').write(t.replace(d['OLD'], d['NEW']))
PY
fi
cd "$tal"
make VERILATOR="$ver" run
