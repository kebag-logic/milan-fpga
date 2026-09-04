#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
Self-test for the campaign's field grader (`Campaign.grade_tx`) and the one
rule it shares with the probe generator (`tsn_model.kind_conflict`).

This does NOT touch the DUT, Verilator or tsn-gen: it drives grade_tx with
synthetic one-field models and hand-built frames, so it runs everywhere the
campaigns themselves skip. That matters, because the defects it guards are
invisible to the campaigns by construction.

WHAT IT GUARDS. grade_tx dispatches on the constraint kind a tsn-gen model
declares. Before issue #146 the chain ended after `values`, so a field
constrained any other way was simply not graded -- no failure, no skip line,
no movement in the tally. The check did not exist. That is not hypothetical:
an Announce `flags` pin was once replaced with `mask: [0x003F]` on the claim
that the harness would catch a regression, and it would not have.

And before issue #151 the chain took the FIRST kind it met. The generator
that builds the stimulus does not: upstream merges `value` into `values`,
prefers that set over `range`, and applies `mask` only to an unconstrained
draw (packet_builder.cpp::pickValue). A field declaring `value: 3` beside
`values: [1, 2, 3]` was therefore legal as {1, 2, 3} to the producer and
"must equal 3" to the grader: a false RED blaming a conformant DUT, the
moment any model declared two kinds. None does today, so nothing red ever
pointed at it.

So the properties below are the point of this file:
  1. `mask:` is graded, and it grades what a mask actually asserts.
  2. Any kind grade_tx does NOT know fails CLOSED, naming the field and kind.
  3. A field declaring MORE THAN ONE kind is REFUSED, fail-closed, with one
     message naming the field and every kind, by the same predicate in
     grade_tx, `Message.legal()` and `Message.illegal()`, so the three
     readers cannot disagree again. Single-kind fields grade as before.
  4. The refusal cases can fail. The predicate is mutated in place (bypassed,
     made to name nothing, made to name only one kind) and every refusal
     case must go red under each mutant while every single-kind case stays
     green. A test that keeps passing when the thing it guards is removed
     was never testing it, and (4) is what separates this file's proof from
     an argument.
"""

import contextlib
import io
import os
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cosim import Report                                    # noqa: E402
import fuzz_ptp                                             # noqa: E402
import tsn_model                                            # noqa: E402


class OneFieldModel:
    """The whole surface grade_tx and extract_fields touch: `.fields`."""

    def __init__(self, fields):
        self._fields = fields

    @property
    def fields(self) -> list[tuple[str, int, dict[str, object]]]:
        """The `.fields` surface tsn_model.Message presents, as given."""
        return self._fields


def grade_model(model: OneFieldModel | tsn_model.Message,
                pdu: Sequence[int]) -> tuple[int, int, str, str]:
    """Run grade_tx over `model` and return (npass, nfail, what, detail).

    `what`/`detail` are the first recorded failure, or empty strings. The
    inner Report prints a banner and a `[FAIL]` line for every case that is
    SUPPOSED to fail. Those are this file's expected results, not its
    verdict, so stdout is swallowed while the grader runs -- otherwise the
    log reads as a wall of failures and `suite_tally.py` would be scanning
    our fixtures. Only the per-case verdict below is printed.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        rep = Report("grade_tx self-test", verbose=False)
        camp = fuzz_ptp.Campaign.__new__(fuzz_ptp.Campaign)  # no cosim socket
        camp.rep = rep
        frame = bytes(14) + bytes(pdu)      # extract_fields reads from byte 14
        camp.grade_tx(model, frame, "t")
    what = detail = ""
    if rep.failures:
        _sec, what, detail = rep.failures[0]
    return rep.npass, rep.nfail, what, detail


def grade(field_bits: int, constraint: dict[str, object],
          pdu: Sequence[int],
          field: str = "f") -> tuple[int, int, str, str]:
    """Grade one synthetic field; see grade_model for the return shape."""
    return grade_model(OneFieldModel([(field, field_bits, constraint)]), pdu)


def message_model(field: str, bits: int,
                  constraint: dict[str, object]) -> tsn_model.Message:
    """A tsn_model.Message holding one synthetic field, built without a YAML.

    The whole surface legal()/illegal() touch is `.vars`; the loader itself
    is exercised separately by loader_checks().
    """
    m = tsn_model.Message.__new__(tsn_model.Message)
    m.path = "<synthetic>"
    m.vars = {field: (bits, constraint)}
    m.order = [field]
    return m


def refusal_of(fn: Callable[[str], object], field: str) -> str | None:
    """str() of the ValueError `fn(field)` raises, or None when it does not."""
    try:
        fn(field)
    except ValueError as exc:
        return str(exc)
    return None


CASES = [
    # (name, bits, constraint, pdu, want_pass, want_fail, msg_must_contain)
    ("mask: no undefined bit set",
     8, {"mask": [0x0F]}, [0x05], 1, 0, ""),
    ("mask: an undefined bit IS set",
     8, {"mask": [0x0F]}, [0x85], 0, 1, "undefined=0x80"),
    ("mask: every defined bit set is still legal",
     8, {"mask": [0x0F]}, [0x0F], 1, 0, ""),

    # REAL WIDTHS. Every mask in the live models is 16, 32 or 64 bits wide
    # (talker/listener_capabilities 16, controller_capabilities 32,
    # tlv_length_and_mode 16, acquire/lock_entity_flags 32, msrp_flags 64) and
    # every undefined bit that matters sits ABOVE bit 7. An 8-bit fixture set
    # cannot see a grader that truncates -- `got & ~m & 0xFF` passes all three
    # cases above while waving an undefined bit through five of the six real
    # fields. Each case below puts the offending bit high enough that any
    # narrower mask arithmetic misses it.
    ("mask 16b talker_capabilities: legal",
     16, {"mask": [0x803F]}, [0x80, 0x3F], 1, 0, ""),
    ("mask 16b: undefined bit 14, above the low byte",
     16, {"mask": [0x803F]}, [0x40, 0x00], 0, 1, "undefined=0x4000"),
    ("mask 32b acquire_entity_flags: legal",
     32, {"mask": [0xC0000000]}, [0xC0, 0, 0, 0], 1, 0, ""),
    ("mask 32b: undefined bit 29, above 16 bits",
     32, {"mask": [0xC0000000]}, [0x20, 0, 0, 0], 0, 1, "undefined=0x20000000"),
    ("mask 64b msrp_flags: legal",
     64, {"mask": [0xF800000000000000]},
     [0xF8, 0, 0, 0, 0, 0, 0, 0], 1, 0, ""),
    ("mask 64b: undefined bit 58, above 32 bits",
     64, {"mask": [0xF800000000000000]},
     [0x04, 0, 0, 0, 0, 0, 0, 0], 0, 1, "undefined=0x400000000000000"),

    ("unknown kind fails closed",
     8, {"regex": ["x"]}, [0x00], 0, 1, "ungradeable constraint kind"),
    ("unknown kind names the field",
     8, {"regex": ["x"]}, [0x00], 0, 1, "t.f"),
    # #146 asks the failure to name the field AND THE KIND. Without this the
    # message could drop the kind and both needles above would still be met.
    ("unknown kind names the KIND itself",
     8, {"regex": ["x"]}, [0x00], 0, 1, "regex"),

    # Every single-kind case, positive and negative: the refusal below must
    # leave these exactly as they were. They are also the specificity control
    # for the mutants at the end of the file, which must not move them.
    ("value: matching", 8, {"value": 0x42}, [0x42], 1, 0, ""),
    ("value: mismatching", 8, {"value": 0x42}, [0x43], 0, 1, "got=67"),
    ("range: inside", 8, {"range": [1, 9]}, [5], 1, 0, ""),
    ("range: outside", 8, {"range": [1, 9]}, [200], 0, 1, "got=200"),
    ("values: legal", 8, {"values": [1, 2]}, [2], 1, 0, ""),
    ("values: illegal", 8, {"values": [1, 2]}, [3], 0, 1, "got=3"),
    # An absent `expected:` block must keep SKIPPING. Failing it here would
    # redden every legitimately unconstrained field (sequence_id, clock
    # identities), so the fail-closed rule deliberately stops at non-empty
    # constraints. The shrinking-tally problem that causes is issue #150.
    ("no constraint at all still skips",
     8, {}, [0xFF], 0, 0, ""),
]

#: the field name every refusal case uses, so the message can be required to
#: carry it. Distinct from the one-letter "f" above: a one-letter needle would
#: be found inside almost any message, which is no test of naming at all.
DUAL = "dual_fld"

# A field declaring MORE THAN ONE constraint kind is refused: 0 pass, 1 fail,
# and the refusal message (the DETAIL, which is the predicate's own words, not
# the check label that carries the field name anyway) names the field and
# every kind, as the sorted parenthesised list.
#
# Every frame below is LEGAL under the old first-kind-wins dispatch, except the
# second case, which is the issue's own scenario. That choice is what gives the
# "refusal bypassed" mutant a clean pass/fail flip to be caught by, instead of
# two failures that differ only in wording.
REFUSALS = [
    # (name, bits, constraint, pdu, needles the DETAIL must contain)
    ("value+values: frame carries the value (first-kind-wins passed it)",
     8, {"value": 3, "values": [1, 2, 3]}, [3],
     (DUAL, "2 constraint kinds", "(value, values)")),
    ("value+values: frame carries 1, legal upstream (first-kind-wins blamed "
     "the DUT)",
     8, {"value": 3, "values": [1, 2, 3]}, [1],
     (DUAL, "(value, values)")),
    ("value+range",
     8, {"value": 5, "range": [1, 9]}, [5], (DUAL, "(range, value)")),
    ("values+mask",
     8, {"values": [1, 2], "mask": [0x0F]}, [2], (DUAL, "(mask, values)")),
    ("value+mask",
     8, {"value": 3, "mask": [0x0F]}, [3], (DUAL, "(mask, value)")),
    ("values+range",
     8, {"values": [1, 2], "range": [0, 255]}, [1], (DUAL, "(range, values)")),
    ("range+mask",
     8, {"range": [1, 9], "mask": [0xFF]}, [5], (DUAL, "(mask, range)")),
    ("three kinds: value+values+range",
     8, {"value": 3, "values": [1, 2, 3], "range": [0, 9]}, [3],
     (DUAL, "3 constraint kinds", "(range, value, values)")),
    ("all four kinds",
     8, {"value": 3, "values": [1, 2, 3], "range": [0, 9], "mask": [0x0F]},
     [3], (DUAL, "4 constraint kinds", "(mask, range, value, values)")),
    # A key outside the grammar beside a known kind. #146's rule could not see
    # it: `value` dispatched and `regex` was ignored in silence. One kind per
    # field can, and names the foreign key in the message.
    ("known kind beside an unknown one: value+regex",
     8, {"value": 3, "regex": ["x"]}, [3], (DUAL, "(regex, value)")),
    # A real width, so the refusal is not an 8-bit fixture artefact.
    ("16b values+mask",
     16, {"values": [0x803F], "mask": [0x803F]}, [0x80, 0x3F],
     (DUAL, "(mask, values)")),
]

# Mutants of the shared predicate. Each is installed in place of
# tsn_model.kind_conflict and must be DETECTED by every refusal case while
# leaving every single-kind case untouched. The three are the three ways the
# refusal could rot: it stops firing, it fires without saying what it refused,
# or it names the field but not all of the kinds.
MUTANTS = [
    ("refusal bypassed: predicate returns None",
     lambda name, con: None),
    ("refusal names neither the field nor the kinds",
     lambda name, con: "refused" if len(con) > 1 else None),
    ("refusal names the field and only the FIRST kind",
     lambda name, con: ("field %s declares constraint kinds (%s)"
                        % (name, sorted(con)[0])) if len(con) > 1 else None),
]

# A floor, for the same reason the campaigns carry one: an emptied table would
# print "0 checks: 0 PASS, 0 FAIL" and exit 0, which reads as success. It is
# the exact tally this file produces today; adding a check raises it.
MIN_CHECKS = 54


class Expect:
    """What one graded case must produce.

    The tally it must reach, the words the message must carry, and where those
    words are looked for: `detail_only` requires them in the DETAIL alone rather
    than in "what | detail", which is what the refusal cases assert because the
    detail is the predicate's own words and the check label carries the field
    name anyway. Four facts about one expectation, so they travel as one.
    """

    def __init__(self, want_p, want_f, needles=(), detail_only=False):
        self.want_p = want_p
        self.want_f = want_f
        self.needles = tuple(needles)
        self.detail_only = detail_only


def run_case(bits: int, con: dict[str, object], pdu: Sequence[int],
             expect: Expect, field: str = "f") -> tuple[bool, str]:
    """Grade one synthetic field and judge it against `expect`: (ok, note)."""
    npass, nfail, what, detail = grade(bits, con, pdu, field)
    hay = detail if expect.detail_only else "%s | %s" % (what, detail)
    missing = [n for n in expect.needles if n not in hay]
    ok = npass == expect.want_p and nfail == expect.want_f and not missing
    note = " pass=%d/%d fail=%d/%d" % (npass, expect.want_p,
                                       nfail, expect.want_f)
    if expect.needles:
        note += ("  needles=%r %s"
                 % (expect.needles, "found" if not missing
                    else "MISSING %r in %r" % (missing, hay)))
    return ok, note


def case_ok(case: tuple[str, int, dict[str, object], list[int],
                        int, int, str]) -> bool:
    """True when one CASES row still grades to its recorded tally."""
    name, bits, con, pdu, want_p, want_f, needle = case
    return run_case(bits, con, pdu,
                    Expect(want_p, want_f, (needle,) if needle else ()))[0]


def refusal_ok(case: tuple[str, int, dict[str, object], list[int],
                           tuple[str, ...]]) -> bool:
    """True when one REFUSALS row is still refused, by name and by kind."""
    name, bits, con, pdu, needles = case
    return run_case(bits, con, pdu,
                    Expect(0, 1, needles, detail_only=True), DUAL)[0]


class Tally:
    def __init__(self):
        self.total = 0
        self.bad = 0

    def check(self, name: str, ok: bool, note: str = "") -> bool:
        """Record and print one verdict; the count is MIN_CHECKS' floor."""
        self.total += 1
        if not ok:
            self.bad += 1
        print("  [%s] %-62s%s" % ("ok  " if ok else "FAIL", name, note))
        return ok


def parity_checks(t: Tally) -> None:
    """(3) legal()/illegal() refuse with the SAME message grade_tx reports.

    One predicate means one message: the detail grade_tx records and the
    ValueError the two probe generators raise must be equal, case by case.
    """
    for name, bits, con, pdu, _needles in REFUSALS:
        _p, _f, _what, detail = grade(bits, con, pdu, DUAL)
        m = message_model(DUAL, bits, con)
        got_legal = refusal_of(m.legal, DUAL)
        got_illegal = refusal_of(m.illegal, DUAL)
        ok = bool(detail) and got_legal == detail and got_illegal == detail
        t.check("same refusal from grade_tx, legal(), illegal(): %s" % name, ok,
                "" if ok else "  grade_tx=%r legal=%r illegal=%r"
                % (detail, got_legal, got_illegal))


def shared_predicate_checks(t: Tally) -> None:
    """(3) all three readers route through tsn_model.kind_conflict.

    Replace the predicate with a sentinel that refuses everything and watch a
    SINGLE-kind field be refused by all three with the sentinel's words. That
    proves each reader asks the predicate before it dispatches, for every
    constrained field, rather than keeping a private copy of the rule (which
    equal messages alone could not distinguish from one shared rule).
    """
    saved = tsn_model.kind_conflict
    tsn_model.kind_conflict = lambda name, con: "SENTINEL %s" % name
    try:
        _p, nfail, _what, detail = grade(8, {"value": 0x42}, [0x42], "solo")
        t.check("grade_tx asks tsn_model.kind_conflict before it dispatches",
                nfail == 1 and detail == "SENTINEL solo",
                "" if detail == "SENTINEL solo" else "  got %r" % detail)
        m = message_model("solo", 8, {"value": 0x42})
        got = refusal_of(m.legal, "solo")
        t.check("legal() asks tsn_model.kind_conflict before it dispatches",
                got == "SENTINEL solo", "" if got == "SENTINEL solo"
                else "  got %r" % got)
        got = refusal_of(m.illegal, "solo")
        t.check("illegal() asks tsn_model.kind_conflict before it dispatches",
                got == "SENTINEL solo", "" if got == "SENTINEL solo"
                else "  got %r" % got)
    finally:
        tsn_model.kind_conflict = saved


def loader_checks(t: Tally) -> None:
    """(3) through the real loader: a YAML model is refused after parsing.

    The synthetic cases hand the predicate a dict. This closes the one way
    they could be vacuous: a loader that normalised `value` into `values`
    (upstream's documented reading of `value`) would leave the predicate
    nothing to refuse, and every case above would still pass. So a model in
    the real grammar, with a single-kind field beside a dual-kind one, goes
    through tsn_model.Message(); the first must grade exactly as before and
    the second must be refused by all three readers.
    """
    doc = {
        "service": "grader_selftest",
        "vars": [
            {"var": "solo", "size": 8, "expected": {"value": 3}},
            {"var": DUAL, "size": 8,
             "expected": {"value": 3, "values": [1, 2, 3]}},
        ],
        "entities": [{"entity": "E", "interfaces": [
            {"interface": "I", "vars": [{"var_ref": "solo"},
                                         {"var_ref": DUAL}]}]}],
    }
    fd, path = tempfile.mkstemp(suffix=".yaml", prefix="grade_tx_selftest_")
    try:
        with os.fdopen(fd, "w") as fh:
            yaml.safe_dump(doc, fh)
        m = tsn_model.Message(path)
        t.check("loaded model: the single-kind field grades legal() as before",
                m.legal("solo") == [3], "  got %r" % m.legal("solo"))
        needles = (DUAL, "(value, values)")
        got = refusal_of(m.legal, DUAL)
        t.check("loaded model: legal() refuses the dual-kind field by name",
                got is not None and all(n in got for n in needles),
                "  got %r" % got)
        got = refusal_of(m.illegal, DUAL)
        t.check("loaded model: illegal() refuses the dual-kind field by name",
                got is not None and all(n in got for n in needles),
                "  got %r" % got)
        npass, nfail, what, detail = grade_model(m, [3, 3])
        ok = (npass, nfail) == (1, 1) and all(n in detail for n in needles)
        t.check("loaded model: grade_tx grades solo and refuses dual_fld",
                ok, " pass=%d/1 fail=%d/1 %s" % (npass, nfail, detail))
    finally:
        Path(path).unlink()


def mutation_checks(t: Tally) -> None:
    """(4) every mutant of the predicate is caught, and only by the refusals."""
    for mname, mutant in MUTANTS:
        saved = tsn_model.kind_conflict
        tsn_model.kind_conflict = mutant
        try:
            survivors = [c[0] for c in REFUSALS if refusal_ok(c)]
            broken = [c[0] for c in CASES if not case_ok(c)]
        finally:
            tsn_model.kind_conflict = saved
        t.check("mutant '%s' goes red in every refusal case (%d/%d)"
                % (mname, len(REFUSALS) - len(survivors), len(REFUSALS)),
                not survivors, "" if not survivors
                else "  SURVIVED: %r" % survivors)
        t.check("mutant '%s' leaves every single-kind case green (%d/%d)"
                % (mname, len(CASES) - len(broken), len(CASES)),
                not broken, "" if not broken else "  BROKE: %r" % broken)


def main() -> int:
    """Run every arm; exit 1 on a red case or on a tally below MIN_CHECKS."""
    t = Tally()
    print("[single-kind and unknown-kind fields]")
    for name, bits, con, pdu, want_p, want_f, needle in CASES:
        ok, note = run_case(bits, con, pdu,
                            Expect(want_p, want_f,
                                   (needle,) if needle else ()))
        t.check(name, ok, note)
    print("[a field declaring more than one kind is refused]")
    for name, bits, con, pdu, needles in REFUSALS:
        ok, note = run_case(bits, con, pdu,
                            Expect(0, 1, needles, detail_only=True), DUAL)
        t.check(name, ok, note)
    print("[one predicate for grade_tx, legal() and illegal()]")
    parity_checks(t)
    shared_predicate_checks(t)
    loader_checks(t)
    print("[the refusal cases can fail: mutants of the predicate]")
    mutation_checks(t)

    if t.total < MIN_CHECKS:
        print("grade_tx self-test: FAIL, only %d checks, expected at least %d"
              % (t.total, MIN_CHECKS))
        return 1
    print("\ngrade_tx self-test: %d checks: %d PASS, %d FAIL"
          % (t.total, t.total - t.bad, t.bad))
    return 1 if t.bad else 0


if __name__ == "__main__":
    sys.exit(main())
