#!/bin/bash
# Run the docs-gates-0 checks that read the changed files, each with its own rc.
# GATE_PATH_PREFIX: the pinned Markdown renderer's venv bin and a Verilator
# 5.050 directory. check_baremetal_only.py needs a python3 with pyyaml.
# usage: docs_gates.sh <tree> <logdir>
T=$1; L=$2; cd "$T" || exit 2
export PATH=${GATE_PATH_PREFIX:+$GATE_PATH_PREFIX:}$PATH
run(){ n=$1; shift; echo "### $n: $*" >> "$L/docs_gates.log"; ( eval "$*" ) >> "$L/docs_gates.log" 2>&1; rc=$?; echo "$n rc=$rc" | tee -a "$L/docs_gates.summary"; }
: > "$L/docs_gates.summary"; : > "$L/docs_gates.log"
run docs_check "python3 scripts/docs_check.py"
run doc_style "python3 scripts/check_doc_style.py"
run toc_anchors "python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
run doc_paths "python3 scripts/check_doc_paths.py"
run feature_status "python3 scripts/check_feature_status.py"
run solution_docs "python3 scripts/check_solution_docs.py"
run traceability "python3 docs/traceability/gen_module_matrix.py --check"
run rtl_source_lists "python3 scripts/check_rtl_source_lists.py"
run naming "python3 scripts/measure_naming.py --check"
run port_contracts "python3 scripts/check_port_contracts.py"
run fail_fast "python3 scripts/measure_fail_fast.py --check"
run todo_owner "python3 scripts/check_todo_ownership.py"
run test_evidence "python3 scripts/measure_test_evidence.py --check"
run hygiene "python3 scripts/check_hygiene.py --check"
run sv_idiom "python3 scripts/check_sv_idiom.py"
run cpp_idiom "python3 scripts/check_cpp_idiom.py"
run py_idiom "python3 scripts/check_py_idiom.py"
run sh_idiom "python3 scripts/check_sh_idiom.py"
run archive "python3 scripts/check_archive.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run lint_rtl "python3 scripts/lint_rtl.py --check"
run emdash "git diff -U0 a032c6d6e3775f145349d5a495c1e1ad12294936..HEAD | grep '^+' | grep -v '^+++' | grep -c $'—' | grep -qx 0"
