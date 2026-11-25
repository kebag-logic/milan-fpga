#!/usr/bin/env python3
"""Run one plan of engine passes_test.py serial vs parallel and print unified diffs of both streams.

usage: python3 passes_diff.py ENGINE_DIR PLAN_NAME [MAKE FLAGS...]
"""
import difflib
import importlib.util
import sys
import tempfile
from pathlib import Path

engine = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("passes_test", engine / "passes_test.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
plan = t.PLANS[sys.argv[2]]
flags = sys.argv[3:] or ["-j4"]
with tempfile.TemporaryDirectory() as d:
    scratch = Path(d)
    trees = t.tree(scratch)
    want = t.make(trees["serial"], flags, plan, scratch / "e1")
    got = t.make(trees["parallel"], flags, plan, scratch / "e2")
    print("rc", want.returncode, got.returncode)
    for name in ("stdout", "stderr"):
        a = t.norm(getattr(want, name), trees["serial"]).splitlines(True)
        b = t.norm(getattr(got, name), trees["parallel"]).splitlines(True)
        sys.stdout.writelines(difflib.unified_diff(a, b, "serial " + name, "parallel " + name))
