#!/usr/bin/env python3
"""Print every control-firmware mutant (name, file, arm, test) of one checkout, one per line, sorted.
Usage: python3 -B mutant_tables.py <checkout>   (imports that checkout's own tables)."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_mutants
rows = []
for m in ctrl_mutants.MUTANTS:
    d = m._asdict() if hasattr(m, "_asdict") else vars(m)
    rows.append("\t".join(str(d.get(k, "")) for k in ("name", "path", "arm", "test")))
for r in sorted(rows):
    print(r)
print(f"TOTAL\t{len(rows)}", file=sys.stderr)
