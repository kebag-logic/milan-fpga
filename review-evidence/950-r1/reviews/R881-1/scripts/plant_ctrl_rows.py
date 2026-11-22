"""plant_ctrl_rows.py <test-dir> <out> <name>...: plant only the named rows of ctrl_mutants.MUTANTS through the control
campaign's own planting and grading (ctrl_mutants.campaign, on a copy), the whole table's unnamed-test check first."""
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import ctrl_mutants as cm
out, names = Path(sys.argv[2]), sys.argv[3:]
rows = tuple(m for m in cm.MUTANTS if m.name in names)
assert {m.name for m in rows} == set(names), set(names) - {m.name for m in rows}
print("tests the whole table names none of:", cm.unnamed_tests())
cm.unnamed_tests = lambda: []
cm.MUTANTS = rows
escaped = cm.campaign(out, out / "reuse", 4)
sys.exit(1 if escaped else 0)
