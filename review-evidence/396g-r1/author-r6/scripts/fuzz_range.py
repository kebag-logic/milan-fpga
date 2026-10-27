#!/usr/bin/env python3
"""Run the in-tree property fuzz's generator and check over a wider seed range.

Usage: python3 -B fuzz_range.py <tb/tools dir> <first seed> <count>

Uses `_fuzz_units` and `_fuzz_check` of the planner under <tb/tools dir>
unchanged, at the 16384 frames the self-test arm uses. Prints one VIOLATION
line per seed the check rejects, then a TALLY of verdicts and of the
allowances the check needed ("clean", "masked", "cancelled"), and a REACH
histogram: for each event on each channel it changes, the samples from its
sample to the nearest DUT event the grader lists there (`_fuzz_reach`), when
not zero; the check allows up to 63.
"""
import collections
import sys
import unittest

sys.path.insert(0, sys.argv[1])
import torture_campaign as m  # noqa: E402

BASES = [getattr(m, n) for n in ("_CounterLawChecks", "_StreamingLicenceChecks", "_PlanContractChecks",
                                 "_AreaContractChecks", "_ReleasePlanChecks", "_ReleaseSoakChecks",
                                 "_ReleaseGateChecks", "_ConcurrencyChecks")]
T = type("T", tuple(BASES) + (unittest.TestCase,), {})
t = T("test_audio_compositions_never_pass_and_list_every_event")
first, count = int(sys.argv[2]), int(sys.argv[3])
tally, reach = collections.Counter(), collections.Counter()
for seed in range(first, first + count):
    units = t._fuzz_units(16384, seed)
    try:
        verdict, allowed = t._fuzz_check(16384, units)
    except AssertionError as error:
        print("VIOLATION", seed, str(error)[:600], flush=True)
        tally["violation"] += 1
        continue
    tally[verdict] += 1
    for allowance in allowed:
        tally["allow " + allowance] += 1
    _, detail, _ = t._sweep_grade(16384, [event for unit in units for event in unit[4]])
    for _, at, channels, _, _ in units:
        for channel in channels:
            near = min((t._fuzz_reach(e, at) for e in detail["events"]
                        if e["channel"] == channel and e["attribution"] == "dut"), default=None)
            if near:
                reach[near if near <= m.AUDIO_GUARD_FRAMES else "over 63 (allowed)"] += 1
print("TALLY", first, dict(sorted(tally.items())), flush=True)
print("REACH", first, dict(sorted(reach.items(), key=str)), flush=True)
