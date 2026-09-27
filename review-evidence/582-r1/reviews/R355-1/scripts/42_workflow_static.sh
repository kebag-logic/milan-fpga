#!/bin/bash
# Workflow-invoked static checks, check/selftest modes, run on the clone.
# Usage: 42_workflow_static.sh <clone> <python>
set -u
C=${1:?clone}; PY=${2:?python}; cd "$C" || exit 2
for cmd in "scripts/ci_scope.py --selftest" "scripts/ci_events.py --check" "scripts/ci_events.py --selftest" \
  "scripts/measure_fail_fast.py --check" "scripts/measure_naming.py --check" "scripts/check_todo_ownership.py" \
  "docs/DOC_MAP.gen.py --check" "scripts/check_feature_status.py" "scripts/check_submodule_docs.py" \
  "scripts/check_gptp_docs.py --with-submodule" "scripts/check_wire_accountability.py --self-test" \
  "scripts/check_rtl_source_lists.py" "docs/traceability/gen_module_matrix.py --check" "scripts/check_archive.py" \
  "scripts/check_baremetal_only.py --selftest" "scripts/check_sh_idiom.py --selftest" "scripts/check_py_idiom.py --selftest" \
  "scripts/check_hygiene.py --selftest" "scripts/check_solution_docs.py --selftest" "scripts/check_doc_style.py --selftest" \
  "scripts/check_nvm_record_space.py" "scripts/check_port_contracts.py" "scripts/ci_litex_env.py"; do
  out=$(timeout 900 "$PY" $cmd 2>&1); echo "rc $?: $cmd :: $(tail -1 <<<"$out" | cut -c1-170)"; done
