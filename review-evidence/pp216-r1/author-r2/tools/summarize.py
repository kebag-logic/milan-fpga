#!/usr/bin/env python3
"""summarize.py <log> <out>: for a log too large to keep (over 200 KB), the lines a reader needs: its size and
sha256, the count of RESULT: PASS / RESULT: FAIL / [ok] / [FAIL] / FAIL: lines, and every line naming a result
(RESULT, a check tally, scenarios/steps passed, PASS/FAIL verdicts), in order."""
import hashlib
import re
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
data = src.read_bytes()
text = data.decode(errors="replace").splitlines()
keep = re.compile(r"RESULT: |\d+ checks: \d+ PASS|scenarios? passed|steps passed|features? passed|: PASS\b|"
                  r"\bFAIL\b|test_ctrl_firmware|ctrl_boundary")
lines = [
    f"{src.name} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}): lines naming a result",
    f"RESULT: PASS lines: {sum('RESULT: PASS' in ln for ln in text)}",
    f"RESULT: FAIL lines: {sum('RESULT: FAIL' in ln for ln in text)}",
    f"[ok] lines: {sum('[ok]' in ln for ln in text)}",
    f"[FAIL] lines: {sum('[FAIL]' in ln for ln in text)}",
    f"FAIL: lines: {sum(ln.startswith('FAIL:') for ln in text)}",
    "",
]
lines += [ln[:300] for ln in text if keep.search(ln) and "[ok]" not in ln]
out.write_text("\n".join(lines) + "\n")
