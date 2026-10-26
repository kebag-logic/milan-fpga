#!/usr/bin/env python3
"""Follow-up classification cases for the #396 audio grader.

Usage: python3 -I grader_probe2.py <path-to-tb/tools> <path-to-grader_probe.py dir>
Prints one line per case: <id> <observed DUT events> (with the arms of the
first probe planted at both ends, so a PASS/FAIL/NOT RUN verdict is real).
"""
import json
import sys

sys.argv = [sys.argv[0], sys.argv[1]]
sys.path.insert(0, __import__("os").path.dirname(__file__))
import grader_probe as gp  # noqa: E402  (re-runs probe 1 output; filtered below)

F, C, AT = gp.F, gp.C, gp.AT
cases = {
    # A one-sample hold (dup) followed k samples later by a skip that restores phase.
    "dup-then-skip-k1": [('shift', AT, -1), ('shift', AT + 1, 1)],
    "dup-then-skip-k5": [('shift', AT, -1), ('shift', AT + 5, 1)],
    # A skip followed at once by a dup.
    "skip-then-dup-k1": [('shift', AT, 1), ('shift', AT + 1, -1)],
    # Tag-bit flip on one channel only (no partner carries this channel's word).
    "tag-flip-nonreciprocal": [('xor', AT, 2, 0x100000)],
    # Static channel swap for the whole capture, with the arms planted on channel 1.
    "static-swap-0-2": [('swap', 0, F, 0, 2)],
    # Static swap that includes the planted flip channel.
    "static-swap-1-3": [('swap', 0, F, 1, 3)],
}
print("--- follow-up ---")
for name, ops in cases.items():
    v, d, dut = gp.grade(F, C, ops)
    summary = sorted({(e[0], e[1], e[2], e[3], e[4], e[5]) for e in dut})[:6]
    print(f"Q-{name} {json.dumps([v, d.get('why'), len(dut), summary])}")
