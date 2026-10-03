#!/usr/bin/env bash
# R447-9: run the executor's round-7 gate list (42 of 43; gptp-docs-make is left out, see REPORT.md)
# at the reviewed head, concurrently, one log and rc per gate.
# Usage: run_gates.sh REPO OUTDIR MDPY DEVBASE JOBS
set -u
REPO=$1 OUT=$2 MDPY=$3 BASE=$4 JOBS=${5:-16}
mkdir -p "$OUT"
cat > "$OUT/gates.list" <<LIST
ooc-tcl-selftest|python3 -B syn/ooc/ooc_tcl_selftest.py
dp-srcs-selftest|python3 -B syn/ooc/dp_srcs.py --selftest
pp-baseline-selftest|python3 -B syn/ooc/pp_baseline.py --selftest
pp-baseline-mutants|python3 -B syn/ooc/pp_baseline_mutants.py
pp-baseline-reports-selftest|python3 -B syn/ooc/pp_baseline_reports_selftest.py
resource-gate-selftest|python3 -B syn/ooc/pp_resource_gate.py --selftest
resource-gate-mutants|python3 -B syn/ooc/pp_resource_gate_mutants.py
resource-gate-check-baseline|python3 -B syn/ooc/pp_resource_gate.py check-baseline
dp-srcs-milan-datapath|python3 -B syn/ooc/dp_srcs.py --top milan_datapath
dp-srcs-kl-pp-shadow|python3 -B syn/ooc/dp_srcs.py --top KL_pp_shadow
pp-srcs-check-selftest|python3 -B scripts/pp_srcs.py --check --selftest
docs-check|$MDPY -B scripts/docs_check.py
docs-check-no-git|env GIT_DIR=/dev/null $MDPY -B scripts/docs_check.py
feature-status-no-git|env GIT_DIR=/dev/null $MDPY -B scripts/check_feature_status.py
feature-status-selftest|$MDPY -B scripts/check_feature_status.py --self-test
em-dash|$MDPY -B scripts/check_em_dash.py --base $BASE
em-dash-selftest|$MDPY -B scripts/check_em_dash.py --selftest
doc-style|$MDPY -B scripts/check_doc_style.py
doc-style-selftest|$MDPY -B scripts/check_doc_style.py --selftest
doc-paths|$MDPY -B scripts/check_doc_paths.py
toc-selftest|$MDPY -B scripts/gen_toc.py --selftest
toc-verify-anchors|$MDPY -B scripts/gen_toc.py --verify-anchors
toc-check|$MDPY -B scripts/gen_toc.py --check
archive|$MDPY -B scripts/check_archive.py
archive-selftest|$MDPY -B scripts/check_archive.py --selftest
doc-map-check|$MDPY -B docs/DOC_MAP.gen.py --check
module-matrix-check|$MDPY -B docs/traceability/gen_module_matrix.py --check
solution-docs|$MDPY -B scripts/check_solution_docs.py
baremetal-only|python3 -B scripts/check_baremetal_only.py --check
ci-scope-selftest|python3 -B scripts/ci_scope.py --selftest
ci-events-check|python3 -B scripts/ci_events.py --check
ci-events-selftest|python3 -B scripts/ci_events.py --selftest
py-idiom|python3 -B scripts/check_py_idiom.py
py-idiom-selftest|python3 -B scripts/check_py_idiom.py --selftest
fail-fast|python3 -B scripts/measure_fail_fast.py --check
hygiene|python3 -B scripts/check_hygiene.py --check
todo-ownership|python3 -B scripts/check_todo_ownership.py
test-evidence|python3 -B scripts/measure_test_evidence.py --check
control-flow-selftest|python3 -B scripts/measure_control_flow.py --selftest
cohesion-selftest|python3 -B scripts/measure_cohesion.py --selftest
diff-check-base|git diff --check $BASE HEAD
diff-check-worktree|git diff --check
LIST
export REPO OUT
while IFS= read -r line; do printf '%s\0' "$line"; done < "$OUT/gates.list" |
  xargs -0 -P "$JOBS" -I{} bash -c '
    line="$1"; name=${line%%|*}; cmd=${line#*|}
    cd "$REPO" || exit 1
    t0=$(date +%s)
    { echo "\$ $cmd"; echo "# head $(git rev-parse HEAD)"; timeout 580 bash -c "$cmd" 2>&1; echo "# rc $?"; } > "$OUT/$name.log"
    grep -o "^# rc [0-9]*" "$OUT/$name.log" | tail -1 | cut -d" " -f3 > "$OUT/$name.rc"
    echo "$name rc=$(cat "$OUT/$name.rc") $(( $(date +%s) - t0 ))s"
  ' _ {}
