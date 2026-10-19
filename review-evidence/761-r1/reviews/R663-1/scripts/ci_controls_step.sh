#!/usr/bin/env bash
# Run every command of docs.yml's "CI scheduling and evidence controls" step
# (gate_50) in one tree, continuing past a failure so that no command hides
# behind an earlier one. Usage: ci_controls_step.sh <tree> <out_dir> <tag>
set -u
TREE=$1; OUT=$2; TAG=$3
mkdir -p "$OUT"
cd "$TREE" || exit 2
: > "$OUT/ci_controls.$TAG.tsv"
while read -r cmd; do
  [ -z "$cmd" ] && continue
  name=$(echo "$cmd" | awk '{print $2}' | sed 's#scripts/##; s#\.py##')
  log="$OUT/ci_controls.$TAG.$name.log"
  timeout 1200 python3 -E -s ${cmd#python3 } > "$log" 2>&1
  printf '%s\t%s\t%s\n' "$name" "$?" "$cmd" >> "$OUT/ci_controls.$TAG.tsv"
done <<'EOF'
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_gate_workflows_selftest.py
python3 scripts/ci_case_receipts_selftest.py
python3 scripts/ci_make_cases_selftest.py
python3 scripts/ci_maap_cases_selftest.py
python3 scripts/ci_capture_cases_selftest.py
python3 scripts/ci_suite_pieces_selftest.py
python3 scripts/ci_suite_collect_selftest.py
python3 scripts/ci_fail_fast_selftest.py
python3 scripts/ci_runtime_evidence_selftest.py
python3 scripts/ci_install_cache_selftest.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/ci_workflow_plan_selftest.py
python3 scripts/ci_manifest_selftest.py
EOF
cat "$OUT/ci_controls.$TAG.tsv"
