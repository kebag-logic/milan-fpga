#!/usr/bin/env bash
# Run the docs and code-quality gates the #649 change touches, in parallel, each with its own log and rc.
# Usage: run_gates.sh <repo> <markdown venv python> <out dir>
set -u
repo=$1 md=$2 out=$3
base=241f91845230ae410506dffb16b71937127fd175 dev=fea346e76c2a57ed5cd131af8fc68dfeff57f877
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
gates=(
"resource-gate-check-baseline|python3 syn/ooc/pp_resource_gate.py check-baseline"
"dp-srcs-selftest|python3 syn/ooc/dp_srcs.py --selftest"
"pp-baseline-reports-selftest|python3 syn/ooc/pp_baseline_reports_selftest.py"
"pp-srcs-check-selftest|python3 scripts/pp_srcs.py --check --selftest"
"rtl-source-lists|python3 scripts/check_rtl_source_lists.py"
"docs-check|$md scripts/docs_check.py"
"docs-check-no-git|env GIT_DIR=/dev/null $md scripts/docs_check.py"
"feature-status-no-git|env GIT_DIR=/dev/null $md scripts/check_feature_status.py"
"em-dash-base|$md scripts/check_em_dash.py --base $base"
"em-dash-dev|$md scripts/check_em_dash.py --base $dev"
"doc-style|$md scripts/check_doc_style.py"
"doc-paths|$md scripts/check_doc_paths.py"
"toc-check|$md scripts/gen_toc.py --check"
"toc-verify-anchors|$md scripts/gen_toc.py --verify-anchors"
"archive|$md scripts/check_archive.py"
"doc-map-check|$md docs/DOC_MAP.gen.py --check"
"module-matrix-check|$md docs/traceability/gen_module_matrix.py --check"
"solution-docs|$md scripts/check_solution_docs.py"
"baremetal-only|python3 scripts/check_baremetal_only.py --check"
"ci-events-check|python3 scripts/ci_events.py --check"
"py-idiom|python3 scripts/check_py_idiom.py"
"fail-fast|python3 scripts/measure_fail_fast.py --check"
"hygiene|python3 scripts/check_hygiene.py --check"
"todo-ownership|python3 scripts/check_todo_ownership.py"
"test-evidence|python3 scripts/measure_test_evidence.py --check"
"naming|python3 scripts/measure_naming.py --check"
"diff-check-base|git diff --check $base HEAD"
"diff-check-dev|git diff --check $dev HEAD"
)
cd "$repo" || exit 2
for g in "${gates[@]}"; do printf '%s\0' "$g"; done | xargs -0 -P 12 -I{} bash -c '
  name=${1%%|*}; cmd=${1#*|}; { echo "\$ $cmd"; eval "$cmd"; echo "# rc=$?"; } > "$2/$name.log" 2>&1
  tail -1 "$2/$name.log" | sed "s/# rc=//" > "$2/$name.rc"' _ {} "$out"
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort
