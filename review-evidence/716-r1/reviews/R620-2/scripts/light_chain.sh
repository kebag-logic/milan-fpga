#!/usr/bin/env bash
# Serial light gates at the review head; each writes its own receipt.
R=$REVIEWS/716-r620-2-packet/scripts/run_logged.sh
$R ci_events_check python3 scripts/ci_events.py --check
$R ci_events_census python3 scripts/ci_events.py --firmware-census
$R shards_selftest python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
$R ci_scope_selftest python3 scripts/ci_scope.py --selftest
$R ci_rv32_sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
$R tally_selftest python3 sw/firmware/gtest/tally_selftest.py
$R docs_check python3 scripts/docs_check.py
$R doc_style python3 scripts/check_doc_style.py
$R doc_style_selftest python3 scripts/check_doc_style.py --selftest
$R gen_toc_check python3 scripts/gen_toc.py --check
$R gen_toc_selftest python3 scripts/gen_toc.py --selftest
$R py_idiom python3 scripts/check_py_idiom.py
$R py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
$R em_dash_selftest python3 scripts/check_em_dash.py --selftest
$R em_dash_base python3 scripts/check_em_dash.py --base 09c7231eca343607c97c0d66abebb2553688712c
$R diff_check git diff --check 09c7231eca343607c97c0d66abebb2553688712c HEAD
$R ci_events_selftest python3 scripts/ci_events.py --selftest
echo done > $REVIEWS/716-r620-2-packet/receipts/light_chain.done
