#!/usr/bin/env bash
# The static gates #408/#409 acceptance 5 names, plus the em-dash and diff
# whitespace checks, run in a disposable copy of the reviewed head.
# Usage: run_static.sh <head-copy> <out-file>
set -u
cd "$1" || exit 2
out=$2
: > "$out"
step() {
  echo "\$ $*" >> "$out"
  "$@" >> "$out" 2>&1
  echo "exit=$?" >> "$out"
}
step git rev-parse HEAD
step git diff --check 759da623072358afdb0e9d570a7b4b6a788492c9 a13b6e2e461695cdb8d978444ae499a5a6745429
step python3 -B scripts/docs_check.py
step python3 -B scripts/check_baremetal_only.py --check
step python3 -B scripts/check_baremetal_only.py --selftest
step python3 -B scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
step python3 -B sw/builder/test_firmware_compiler.py --selftest
grep -E '^\$|^exit=' "$out"
