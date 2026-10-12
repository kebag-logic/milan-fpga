#!/usr/bin/env python3
"""Check detection and omission controls without altering tracked source."""
import importlib.util
import io
import json
import pathlib
import re
import sys
import types
import unittest

root, packet = map(pathlib.Path, sys.argv[1:])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

steps = load("review_counter_steps", root / "tests/steps/counters_contract_steps.py")
source = steps.CRF_RX.read_text()
steps.step_cc_crf_era_wipe(types.SimpleNamespace())
key = "if (w_bind_rise_w) begin"
start = source.index(key)
end = source.index("\n      end", start)
body = source[start:end]
registers = list(steps.CRF_COUNTER_REG.values()) + ["iv_uf_r", "iv_sm_r", "iv_mr_r", "iv_tu_r", "iv_lt_r", "iv_et_r"]
records = []
for register in registers:
    changed, count = re.subn(r"\b" + register + r"\s*<=\s*(?:'0|1'b0)\s*;", "", body)
    assert count == 1, register
    mutant = packet / "scratch" / ("missing-reset-" + register + ".sv")
    mutant.write_text(source[:start] + changed + source[end:])
    steps.CRF_RX = mutant
    try:
        steps.step_cc_crf_era_wipe(types.SimpleNamespace())
    except AssertionError as error:
        assert register in str(error), (register, str(error))
        message = str(error)
    else:
        raise AssertionError("reset plant escaped: " + register)
    steps.step_cc_crf_era_edge(types.SimpleNamespace())
    steps.step_cc_crf_era_lock(types.SimpleNamespace())
    records.append({"reset": register, "detected": True,
                    "omitting_era_wipe_check_passes_other_era_checks": True, "diagnostic": message})

grader_source = (root / "tb/tools/torture_campaign.py").read_text()
assert grader_source.count("if total > frx:") == 1
mutant = packet / "scratch/old_snapshot_guard.py"
mutant.write_text(grader_source.replace("if total > frx:", "if frx and total > frx:"))
module = load("old_snapshot_guard", mutant)
mixins = [getattr(module, name) for name in ("_CounterLawChecks", "_StreamingLicenceChecks",
          "_PlanContractChecks", "_AreaContractChecks", "_ReleasePlanChecks",
          "_ReleaseSoakChecks", "_ConcurrencyChecks")]
case = type("StandingChecks", tuple(mixins) + (unittest.TestCase,), {})
suite = unittest.TestLoader().loadTestsFromTestCase(case)
output = io.StringIO()
result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
(packet / "receipts/old-guard-detect.log").write_text(output.getvalue())
assert not result.errors
assert len(result.failures) == 1 and result.failures[0][0]._testMethodName == "test_unpublished_zero_receive_snapshot"
suite = unittest.TestSuite(t for t in unittest.TestLoader().loadTestsFromTestCase(case)
                          if t._testMethodName != "test_unpublished_zero_receive_snapshot")
output = io.StringIO()
escape = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
(packet / "receipts/old-guard-escape.log").write_text(output.getvalue())
assert escape.wasSuccessful()
receipt = {"reset_controls": records,
           "old_guard": {"tests_run": result.testsRun, "failures": len(result.failures),
                         "named_test": "test_unpublished_zero_receive_snapshot",
                         "omission_tests_run": escape.testsRun, "omission_pass": escape.wasSuccessful()}}
(packet / "receipts/standing-controls.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"reset_controls": len(records), "old_guard": receipt["old_guard"]}))
