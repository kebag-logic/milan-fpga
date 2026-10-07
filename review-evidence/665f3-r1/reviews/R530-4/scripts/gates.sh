#!/bin/sh
# Focused gates for the round-5 delta, run concurrently; each writes <name>.log and <name>.rc under $1.
out=$1; shift
run() { name=$1; shift; ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) & }
run em_dash python3 scripts/check_em_dash.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c
run doc_style python3 scripts/check_doc_style.py
run docs_check python3 scripts/docs_check.py
run doc_map python3 docs/DOC_MAP.gen.py --check
run baremetal python3 scripts/check_baremetal_only.py --check
run baremetal_selftest python3 scripts/check_baremetal_only.py --selftest
run hygiene python3 scripts/check_hygiene.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run naming python3 scripts/measure_naming.py --check
run fail_fast python3 scripts/measure_fail_fast.py --check
run todo python3 scripts/check_todo_ownership.py
run py_idiom python3 scripts/check_py_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run toc_check python3 scripts/gen_toc.py --check
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
wait
run ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 8
run fw_coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8
run tally_selftest python3 sw/firmware/gtest/tally_selftest.py
run sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
wait
