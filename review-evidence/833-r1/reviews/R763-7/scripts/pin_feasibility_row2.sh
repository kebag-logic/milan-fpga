#!/bin/bash
# Feasibility of pinning row 2 while a notified shell waits stopped (review probe; never published as a fix).
# Usage: pin_feasibility_row2.sh <packet> <gtrees-dir> NAME...
packet=$1 trees=$2; shift 2
for n in "$@"; do
  d=$packet/scratch/pin2/$n; rm -rf "$d"; mkdir -p "$d"; cp -r "$trees/$n/scripts" "$d/"
  python3 -I - "$d/scripts/test_suite_cancellation.py" <<'PY'
import sys
from pathlib import Path
path = Path(sys.argv[1]); text = path.read_text()
anchor = '        kept("a second-stage resume", resumed_at(3), window(3), shell)\n'
add = ('        kept("a new descendant beside a stopped shell", lambda clock: {shell: (owner_pid, "2"), child: (shell, "4"),'
       ' **({cleanup: (child, "7")} if clock else {})},\n'
       '             [(0, "SIGTERM", "child"), (2, "SIGKILL", "child"), (2, "SIGKILL", "cleanup command"),'
       ' (14, "SIGKILL", "shell"), (14, "SIGKILL", "child"), (14, "SIGKILL", "cleanup command"), (14, "verdict")], shell)\n')
assert text.count(anchor) == 1
path.write_text(text.replace(anchor, add + anchor))
PY
  out=$(python3 -B "$d/scripts/test_suite_cancellation.py" --control owner_stated_seconds 2>&1); rc=$?
  echo "$n: rc $rc: $(echo "$out" | tail -1 | cut -c1-300)"
done
