#!/usr/bin/env bash
# Differential: run the ratchet/contract gates that read files changed by the
# composition on the train-before tree (9912748d) and the PR source tree
# (d253f86e), to attribute the candidate's counts. Scratch trees carry no
# submodule checkouts; a gate that refuses for that reason is recorded as such.
# Usage: differential.sh <scratch-dir> <receipt-dir>
set -uo pipefail
scratch=${1:?scratch}
out=${2:?receipts}
mkdir -p "$out"
out=$(cd "$out" && pwd)
export PYTHONDONTWRITEBYTECODE=1
cmds=(
  "python3 scripts/ci_events.py --check"
  "python3 scripts/check_py_idiom.py"
  "python3 scripts/check_sh_idiom.py"
  "python3 scripts/check_hygiene.py --check"
  "python3 scripts/measure_fail_fast.py --check"
  "python3 scripts/measure_test_evidence.py --check"
  "python3 scripts/check_todo_ownership.py"
  "python3 scripts/gen_toc.py --check"
)
: > "$out/summary.tsv"
for tree in t-9912748d t-d253f86e; do
  n=0
  for c in "${cmds[@]}"; do
    n=$((n + 1))
    log="$out/$tree-$(printf '%02d' "$n").log"
    printf '$ (%s) %s\n' "$tree" "$c" > "$log"
    (cd "$scratch/$tree" && bash -c "$c") >> "$log" 2>&1 < /dev/null
    rc=$?
    printf '[exit %s]\n' "$rc" >> "$log"
    printf '%s\t%02d\t%s\t%s\t%s\n' "$tree" "$n" "$rc" "$c" "$(grep -v '^\[exit' "$log" | tail -1)" >> "$out/summary.tsv"
  done
done
cat "$out/summary.tsv"
