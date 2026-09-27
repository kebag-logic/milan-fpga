#!/usr/bin/env bash
# R346-4 composition gates for the #396 merge-train candidate.
# Usage: run_gates.sh <candidate-clone> <python-with-pinned-markdown-deps> <receipt-dir>
# Each gate runs in the foreground; stdout+stderr and rc are recorded per gate.
set -u
REPO=${1:?candidate clone}
PY=${2:?python}
OUT=${3:?receipt dir}
PARENT=a054172abc5c1b6bce5d4c3f06830b603f37b157
SRCBASE=ac18b50968b12efe4d15c0a06301264b35656b31
HEAD_EXPECT=10a5bf59a6a73e9b6487d9ea6f42669ce142ae25
mkdir -p "$OUT"
cd "$REPO" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD_EXPECT" ] || { echo "wrong head"; exit 2; }
DUT_SPEC='entity=0011223344556677,mac=001122334455,talkers=8,listeners=8,crf_out=8,crf_in=8'
PEER_SPEC='entity=8899aabbccddeeff,mac=8899aabbccdd,talkers=8,listeners=8,crf_out=8,crf_in=8'
run() {
  name=$1; shift
  "$@" >"$OUT/$name.log" 2>&1
  rc=$?
  printf '%s rc=%d cmd=%s\n' "$name" "$rc" "$*" | tee -a "$OUT/SUMMARY.txt"
}
: >"$OUT/SUMMARY.txt"
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})" >>"$OUT/SUMMARY.txt"
run docs_check            "$PY" -B scripts/docs_check.py
run docs_check_selftest   "$PY" -B scripts/docs_check.py --selftest
run check_doc_paths       "$PY" -B scripts/check_doc_paths.py
run gen_toc_check         "$PY" -B scripts/gen_toc.py --check
run gen_toc_verify_anchors "$PY" -B scripts/gen_toc.py --verify-anchors
run em_dash_parent        "$PY" -B scripts/check_em_dash.py --base "$PARENT"
run em_dash_srcbase       "$PY" -B scripts/check_em_dash.py --base "$SRCBASE"
run em_dash_selftest      "$PY" -B scripts/check_em_dash.py --selftest
run doc_style             "$PY" -B scripts/check_doc_style.py
run py_idiom              "$PY" -B scripts/check_py_idiom.py
run feature_status        "$PY" -B scripts/check_feature_status.py
run feature_status_selftest "$PY" -B scripts/check_feature_status.py --self-test
run ci_events_check       "$PY" -B scripts/ci_events.py --check
run ci_events_selftest    "$PY" -B scripts/ci_events.py --selftest
run torture_selftest      "$PY" -B tb/tools/torture_campaign.py --self-test
run torture_release_mutants "$PY" -B tb/tools/torture_release_mutants.py
run torture_plan_6d       "$PY" -B tb/tools/torture_campaign.py --plan --areas soak,power --json \
  --dut "$DUT_SPEC" --peer "$PEER_SPEC" \
  --soak-duration-s 604800 --soak-interval-s 60 \
  --power-cycles 200 --idle-cycles 160 --commit-cycles 40 \
  --persisted-items stream_binding --restore-bound-s 30 --boot-margin-s 5 \
  --power-off-hold-s 8
run torture_coverage_6d   "$PY" -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power \
  --dut "$DUT_SPEC" --peer "$PEER_SPEC"
run torture_coverage_default "$PY" -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
run behave_plan_feature   "$PY" -B -m behave tests/features/torture_campaign_plan.feature -f plain
run behave_torture_tier   "$PY" -B -m behave tests/features --tags=@torture -f progress
run diff_check_parent     git diff --check "$PARENT" HEAD
run diff_check_srcbase    git diff --check "$SRCBASE" HEAD
run status_clean          git status --porcelain --untracked-files=all
