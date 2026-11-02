#!/bin/bash
# Feasibility of pinning a later-pass, in-grace resume (review probe; never published as a fix).
# Usage: pin_feasibility.sh <packet> <gtrees-dir> NAME...
# Copies each tree from grace_trees.py, adds one owner_stated_seconds listing whose shell is
# resumed at 0.5 s (pass 2+, inside grace), and runs that control alone.
packet=$1 trees=$2; shift 2
for n in "$@"; do
  d=$packet/scratch/pin/$n; rm -rf "$d"; mkdir -p "$d"; cp -r "$trees/$n/scripts" "$d/"
  python3 -I - "$d/scripts/test_suite_cancellation.py" <<'PY'
import sys
from pathlib import Path
path = Path(sys.argv[1]); text = path.read_text()
anchor = '        kept("a second-stage resume", resumed_at(3), window(3), shell)\n'
assert text.count(anchor) == 1
path.write_text(text.replace(anchor, '        kept("an in-grace resume", resumed_at(0.5), window(0.5), shell)\n' + anchor))
PY
  out=$(python3 -B "$d/scripts/test_suite_cancellation.py" --control owner_stated_seconds 2>&1); rc=$?
  echo "$n: rc $rc: $(echo "$out" | tail -1 | cut -c1-260)"
done
