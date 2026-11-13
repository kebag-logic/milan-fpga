#!/bin/bash
# Round 31's gates at the lane's head, one log and one rc per gate, never piped. usage: gates31.sh OUTDIR
set -u
O=$1
mkdir -p "$O" $TMPDIR
cd $LANE || exit 3
H=$(git rev-parse HEAD)
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo $rc > "$O/$id.rc"; echo "$id rc=$rc" >> "$O/summary.txt"; }
: > "$O/summary.txt"
echo "head $H" >> "$O/summary.txt"
run git_status "git status --short --untracked-files=all"
run diff_check "git diff --check 32551422 HEAD"
run docs_check "python3 -B scripts/docs_check.py"
run doc_style "python3 -B scripts/check_doc_style.py"
run em_dash "$DOCS_VENV/bin/python -B scripts/check_em_dash.py --base 32551422"
run em_dash_selftest "$DOCS_VENV/bin/python -B scripts/check_em_dash.py --selftest"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run test_ctrl_memory "PATH=$LITEX_VENV/bin:$RV32_SDK/host/bin:\$PATH PYTHONHASHSEED=0 TMPDIR=$TMPDIR python3 -B sw/litex/test_ctrl_memory.py"
run s14_reason_grep "! grep -n 'owed to S14' sw/litex/ctrl_memory.py"
run diff_vs_dev_soft_core "git diff e5f88a8e HEAD -- docs/design/SPLIT_CONTROL_MEMORY.md"
run diff_round "git diff --stat 32551422 HEAD"
