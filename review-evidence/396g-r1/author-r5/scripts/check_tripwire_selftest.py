#!/usr/bin/env python3
"""The tripwire copy's self-test log: only the balance arm may trip; it plants a lossy and an unbalanced reading.

Usage: python3 -I check_tripwire_selftest.py <self-test log>

Exit 0 when the log ran every arm, exactly one arm errored, that arm is
test_audio_slip_totals_balance_the_bytes and its error is the tripwire's;
1 otherwise.
"""
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
ran = re.search(r"^Ran (\d+) tests", text, re.M)
problems = re.findall(r"^(FAIL|ERROR): (\w+)", text, re.M)
ok = (ran is not None and problems == [("ERROR", "test_audio_slip_totals_balance_the_bytes")]
      and "RuntimeError: TRIPWIRE: " in text)
print(f"ran {ran.group(1) if ran else '?'} arms; problems {problems}; only the balance arm, which plants the defect, trips: {ok}")
sys.exit(0 if ok else 1)
