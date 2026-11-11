#!/usr/bin/env bash
# gate_mutants.sh <clone> <log>: gate 23p on three planted copies of sw/litex/check_image_identity.py, each restored
# after its run: the bound comparison always refusing (if True), inverted (have == bound), the manifest-ident rule removed
set -uo pipefail
source <scratch>/tools/env.sh
D=$1; LOG=$2; F=sw/litex/check_image_identity.py
cd "$D" || exit 2
: > "$LOG"
plant() { python3 -I - "$F" "$1" <<'PY'
import sys
from pathlib import Path
p, arm = Path(sys.argv[1]), sys.argv[2]
s = p.read_text()
old = {"if-true": "    if have != bound:\n", "have-eq-bound": "    if have != bound:\n",
       "no-manifest-ident": "    if claimed[\"ident\"] != got[\"ident\"]:\n        found.append((\"manifest\", f\"the manifest's ident {claimed['ident']!r} is not the image's {got['ident']!r}\"))\n"}[arm]
new = {"if-true": "    if True:\n", "have-eq-bound": "    if have == bound:\n", "no-manifest-ident": ""}[arm]
assert s.count(old) == 1, arm
p.write_text(s.replace(old, new))
PY
}
for arm in if-true have-eq-bound no-manifest-ident; do
  plant $arm || { echo "PLANT FAILED $arm" >> "$LOG"; exit 3; }
  echo "=== arm $arm: $(git diff --stat -- $F | tail -1)" >> "$LOG"
  git diff -- $F >> "$LOG"
  PATH=$LITEX:$SDK:$PATH python3 sw/builder/test_builder.py --gates test_image_identity_gate > "$LOG.$arm" 2>&1
  rc=$?
  grep -E "^  (the good|a bound bitstream|the manifest's ident changed)|^    a bound bitstream|^    the manifest's ident changed|ALL GATES PASS|AssertionError|gate 23p:" "$LOG.$arm" | cut -c1-400 >> "$LOG"
  echo "arm $arm: test_builder rc=$rc" >> "$LOG"
  git checkout -q -- $F
  test -z "$(git status --porcelain -- $F)" || { echo "RESTORE FAILED" >> "$LOG"; exit 4; }
done
echo "restored: $(git diff --stat -- $F | wc -l) changed lines in $F" >> "$LOG"
