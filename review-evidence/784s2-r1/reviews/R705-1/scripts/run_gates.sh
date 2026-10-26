#!/usr/bin/env bash
# Run the CI-tooling, runner, docs and Python gates the #784 step-2 delta reaches,
# concurrently (at most JOBS at once), under one interpreter environment.
# Usage: run_gates.sh <checkout> <venv-bin-dir> <out-dir> [jobs]
# Each gate writes <out-dir>/<name>.log and <out-dir>/<name>.rc. Offline only:
# DOCKER_HOST points at a socket that does not exist and no credential is passed.
set -u
repo=$1 bin=$2 out=$3 jobs=${4:-16}
mkdir -p "$out"
export PATH="$bin:/usr/bin:/bin" DOCKER_HOST="unix:///nonexistent/docker.sock" GITHUB_TOKEN="" GH_TOKEN=""
export PYTHONDONTWRITEBYTECODE=1
cd "$repo" || exit 2
base=a8594bb95631fa5c49d18fa0bbc9530e31ad59aa
gates=(
  "gen-check|python3 scripts/ci_gate_workflows.py --check"
  "gen-selftest|python3 scripts/ci_gate_workflows_selftest.py"
  "yosys-shards-selftest|python3 scripts/yosys_shards.py --selftest"
  "ci-events-check|python3 scripts/ci_events.py --check"
  "ci-events-selftest|python3 scripts/ci_events.py --selftest"
  "act-ci-selftest|python3 scripts/act_ci.py --selftest"
  "act-ci-contract|d=\$(mktemp -d) && install -m 0555 scripts/act_ci.py \$d/act_ci.py && python3 -I \$d/act_ci.py --selftest --worktree $repo; rc=\$?; rm -rf \$d; exit \$rc"
  "case-receipts|python3 scripts/ci_case_receipts_selftest.py"
  "make-cases|python3 scripts/ci_make_cases_selftest.py"
  "maap-cases|python3 scripts/ci_maap_cases_selftest.py"
  "capture-cases|python3 scripts/ci_capture_cases_selftest.py"
  "suite-pieces|python3 scripts/ci_suite_pieces_selftest.py"
  "suite-collect|python3 scripts/ci_suite_collect_selftest.py"
  "fail-fast|python3 scripts/ci_fail_fast_selftest.py"
  "runtime-evidence|python3 scripts/ci_runtime_evidence_selftest.py"
  "install-cache|python3 scripts/ci_install_cache_selftest.py"
  "evidence-pins|python3 scripts/generate_ci_evidence_pins.py --check"
  "workflow-plan|python3 scripts/ci_workflow_plan_selftest.py"
  "manifest|python3 scripts/ci_manifest_selftest.py"
  "ci-scope|python3 scripts/ci_scope.py --selftest"
  "docs-check|python3 scripts/docs_check.py"
  "em-dash|python3 scripts/check_em_dash.py --base $base && python3 scripts/check_em_dash.py --selftest"
  "doc-style|python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest"
  "gen-toc|python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
  "doc-paths|python3 scripts/check_doc_paths.py"
  "baremetal|python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest"
  "feature-status|python3 scripts/check_feature_status.py && python3 scripts/check_feature_status.py --self-test"
  "archive|python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest"
  "doc-map|python3 docs/DOC_MAP.gen.py --check"
  "gptp-docs|python3 scripts/check_gptp_docs.py"
  "py-idiom|python3 scripts/check_py_idiom.py && python3 scripts/check_py_idiom.py --selftest"
  "hygiene|python3 scripts/check_hygiene.py"
  "fail-fast-measure|python3 scripts/measure_fail_fast.py"
  "test-evidence|python3 scripts/measure_test_evidence.py"
  "todo-ownership|python3 scripts/check_todo_ownership.py"
)
run_one() {
  local name=${1%%|*} cmd=${1#*|}
  local t0=$SECONDS
  bash -c "$cmd" > "$out/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$out/$name.rc"
  printf '%-22s rc=%s %ss\n' "$name" "$rc" "$((SECONDS - t0))"
}
for g in "${gates[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge "$jobs" ]; do wait -n; done
  run_one "$g" &
done
wait
