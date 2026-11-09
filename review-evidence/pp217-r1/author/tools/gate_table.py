#!/usr/bin/env python3
"""gate_table.py <runs-dir> [name...]: one markdown row per gate record (<name>.cmd/.rc/.start/.end) in <runs-dir>,
in start order, or in the order named: gate, command (host paths scrubbed as collect.py does), rc, minutes.
A gate with no rc file prints rc "none" (not finished)."""
import sys
from pathlib import Path
sys.argv, args = sys.argv[:1], sys.argv[1:]
ROOTS = [("$VALIDATION_STORAGE/scratch/pp217-a755", "$SCRATCH"), ("$VALIDATION_STORAGE/scratch/pp217-parent", "$PARENT"),
         ("$HOME/milan-fpga-management/2026-09-23/pp217-a755", "$OUT")]
d = Path(args[0])
names = args[1:] or sorted((p.stem for p in d.glob("*.cmd")),
                           key=lambda n: int((d / f"{n}.start").read_text() or 0) if (d / f"{n}.start").exists() else 0)
def rd(n, s):
    p = d / f"{n}.{s}"
    return p.read_text().strip() if p.exists() else None
print("| Gate | Command | rc | min |")
print("|---|---|---:|---:|")
for n in names:
    cmd = rd(n, "cmd") or ""
    for a, b in ROOTS:
        cmd = cmd.replace(a, b)
    rc, st, en = rd(n, "rc"), rd(n, "start"), rd(n, "end")
    mins = f"{(int(en) - int(st)) / 60:.1f}" if st and en else "-"
    print(f"| {n} | `{cmd.replace('|', chr(92) + '|')}` | {rc if rc is not None else 'none'} | {mins} |")
