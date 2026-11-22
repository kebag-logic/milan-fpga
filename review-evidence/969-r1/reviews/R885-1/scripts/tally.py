#!/usr/bin/env python3
"""Summarise an arms.py output directory: per arm log, the tally and the failing test names.

Usage: python3 -I tally.py <out-dir>
"""
import re
import sys
from pathlib import Path

for log in sorted(Path(sys.argv[1]).glob("[0-9][0-9]-*.log")):
    text = log.read_text(encoding="utf-8", errors="replace")
    passed = re.findall(r"\[  PASSED  \] (\d+) tests?", text)
    failed = sorted(set(re.findall(r"^\[  FAILED  \] ([A-Za-z0-9_]+\.[A-Za-z0-9_]+)\s*$", text, re.M)))
    print(f"{log.name}: passed={passed[-1] if passed else '?'} failed={len(failed)}")
    for name in failed:
        print(f"    FAILED {name}")
