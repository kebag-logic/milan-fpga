#!/usr/bin/env python3
"""plants.py CTRL_TEST_DIR OUT JOBS EXTRA PREFIX...: srp_mutants.campaign over the table's defects whose names start
with a PREFIX, plus, when EXTRA is a path, the reviewer's own defects from that module (its defects(Defect)), at
1x1/1if, 8x8/1if and 1x1/2if ($PLANT_SHAPES selects some). Prints each campaign's result; the campaign prints each defect's [ok]/ESCAPED line."""
import importlib.util
import os
import sys
from pathlib import Path

here = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3])
extra = sys.argv[4]
sys.path.insert(0, str(here))
sys.path.insert(0, str(here.parents[1] / "gtest"))
import srp_mutants  # noqa: E402
from ctrl_build import CTRL  # noqa: E402

lwsrp = (CTRL.parents[2] / "third_party/lwSRP").resolve()
table = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(tuple(sys.argv[5:]))) if sys.argv[5:] else ()
if extra != "-":
    spec = importlib.util.spec_from_file_location("reviewer_defects", extra)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    table += tuple(mod.defects(srp_mutants.Defect))
srp_mutants.DEFECTS = table
print(f"{len(table)} defects: {[d.name for d in table]}", flush=True)
bad = False
shapes = (("if1", 1, ""), ("8x8-if1", 1, "endstation_ax7101_8x8"), ("if2", 2, ""))
wanted = os.environ.get("PLANT_SHAPES", "if1,8x8-if1,if2").split(",")
for label, interfaces, entity in (s for s in shapes if s[0] in wanted):
    failed = srp_mutants.campaign(out / label, lwsrp, jobs, interfaces, entity)
    print(f"CAMPAIGN {label}: {'FAIL' if failed else 'PASS'}", flush=True)
    bad |= failed
sys.exit(1 if bad else 0)
