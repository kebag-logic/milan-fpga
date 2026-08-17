#!/usr/bin/env python3
"""Tally the check counts out of a Verilator sweep's per-suite logs.

    python3 scripts/suite_tally.py <logdir> [--quiet]

``<logdir>`` is the directory ``scripts/run_all_suites.sh`` writes
``<suite>.log`` into (default ``.suite-logs/``).  This script is the *only*
thing that turns those logs into the headline "checks:" figure, so that the
rule below lives in exactly one place.

WHY THIS EXISTS
---------------
The sweep used to total the checks with ``grep -o 'checks: *[0-9]*'``.  Suites
do not all print that string: the tree emits **five** different summary shapes,
all listed below.  Measured over a full 57-suite sweep on 2026-07-28, that grep
saw **zero** from 29 of the 57 suite logs and only part of two more (``aecp``,
``milan_dp``, which run several executables in a mix of shapes) -- a shortfall
of **37 784 checks**, against a headline the project quotes as its evidence
that a change is safe.  A suite contributing zero was indistinguishable from a
suite with no assertions at all.  The defect was demonstrated by adding 66
assertions to a suite and watching the printed total not move.

So the rule this file enforces is the sweep's own version of *a structural zero
is not a measurement*:

    **An unparseable or absent check count is an UNKNOWN, and an unknown must
    never look like agreement.  It fails the sweep, loudly.**

Two detectors implement that:

* ``NOCOUNT``  -- a suite log from which no tally line could be read at all.
  Silence is not zero.
* ``UNPARSED`` -- a line that *looks* like a tally (a number next to the word
  "checks") but matches none of the known shapes.  This is the one that keeps a
  **new** suite honest without anyone having to remember: invent a seventh
  summary shape and the sweep stops, rather than quietly dropping your checks
  on the floor.  It fires even when the suite's *other* executables did parse,
  which is the case a per-log "did anything match?" test would miss.

Both are accounting verdicts.  Neither changes whether a suite passed --
``run_all_suites.sh`` still gates that on the suite's exit status alone.

DECLARED SKIPS ARE REPORTING, NOT A VERDICT
-------------------------------------------
A campaign whose *optional* dependency is absent has run nothing.  A suite may
say so with a ``SUITE-SKIP:`` line, and every one is listed in this tool's
output so a reader can see **why** a total is smaller than usual.

That is *all* it does.  A declared skip:

* adds nothing to the total -- it is not a tally and must never carry pass/fail
  numbers.  A skip worded ``0 pass, 0 fail`` matches the campaign shape below
  and would read as a campaign that ran and checked nothing;
* **does not excuse a suite from producing a count.**  A log whose only content
  is a skip marker is still a ``NOCOUNT``.

That last rule is the one worth defending, because the obvious design gets it
wrong.  Letting a marker suppress ``NOCOUNT`` sounds harmless and is not: it
makes the verdict a suite's own to declare.  Measured on a real 50-log sweep,
replacing one suite's log with the single line
``SUITE-SKIP: shaper_core campaign (optional dependency absent)`` moved the
total from 2 113 139 to 591 512 -- **72% of the sweep gone, exit 0** -- with
nothing but a listing line to show for it.  A suite that must skip should still
report the checks it *did* run; ``tb/verilator/tsn_fuzz`` prints its
unconditional traceability check for exactly that reason.

The marker is an anchored, all-caps token rather than prose so a log merely
mentioning a skip cannot trip it, and it still faces the ``UNPARSED`` net so it
cannot be used as a hiding place for a tally.

THE SHAPES
----------
Ordered, first match wins.  Order matters: ``N checks: P PASS, F FAIL`` must be
tried before ``checks: N``, because the number *after* the colon in that shape
is the PASS count, not the total.  The old grep read exactly that number, which
was right only for as long as those suites had zero failures -- a check that
could not fail.
"""

import re
import sys
from pathlib import Path

# --- the recognised summary shapes -------------------------------------------
#
# Each entry: (name, compiled regex, checks-group, failures-group).
# Every regex must capture BOTH the total and the failure count, so the two
# halves of the headline can never drift apart.
SHAPES = (
    # "73 checks: 73 PASS, 0 FAIL"                 aaf_latency_taps, eth_tx_reset,
    # "pcm_playback: 40 checks: 40 PASS, 0 FAIL"   link_guard, pcm_playback
    #
    # MUST come first -- see the module docstring.
    ("n-checks-pass-fail",
     re.compile(r"(?<![\w.])(\d+)\s+checks:\s*(\d+)\s+PASS,\s*(\d+)\s+FAIL"), 1, 3),

    # "== ADP discovery field campaign (tsn-gen driven): 222 pass, 0 fail, 0
    #  known gaps =="   and   "== co-sim: 42 pass, 0 fail =="
    #
    # tsn_fuzz's own vocabulary: it prints one line per campaign and, by
    # design, NO grand total (tb/verilator/tsn_fuzz/README.md explains why), so
    # its five campaign lines sum to the suite. "known gaps" are documented
    # gaps, not failures, and are deliberately not added to the failure count.
    #
    # MUST come after n-checks-pass-fail: "73 checks: 73 PASS, 0 FAIL" also
    # contains "73 PASS, 0 FAIL", and first-match-wins is what stops the six
    # suites using that shape from being counted twice.
    ("campaign-pass-fail",
     re.compile(r"(?<![\w.])(\d+)\s+pass,\s*(\d+)\s+fail", re.IGNORECASE), 1, 2),

    # "aaf: 27 checks, 0 failures"                 the commonest label form
    # "== 43 checks, 0 failures =="                lwsrp family
    # "31 checks, 0 failures, RESULT: PASS"        chmap_render, lat_history_ring
    ("n-checks-m-failures",
     re.compile(r"(?<![\w.])(\d+)\s+checks,\s*(\d+)\s+failures"), 1, 2),

    # "cycle checks: 129407   mismatches: 0"       cbs -- calls them mismatches
    ("cycle-checks-mismatches",
     re.compile(r"cycle\s+checks:\s*(\d+)\s+mismatches:\s*(\d+)"), 1, 2),

    # "checks: 228   failures: 0"                  the shape the old grep knew
    # "== clkvalid: checks: 74  failures: 0 =="    same, decorated
    ("checks-colon-failures-colon",
     re.compile(r"checks:\s*(\d+)\s+failures:\s*(\d+)"), 1, 2),
)

# A line that looks like it is reporting a check tally.  Anything matching this
# and none of SHAPES is an UNPARSED finding.  Kept deliberately tight so log
# prose ("[15] new descriptor spot checks", "no MAC checks") does not trip it:
# the number must be directly adjacent to the word.
TALLY_SHAPED = re.compile(
    r"(?<![\w.])\d+\s+checks\b"      # "27 checks", "73 checks:"
    r"|"
    r"\bchecks\s*[:=]\s*\d"          # "checks: 27", "checks=27"
    r"|"
    r"(?<![\w.])\d+\s+assertions?\b" # "419 assertions"
    r"|"
    r"(?<![\w.])\d+\s+pass(ed)?\s*,", # "222 pass," -- tsn_fuzz's campaign form
    re.IGNORECASE,
)
# NOTE the limit of this net, honestly: it only catches vocabularies that
# overlap the ones above. A suite inventing wording that shares NOTHING with
# them slips past it -- and is then caught by the NOCOUNT detector instead,
# which is why both exist. That is exactly how tsn_fuzz was found: it printed
# "222 pass, 0 fail" per campaign and the word "checks" nowhere, so it read as
# a silent zero for as long as the sweep only grepped for `checks:`.

# An explicit declaration that an optional campaign did not run.  Anchored and
# all-caps on purpose: it must be something a suite states deliberately, never
# something prose can trip.  "campaign skipped", "SKIP: ..." and friends appear
# in ordinary log chatter and are NOT this.  Purely informational -- see the
# module docstring for why it is deliberately not a verdict.
SKIP_DECLARED = re.compile(r"^\s*SUITE-SKIP:\s*(\S.*?)\s*$")


def scan(text):
    """Return (checks, failures, matched, unparsed, skipped) for one log."""
    checks = failures = 0
    matched = []
    unparsed = []
    skipped = []
    for raw in text.splitlines():
        line = raw.rstrip()
        sk = SKIP_DECLARED.match(line)
        if sk:
            skipped.append(sk.group(1))
            #! The marker is not a tally, so it never reaches SHAPES and cannot
            #! inject counts. It DOES still face the UNPARSED net, or it would
            #! be a hiding place: "SUITE-SKIP: ... dropping 419 checks" would
            #! otherwise pass in silence.
            if TALLY_SHAPED.search(line):
                unparsed.append(line.strip())
            continue
        for name, rx, cg, fg in SHAPES:
            m = rx.search(line)
            if m:
                c, f = int(m.group(cg)), int(m.group(fg))
                checks += c
                failures += f
                matched.append((name, c, f, line.strip()))
                break
        else:
            if TALLY_SHAPED.search(line):
                unparsed.append(line.strip())
    return checks, failures, matched, unparsed, skipped


def is_nocount(checks, failures, matched, skipped):
    """Is this log an UNKNOWN? Yes unless something was actually measured.

    Two ways to measure nothing, and both are unknowns:

    * no tally line at all -- silence;
    * tallies that sum to **zero checks and zero failures**.  ``0 pass, 0 fail``
      is a shape the parser accepts, so without this a suite could clear the
      gate while reporting that it had checked nothing.  That is the file's own
      motto turned on the instrument: a structural zero is not a measurement.

    ``skipped`` is taken and deliberately **ignored**.  The parameter is here so
    that the one place tempted to consult it says out loud that it does not:
    a suite does not get to declare its own way out of ``NOCOUNT``.  A review
    found this decision sitting inline in ``main()`` where ``--selftest`` could
    not reach it, so breaking it was silent; it is a named function now for no
    other reason than that a self-test can call it.
    """
    return (not matched) or (checks == 0 and failures == 0)


# --- self-test ---------------------------------------------------------------
# A gate that cannot fail is not a gate. These cases exist so the two loud
# verdicts are demonstrated rather than assumed -- run `suite_tally.py
# --selftest`. Every shape below was copied from a real suite log.
SELFTEST = [
    # (name, log text, expected checks, expected failures, expected unparsed?,
    #  expected number of declared skips)
    #
    #! The skip count is asserted, not ignored. A first cut of these cases left
    #! it out, and a review showed two of them then pinned nothing: a case whose
    #! only expectations are "0 checks, 0 failures, no unparsed" holds whether
    #! or not the marker regex matches prose, so widening SKIP_DECLARED to match
    #! "campaign skipped" sailed straight through the self-test.
    ("n-checks-pass-fail",  "73 checks: 70 PASS, 3 FAIL\n",          73, 3, False, 0),
    ("labelled-pass-fail",  "pcm_playback: 40 checks: 40 PASS, 0 FAIL\n", 40, 0, False, 0),
    ("labelled",            "aaf: 27 checks, 2 failures\n",          27, 2, False, 0),
    ("eqeq",                "== 43 checks, 1 failures ==\n",         43, 1, False, 0),
    ("result-suffix",       "31 checks, 0 failures, RESULT: PASS\n", 31, 0, False, 0),
    ("cbs-mismatches",      "cycle checks: 1000   mismatches: 4\n", 1000, 4, False, 0),
    ("canonical",           "checks: 228   failures: 5\n",          228, 5, False, 0),
    ("clkvalid-decorated",  "== clkvalid: checks: 74  failures: 0 ==\n", 74, 0, False, 0),
    ("extras-after",        "checks: 26   failures: 0   (data=4 adp=3 frames)\n", 26, 0, False, 0),
    ("multi-executable",    "checks: 10   failures: 0\nchecks: 5   failures: 1\n", 15, 1, False, 0),
    ("tsn-fuzz-campaign",   "== ADP discovery field campaign: 222 pass, 0 fail, 0 known gaps ==\n"
                            "== co-sim: 42 pass, 1 fail ==\n",      264, 1, False, 0),
    # ORDERING GUARD: this line contains BOTH "73 checks: ... " and
    # "73 PASS, 0 FAIL". If campaign-pass-fail were tried first, or if both
    # shapes were allowed to match, it would count 146 instead of 73.
    ("no-double-count",     "73 checks: 73 PASS, 0 FAIL\n",          73, 0, False, 0),
    # prose that merely contains the word must NOT be read as a tally
    ("prose-not-a-tally",   "[15] new descriptor spot checks\n"
                            "== KL_mac_rmon_events (no MAC checks) ==\n",  0, 0, False, 0),
    # THE POINT OF THE GATE: a shape nobody taught it must be LOUD, never zero
    ("novel-shape",         "assertions=419 errors=0\ntotal 419 checks OK\n", 0, 0, True, 0),
    # A declared skip is not a tally: it must add NOTHING to the total, and the
    # numbers must be the ones from the REAL tally beside it. The skip line here
    # deliberately carries a tally of its own, because a skip line with no
    # numbers cannot tell "excluded from the shapes" from "scanned like any
    # other line" -- a review deleted that exclusion and the first cut of this
    # case did not notice.
    ("skip-adds-nothing",   "SUITE-SKIP: aaf campaign not run -- 164 checks: 164 PASS, 0 FAIL\n"
                            "1 checks: 1 PASS, 0 FAIL\n",                1, 0, True, 1),
    # ...and a skip must not launder an unparseable tally sitting beside it
    ("skip-does-not-hide-unparsed",
                            "SUITE-SKIP: aaf campaign (tsn-gen absent)\n"
                            "total 419 checks OK\n",                     0, 0, True, 1),
    # ...nor be a hiding place itself: a marker that smuggles a tally is UNPARSED
    ("skip-line-is-not-a-hiding-place",
                            "SUITE-SKIP: absent, dropping 419 checks\n",  0, 0, True, 1),
    # prose about skipping is NOT the marker. The skip count is what pins this:
    # without it the case holds whether or not SKIP_DECLARED matches prose.
    ("skip-prose-is-not-a-marker",
                            "  ..... campaign skipped (tsn-gen absent)\n"
                            "  SKIP: tsn-gen not found\n",               0, 0, False, 0),
    # the marker is anchored and case-sensitive: neither of these is one
    ("skip-marker-must-start-the-line",
                            "[info] SUITE-SKIP: aaf campaign absent\n"
                            "suite-skip: aaf campaign absent\n",         0, 0, False, 0),
]


def selftest():
    bad = 0
    for name, text, want_c, want_f, want_unparsed, want_skips in SELFTEST:
        c, f, matched, unparsed, skipped = scan(text)
        got_unparsed = bool(unparsed)
        ok = (c == want_c and f == want_f and got_unparsed == want_unparsed
              and len(skipped) == want_skips)
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} "
              f"checks={c} failures={f} unparsed={got_unparsed} "
              f"skips={len(skipped)}")
        if not ok:
            bad += 1
            print(f"       expected checks={want_c} failures={want_f} "
                  f"unparsed={want_unparsed} skips={want_skips}")

    # --- the CLASSIFICATION, not just the parse ------------------------------
    # These call is_nocount() directly. The parse cases above cannot reach it,
    # and a review showed that breaking the decision -- letting a declared skip
    # excuse a suite from counting -- passed the whole self-test in silence.
    for name, text, want_nocount, why in (
        ("nocount-silent", "Verilating...\nbuild finished\n", True,
         "a silent log is an UNKNOWN, not a zero"),
        ("nocount-skip-only",
         "== AAF campaign ==\nSUITE-SKIP: aaf campaign (tsn-gen absent)\n", True,
         "a DECLARED skip does not excuse a suite from counting"),
        ("nocount-cleared-by-a-real-tally",
         "SUITE-SKIP: aaf campaign (tsn-gen absent)\n1 checks: 1 PASS, 0 FAIL\n",
         False, "...but a real tally beside it does"),
        ("nocount-all-zero-tally",
         "campaign skipped: 0 pass, 0 fail (dependency absent)\n", True,
         "a tally that measured NOTHING is an unknown, not agreement"),
    ):
        c, f, matched, unparsed, skipped = scan(text)
        got = is_nocount(c, f, matched, skipped)
        ok = got == want_nocount
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} "
              f"nocount={got}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected nocount={want_nocount}")

    # --- END TO END, through main() ------------------------------------------
    # The cases above test the parser and the decision. Neither reaches the CALL
    # -- a review changed `if nc:` back to the rejected predicate and every case
    # above still passed while the real gate went from rc=1 to rc=0 on a
    # lone-marker log. So these run the whole tool over a temporary log dir and
    # assert the EXIT CODE, which is what CI actually consumes.
    import tempfile
    for name, logs, want_rc, why in (
        ("e2e-lone-marker", {"a": "SUITE-SKIP: campaign (dep absent)\n"}, 1,
         "a suite whose only content is a marker still fails the sweep"),
        ("e2e-marker-plus-real-tally",
         {"a": "SUITE-SKIP: campaign (dep absent)\n2 checks: 2 PASS, 0 FAIL\n"}, 0,
         "...and passes once it reports what it DID run"),
        ("e2e-one-silent-suite-among-many",
         {"a": "checks: 100   failures: 0\n", "b": "building...\n"}, 1,
         "one silent suite fails the sweep even beside a healthy one"),
    ):
        with tempfile.TemporaryDirectory() as td:
            for stem, text in logs.items():
                Path(td, stem + ".log").write_text(text)
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = main([sys.argv[0], td, "--quiet"])
        ok = rc == want_rc
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} rc={rc}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected rc={want_rc}")

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv[1:]:
        return selftest()
    args = [a for a in argv[1:] if not a.startswith("-")]
    quiet = "--quiet" in argv[1:]
    if len(args) != 1:
        sys.stderr.write("usage: suite_tally.py <logdir> [--quiet]\n")
        return 2

    logdir = Path(args[0])
    logs = sorted(logdir.glob("*.log"))
    if not logs:
        sys.stderr.write(f"suite_tally: no *.log under {logdir} -- nothing to "
                         f"tally, which is an unknown, not a zero\n")
        return 2

    total_checks = total_fails = 0
    nocount = []
    unparsed_findings = []
    skip_findings = []
    rows = []

    for log in logs:
        suite = log.stem
        text = log.read_text(errors="replace")
        c, f, matched, unparsed, skipped = scan(text)
        total_checks += c
        total_fails += f
        nc = is_nocount(c, f, matched, skipped)
        rows.append((suite, c, f, len(matched), len(skipped), nc))
        if nc:
            nocount.append(suite)
        for line in unparsed:
            unparsed_findings.append((suite, line))
        for reason in skipped:
            skip_findings.append((suite, reason))

    if not quiet:
        print("suite                        checks   failures  tallies")
        for suite, c, f, n, s, nc in rows:
            #! ONE predicate, shared with the verdict below. This
            #! line used to carry its own copy and they disagreed
            #! on exactly the case this tool is about.
            flag = "  <- NO COUNT" if nc else ""
            if s:
                flag += f"  <- {s} SKIPPED"
            print(f"{suite:<28} {c:>8} {f:>10} {n:>8}{flag}")
        print()

    print(f"checks: {total_checks}   in-suite failures: {total_fails}")

    #! Printed ALWAYS, including --quiet, and above the accounting verdicts:
    #! the total being smaller than usual is the thing a reader most needs
    #! told, and it is not a failure so nothing else would say it.
    if skip_findings:
        print()
        print(f"declared skips ({len(skip_findings)}) -- these ran NOTHING and "
              f"contribute 0 to the total above:")
        for suite, reason in skip_findings:
            print(f"  SKIPPED  {suite}: {reason}")

    bad = False
    if nocount:
        bad = True
        print()
        print("ACCOUNTING FAILURE -- no check count could be read from "
              f"{len(nocount)} suite log(s):")
        for suite in nocount:
            print(f"  NOCOUNT  {suite}")
        print("  A suite that reports no count is an UNKNOWN, not a zero. Make")
        print("  it print one of the shapes in scripts/suite_tally.py.")
    if unparsed_findings:
        bad = True
        print()
        print("ACCOUNTING FAILURE -- line(s) that look like a check tally but "
              "match no known shape:")
        for suite, line in unparsed_findings:
            print(f"  UNPARSED {suite}: {line}")
        print("  These checks would have been silently dropped from the total.")
        print("  Add the shape to SHAPES in scripts/suite_tally.py, or make the")
        print("  suite print an existing one.")

    if bad:
        print()
        print("The check total above is INCOMPLETE and must not be quoted.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
