#!/usr/bin/env python3
"""gate_table.py <runs-dir> <gate>...: one markdown row per gate: its name, rc, wall seconds and the last line of
its log matching the gate's result pattern (PASS/FAIL tallies, OK lines, RESULT lines), read from
<runs-dir>/<gate>.{rc,start,end,log}."""
import re
import sys
from pathlib import Path

PAT = re.compile(r"(\d+ checks: \d+ PASS, \d+ FAIL|RESULT: (PASS|FAIL)|: PASS\b|\bPASS\b \(|OK\b|caught|"
                 r"verdict: |coverage: |LINT GATE|matrix: |elab guards: |passed, \d+ failed|scenarios passed|"
                 r"selftest: |self-test: |YOSYS XILINX OK|all figures agree|figures? .*agree)")
runs = Path(sys.argv[1])
for g in sys.argv[2:]:
    rc = (runs / f"{g}.rc").read_text().strip() if (runs / f"{g}.rc").exists() else "running"
    try:
        secs = int((runs / f"{g}.end").read_text()) - int((runs / f"{g}.start").read_text())
    except (OSError, ValueError):
        secs = -1
    log = (runs / f"{g}.log").read_text(errors="replace").splitlines() if (runs / f"{g}.log").exists() else []
    hits = [ln.strip() for ln in log if PAT.search(ln)]
    last = hits[-1][:160] if hits else (log[-1][:160] if log else "")
    print(f"| {g} | {rc} | {secs} | `{last}` |")
