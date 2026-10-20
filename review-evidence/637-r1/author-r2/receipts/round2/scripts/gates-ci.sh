#!/usr/bin/env bash
# docs.yml docs-gates-0 step 54, "CI scheduling and evidence controls": one log and one rc per command, no pipes.
# usage: gates-ci.sh <tree> <logdir>
set -u
tree=$1; out=$2
S=<scratch>
export TMPDIR=$S/r2/tmp
export PATH=$S/venv312/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:$S/sdk/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out"
cd "$tree" || exit 2
tsv=$out/rc.tsv
g() {
  local name=$1; shift
  local t0; t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%ss\t%s\n' "$name" "$rc" "$(( $(date +%s) - t0 ))" "$*" >> "$tsv"
  echo "$name rc=$rc"
}
g d0-54-ci_gate_workflows-check python3 scripts/ci_gate_workflows.py --check
for s in ci_gate_workflows_selftest ci_case_receipts_selftest ci_make_cases_selftest ci_maap_cases_selftest \
         ci_capture_cases_selftest ci_suite_pieces_selftest ci_suite_collect_selftest ci_fail_fast_selftest \
         ci_runtime_evidence_selftest ci_install_cache_selftest ci_workflow_plan_selftest ci_manifest_selftest; do
  g "d0-54-$s" python3 "scripts/$s.py"
done
g d0-54-generate_ci_evidence_pins-check python3 scripts/generate_ci_evidence_pins.py --check
