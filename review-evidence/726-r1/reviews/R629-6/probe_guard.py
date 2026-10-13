#!/usr/bin/env python3
"""Restore the old zero-publication guard and exercise the standing regression."""
import importlib.util,sys,unittest
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(__file__).resolve().parent
original=(root/"tb/tools/torture_campaign.py").read_text()
assert original.count("    if total > frx:")==1
mutant=packet/"scratch/torture_guard.py"
mutant.write_text(original.replace("    if total > frx:","    if frx and total > frx:"))
spec=importlib.util.spec_from_file_location("torture_guard",mutant)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
class T(m._CounterLawChecks,m._StreamingLicenceChecks,m._PlanContractChecks,m._AreaContractChecks,m._ReleasePlanChecks,m._ReleaseSoakChecks,m._ConcurrencyChecks,unittest.TestCase):
    pass
cases=list(unittest.TestLoader().loadTestsFromTestCase(T))
with (packet/"guard-detection.log").open("w") as out:
    detected=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.TestSuite(cases))
assert len(detected.failures)==1 and not detected.errors
assert detected.failures[0][0]._testMethodName=="test_unpublished_zero_receive_snapshot"
with (packet/"guard-escape.log").open("w") as out:
    escaped=unittest.TextTestRunner(stream=out,verbosity=2).run(unittest.TestSuite(c for c in cases if c._testMethodName!="test_unpublished_zero_receive_snapshot"))
assert escaped.wasSuccessful()
print("Old guard detected only by test_unpublished_zero_receive_snapshot; omission escape passed",escaped.testsRun,"checks")
