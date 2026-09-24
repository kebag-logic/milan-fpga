#!/usr/bin/env python3
"""Run a tree's own engine mutation arm unmodified and record, per mutant,
every FAIL line the harness printed, so two commits can be compared.

Usage: probe_mutants.py <tree> <out.txt>   (VERILATOR must be on PATH)
"""
import io, sys, contextlib
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
sys.path.insert(0, str(tree / "tb/verilator/engine"))
import mutants  # noqa: E402

seen = {}
orig = mutants.run_harness
def recording(exe, rundir):
    rc, output = orig(exe, rundir)
    seen[Path(rundir).name] = (rc, [l for l in output.splitlines()
                                    if l.startswith("FAIL ") or " checks: " in l])
    return rc, output
mutants.run_harness = recording

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = mutants.main()
with out.open("w") as f:
    f.write(buf.getvalue())
    f.write(f"arm exit {rc}\n")
    for name, *_ in [("clean",)] + [(m[0],) for m in mutants.MUTATIONS]:
        tag = "clean" if name == "clean" else "".join(c if c.isalnum() else "_" for c in name)
        r = seen.get(f"run_{tag}")
        f.write(f"== {name}\n")
        if r is None:
            f.write("  (not run)\n"); continue
        f.write(f"  rc {r[0]}\n")
        for l in r[1]:
            f.write(f"  {l}\n")
print(f"arm exit {rc}")
