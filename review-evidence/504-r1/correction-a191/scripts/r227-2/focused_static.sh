#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Reviewer-owned focused static gates at the reviewed head (R227-2, #504 / PR #521).
# Usage: focused_static.sh <reviewed-clone> <receipt-dir>
set -uo pipefail
clone=$1 out=$2
cd "$clone" || exit 2
run() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  echo "exit=$?" >> "$out/$name.log"
  printf '%s %s\n' "$(tail -n 1 "$out/$name.log")" "$name"
}
run docs_check python3 scripts/docs_check.py
run em_dash_vs_483a133e python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f
run em_dash_vs_52711029 python3 scripts/check_em_dash.py --base 52711029f374650dc93830d5ea28e81cb5c8f410
run doc_style python3 scripts/check_doc_style.py
run doc_paths python3 scripts/check_doc_paths.py
run toc_check python3 scripts/gen_toc.py --check
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run py_idiom python3 scripts/check_py_idiom.py
run hygiene python3 scripts/check_hygiene.py --check
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run baremetal_check python3 scripts/check_baremetal_only.py --check
run baremetal_selftest python3 scripts/check_baremetal_only.py --selftest
run fail_fast python3 scripts/measure_fail_fast.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run naming python3 scripts/measure_naming.py --check
run sh_idiom python3 scripts/check_sh_idiom.py
