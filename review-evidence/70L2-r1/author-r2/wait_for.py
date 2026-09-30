#!/usr/bin/env python3
"""Wait in the foreground, at most <seconds>, until <path> exists or contains <text>.

usage: wait_for.py <seconds> <path> [<text>]
Exit 0 when the condition holds, 1 on timeout; prints the elapsed time.
"""
import sys
import time
from pathlib import Path

limit, path = float(sys.argv[1]), Path(sys.argv[2])
text = sys.argv[3] if len(sys.argv) > 3 else None
start = time.monotonic()
while time.monotonic() - start < limit:
    if path.exists() and (text is None or text in path.read_text(errors="replace")):
        print(f"condition met after {time.monotonic() - start:.0f}s")
        sys.exit(0)
    time.sleep(15)
print(f"timed out after {limit:.0f}s")
sys.exit(1)
