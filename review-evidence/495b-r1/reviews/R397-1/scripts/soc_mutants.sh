#!/bin/bash
# Item 3 SoC-side mutants in the probe copy, run with the pinned LiteX venv.
# Usage: soc_mutants.sh <probe-tree>
set -u
T=$1; F=$T/sw/litex/milan_soc.py
cp -p "$F" "$F.orig"
old='BAREMETAL_CLK_HZ = runpy.run_path(REPO_ROOT / "tb/verilator/nvm_capture_cpu/recipe.py")["CPU_HZ"]'
check() { (cd "$T" && python3 -B -c "import sys; sys.path.insert(0,'sw/builder'); import test_clock_contract as t; from pathlib import Path; t._assert_clock_source('milan_soc', t.ROOT / 'sw/litex')" > /tmp/r397-soc-mut.log 2>&1); rc=$?; echo "$1: rc=$rc $([ $rc -ne 0 ] && echo KILLED || echo SURVIVED) | $(tail -1 /tmp/r397-soc-mut.log | cut -c1-200)"; }
check CONTROL
python3 - "$F" "$old" 'BAREMETAL_CLK_HZ = 50_000_000' <<'PY'
import sys; p,o,n=sys.argv[1:]; s=open(p).read(); assert s.count(o)==1; open(p,'w').write(s.replace(o,n))
PY
check S7-literal
cp -p "$F.orig" "$F"
python3 - "$F" "$old
sys.path.insert(0, str(REPO_ROOT))" 'sys.path.insert(0, str(REPO_ROOT))
from tb.verilator.nvm_capture_cpu.recipe import CPU_HZ as BAREMETAL_CLK_HZ' <<'PY'
import sys; p,o,n=sys.argv[1:]; s=open(p).read(); assert s.count(o)==1; open(p,'w').write(s.replace(o,n))
PY
check S7-namespace-import
cp -p "$F.orig" "$F"; rm -f "$F.orig" /tmp/r397-soc-mut.log
