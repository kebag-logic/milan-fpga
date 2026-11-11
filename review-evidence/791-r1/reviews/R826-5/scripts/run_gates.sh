#!/usr/bin/env bash
# The gates this round ran at PR #888 head 6a5acf06, from the checkout root.
# Usage: run_gates.sh <checkout> <receipts-dir> <scratch-dir>
# The LiteX interpreter is the venv sw/litex/sweep.sh puts on PATH
# ($HOME/litex-milan/venv); set LITEX_PY to override.
set -u
C=$(cd "$1" && pwd); R=$2; S=$3; mkdir -p "$R" "$S/region"
LITEX_PY=${LITEX_PY:-$HOME/litex-milan/venv/bin/python3}
export TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 PATH="$(dirname "$LITEX_PY"):$PATH"
cd "$C" || exit 2
( python3 scripts/check_py_idiom.py > "$R/py_idiom.log" 2>&1; echo $? > "$R/py_idiom.rc" ) &
( python3 scripts/check_py_idiom.py --selftest > "$R/py_idiom_selftest.log" 2>&1; echo $? > "$R/py_idiom_selftest.rc" ) &
( cd sw/litex && python3 test_ctrl_memory.py > "$R/test_ctrl_memory.log" 2>&1; echo $? > "$R/test_ctrl_memory.rc" ) &
( python3 tb/verilator/ctrl_region_decode/run.py --build-dir "$S/region" --self-test > "$R/region_selftest.log" 2>&1
  echo $? > "$R/region_selftest.rc" ) &
( git diff --check 1d6bf555..HEAD > "$R/diff_check.log" 2>&1; echo $? > "$R/diff_check.rc" ) &
wait
for f in "$R"/*.rc; do echo "$(basename "$f") $(cat "$f")"; done
# The docs gates were run the same way from a scratch clone (see gate_probes.sh):
#   python3 -I scripts/docs_check.py ; python3 -I scripts/check_doc_paths.py
