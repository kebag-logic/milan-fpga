#!/usr/bin/env python3
"""Check-suppression probe: drop every finding of ONE lint check (or none) in
the test process, run the whole generator gate, and report whether it failed.

usage: probe_check_suppression.py <processor-tree> <check|NONE>
Prints `<check> KILLED|SURVIVED failures=<n> errors=<n> tests=<n>`; exit 0.
No file of the tree is changed.
"""
import io
import sys
import unittest
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
check = sys.argv[2]
sys.path.insert(0, str(tree / "tb/desc_store"))
sys.argv = sys.argv[:1]
import test_gen_desc_image as gate  # noqa: E402

rules = sys.modules["model_rules"]
if check != "NONE" and check not in rules.CHECKS:
    raise SystemExit(f"unknown check {check}")
original = rules.RuleContext.bad


def bad(self, name, where, detail):
    if name != check:
        original(self, name, where, detail)


rules.RuleContext.bad = bad
suite = unittest.defaultTestLoader.loadTestsFromModule(gate)
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
failed = not result.wasSuccessful()
names = sorted({t.id().split(".", 1)[1] for t, _ in result.failures + result.errors})
verdict = "KILLED" if failed else "SURVIVED"
if check == "NONE":
    verdict = "CONTROL-FAIL" if failed else "CONTROL-PASS"
print(f"{check} {verdict} failures={len(result.failures)} errors={len(result.errors)} "
      f"tests={result.testsRun} failing={','.join(names)}")
