#!/usr/bin/env bash
# [R293] R293-3 composition gates for issue #514 / PR #552 merge-train candidate.
# Usage: run_composition_gates.sh <repo> <python-with-locked-renderer> <outdir>
# The Python needs the hash-locked tools/markdown lock and pyyaml (as the docs
# workflow installs). Runs each gate in the foreground from <repo>, writing <outdir>/<name>.log and
# one "<name> rc=<n>" line per gate to <outdir>/SUMMARY.txt.
set -u
REPO=$1 PY=$2 OUT=$3
PARENT=cf43b4716772582d0c77d40f1eeac5934a0cd9da
SRCBASE=3d2f3e3131c9db5898e1db9dd3e2a35149843109
mkdir -p "$OUT"; : > "$OUT/SUMMARY.txt"
cd "$REPO" || exit 2
{ echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"; "$PY" --version; } > "$OUT/IDENTITY.txt" 2>&1
run() {
  local name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc" >> "$OUT/SUMMARY.txt"
}
run docs_check               "$PY" scripts/docs_check.py
run docs_check_nogit         env GIT_DIR=/dev/null "$PY" scripts/docs_check.py
run em_dash_base_parent      "$PY" scripts/check_em_dash.py --base "$PARENT"
run em_dash_base_srcbase     "$PY" scripts/check_em_dash.py --base "$SRCBASE"
run em_dash_selftest         "$PY" scripts/check_em_dash.py --selftest
run doc_style                "$PY" scripts/check_doc_style.py
run doc_style_selftest       "$PY" scripts/check_doc_style.py --selftest
run gen_toc_check            "$PY" scripts/gen_toc.py --check
run gen_toc_verify_anchors   "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest         "$PY" scripts/gen_toc.py --selftest
run doc_paths                "$PY" scripts/check_doc_paths.py
run py_idiom                 "$PY" scripts/check_py_idiom.py
run py_idiom_selftest        "$PY" scripts/check_py_idiom.py --selftest
run hygiene_check            "$PY" scripts/check_hygiene.py --check
run todo_ownership           "$PY" scripts/check_todo_ownership.py
run test_evidence_check      "$PY" scripts/measure_test_evidence.py --check
run naming_check             "$PY" scripts/measure_naming.py --check
run fail_fast_check          "$PY" scripts/measure_fail_fast.py --check
run feature_status           "$PY" scripts/check_feature_status.py
run ci_events_check          "$PY" scripts/ci_events.py --check
run ci_events_selftest       "$PY" scripts/ci_events.py --selftest
run containment_selftest     "$PY" scripts/check_merge_containment.py --selftest
run diff_check_parent        git diff --check "$PARENT" HEAD
cat "$OUT/SUMMARY.txt"
