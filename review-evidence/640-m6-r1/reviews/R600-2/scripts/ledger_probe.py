#!/usr/bin/env python3
"""Show ledger_arith.py can fail: plant one error per copy and require rc 1.

usage: python3 -I ledger_probe.py <checkout> <scratch-dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

CO, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
ARITH = Path(__file__).with_name("ledger_arith.py")
PLANTS = [
    ("cumulative-row", "MARK_II_AREA_PLAN.md", "| 4 | M6 | 600 | 34,867 |", "| 4 | M6 | 600 | 34,868 |"),
    ("m6-block-credit", "MARK_II_AREA_PLAN.md", "| Listener monitor | 966 -> 754 |", "| Listener monitor | 966 -> 755 |"),
    ("m2-route-lut", "MARK_II_AREA_PLAN.md", "| M2 route at `4177835c` | 50,139 |", "| M2 route at `4177835c` | 50,138 |"),
    ("m6-section-claims-m2-array", "MARK_II_AREA_PLAN.md", "Render set-point already used distributed RAM", "The CSR W FIFO and render set-point already used distributed RAM"),
    ("bram-running-total", "AREA_BUDGET.md", "| M2 maximum additional allocation | +2 | 0 | +2 | 120.5 |", "| M2 maximum additional allocation | +2 | 0 | +2 | 121.5 |"),
    ("budget-lane-row", "AREA_BUDGET.md", "| M6 media contexts | 600 | 34,867 |", "| M6 media contexts | 600 | 34,767 |"),
    ("m6-budget-note-lost", "AREA_BUDGET.md", "M6 has measured its lane: 418 LUTs", "M6 lane: 418 LUTs"),
    ("m2-budget-note-lost", "AREA_BUDGET.md", "M2 has measured its lane: 34 LUTs", "M2 lane: 34 LUTs"),
]
bad = 0
for name, fname, old, new in PLANTS:
    tree = SCRATCH / name
    shutil.rmtree(tree, ignore_errors=True)
    (tree / "docs/design").mkdir(parents=True)
    (tree / "syn/ooc").mkdir(parents=True)
    for f in ("MARK_II_AREA_PLAN.md", "AREA_BUDGET.md"):
        shutil.copy(CO / "docs/design" / f, tree / "docs/design" / f)
    shutil.copy(CO / "syn/ooc/pp_resource_baseline.json", tree / "syn/ooc")
    p = tree / "docs/design" / fname
    text = p.read_text()
    assert text.count(old) == 1, (name, text.count(old))
    p.write_text(text.replace(old, new))
    r = subprocess.run([sys.executable, "-I", str(ARITH), str(tree)], capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL")]
    caught = r.returncode == 1 and fails
    bad += not caught
    print(f"{'CAUGHT' if caught else 'MISSED'} {name}: rc={r.returncode}; " + "; ".join(fails))
print(f"{len(PLANTS) - bad}/{len(PLANTS)} plants caught")
sys.exit(1 if bad else 0)
