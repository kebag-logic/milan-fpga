#!/usr/bin/env python3
"""wait_rc.py DIR MAXSECONDS NAME... : wait until DIR/NAME.rc exists for every NAME
(or MAXSECONDS elapses), then print each rc. Exit 0 if all present."""
import sys
import time
from pathlib import Path

d, limit, names = Path(sys.argv[1]), float(sys.argv[2]), sys.argv[3:]
end = time.time() + limit
while time.time() < end and not all((d / f"{n}.rc").exists() for n in names):
    time.sleep(5)
missing = 0
for n in names:
    p = d / f"{n}.rc"
    print(n, p.read_text().strip() if p.exists() else "RUNNING")
    missing += not p.exists()
sys.exit(1 if missing else 0)
