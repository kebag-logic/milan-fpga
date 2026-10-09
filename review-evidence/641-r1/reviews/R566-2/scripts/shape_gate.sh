#!/usr/bin/env bash
# The real shape gate (not its self-test) with the given make first on PATH,
# showing the two nested-derivation consumers' rows. Arg 1: make bin dir.
set -u
export PATH="$1:$PATH" PYTHONDONTWRITEBYTECODE=1
make --version | head -1
python3 scripts/check_entity_shape.py > shape_gate.out 2>&1
rc=$?
grep -n -E 'pp_shadow|milan_dp_render|RESULT|checks:' shape_gate.out | head -40
rm -f shape_gate.out
exit $rc
