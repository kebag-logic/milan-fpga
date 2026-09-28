#!/usr/bin/env python3
"""Compare tb/acmp_talker/README.md's mutant table with retry_mutants.py logs.

Each killed row must match the rerun's nonzero rc, its exact failure count and
contain its named assertion among the failures; each control row must be rc 0
with no failures and sit in the matching EQUIVALENT/PERFORMANCE dictionary.
Usage: readme_table_check.py <processor-tree> <retry_mutants --logs dir>
Loads retry_mutants.py without writing bytecode into the tree.
"""
import importlib.util
import pathlib
import re
import sys

sys.dont_write_bytecode = True
tree, logs = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
readme = (tree / "tb/acmp_talker/README.md").read_text()
rows = re.findall(r"^\| `(\w+)` \| (killed, (\d+) failures|equivalent control, rc 0|"
                  r"performance control, rc 0) \| (.*?) \|$", readme, re.M)
spec = importlib.util.spec_from_file_location("rm", tree / "tb/acmp_talker/retry_mutants.py")
rm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rm)
names = {r[0] for r in rows}
print(f"README rows={len(rows)} MUTATIONS={len(rm.MUTATIONS)} "
      f"EQUIVALENT={len(rm.EQUIVALENT_MUTATIONS)} PERFORMANCE={len(rm.PERFORMANCE_MUTATIONS)}")
print("in MUTATIONS not in README:", sorted(set(rm.MUTATIONS) - names),
      "; in README not in MUTATIONS:", sorted(names - set(rm.MUTATIONS)))
bad = 0
for name, kind, count, named in rows:
    log = (logs / f"{name}.txt").read_text().splitlines()
    rc = int(log[0].split(": ")[1])
    fails = [l for l in log[2:] if l.startswith("FAIL:")]
    if count:
        ok = rc != 0 and len(fails) == int(count) and ("FAIL: " + named) in fails
    else:
        ok = (rc == 0 and not fails
              and (name in rm.EQUIVALENT_MUTATIONS) == kind.startswith("equivalent")
              and (name in rm.PERFORMANCE_MUTATIONS) == kind.startswith("performance"))
    if not ok:
        bad += 1
        print("MISMATCH", name, kind, rc, len(fails))
print(f"rows matching rerun: {len(rows) - bad}/{len(rows)}")
sys.exit(1 if bad else 0)
