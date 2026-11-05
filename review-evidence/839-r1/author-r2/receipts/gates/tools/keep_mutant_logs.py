#!/usr/bin/env python3
"""Receipts for the campaign's controls: plant each named mutation of bootsa_mutants.py through that driver's own
code, build the leg through its recipe, run it, and keep the whole run's output and the planted diff.
The campaign (make bootsa-mutants) is the gate; this only keeps what each control's run printed.

usage: keep_mutant_logs.py <milan_dp dir of a clean clone> <work dir> <out dir> <jobs> <index>...
"""
import concurrent.futures, difflib, importlib.util, sys
from pathlib import Path

here, work, out = (Path(a).resolve() for a in sys.argv[1:4])
jobs = int(sys.argv[4]); picks = [int(a) for a in sys.argv[5:]]
sys.path.insert(0, str(here / "../../../scripts"))
spec = importlib.util.spec_from_file_location("bootsa_mutants", here / "bootsa_mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
work.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)

def one(i):
    name, plants, breaks = m.MUTATIONS[i]
    d = work / f"m{i}"; d.mkdir(exist_ok=True)
    sources = {}
    for var, edits in plants.items():
        orig = m.RTL[var].read_text(); text = orig
        for a, b in edits:
            assert text.count(a) == 1, (name, a)
            text = text.replace(a, b)
        p = d / m.RTL[var].name; p.write_text(text); sources[var] = p
        rel = f"hdl/milan/{m.RTL[var].name}"
        (out / f"mutant-{i:02d}.diff").write_text("".join(difflib.unified_diff(
            orig.splitlines(True), text.splitlines(True), f"a/{rel}", f"b/{rel}")))
    exe = m.build(sources, d / "obj")
    if exe is None:
        (out / f"run-{i:02d}.log").write_text(f"# {name}: did not build\n"); return i, "did not build"
    rc, text = m.run_leg(exe)
    v = m.verdict(rc, text, breaks)
    (out / f"run-{i:02d}.log").write_text(f"# control {i}: {name}\n# must fail by: {breaks}\n# rc {rc}, verdict {v}\n" + text)
    return i, v

with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
    res = list(pool.map(one, picks))
for i, v in res:
    print(f"control {i}: {v}: {m.MUTATIONS[i][0]}")
sys.exit(0 if all(v == "caught" for _, v in res) else 1)
