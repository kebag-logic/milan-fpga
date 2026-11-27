"""log_diff_rm.py <checkout> <work-dir> [--msan]: append to the cleanup log, before the run, every scratch tree
tests/check_differential.py removes with shutil.rmtree (one per planted defect)."""
import ast
import datetime
import sys
from pathlib import Path

LOG = Path("$MANAGEMENT/2026-09-23/disk-cleanup.log")
checkout, work = Path(sys.argv[1]), Path(sys.argv[2]).resolve()
tree = ast.parse((checkout / "tests/check_differential.py").read_text())
names = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "MUTANTS" for t in node.targets):
        names = [elt.elts[0].value for elt in node.value.elts]
if "--msan" in sys.argv:
    names.append("lean-reads-value")
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
with LOG.open("a") as log:
    for name in names:
        log.write(f"{stamp} A861 lwsrp22 r2: rm -r (planned; check_differential.py removes its copy after the defect's run): {work}/mutant-{name}\n")
print(f"logged {len(names)} planned removals under {work}")
