#!/bin/sh
# Run the documentation-workflow gates relevant to this PR from the repository
# root, recording each command's exit status. Renderer wheels come from a local
# venv's site-packages via PYTHONPATH; every other import is the system's.
cd "$1" || exit 2
# RENDERER_SITE: site-packages holding the pinned cmarkgfm/html5lib wheels
export PYTHONPATH=${RENDERER_SITE:?set RENDERER_SITE}
fail=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  sh -c "$cmd" > /dev/null 2> "$2.err" ; rc=$?
  [ $rc -ne 0 ] && { fail=1; echo "--- stderr tail:"; tail -5 "$2.err"; }
  printf '%s\t%s\n' "$rc" "$cmd"
done <<'LIST'
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base c6bd08c6
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py
python3 docs/DOC_MAP.gen.py --check
python3 scripts/check_solution_docs.py
python3 scripts/check_submodule_docs.py
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_nvm_capture.py
python3 scripts/check_soc_sources.py
python3 scripts/check_rtl_source_lists.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_naming.py --selftest
python3 scripts/check_port_contracts.py
python3 scripts/measure_fail_fast.py --check
python3 scripts/check_todo_ownership.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
python3 scripts/check_hygiene.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_cpp_idiom.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_sh_idiom.py
python3 scripts/check_doc_paths.py
python3 scripts/check_archive.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/lint_rtl.py --check --jobs 4
git diff --check c6bd08c6 HEAD
LIST
exit $fail
