#!/usr/bin/env bash
# The service-budget charge control on a clean clone at <head>: service_controls() as
# committed, then with the PHY init's charge planted back to fifteen transactions (the
# count before the register 15 read), in memory, which must fail by name.
# Usage: service_charge_mutant.sh <head> <clone> <log>
set -u
head=$1; w=$2; log=$3
cd "$w/tb/verilator/fw_service_budget" || exit 2
test "$(git rev-parse HEAD)" = "$head" || exit 3
{
echo "# head $head gate: fw_service_budget service_controls() and the charge-fifteen mutant"
python3 -B - <<'PY'
import sys, types
from pathlib import Path
src = Path('run.py').read_text()
old = "charge_cycles = int(timing[4]) + 16 * int(timing[3])"
assert src.count(old) == 1, 'charge anchor'
def load(text):
    mod = types.ModuleType('run'); mod.__file__ = str(Path('run.py').resolve())
    sys.modules['run'] = mod
    exec(compile(text, mod.__file__, 'exec'), mod.__dict__)
    return mod
print('AS COMMITTED service_controls():', load(src).service_controls())
try:
    load(src.replace(old, "charge_cycles = int(timing[4]) + 15 * int(timing[3])")).service_controls()
except RuntimeError as error:
    print('MUTANT charge-fifteen caught:', error)
else:
    raise SystemExit('MUTANT charge-fifteen escaped')
PY
} > "$log" 2>&1
rc=$?; echo "$rc" > "$log.rc"
git -C "$w" status --porcelain > "$log.tree-after"
