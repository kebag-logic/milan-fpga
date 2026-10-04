#!/bin/bash
# R456-3 static gates for #643 / PR #648 at 36207e91, in a disposable clone.
# Usage: r3_gates.sh TREE MDVENV   (prints one "rc=<n> <gate>" line per gate)
set -u
T=$1; V=$2; cd "$T" || exit 9
g() { local name=$1; shift; "$@" > /tmp/r456-3-gate.$$ 2>&1; local rc=$?
      echo "rc=$rc $name"; tail -n 4 /tmp/r456-3-gate.$$ | sed 's/^/    /'; }
g "docs_check"                     python3 scripts/docs_check.py
g "check_doc_style"                python3 scripts/check_doc_style.py
g "check_doc_paths"                python3 scripts/check_doc_paths.py
g "check_em_dash --base 241f9184"  "$V/bin/python3" scripts/check_em_dash.py --base 241f91845230ae410506dffb16b71937127fd175
g "check_em_dash --base 6b96391d"  "$V/bin/python3" scripts/check_em_dash.py --base 6b96391d13c5d777a98b1c7be9265c63d651c911
g "gen_toc --check"                "$V/bin/python3" scripts/gen_toc.py --check
g "gen_toc --verify-anchors"       "$V/bin/python3" scripts/gen_toc.py --verify-anchors
g "check_cpp_idiom"                python3 scripts/check_cpp_idiom.py
g "check_py_idiom"                 python3 scripts/check_py_idiom.py
g "check_hygiene"                  python3 scripts/check_hygiene.py
g "py_compile tdm8_render_mutants" python3 -m py_compile tb/verilator/milan_dp_render/tdm8_render_mutants.py
rm -f /tmp/r456-3-gate.$$
