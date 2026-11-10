#!/bin/bash
# Usage: gates.sh <clone> <receipt-dir>: runs the delta's lane gates concurrently, one log and rc each.
C=$1; R=$2
cd "$C" || exit 2
run() { n=$1; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run mbx-check    python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck
run mbx-selftest python3 -B sw/mailbox/gen_mailbox.py --selftest
run ctrl-memory  python3 -B sw/litex/test_ctrl_memory.py
run builder3     python3 -B sw/builder/test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged
run py-idiom     bash -c 'python3 scripts/check_py_idiom.py && python3 scripts/check_py_idiom.py --selftest'
run harness-self python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
run docs         bash -c 'python3 scripts/docs_check.py && python3 scripts/check_doc_paths.py && python3 scripts/gen_toc.py --check && python3 scripts/check_em_dash.py --base 1d6bf555'
run soc-options  python3 -B sw/builder/test_soc_options.py
run diff-check   git diff --check 1d6bf555 HEAD
wait
