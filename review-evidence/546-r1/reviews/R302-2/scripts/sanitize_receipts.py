#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Replace local paths in receipts with placeholders; drop compiler build logs.

Usage: python3 sanitize_receipts.py <packet> <clone> <tool-bin-dir>
Rewrites <packet>/receipts in place. Compiler command lines (g++/ccache and
Verilator's per-file compile echoes) are removed from make logs; verdict,
check and probe output is kept verbatim. Build-only logs (*.build.log) and
the tool wrapper text are deleted, as in round 1.
"""

import re
import sys
from pathlib import Path

packet, clone, toolbin = (str(Path(a).resolve()) for a in sys.argv[1:4])
SUBS = [
    (re.escape(packet), "<packet>"),
    (re.escape(clone), "<clone>"),
    (re.escape(toolbin), "<tool-bin>"),
    (r"/home/[A-Za-z0-9_.-]+", "$HOME"),
    (r"/tmp/crf-step-mutants-[A-Za-z0-9_]+", "<tmp>/crf-step-mutants"),
    (r"/tmp/[A-Za-z0-9_.-]+", "<tmp>"),
    (r"/data/[A-Za-z0-9_./-]+", "<local-path>"),
]
COMPILER = re.compile(r"^\s*(ccache\s+)?(g\+\+|c\+\+|clang\+\+|/usr/bin/(g|c)\+\+)\s|"
                      r"^\s*(echo \"\" > |rm -f .*\.verilator_deplist|python3 .*verilator_includer)")
root = Path(packet) / "receipts"
for p in list(root.rglob("*.build.log")):
    p.unlink()
(root / "verilator-wrapper.txt").unlink(missing_ok=True)
for p in root.rglob("*"):
    if not p.is_file():
        continue
    lines = p.read_text(errors="replace").splitlines(keepends=True)
    out = []
    for line in lines:
        if COMPILER.search(line):
            continue
        for pat, rep in SUBS:
            line = re.sub(pat, rep, line)
        out.append(line)
    p.write_text("".join(out))
print("sanitized", sum(1 for q in root.rglob("*") if q.is_file()), "files")
