#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# R227-3 focused static and policy gates, run on an exact-head copy.
# Usage: run_focused_static.sh <exact-head-tree> <receipt-dir> <base-sha>
# Excludes: full banks, act/Docker, and the host act runner or its self-test.
set -u
tree=$1 out=$2 base=$3
mkdir -p "$out"
cd "$tree" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() {
  local name=$1; shift
  local start=$SECONDS
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%s exit=%s elapsed=%ss argv=%s\n' "$name" "$rc" "$((SECONDS-start))" "$*" \
    | tee -a "$out/SUMMARY.txt"
}
: > "$out/SUMMARY.txt"
run ci_rv32_sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
run firmware_compiler_selftest python3 sw/builder/test_firmware_compiler.py --selftest
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run baremetal_check python3 scripts/check_baremetal_only.py --check
run baremetal_selftest python3 scripts/check_baremetal_only.py --selftest
run em_dash_base python3 scripts/check_em_dash.py --base "$base"
run em_dash_selftest python3 scripts/check_em_dash.py --selftest
run docs_check python3 scripts/docs_check.py
run doc_style python3 scripts/check_doc_style.py
run doc_style_selftest python3 scripts/check_doc_style.py --selftest
run doc_paths python3 scripts/check_doc_paths.py
run toc_selftest python3 scripts/gen_toc.py --selftest
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
run py_idiom python3 scripts/check_py_idiom.py
run py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
run hygiene_check python3 scripts/check_hygiene.py --check
run hygiene_selftest python3 scripts/check_hygiene.py --selftest
run todo_ownership python3 scripts/check_todo_ownership.py
run fail_fast_check python3 scripts/measure_fail_fast.py --check
run naming_check python3 scripts/measure_naming.py --check
run test_evidence_check python3 scripts/measure_test_evidence.py --check
run feature_status_selftest python3 scripts/check_feature_status.py --self-test
run feature_status python3 scripts/check_feature_status.py
