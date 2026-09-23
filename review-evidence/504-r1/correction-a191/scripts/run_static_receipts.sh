#!/usr/bin/env bash
# Focused static gates at the committed head, one at a time, each with its own log and exit.
# Usage: run_static_receipts.sh <checkout> <out-dir> <pr-base> <dev-base> <source-base>
set -uo pipefail
checkout=$1 out=$2 pr_base=$3 dev_base=$4 source_base=$5
mkdir -p "$out"
cd "$checkout" || exit 2
head=$(git rev-parse HEAD)
failed=0
run() {  # name command...
  local name=$1; shift
  local start; start=$(date +%s)
  "$@" > "$out/$name.log" 2>&1; local rc=$?
  echo "exit=$rc elapsed=$(( $(date +%s) - start ))s head=$head dirty=$(git status --porcelain | wc -l) argv=$*" > "$out/$name.exit"
  printf '%-34s exit=%s  %s\n' "$name" "$rc" "$(tail -1 "$out/$name.log" | cut -c1-150)"
  [ "$rc" -eq 0 ] || failed=1
}
run ci_rv32_sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
run test_firmware_compiler_selftest python3 sw/builder/test_firmware_compiler.py --selftest
run check_baremetal_only_check python3 scripts/check_baremetal_only.py --check
run check_baremetal_only_selftest python3 scripts/check_baremetal_only.py --selftest
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run docs_check python3 scripts/docs_check.py
run check_em_dash_pr_base python3 scripts/check_em_dash.py --base "$pr_base"
run check_em_dash_dev_base python3 scripts/check_em_dash.py --base "$dev_base"
run check_em_dash_source_base python3 scripts/check_em_dash.py --base "$source_base"
run check_em_dash_selftest python3 scripts/check_em_dash.py --selftest
run check_doc_paths python3 scripts/check_doc_paths.py
run gen_toc_check python3 scripts/gen_toc.py --check
run gen_toc_anchors python3 scripts/gen_toc.py --verify-anchors
run check_doc_style python3 scripts/check_doc_style.py
run check_py_idiom python3 scripts/check_py_idiom.py
run check_hygiene python3 scripts/check_hygiene.py --check
run measure_fail_fast python3 scripts/measure_fail_fast.py --check
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run measure_naming python3 scripts/measure_naming.py --check
run check_todo_ownership python3 scripts/check_todo_ownership.py
run py_compile python3 -m py_compile sw/builder/test_builder.py sw/builder/test_firmware_compiler.py
echo "static receipts: $([ $failed -eq 0 ] && echo ALL PASS || echo FAILURES) at $head"
exit $failed
