#!/usr/bin/env python3
"""Which finding (p.append / return [...]) and refusal (raise GateError) lines of
the AECP command gate does its own --selftest execute?
Usage: python3 -I selftest_coverage.py HEAD_TREE"""
import importlib.util, io, re, sys, contextlib
from pathlib import Path
root = Path(sys.argv[1]).resolve()
src = root / "scripts/check_aecp_commands.py"
spec = importlib.util.spec_from_file_location("gate", src)
g = importlib.util.module_from_spec(spec); sys.dont_write_bytecode = True; spec.loader.exec_module(g)
hit = set()
fname = str(src)
def tracer(frame, event, arg):
    if frame.f_code.co_filename == fname:
        if event == "line":
            hit.add(frame.f_lineno)
        return tracer
    return None
sys.settrace(tracer)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = g.selftest(root)
sys.settrace(None)
print(f"selftest rc {rc}: {buf.getvalue().strip().splitlines()[-1]}")
lines = src.read_text().splitlines()
end = next(i for i, l in enumerate(lines, 1) if l.startswith("def cmd("))  # checks end before the self-test
sites = [(i, l.strip()) for i, l in enumerate(lines[:end], 1)
         if re.search(r"\bp\.append\(|raise GateError\(|return \[f\"|return p \+ \[", l)]
miss = [(i, l) for i, l in sites if i not in hit]
print(f"finding/refusal sites before the self-test: {len(sites)}; executed by the self-test: {len(sites) - len(miss)}")
for i, l in miss:
    print(f"  NOT EXECUTED :{i}: {l[:110]}")
