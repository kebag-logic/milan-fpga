#!/bin/bash
# R532-6: the docs-workflow commands relevant to this delta, each with its own rc.
# usage: docs_gates.sh REPO BASE ; prints "rc command" lines; logs to $DOCS_LOG_DIR
R=$1; BASE=$2; L=${DOCS_LOG_DIR:?}; mkdir -p $L; cd $R
export PYTHONDONTWRITEBYTECODE=1
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue; i=$((i+1))
  bash -c "$cmd" > $L/$i.log 2>&1; echo "$? $cmd" | tee -a $L/summary.txt
done <<LIST
python3 scripts/check_em_dash.py --base $BASE
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 docs/DOC_MAP.gen.py --check
python3 scripts/check_solution_docs.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/check_submodule_docs.py --selftest
python3 scripts/check_diagram_pngs.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/measure_naming.py --check
python3 scripts/measure_fail_fast.py --check
python3 scripts/check_todo_ownership.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_hygiene.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_sh_idiom.py
python3 scripts/ci_events.py --check
python3 scripts/check_archive.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
python3 sw/mailbox/gen_mailbox.py --check
python3 scripts/check_wire_accountability.py
python3 scripts/ci_scope.py --selftest
LIST
