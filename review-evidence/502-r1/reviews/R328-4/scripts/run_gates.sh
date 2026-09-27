#!/bin/sh
# R328-4 composition gates. Usage: run_gates.sh <candidate-clone> <receipt-dir> <bin-dir> <python>
# Runs each gate in the foreground from the candidate root, records command, rc and full output.
# The docs/pin/record gates below are the ones that read files the composition touches.
set -u
C=$1; OUT=$2; BIN=$3; PY=$4
mkdir -p "$OUT"
PATH="$BIN:$PATH"; export PATH
cd "$C" || exit 2
SUMMARY="$OUT/summary.tsv"
: > "$SUMMARY"
run() {
  name=$1; shift
  log="$OUT/$name.log"
  printf '$ %s\n' "$*" > "$log"
  "$@" >> "$log" 2>&1
  rc=$?
  printf '%s\t%s\t%s\n' "$name" "$rc" "$*" >> "$SUMMARY"
  printf '%s rc=%s\n' "$name" "$rc"
}
run docs_check           "$PY" -B scripts/docs_check.py
run docs_check_nogit     env GIT_DIR=/dev/null "$PY" -B scripts/docs_check.py
run gen_toc_check        "$PY" scripts/gen_toc.py --check
run gen_toc_anchors      "$PY" scripts/gen_toc.py --verify-anchors
run em_dash_vs_train     "$PY" scripts/check_em_dash.py --base dab01daf2c574727bd9b1a5ecc63a05538695b12
run em_dash_vs_prbase    "$PY" scripts/check_em_dash.py --base 831f94f4146cc45ec476f8c8dcf5afac7cd8eacf
run doc_style            "$PY" scripts/check_doc_style.py
run doc_paths            "$PY" scripts/check_doc_paths.py
run submodule_docs       "$PY" scripts/check_submodule_docs.py
run ci_events_check      "$PY" scripts/ci_events.py --check
run ci_events_selftest   "$PY" scripts/ci_events.py --selftest
run nvm_capture          "$PY" scripts/check_nvm_capture.py
run measure_test_evidence "$PY" scripts/measure_test_evidence.py --check
run rtl_source_lists     "$PY" scripts/check_rtl_source_lists.py
run port_contracts       "$PY" scripts/check_port_contracts.py
run lint_rtl             "$PY" scripts/lint_rtl.py --check
run pp_srcs_check        "$PY" scripts/pp_srcs.py --check
run dp_srcs_pp_shadow    "$PY" syn/ooc/dp_srcs.py --top KL_pp_shadow
run dp_srcs_datapath     "$PY" syn/ooc/dp_srcs.py --top milan_datapath
run pp_baseline_selftest "$PY" syn/ooc/pp_baseline.py --selftest
run pp_baseline_mutants  "$PY" syn/ooc/pp_baseline_mutants.py
run pp_baseline_reports  "$PY" syn/ooc/pp_baseline_reports_selftest.py
run diff_check_train     git diff --check dab01daf2c574727bd9b1a5ecc63a05538695b12 f80525e695ce7937ba1a2c1caa01ec9cdde93904
