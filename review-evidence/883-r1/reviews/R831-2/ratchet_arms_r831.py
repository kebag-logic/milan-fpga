#!/usr/bin/env python3
"""Run only check_cpp_idiom.py's construct-rule selftest group on one copy.

Usage: python3 -I ratchet_arms_r831.py <path/to/check_cpp_idiom.py>

Calls `_selftest_ratchets` (the group holding the multi-declarator arms),
which needs no git checkout, prints its tally and exits 1 on any FAIL. Used
on a head copy (control) and on copies with an earlier `_DECL_TEXT` planted.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("cci", sys.argv[1])
cci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cci)
ck = cci._Tally()
cci._selftest_ratchets(ck)
print(f"ratchet group: {ck.checks} checks: {ck.checks - ck.failures} PASS, {ck.failures} FAIL")
sys.exit(1 if ck.failures else 0)
