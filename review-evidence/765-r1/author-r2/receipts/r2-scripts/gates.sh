#!/bin/bash
# Static gates at the lane head; one log and rc each, summary in gates.tsv.
export PATH=<scratch>/venv/bin:<tools>/pinned-verilator-5.050:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
export TMPDIR=<scratch>/r2/tmp
O=<scratch>/r2/static; mkdir -p $O
cd <scratch>/r2/cloneS
echo "head $(git rev-parse HEAD) python $(python --version 2>&1)" > $O/HEAD.txt
: > $O/gates.tsv
run() { name=$1; shift; "$@" > $O/$name.log 2>&1; rc=$?; printf '%s\t%s\t%s\n' "$name" "$rc" "$*" >> $O/gates.tsv; }
run lint_rtl python scripts/lint_rtl.py --check
run measure_test_evidence python scripts/measure_test_evidence.py --check
run check_py_idiom python scripts/check_py_idiom.py
run check_cpp_idiom python scripts/check_cpp_idiom.py
run check_sv_idiom python scripts/check_sv_idiom.py
run check_sh_idiom python scripts/check_sh_idiom.py
run check_hygiene python scripts/check_hygiene.py --check
run check_port_contracts python scripts/check_port_contracts.py
run check_rtl_source_lists python scripts/check_rtl_source_lists.py
run check_todo_ownership python scripts/check_todo_ownership.py
run check_em_dash python scripts/check_em_dash.py --base e9cbb676d
run check_doc_style python scripts/check_doc_style.py
run check_doc_paths python scripts/check_doc_paths.py
run check_archive python scripts/check_archive.py
run check_feature_status python scripts/check_feature_status.py
run check_solution_docs python scripts/check_solution_docs.py
run check_submodule_docs python scripts/check_submodule_docs.py
run check_gptp_docs python scripts/check_gptp_docs.py
run check_diagram_pngs python scripts/check_diagram_pngs.py
run check_baremetal_only python scripts/check_baremetal_only.py --check
run check_soc_sources python scripts/check_soc_sources.py
run check_nvm_capture python scripts/check_nvm_capture.py
run check_nvm_record_space python scripts/check_nvm_record_space.py
run ci_events python scripts/ci_events.py --check
run ci_gate_workflows python scripts/ci_gate_workflows.py --check
run gen_module_matrix_check python docs/traceability/gen_module_matrix.py --check
run pp_resource_gate_selftest python syn/ooc/pp_resource_gate.py --selftest
run pp_resource_gate_check_baseline python syn/ooc/pp_resource_gate.py check-baseline
run git_diff_check git diff --check e9cbb676d HEAD
run check_em_dash_dev python scripts/check_em_dash.py --base 78ca9bdf1
run git_diff_check_dev git diff --check 78ca9bdf1 HEAD
run check_em_dash_r2 python scripts/check_em_dash.py --base 75db4b57c
run git_diff_check_r2 git diff --check 75db4b57c HEAD
run docs_check python scripts/docs_check.py
echo done > $O/DONE
