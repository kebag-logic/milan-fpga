#!/usr/bin/env python3
"""Instrument a SCRATCH copy of sw/builder/test_builder.py (argv[1]) for the
gate-1b probe. Two env-guarded edits only; with neither variable set the
instrumented file behaves as the original:
  R413_STOP_AFTER_BASELINE=1  return right after the shipping firmware's
                              assert_boot_contract() (all source rules plus
                              the resolver on the firmware under test)
  R413_FORCE_FORGET=1         the forget-on-call rule (never keep a slot)"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
a = ("    baseline_census_verdict = assert_boot_contract(\n"
     "        firmware_source, docs_source, csr_source)\n")
assert s.count(a) == 1
s = s.replace(a, a + "    if __import__('os').environ.get('R413_STOP_AFTER_BASELINE'):\n"
     "        print('R413 PROBE: shipping-firmware gate 1b ACCEPTED; ran=',\n"
     "              baseline_census_verdict.get('ran'), 'kept=',\n"
     "              (baseline_census_verdict.get('resolved') or {}).get('kept'))\n"
     "        return\n")
b = '        kept = frozenset() if broken else frozenset({"aem_loaded"})\n'
assert s.count(b) == 1
s = s.replace(b, '        kept = frozenset() if (broken or __import__("os").environ.get("R413_FORCE_FORGET")) else frozenset({"aem_loaded"})\n')
p.write_text(s); print("instrumented", p)
