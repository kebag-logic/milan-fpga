#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# R228-3: focused static/docs gates relevant to the PR's changed files, run in
# a disposable clean copy of the review clone. Usage: r228_static_gates.sh <tree> <outdir>
set -u
tree=$1
out=$2
mkdir -p "$out"
cd "$tree" || exit 2
run() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$out/$name.exit"
  printf '%-34s rc=%s  %s\n' "$name" "$rc" "$(tail -n 1 "$out/$name.log" | cut -c1-150)"
}
run ci_events_check            python3 scripts/ci_events.py --check
run ci_events_selftest         python3 scripts/ci_events.py --selftest
run baremetal_check            python3 scripts/check_baremetal_only.py --check
run baremetal_selftest         python3 scripts/check_baremetal_only.py --selftest
run docs_check                 python3 scripts/docs_check.py
run em_dash_base               python3 scripts/check_em_dash.py --base 574c29fa111c74e5e5ed63e4670aff1f492e28e2
run em_dash_selftest           python3 scripts/check_em_dash.py --selftest
run doc_style                  python3 scripts/check_doc_style.py
run doc_paths                  python3 scripts/check_doc_paths.py
run gen_toc_check              python3 scripts/gen_toc.py --check
run gen_toc_anchors            python3 scripts/gen_toc.py --verify-anchors
run feature_status             python3 scripts/check_feature_status.py
run py_idiom                   python3 scripts/check_py_idiom.py
run hygiene                    python3 scripts/check_hygiene.py --check
run fail_fast                  python3 scripts/measure_fail_fast.py --check
run todo_ownership             python3 scripts/check_todo_ownership.py
run sdk_installer_selftest     python3 scripts/ci_rv32_sdk_selftest.py
run compiler_audit_selftest    python3 sw/builder/test_firmware_compiler.py --selftest
run py_compile                 python3 -m py_compile scripts/ci_rv32_sdk.py scripts/ci_rv32_sdk_selftest.py sw/builder/test_firmware_compiler.py sw/builder/test_builder.py scripts/ci_events.py scripts/check_baremetal_only.py
run git_status_after           git status --porcelain --ignored=no
