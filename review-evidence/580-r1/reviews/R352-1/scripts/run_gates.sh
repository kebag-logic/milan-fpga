#!/usr/bin/env bash
# Run the static gates sequentially from the clone root; print each command, its rc and output tail.
cd "${1:?clone}" || exit 2
BASE=682ecf0cb995473b72d5b4921088053ba753fc93
fail=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  out=$(eval "$cmd" 2>&1); rc=$?
  printf '$ %s\nrc=%s\n%s\n\n' "$cmd" "$rc" "$(printf '%s\n' "$out" | tail -4)"
  [ $rc -eq 0 ] || fail=1
done <<CMDS
python3 scripts/check_port_contracts.py
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_em_dash.py --base $BASE
python3 scripts/check_em_dash.py --selftest
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 scripts/check_gptp_docs.py --selftest
python3 docs/DOC_MAP.gen.py --check
python3 docs/diagrams/timesync_chain.gen.py --check
python3 scripts/check_solution_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 scripts/check_diagram_pngs.py
python3 scripts/check_diagram_pngs.py --selftest
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 scripts/check_archive.py
python3 scripts/check_baremetal_only.py --check
git diff --check $BASE HEAD
CMDS
echo "overall=$fail"
exit $fail
