#!/bin/sh
# R301-4 gate commands, as run from a clone at 4538d7c03dc4f56d7ed4c971603e15bda82050a8.
# Usage: sh commands.sh <repo-root> <packet-root> <python-with-pinned-renderer>
# The renderer interpreter is a private venv built with
#   python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
set -u
ROOT=$1 PKT=$2 PY=$3
R=$PKT/receipts
cd "$ROOT" || exit 2
git diff --no-color b376f6113..4538d7c03 > "$R/delta.diff"
python3 scripts/docs_check.py > "$R/docs_check.py.log" 2>&1; echo "docs_check rc=$?"
python3 scripts/docs_check.py --selftest > "$R/docs_check.py_--selftest.log" 2>&1; echo "docs_check --selftest rc=$?"
python3 scripts/measure_test_evidence.py --check > "$R/measure_test_evidence.py_--check.log" 2>&1; echo "mte --check rc=$?"
python3 scripts/measure_test_evidence.py --selftest > "$R/measure_test_evidence.py_--selftest.log" 2>&1; echo "mte --selftest rc=$?"
"$PY" scripts/gen_toc.py --verify-anchors > "$R/gen_toc_verify_anchors.log" 2>&1; echo "gen_toc --verify-anchors rc=$?"
"$PY" scripts/gen_toc.py > "$R/gen_toc_check.log" 2>&1; echo "gen_toc rc=$?"
NOGIT=$PKT/scratch/nogit; rm -rf "$NOGIT"; mkdir -p "$NOGIT"
git archive HEAD | tar -x -C "$NOGIT"
(cd "$NOGIT" && python3 -B scripts/docs_check.py) > "$R/docs_check_nogit.log" 2>&1; echo "docs_check no-git rc=$?"
"$PY" scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7 > "$R/check_em_dash_base.log" 2>&1; echo "em_dash rc=$?"
for c in check_doc_style check_doc_paths check_py_idiom; do
  "$PY" scripts/$c.py > "$R/$c.log" 2>&1; echo "$c rc=$?"
done
python3 "$PKT/scripts/derive_counts.py" "$ROOT" > "$R/derive_counts_head.log"; echo "derive_counts head rc=$? (1 = the two dated records, see S1)"
B=$PKT/scratch/b376; rm -rf "$B"; mkdir -p "$B"
git archive b376f6113 scripts/measure_test_evidence.py tb/verilator/milan_dp \
  tb/verilator/mmcm_servo/slew_mutants.py docs/testing/TESTING.md | tar -x -C "$B"
python3 "$PKT/scripts/derive_counts.py" "$B" > "$R/derive_counts_b376f611.log"; echo "derive_counts parent rc=$?"
rm -rf scripts/__pycache__
