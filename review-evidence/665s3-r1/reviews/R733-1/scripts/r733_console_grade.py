#!/usr/bin/env python3
"""Reviewer probe: grade the host console transcript with scripts/baremetal_uart_smoke.py's own grade().
usage: r733_console_grade.py CHECKOUT TRANSCRIPT"""
import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
import baremetal_uart_smoke as smoke  # noqa: E402
text = Path(sys.argv[2]).read_text()
parts = re.findall(r"@@CMD \d+\n(.*?)@@END\n", text, re.S)
assert len(parts) == 3, parts
for k, p in enumerate(parts):
    print(f"RESPONSE {k}: {len(p)} bytes {p!r}")
bad = 0
for name, ok, detail in smoke.grade(*parts):
    want = name != "fabric-enabled"
    bad += ok != want
    print(f"GRADER {name}: {'PASS' if ok else 'FAIL'} ({detail}){'' if ok == want else '  <-- UNEXPECTED'}")
print(f"r733 console grade: {'PASS' if not bad else 'FAIL'} (fabric-enabled fails as the ruled difference)")
raise SystemExit(1 if bad else 0)
