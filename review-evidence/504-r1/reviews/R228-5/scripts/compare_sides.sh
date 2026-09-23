#!/usr/bin/env bash
# Run the two overlap-reading gates at the merge base, the predecessor side,
# the reviewed PR head and the candidate, in a disposable clone ($1), and
# print each summary line. Additivity (candidate = predecessor + PR - base)
# shows both sides' controls execute in the composed tree.
set -u
clone="$1"
cd "$clone" || exit 2
for rev in 574c29fa111c74e5e5ed63e4670aff1f492e28e2 \
           18271bebbd1a4abf2e32e7783477573114e2a5fa \
           4876423d4cf8e89b820c56f8339f230abefb4827 \
           50c0d00ac3e7b7aa319ba4eab995d7e12b89149e; do
  git -c advice.detachedHead=false checkout -q "$rev" || exit 2
  echo "== $rev"
  for args in "scripts/check_baremetal_only.py --check" \
              "scripts/check_baremetal_only.py --selftest" \
              "scripts/ci_events.py --check" \
              "scripts/ci_events.py --selftest"; do
    # shellcheck disable=SC2086
    out=$(python3 -B $args 2>&1)
    rc=$?
    printf '%s exit=%s | %s\n' "$args" "$rc" "$(printf '%s\n' "$out" | tail -1)"
  done
done
git -c advice.detachedHead=false checkout -q 50c0d00ac3e7b7aa319ba4eab995d7e12b89149e
