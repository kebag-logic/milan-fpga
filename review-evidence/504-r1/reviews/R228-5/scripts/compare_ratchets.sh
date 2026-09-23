#!/usr/bin/env bash
# Ratchet gates whose budgets both lanes could consume, at the merge base, the
# predecessor side, the PR head and the candidate, in a disposable clone ($1).
set -u
cd "$1" || exit 2
for rev in 574c29fa111c74e5e5ed63e4670aff1f492e28e2 \
           18271bebbd1a4abf2e32e7783477573114e2a5fa \
           4876423d4cf8e89b820c56f8339f230abefb4827 \
           50c0d00ac3e7b7aa319ba4eab995d7e12b89149e; do
  git -c advice.detachedHead=false checkout -q "$rev" || exit 2
  echo "== $rev"
  for args in "scripts/check_py_idiom.py" "scripts/check_sh_idiom.py" \
              "scripts/measure_fail_fast.py --check" \
              "scripts/measure_test_evidence.py --check" \
              "scripts/measure_naming.py --check" "scripts/check_todo_ownership.py" \
              "scripts/check_hygiene.py --check"; do
    # shellcheck disable=SC2086
    out=$(python3 -B $args 2>&1)
    rc=$?
    summary=$(printf '%s\n' "$out" | grep -E 'RATCHET|PASS|FAIL|OK|<=' | tr '\n' ';' | cut -c1-400)
    printf '%s exit=%s | %s\n' "$args" "$rc" "$summary"
  done
done
git -c advice.detachedHead=false checkout -q 50c0d00ac3e7b7aa319ba4eab995d7e12b89149e
