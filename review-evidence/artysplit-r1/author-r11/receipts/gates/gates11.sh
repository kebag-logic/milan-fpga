#!/bin/bash
# Round 8 gates at the head: documentation and idiom gates, standalone self-tests, and fixture identity.
R=$VALIDATION_STORAGE/r11/gates; V=$VALIDATION_STORAGE/docs-venv/bin/python
cd $SOURCE
run(){ n=$1; shift; "$@" > $R/gate-$n.log 2>&1; echo "$n $?" | tee -a $R/gates11.rc; }
: > $R/gates11.rc
echo "HEAD $(git rev-parse HEAD)" | tee -a $R/gates11.rc
run docs-check python3 -B scripts/docs_check.py
run doc-style python3 -B scripts/check_doc_style.py
run doc-paths python3 -B scripts/check_doc_paths.py
run gptp-docs python3 -B scripts/check_gptp_docs.py
run inventory python3 -B scripts/docs_inventory.py --check
run idiom python3 -B scripts/check_py_idiom.py
run cpp-idiom python3 -B scripts/check_cpp_idiom.py
run em-dash $V -B scripts/check_em_dash.py --base 0b5940237e8de8bd5912db87e5e036a78f59b5a6
run toc-check $V -B scripts/gen_toc.py --check
run toc-verify-anchors $V -B scripts/gen_toc.py --verify-anchors
for t in rows_tiers load_grade egress_ledger record_classes arty_grade kept_grade census_extract egress_mii; do
  run standalone-$t python3 -I -B tb/verilator/ctrl_service_budget/$t.py --selftest
done
run arty-grade python3 -I -B tb/verilator/ctrl_service_budget/arty_grade.py
run baremetal python3 -B scripts/check_baremetal_only.py --check
run baremetal-selftest python3 -B scripts/check_baremetal_only.py --selftest
run test-evidence python3 -B scripts/measure_test_evidence.py --check
run register-reference python3 -B scripts/gen_register_reference.py --check
