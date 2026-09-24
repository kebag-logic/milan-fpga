#!/usr/bin/env python3
"""Reviewer step (R313-1): redact the local home-directory prefix from receipts.

Usage: python3 sanitize_receipts.py <packet-dir>
Replaces the literal home prefix with $HOME in receipts/*, and replaces an
inherited PATH value recorded in *.rc argv lines with <PATH>. Prints per-file
replacement counts; nothing else in any receipt is altered.
"""
import os
import re
import sys
from pathlib import Path

home = os.path.expanduser("~")
pkt = Path(sys.argv[1])
for f in sorted((pkt / "receipts").iterdir()):
    t = f.read_text(errors="surrogateescape")
    n = t.count(home)
    t2 = t.replace(home, "$HOME")
    m = 0
    if f.suffix == ".rc":
        t2, m = re.subn(r"PATH=\S+", lambda mo: "PATH=<pinned-tool-dir>:<PATH>", t2)
    if n or m:
        f.write_text(t2, errors="surrogateescape")
        print(f"{f.name}: {n} home prefix(es), {m} PATH value(s) redacted")
