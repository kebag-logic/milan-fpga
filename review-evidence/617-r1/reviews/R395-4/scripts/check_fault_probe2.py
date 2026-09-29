#!/usr/bin/env python3
"""Second build-break fault probe (probe D of check_fault_probe.py was void:
BUILD_TAIL_LINES = 0 slices lines[-0:], the whole log). The committed
build_break_result() must FAIL when:
  D1  the printed tail is 1 line (the compiler's %Error is no longer in it);
  D2  build() keeps no output (the log it writes is empty).
Usage: check_fault_probe2.py <capture_coherence dir> <workdir>"""
import importlib.util, sys
from pathlib import Path
suite, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("m", suite / "mutants.py")
m = importlib.util.module_from_spec(spec); sys.argv = ["mutants.py"]; spec.loader.exec_module(m)
def show(tag, result):
    ok, lines = result
    print(f"{tag}: check {'PASSES' if ok else 'FAILS'}"); [print("     ", l[:220]) for l in lines[:4]]
d = work / "D1"; d.mkdir(parents=True, exist_ok=True); m.BUILD_TAIL_LINES = 1
show("D1 build_break_result with BUILD_TAIL_LINES=1", m.build_break_result(d)); m.BUILD_TAIL_LINES = 40
orig = m.run_child
def silent(cmd, cwd=None, env=None):
    rc, _ = orig(cmd, cwd=cwd, env=env); return rc, ""
m.run_child = silent
d = work / "D2"; d.mkdir(parents=True, exist_ok=True)
show("D2 build_break_result with the build's output discarded", m.build_break_result(d))
