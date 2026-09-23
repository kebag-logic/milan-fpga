#!/usr/bin/env bash
# Run read-only focused gates in a checkout; one receipt per gate.
# Usage: run_gates.sh <checkout> <receipt-dir>
set -u
repo="$1"; out="$2"; mkdir -p "$out"
gates=(
 "python-idiom|python3 scripts/check_py_idiom.py"
 "python-idiom-selftest|python3 scripts/check_py_idiom.py --selftest"
 "shell-idiom|python3 scripts/check_sh_idiom.py"
 "shell-idiom-selftest|python3 scripts/check_sh_idiom.py --selftest"
 "evidence|python3 scripts/measure_test_evidence.py --check"
 "evidence-selftest|python3 scripts/measure_test_evidence.py --selftest"
 "fail-fast|python3 scripts/measure_fail_fast.py --check"
 "baremetal|python3 scripts/check_baremetal_only.py --check"
 "baremetal-selftest|python3 scripts/check_baremetal_only.py --selftest"
 "docs|python3 scripts/docs_check.py"
 "doc-style|python3 scripts/check_doc_style.py"
 "em-dash|python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f"
 "doc-paths|python3 scripts/check_doc_paths.py"
 "contents|python3 scripts/gen_toc.py --check"
 "shell-syntax|bash -n scripts/run_all_suites.sh"
)
run() {
  local name="${1%%|*}" cmd="${1#*|}"
  ( cd "$repo" && /usr/bin/time -f 'wall=%e' bash -c "$cmd" ) > "$out/$name.log" 2>&1
  echo "$name exit $?" > "$out/$name.status"
}
for g in "${gates[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge 8 ]; do wait -n; done
  run "$g" &
done
wait
cat "$out"/*.status
