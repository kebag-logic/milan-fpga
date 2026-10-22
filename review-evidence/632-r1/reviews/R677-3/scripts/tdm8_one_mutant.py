#!/usr/bin/env python3
"""Plant ONE tdm8render mutant through the campaign driver's own plant/build/
run_leg functions and print every [FAIL] line of its leg run.
usage: tdm8_one_mutant.py <repo> <workdir> <mutant name prefix>"""
import importlib.util, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); work = Path(sys.argv[2]).resolve(); want = sys.argv[3]
here = root / "tb/verilator/milan_dp_render"
sys.path.insert(0, str(root / "scripts"))
spec = importlib.util.spec_from_file_location("t", here / "tdm8_render_mutants.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
work.mkdir(parents=True, exist_ok=True)
for name, source, edits, leg, mode, breaks in t.MUTATIONS:
    if not name.startswith(want):
        continue
    value, why = t.plant(source, edits, work, "one")
    if value is None:
        print("PLANT FAILED:", why); sys.exit(2)
    exe = t.build(leg, {t.SOURCES[source][1]: value}, work / "obj_one")
    if exe is None:
        print("BUILD FAILED"); sys.exit(2)
    rc, out = t.run_leg(exe, mode)[:2]
    print(f"mutant: {name}\nleg: {leg} {mode}\nrc: {rc}\nnamed check: {breaks}")
    for line in str(out).splitlines():
        if "[FAIL]" in line or "T26" in line:
            print(line)
    print("verdict:", t.verdict(*t.run_leg(exe, mode), breaks) if False else "")
    sys.exit(0)
print("no such mutant"); sys.exit(2)
