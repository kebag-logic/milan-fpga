#!/usr/bin/env bash
# Run the focused gate set for the R447-8 review concurrently, one log and rc per gate.
# Usage: run_gates.sh REPO OUTDIR MDPY JOBS
set -u
REPO=$1 OUT=$2 MDPY=$3 JOBS=${4:-16}
mkdir -p "$OUT"
cat > "$OUT/gates.list" <<LIST
resource-gate-selftest|python3 syn/ooc/pp_resource_gate.py --selftest
resource-gate-mutants|python3 syn/ooc/pp_resource_gate_mutants.py
resource-gate-check-baseline|python3 syn/ooc/pp_resource_gate.py check-baseline
pp-baseline-selftest|python3 syn/ooc/pp_baseline.py --selftest
pp-baseline-mutants|python3 syn/ooc/pp_baseline_mutants.py
ci-scope-selftest|python3 scripts/ci_scope.py --selftest
ci-events-check|python3 scripts/ci_events.py --check
docs-check|$MDPY scripts/docs_check.py
docs-check-no-git|env GIT_DIR=/dev/null $MDPY scripts/docs_check.py
toc-check|$MDPY scripts/gen_toc.py --check
toc-verify-anchors|$MDPY scripts/gen_toc.py --verify-anchors
doc-paths|$MDPY scripts/check_doc_paths.py
em-dash|$MDPY scripts/check_em_dash.py --base 5fabb46e767c9308ab2580916237f43577698c6e
doc-style|$MDPY scripts/check_doc_style.py
doc-map-check|$MDPY docs/DOC_MAP.gen.py --check
archive|$MDPY scripts/check_archive.py
module-matrix-check|$MDPY docs/traceability/gen_module_matrix.py --check
solution-docs|$MDPY scripts/check_solution_docs.py
feature-status-no-git|env GIT_DIR=/dev/null $MDPY scripts/check_feature_status.py
diff-check-base|git diff --check 5fabb46e767c9308ab2580916237f43577698c6e HEAD
LIST
export REPO OUT MDPY
while IFS= read -r line; do printf '%s\0' "$line"; done < "$OUT/gates.list" |
  xargs -0 -P "$JOBS" -I{} bash -c '
    line="$1"; name=${line%%|*}; cmd=${line#*|}
    cd "$REPO" || exit 1
    t0=$(date +%s)
    { echo "\$ $cmd"; echo "# head $(git rev-parse HEAD)"; bash -c "$cmd" 2>&1; echo "# rc $?"; } > "$OUT/$name.log"
    grep -o "^# rc [0-9]*" "$OUT/$name.log" | tail -1 | cut -d" " -f3 > "$OUT/$name.rc"
    echo "$name rc=$(cat "$OUT/$name.rc") $(( $(date +%s) - t0 ))s"
  ' _ {}
