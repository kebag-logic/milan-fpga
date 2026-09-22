#!/usr/bin/env bash
# [R238] focused documentation-side gates, run in a scratch clone at one
# revision. Usage: run_gates.sh <clone> <label>
# Each command's exit code and full output are kept under receipts/gates-<label>/.
set -u
clone=$(realpath "$1")
label=$2
out=$(realpath "$(dirname "$0")/..")/receipts/gates-$label
mkdir -p "$out"
: > "$out/summary.txt"
run() {
  local name=$1
  shift
  (cd "$clone" && "$@") > "$out/$name.log" 2>&1
  local rc=$?
  printf '%-28s exit %d  | %s\n' "$name" "$rc" "$(tail -n 1 "$out/$name.log")" >> "$out/summary.txt"
}
run toc-selftest       python3 -B scripts/gen_toc.py --selftest
run toc-check          python3 -B scripts/gen_toc.py --check
run toc-anchors        python3 -B scripts/gen_toc.py --verify-anchors
run toc-sites          python3 -B scripts/gen_toc.py --sites
run emdash-selftest    python3 -B scripts/check_em_dash.py --selftest
run emdash-base        python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
run docs-check         python3 -B scripts/docs_check.py
run docs-selftest      python3 -B scripts/docs_check.py --selftest
run doc-style          python3 -B scripts/check_doc_style.py
run doc-style-selftest python3 -B scripts/check_doc_style.py --selftest
run doc-paths          python3 -B scripts/check_doc_paths.py
run py-idiom           python3 -B scripts/check_py_idiom.py
run py-idiom-selftest  python3 -B scripts/check_py_idiom.py --selftest
run hygiene            python3 -B scripts/check_hygiene.py --check
run hygiene-selftest   python3 -B scripts/check_hygiene.py --selftest
run ci-events          python3 -B scripts/ci_events.py --check
run ci-events-selftest python3 -B scripts/ci_events.py --selftest
cat "$out/summary.txt"
