#!/usr/bin/env bash
# Run the F1 gates in one tree: the rtl-fast step command and the declaration
# suite. Bytecode writes are suppressed so a tree stays byte-clean.
# Usage: gates.sh <tree>
set -uo pipefail
t=$1
cd "$t"
echo "== tree $(git rev-parse HEAD 2>/dev/null) dirty=$(git status --porcelain | wc -l)"
echo "== python3 -B scripts/pp_srcs.py --check --selftest"
python3 -B scripts/pp_srcs.py --check --selftest 2>&1 | tail -8; echo "rc=${PIPESTATUS[0]}"
echo "== (cd sw/builder && python3 -B test_declarations.py)"
( cd sw/builder && python3 -B test_declarations.py 2>&1 | tail -25; echo "rc=${PIPESTATUS[0]}" )
