#!/bin/bash
# Run the docs-check job's documentation gates (no submodule initialised) in a clone.
# usage: docs_gates.sh <clone> <python> <base-sha>
cd "$1" || exit 2
PY=$2; BASE=$3; fails=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  out=$(eval "$PY -B $cmd" 2>&1); rc=$?
  printf 'rc=%s  %s\n' "$rc" "$cmd"
  [ "$rc" -ne 0 ] && { fails=$((fails+1)); printf '%s\n' "$out" | tail -15 | sed 's/^/    /'; }
done <<CMDS
scripts/docs_check.py
scripts/check_em_dash.py --base $BASE
scripts/check_doc_style.py
scripts/check_doc_style.py --selftest
scripts/check_gptp_docs.py
docs/DOC_MAP.gen.py --check
docs/diagrams/timesync_chain.gen.py --check
scripts/check_solution_docs.py
docs/diagrams/submodule_boundaries.gen.py --check
docs/diagrams/submodule_boundaries.gen.py --selftest
scripts/check_submodule_docs.py
scripts/check_submodule_docs.py --selftest
scripts/check_diagram_pngs.py
scripts/check_diagram_pngs.py --selftest
scripts/check_feature_status.py --self-test
docs/traceability/gen_module_matrix.py --check
scripts/ci_events.py --check
scripts/ci_events.py --selftest
scripts/ci_scope.py --selftest
CMDS
echo "docs gates: $fails failing"
[ "$fails" -eq 0 ]
