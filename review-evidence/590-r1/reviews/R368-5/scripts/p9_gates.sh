#!/usr/bin/env bash
# P9: focused Markdown, idiom and source gates at the exact head, run in a
# scratch clone with the pinned Markdown interpreter. One log per gate.
# Usage: p9_gates.sh <scratch clone at head> <out dir> <pinned python>
set -u
C=$1; OUT=$2; PY=$3; BASE=b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a
cd "$C"
test "$(git rev-parse HEAD)" = 4c2a30debb031595b81c5c4bfc53b601a0fec528 || { echo "wrong head"; exit 2; }
run() { local name=$1; shift; "$@" > "$OUT/gate-$name.log" 2>&1; local rc=$?; echo "$name rc=$rc"; }
run em-dash            "$PY" scripts/check_em_dash.py --base "$BASE"
run em-dash-selftest   "$PY" scripts/check_em_dash.py --selftest
run docs-check         "$PY" scripts/docs_check.py
run feature-status     "$PY" scripts/check_feature_status.py
run doc-style          "$PY" scripts/check_doc_style.py
run toc-check          "$PY" scripts/gen_toc.py --check
run toc-anchors        "$PY" scripts/gen_toc.py --verify-anchors
run solution-docs      "$PY" scripts/check_solution_docs.py
run submodule-docs     "$PY" scripts/check_submodule_docs.py
run baremetal-only     "$PY" scripts/check_baremetal_only.py --check
run cpp-idiom          "$PY" scripts/check_cpp_idiom.py
run py-idiom           "$PY" scripts/check_py_idiom.py
run hygiene            "$PY" scripts/check_hygiene.py --check
run test-evidence      "$PY" scripts/measure_test_evidence.py --check
run archive            "$PY" scripts/check_archive.py
run nvm-capture        "$PY" scripts/check_nvm_capture.py
run diff-check         git diff --check "$BASE" HEAD
echo "worktree after gates:"; git status --porcelain
