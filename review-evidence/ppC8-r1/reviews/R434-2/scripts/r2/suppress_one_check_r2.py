#!/usr/bin/env python3
"""Round-2 port of the round-1 reviewer suppression probe: the packer now loads
the lint by path, so the recorder is patched on the module instance the packer
actually uses (gen_desc_image.model_lint.model_rules.RuleContext).
Usage: suppress_one_check_r2.py <repo-root> <check|NONE>. Exit 0 = gate passed."""
import io, os, sys, pathlib, unittest
root = pathlib.Path(sys.argv[1]).resolve(); check = sys.argv[2]
sys.path.insert(0, str(root / "tb/desc_store")); os.chdir(root / "tb/desc_store"); sys.argv = [sys.argv[0]]
import test_gen_desc_image as t
rules = t.gen_desc_image.model_lint.model_rules
assert check == "NONE" or check in rules.CHECKS, check
assert t.gen_desc_image.model_lint.RuleContext is rules.RuleContext
orig = rules.RuleContext.bad
def bad(self, c, where, detail):
    if c != check:
        orig(self, c, where, detail)
rules.RuleContext.bad = bad
r = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(unittest.defaultTestLoader.loadTestsFromModule(t))
print(f"{check}: tests={r.testsRun} failures={len(r.failures)} errors={len(r.errors)} -> {'PASSED (not covered)' if r.wasSuccessful() else 'KILLED'}")
sys.exit(0 if r.wasSuccessful() else 1)
