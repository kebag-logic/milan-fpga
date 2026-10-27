#!/usr/bin/env python3
"""Run named self-test methods of a (possibly mutated) torture_campaign.py copy.

usage: run_named.py <planner.py> <test_name> [<test_name> ...]
Prints one line per test, OK or FAIL with the first assertion line; exit 0 if all pass.
"""
import importlib.util
import sys
import unittest

path, names = sys.argv[1], sys.argv[2:]
sys.path.insert(0, str(__import__("pathlib").Path(path).resolve().parent))
spec = importlib.util.spec_from_file_location("planner_under_probe", path)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
bases = [getattr(mod, n) for n in ("_CounterLawChecks", "_StreamingLicenceChecks", "_PlanContractChecks",
                                   "_AreaContractChecks", "_ReleasePlanChecks", "_ReleaseSoakChecks",
                                   "_ReleaseGateChecks", "_ConcurrencyChecks")]
T = type("T", tuple(bases) + (unittest.TestCase,), {})
suite = unittest.TestSuite(T(n) for n in names)
result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
for test, tb in result.failures + result.errors:
    print("FAILED:", test.id().rsplit(".", 1)[-1], "::", tb.strip().splitlines()[-1][:600])
sys.exit(0 if result.wasSuccessful() else 1)
