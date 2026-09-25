#!/bin/sh
# [R325] R325-3 planted grader defects in run.py; check_nvm_capture.py must fail
# in its embedded controls (before the harness-hash check could).
# Usage: r325_grader_mutations.sh <clean clone at b02af048> <scratch dir>
set -u
CLONE=$1; SCRATCH=$2; M=$SCRATCH/gradermut
rm -rf "$M"; cp -a "$CLONE" "$M"; cd "$M"
test "$(git rev-parse HEAD)" = b02af0480d3a3061df24683d522799d1759f7c33
export PYTHONDONTWRITEBYTECODE=1
R=tb/verilator/nvm_capture_cpu/run.py
clean() { git checkout -q -- .; find . -name __pycache__ -type d -prune -exec rm -rf {} + ; }
arm() {
  clean
  python3 - "$2" "$3" <<'PY'
import sys, pathlib
p = pathlib.Path('tb/verilator/nvm_capture_cpu/run.py'); t = p.read_text()
assert t.count(sys.argv[1]) == 1, sys.argv[1]
p.write_text(t.replace(sys.argv[1], sys.argv[2]))
PY
  out=$(python3 -B scripts/check_nvm_capture.py 2>&1); rc=$?
  echo "ARM $1 rc=$rc :: $(echo "$out" | grep -E '^(FAIL|PASS)|Error' | tail -1 | cut -c1-200)"
}
arm off-time-limit-skipped \
  "        if row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']:" \
  "        if spec['traffic'] == 'on' and row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']:"
arm maximum-on-only \
  "               for arm in arms for row in arm['rows'])" \
  "               for arm in arms if arm['traffic'] == 'on' for row in arm['rows'])"
arm limit-off-by-one-tick \
  "        if row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']:" \
  "        if row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz'] + 2000:"
arm limit-at-25ms \
  "        if row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']:" \
  "        if row['sys_cycles'] * 2000 > 50 * spec['sys_hz']:"
arm off-counters-unchecked \
  "                or spec['traffic'] == 'off' and any(counts)):" \
  "                or False):"
arm on-counters-unchecked \
  "        if (spec['traffic'] == 'on' and not all(value > 0 for value in counts)" \
  "        if (False"
clean; test -z "$(git status --porcelain --untracked-files=no)" && echo "probe copy restored clean"
