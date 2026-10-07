#!/bin/bash
# [R530] R530-3: the docs-workflow and idiom commands that need no submodule, pip install or builder bank.
# usage: docs_gates.sh [CLONE]  (default: the current directory). The four Markdown-renderer
# commands (check_em_dash, gen_toc) need the pinned tools/markdown/requirements.txt set.
cd "${1:-$PWD}" || exit 2
fail=0
while IFS= read -r c; do
  [ -z "$c" ] && continue
  out=$(bash -c "$c" 2>&1); rc=$?
  printf '=== rc=%s :: %s\n%s\n' "$rc" "$c" "$(printf '%s\n' "$out" | tail -4)"
  [ $rc -ne 0 ] && fail=$((fail+1))
done <<'LIST'
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c
python3 scripts/check_em_dash.py --base 021b9c1fb966e9a1a4acef6b5233edd3518f32a0
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 docs/DOC_MAP.gen.py --check
python3 scripts/check_solution_docs.py
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/measure_control_flow.py --selftest
python3 scripts/measure_cohesion.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_nvm_record_space.py
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/measure_naming.py --check
python3 scripts/check_port_contracts.py
python3 scripts/measure_fail_fast.py --check
python3 scripts/check_todo_ownership.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_hygiene.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_sh_idiom.py
python3 scripts/ci_events.py --check
python3 scripts/check_archive.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 scripts/lint_rtl.py --check
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 scripts/ci_rv32_sdk_selftest.py
LIST
echo "docs gates: $fail failing"
exit $fail
