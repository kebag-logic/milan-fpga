#!/usr/bin/env python3
"""Run the gate with one lint check suppressed (its findings dropped).
Usage: suppress_one_check.py <repo-root> <check>. Exit 0 = gate passed (check NOT covered)."""
import sys, pathlib, unittest, io
root = pathlib.Path(sys.argv[1]).resolve(); check = sys.argv[2]
sys.path.insert(0, str(root / "hdl/aecp/desc")); sys.path.insert(0, str(root / "tb/desc_store"))
import model_rules
assert check == "NONE" or check in model_rules.CHECKS, check
orig = model_rules.RuleContext.bad
def bad(self, c, where, detail):
    if c != check: orig(self, c, where, detail)
model_rules.RuleContext.bad = bad
import os; os.chdir(root / "tb/desc_store")
sys.argv = [sys.argv[0]]
import test_gen_desc_image as t
assert t.gen_desc_image.model_lint.model_rules if hasattr(t.gen_desc_image.model_lint,'model_rules') else True
import model_lint; assert model_lint.RuleContext is model_rules.RuleContext
suite = unittest.defaultTestLoader.loadTestsFromModule(t)
r = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
print(f"{check}: tests={r.testsRun} failures={len(r.failures)} errors={len(r.errors)}")
sys.exit(0 if r.wasSuccessful() else 1)
