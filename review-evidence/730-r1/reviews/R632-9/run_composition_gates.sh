#!/usr/bin/env bash
# Composition gates for the #730 merge-train candidate.
# Usage: run_composition_gates.sh <candidate-checkout> <receipt-dir>
# Runs, in parallel, every offline gate that reads docs/testing/CI_WORKFLOWS.md,
# scripts/act_ci.py or the predecessor-changed gate scripts. Never runs
# scripts/act_ci.py itself (host execution of the runner is out of scope).
set -u
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
cd "$repo" || exit 2
SRC_BASE=dc4d06cbfec209cc2ff76806f4b49c51f46639ae   # PR #731 base
TRAIN_PARENT=ada26e56ac42ee5de311aef84cb86c8435b97cee # candidate first parent
DEV=49da9fd974e8805d56c90e29dcfcb67994c2c430          # live dev
MDPY=${MD_PYTHON:-python3}  # interpreter with the pinned cmarkgfm/html5lib renderer

run() { # name, command...
  local name=$1; shift
  ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
}
run docs_check            python3 -I scripts/docs_check.py
run doc_style             python3 -I scripts/check_doc_style.py
run doc_style_selftest    python3 -I scripts/check_doc_style.py --selftest
run gen_toc_check         "$MDPY" -I scripts/gen_toc.py --check
run gen_toc_anchors       "$MDPY" -I scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      "$MDPY" -I scripts/gen_toc.py --selftest
run em_dash_train_parent  "$MDPY" -I scripts/check_em_dash.py --base "$TRAIN_PARENT"
run em_dash_src_base      "$MDPY" -I scripts/check_em_dash.py --base "$SRC_BASE"
run em_dash_dev           "$MDPY" -I scripts/check_em_dash.py --base "$DEV"
run em_dash_selftest      "$MDPY" -I scripts/check_em_dash.py --selftest
run doc_paths             python3 -I scripts/check_doc_paths.py
run doc_map_check         python3 -I docs/DOC_MAP.gen.py --check
run archive               python3 -I scripts/check_archive.py
run ci_events_check       python3 -I scripts/ci_events.py --check
run ci_events_selftest    python3 -I scripts/ci_events.py --selftest
run ci_scope_selftest     python3 -I scripts/ci_scope.py --selftest
run py_idiom              python3 -I scripts/check_py_idiom.py
run py_idiom_selftest     python3 -I scripts/check_py_idiom.py --selftest
run baremetal_check       python3 -I scripts/check_baremetal_only.py --check
run baremetal_selftest    python3 -I scripts/check_baremetal_only.py --selftest
run test_evidence_check   python3 -I scripts/measure_test_evidence.py --check
run hygiene_check         python3 -I scripts/check_hygiene.py --check
run fail_fast_check       python3 -I scripts/measure_fail_fast.py --check
run suite_shards_selftest python3 -I scripts/suite_shards.py --selftest
run diff_check_train      git diff --check "$TRAIN_PARENT" HEAD
run diff_check_src        git diff --check "$SRC_BASE" HEAD -- docs/testing/CI_WORKFLOWS.md scripts/act_ci.py
wait
for f in "$out"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | tee "$out/SUMMARY.txt"
