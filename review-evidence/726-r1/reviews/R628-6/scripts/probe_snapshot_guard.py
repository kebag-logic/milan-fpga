#!/usr/bin/env python3
"""Replant the prior unpublished-zero guard and run the standing law tests.

Usage: probe_snapshot_guard.py REPO PACKET
Only a module copy under PACKET/scratch is changed. The unchanged self-tests
must detect the old guard; omitting only the detecting test must pass.
"""
import importlib.util
import pathlib
import sys
import unittest

repo, packet = map(pathlib.Path, sys.argv[1:3])
source = repo / "tb/tools/torture_campaign.py"
work = packet / "scratch/snapshot-guard"
work.mkdir(parents=True, exist_ok=True)
text = source.read_text()
anchor = "    if total > frx:\n"
assert text.count(anchor) == 1
target = work / "torture_campaign.py"
target.write_text(text.replace(anchor, "    if frx > 0 and total > frx:\n"))
sys.path.insert(0, str(source.parent))
spec = importlib.util.spec_from_file_location("snapshot_guard_plant", target)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
case = type("StandingCounterLaws", (module._CounterLawChecks, unittest.TestCase), {})
names = unittest.defaultTestLoader.getTestCaseNames(case)
check = "test_unpublished_zero_receive_snapshot"
assert check in names
for omitted in (False, True):
    tests = [case(name) for name in names if not (omitted and name == check)]
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(unittest.TestSuite(tests))
    failures = {test._testMethodName for test, _ in result.failures + result.errors}
    print(f"OMITTED={omitted} tests={result.testsRun} failures={sorted(failures)}")
    assert not result.errors
    assert failures == (set() if omitted else {check})
print("SNAPSHOT GUARD DETECTION AND OMISSION: PASS")
