#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Self-test for the campaign's field grader (`Campaign.grade_tx`).

This does NOT touch the DUT, Verilator or tsn-gen: it drives grade_tx with
synthetic one-field models and hand-built frames, so it runs everywhere the
campaigns themselves skip. That matters, because the defect it guards is
invisible to the campaigns by construction.

WHAT IT GUARDS. grade_tx dispatches on the constraint kind a tsn-gen model
declares. Before issue #146 the chain ended after `values`, so a field
constrained any other way was simply not graded -- no failure, no skip line,
no movement in the tally. The check did not exist. That is not hypothetical:
an Announce `flags` pin was once replaced with `mask: [0x003F]` on the claim
that the harness would catch a regression, and it would not have.

So the two properties below are the point of this file:
  1. `mask:` is graded, and it grades what a mask actually asserts.
  2. Any kind grade_tx does NOT know fails CLOSED, naming the field and kind.

A grader that silently ignores what it does not understand cannot be trusted
to mean anything, so (2) is the durable half: it holds for constraint kinds
nobody has invented yet, while (1) only covers the one we know about.
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cosim import Report                                    # noqa: E402
import fuzz_ptp                                             # noqa: E402


class OneFieldModel:
    """The whole surface grade_tx and extract_fields touch: `.fields`."""

    def __init__(self, fields):
        self._fields = fields

    @property
    def fields(self):
        return self._fields


def grade(field_bits, constraint, pdu):
    """Grade one synthetic field and return (npass, nfail, first message).

    The inner Report prints a banner and a `[FAIL]` line for every case that
    is SUPPOSED to fail. Those are this file's expected results, not its
    verdict, so stdout is swallowed while the grader runs -- otherwise the log
    reads as a wall of failures and `suite_tally.py` would be scanning our
    fixtures. Only the per-case verdict below is printed.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        rep = Report("grade_tx self-test", verbose=False)
        camp = fuzz_ptp.Campaign.__new__(fuzz_ptp.Campaign)  # no cosim socket
        camp.rep = rep
        frame = bytes(14) + bytes(pdu)      # extract_fields reads from byte 14
        camp.grade_tx(OneFieldModel([("f", field_bits, constraint)]),
                      frame, "t")
    msg = ""
    if rep.failures:
        _sec, what, detail = rep.failures[0]
        msg = "%s | %s" % (what, detail)
    return rep.npass, rep.nfail, msg


CASES = [
    # (name, bits, constraint, pdu, want_pass, want_fail, msg_must_contain)
    ("mask: no undefined bit set",
     8, {"mask": [0x0F]}, [0x05], 1, 0, ""),
    ("mask: an undefined bit IS set",
     8, {"mask": [0x0F]}, [0x85], 0, 1, "undefined=0x80"),
    ("mask: every defined bit set is still legal",
     8, {"mask": [0x0F]}, [0x0F], 1, 0, ""),
    ("unknown kind fails closed",
     8, {"regex": ["x"]}, [0x00], 0, 1, "ungradeable constraint kind"),
    ("unknown kind names the field",
     8, {"regex": ["x"]}, [0x00], 0, 1, "t.f"),
    ("value: matching", 8, {"value": 0x42}, [0x42], 1, 0, ""),
    ("value: mismatching", 8, {"value": 0x42}, [0x43], 0, 1, "got=67"),
    ("range: inside", 8, {"range": [1, 9]}, [5], 1, 0, ""),
    ("range: outside", 8, {"range": [1, 9]}, [200], 0, 1, "got=200"),
    ("values: legal", 8, {"values": [1, 2]}, [2], 1, 0, ""),
    ("values: illegal", 8, {"values": [1, 2]}, [3], 0, 1, "got=3"),
    # An absent `expected:` block must keep SKIPPING. Failing it here would
    # redden every legitimately unconstrained field (sequence_id, clock
    # identities), so the fail-closed rule deliberately stops at non-empty
    # constraints. The shrinking-tally problem that causes is tracked apart.
    ("no constraint at all still skips",
     8, {}, [0xFF], 0, 0, ""),
]


def main():
    bad = 0
    for name, bits, con, pdu, want_p, want_f, needle in CASES:
        npass, nfail, msg = grade(bits, con, pdu)
        ok = (npass == want_p and nfail == want_f
              and (not needle or needle in msg))
        if not ok:
            bad += 1
        print("  [%s] %-46s pass=%d/%d fail=%d/%d%s"
              % ("ok  " if ok else "FAIL", name, npass, want_p, nfail, want_f,
                 "" if not needle else
                 ("  needle=%r %s" % (needle, "found" if needle in msg
                                      else "MISSING in %r" % msg))))

    print("\ngrade_tx self-test: %d checks: %d PASS, %d FAIL"
          % (len(CASES), len(CASES) - bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
