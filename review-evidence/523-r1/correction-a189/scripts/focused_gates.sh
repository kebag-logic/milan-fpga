#!/usr/bin/env bash
# Run the focused gates this diff touches, one receipt each, at most 8 at once.
# Usage: focused_gates.sh <checkout> <receipt-prefix> <em-dash-base>
set -u
repo="$1"; prefix="$2"; base="$3"
here="$(cd "$(dirname "$0")" && pwd)"
gates=(
 "lifecycle|python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py"
 "cancellation|python3 scripts/test_suite_cancellation.py"
 "py-idiom|python3 scripts/check_py_idiom.py"
 "py-idiom-selftest|python3 scripts/check_py_idiom.py --selftest"
 "sh-idiom|python3 scripts/check_sh_idiom.py"
 "sh-idiom-selftest|python3 scripts/check_sh_idiom.py --selftest"
 "evidence|python3 scripts/measure_test_evidence.py --check"
 "evidence-selftest|python3 scripts/measure_test_evidence.py --selftest"
 "fail-fast|python3 scripts/measure_fail_fast.py --check"
 "fail-fast-selftest|python3 scripts/measure_fail_fast.py --selftest"
 "baremetal|python3 scripts/check_baremetal_only.py --check"
 "baremetal-selftest|python3 scripts/check_baremetal_only.py --selftest"
 "docs|python3 scripts/docs_check.py"
 "doc-style|python3 scripts/check_doc_style.py"
 "em-dash|python3 scripts/check_em_dash.py --base $base"
 "em-dash-selftest|python3 scripts/check_em_dash.py --selftest"
 "doc-paths|python3 scripts/check_doc_paths.py"
 "contents|python3 scripts/gen_toc.py --check"
 "shell-syntax|bash -n scripts/run_all_suites.sh"
 "make-dry-run|make -n -C tb/verilator/gptp_shadow"
)
for g in "${gates[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 8 ]; do wait -n; done
  name="${g%%|*}"; cmd="${g#*|}"
  # shellcheck disable=SC2086
  python3 "$here/rcpt.py" "$prefix-$name" --cwd "$repo" -- bash -c "$cmd" &
done
wait
