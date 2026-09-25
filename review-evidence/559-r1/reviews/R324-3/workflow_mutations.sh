#!/usr/bin/env bash
# R324-3: independent mutations of the new docs-check step, graded by
# scripts/ci_events.py --check in a scratch COPY of the exact-head clone.
# Usage: CLONE=<exact-head clone> bash workflow_mutations.sh
set -uo pipefail
PKT=$(cd "$(dirname "$0")" && pwd)
: "${CLONE:?set CLONE to the exact-head review clone}"
R=$PKT/scratch/repo_wf; rm -rf "$R"; cp -a "$CLONE" "$R"; cd "$R"
W=.github/workflows/docs.yml
STEP='      - name: Capture measurement census and clock gate
        # Regenerates tables and checks the receipt without compilation or simulation.
        run: python3 scripts/check_nvm_capture.py
'
arm() {  # name, expected rc (0 pass / 1 refuse), python edit
  python3 - "$W" "$STEP" <<PY
import sys
p, step = sys.argv[1], sys.argv[2]
s = open(p).read(); assert s.count(step) == 1
$3
open(p, 'w').write(s)
PY
  out=$(python3 scripts/ci_events.py --check 2>&1); rc=$?
  [ "$rc" -ne 0 ] && rc=1
  echo "ARM $1 rc=$rc want=$2 $([ "$rc" = "$2" ] && echo EXPECTED || echo UNEXPECTED) :: $(printf '%s\n' "$out" | grep -m1 -iE 'must|FAIL|OK' | sed 's/^ *//' | cut -c1-200)"
  git checkout -q -- . && [ -z "$(git status --porcelain)" ] || echo "RESTORE FAILED $1"
}
arm baseline 0 'pass'
arm removed 1 's = s.replace(step, "")'
arm renamed 1 's = s.replace("name: Capture measurement census and clock gate", "name: Capture measurement gate")'
arm swallowed 1 's = s.replace("run: python3 scripts/check_nvm_capture.py", "run: python3 scripts/check_nvm_capture.py || true")'
arm replaced-with-mutation-flag 1 's = s.replace("run: python3 scripts/check_nvm_capture.py", "run: python3 scripts/check_nvm_capture.py --help")'
arm continue-on-error 1 's = s.replace(step, step + "        continue-on-error: true\n")'
arm if-false 1 's = s.replace(step, step.replace("        run:", "        if: false\n        run:"))'
arm moved-after-writer-gate 1 '
w = "      - name: Saved-state writer gate\n        run: python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test\n"
assert s.count(w) == 1
s = s.replace(step, "").replace(w, w + step)'
arm duplicated 1 's = s.replace(step, step + step)'
cd "$CLONE" && echo "CLONE_STATUS $(git status --porcelain | wc -l) HEAD $(git rev-parse HEAD)"
