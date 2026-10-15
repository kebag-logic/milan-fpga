#!/usr/bin/env bash
# Run the PR's touched, non-runner gates concurrently at the checked-out head.
# Usage: run_gates.sh <clone> <receipt-dir>
set -u
clone="$1"; out="$2"
mkdir -p "$out"
cd "$clone" || exit 2
base=84f9e3001b7d9b77835c4a9a599dbe6230a8031b
declare -A gates=(
  [g01-gate-workflows-check]="python3 scripts/ci_gate_workflows.py --check"
  [g02-gate-workflows-selftest]="python3 scripts/ci_gate_workflows_selftest.py"
  [g03-ci-events-check]="python3 scripts/ci_events.py --check"
  [g04-ci-events-selftest]="python3 scripts/ci_events.py --selftest"
  [g05-em-dash]="python3 scripts/check_em_dash.py --base $base"
  [g06-docs-check]="python3 scripts/docs_check.py"
  [g07-toc-check]="python3 scripts/gen_toc.py --check"
  [g08-toc-anchors]="python3 scripts/gen_toc.py --verify-anchors"
  [g09-doc-style]="python3 scripts/check_doc_style.py"
  [g10-doc-paths]="python3 scripts/check_doc_paths.py"
  [g11-py-idiom]="python3 scripts/check_py_idiom.py"
  [g12-sh-idiom]="python3 scripts/check_sh_idiom.py"
  [g13-hygiene]="python3 scripts/check_hygiene.py --check"
  [g14-runtime-evidence-selftest]="python3 scripts/ci_runtime_evidence_selftest.py"
  [g15-manifest-selftest]="python3 scripts/ci_manifest_selftest.py"
)
for name in "${!gates[@]}"; do
  ( start=$(date +%s.%N)
    bash -c "${gates[$name]}" > "$out/$name.log" 2>&1
    rc=$?
    end=$(date +%s.%N)
    printf '%s\t%s\t%.1fs\t%s\n' "$name" "$rc" "$(echo "$end - $start" | bc)" "${gates[$name]}" > "$out/$name.rc"
  ) &
done
wait
cat "$out"/*.rc | sort
