#!/usr/bin/env python3
"""Run a tree's test_gen_desc_image.py and count tests and subtest outcomes.

Usage: count_cases.py <tree>
Exit 0 only if 6 tests ran, 24 subtests passed and nothing failed or errored.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "t", tree / "tb/desc_store/test_gen_desc_image.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Counting(unittest.TextTestResult):
    sub_pass = 0
    sub_fail = 0

    def addSubTest(self, test, subtest, err):  # noqa: N802 (unittest API)
        if err is None:
            Counting.sub_pass += 1
        else:
            Counting.sub_fail += 1
        super().addSubTest(test, subtest, err)


suite = unittest.defaultTestLoader.loadTestsFromModule(mod)
result = unittest.TextTestRunner(verbosity=2, resultclass=Counting,
                                 stream=sys.stdout).run(suite)
print(f"tests run {result.testsRun}; subtests passed {Counting.sub_pass}, "
      f"failed/errored {Counting.sub_fail}; failures {len(result.failures)}, "
      f"errors {len(result.errors)}")
ok = (result.testsRun == 6 and Counting.sub_pass == 24 and Counting.sub_fail == 0
      and result.wasSuccessful())
sys.exit(0 if ok else 1)
