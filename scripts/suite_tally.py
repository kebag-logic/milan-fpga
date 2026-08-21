#!/usr/bin/env python3
"""Tally the check counts out of a Verilator sweep's per-suite logs.

    python3 scripts/suite_tally.py <logdir>... [--quiet]
        [--expect-suite-root <tb/verilator>]

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

    **A check count that is absent, unparseable, or measures nothing is an
    UNKNOWN, and an unknown must never look like agreement.  It fails the
    sweep, loudly.**

Two detectors implement that:

* ``NOCOUNT``  -- a suite that measured nothing: either no tally line could be
  read at all, or the tallies sum to zero checks and zero failures.  Silence is
  not zero, and neither is a reported zero.
* ``UNPARSED`` -- a line that *looks* like a tally (a number next to the word
  "checks") but matches none of the known shapes.  This is the one that keeps a
  **new** suite honest without anyone having to remember: invent a sixth
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
from collections import Counter
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

    ``matched`` is redundant today -- ``scan()`` only ever adds non-negative
    captures, so an empty ``matched`` already implies zero and zero.  It is kept
    because the two conditions are different *claims* (nothing was said / what
    was said measured nothing) and a future shape with a signed or defaulted
    capture would separate them again.  Do not simplify it away on the grounds
    that it is dead; it is load-bearing documentation of the rule.
    """
    return (not matched) or (checks == 0 and failures == 0)


def campaign_accounted_for(text):
    """Did one campaign log account for itself? (reason, ok).

    A campaign has exactly two honest outcomes: it measured something, or it
    declared that it ran nothing.  Anything else -- a summary reworded past the
    shapes, or a tally that adds up to zero -- means its checks silently leave
    the headline.

    This exists because the suite that owns the campaign also prints an
    unconditional floor of its own, and that floor clears ``NOCOUNT`` for the
    whole suite.  The floor is what makes the suite countable; it is also what
    took away the backstop the campaign used to have.  So the campaign is
    checked on its own, in its own log, against the SAME recognisers the sweep
    uses -- a second hand-rolled matcher in a Makefile is how the two come to
    disagree, and a first cut of this guard did exactly that: it rejected four
    tally shapes this file reads perfectly well, and accepted ``0 pass, 0 fail``.
    """
    checks, failures, matched, _unparsed, skipped = scan(text)
    #! `and not matched`, NOT `if skipped:`. A marker excuses a campaign only
    #! when nothing else tallied. Otherwise a log carrying a marker anywhere
    #! would pass regardless of what else it printed -- the same "a suite
    #! declares its own way out" that is_nocount() takes `skipped` purely in
    #! order to refuse.
    #!
    #! It does NOT catch a marker beside a REWORDED tally: that line matches no
    #! shape, so `matched` is empty and the log is indistinguishable from a
    #! plain skip. Nothing here can see it. Unreachable today because
    #! require_tsn_gen() prints the marker and exits immediately, so a campaign
    #! cannot both skip and report -- and pinned by a self-test case so that
    #! stays a decision rather than a surprise.
    if skipped and not matched:
        return ("declared a skip: " + skipped[0], True)
    if not matched:
        return ("printed no tally in any shape scripts/suite_tally.py reads",
                False)
    if checks == 0 and failures == 0:
        return (f"tallied {checks} checks and {failures} failures -- it ran, "
                f"and measured nothing", False)
    return (f"tallied {checks} checks, {failures} failures", True)


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
    import contextlib
    import io
    import tempfile
    for name, logs, want_rc, want_out, why in (
        ("e2e-lone-marker", {"a": "SUITE-SKIP: campaign (dep absent)\n"}, 1,
         "SKIPPED  a: campaign (dep absent)",
         "a suite whose only content is a marker still fails the sweep, and "
         "the skip is LISTED"),
        ("e2e-marker-plus-real-tally",
         {"a": "SUITE-SKIP: campaign (dep absent)\n2 checks: 2 PASS, 0 FAIL\n"}, 0,
         "checks: 2   in-suite failures: 0",
         "...and passes once it reports what it DID run, at the right total"),
        ("e2e-one-silent-suite-among-many",
         {"a": "checks: 100   failures: 0\n", "b": "building...\n"}, 1,
         "checks: 100   in-suite failures: 0",
         "one silent suite fails the sweep even beside a healthy one"),
        #! UNPARSED is NOCOUNT's co-equal detector and its wiring to the exit
        #! code was the half nothing pinned: 419 checks could be dropped beside
        #! a healthy tally with the self-test green.
        ("e2e-unparsed-beside-a-real-tally",
         {"a": "checks: 100   failures: 0\ntotal 419 checks OK\n"}, 1,
         "UNPARSED a: total 419 checks OK",
         "an unreadable tally fails the sweep even when another one parsed"),
        ("e2e-empty-logdir", {}, 2, None,
         "no logs at all is an unknown, not a zero-check pass"),
        #! the two causes of NOCOUNT get DIFFERENT advice, and that is worth
        #! pinning: telling someone whose suite printed "0 pass, 0 fail" to
        #! "print one of the shapes" sends them to fix what they already did.
        ("e2e-nocount-says-which-cause-silence",
         {"a": "building...\n"}, 1, "printed no tally line at all",
         "a silent suite is told it printed nothing"),
        #! the FAILURES half of the headline. Every other case expects
        #! "failures: 0", so hard-coding that half survived them all -- and the
        #! docstring claims both halves are protected.
        ("e2e-failures-reach-the-headline",
         {"a": "checks: 100   failures: 3\n"}, 0,
         "checks: 100   in-suite failures: 3",
         "the failure count is carried, not just the check count"),
        ("e2e-nocount-says-which-cause-zero",
         {"a": "== campaign: 0 pass, 0 fail ==\n"}, 1,
         "measured 0 checks and 0 failures",
         "...and a zero-tallying one is told the opposite, not the same thing"),
    ):
        with tempfile.TemporaryDirectory() as td:
            for stem, text in logs.items():
                Path(td, stem + ".log").write_text(text)
            import io
            import contextlib
            buf = io.StringIO()
            #! NOT --quiet: the per-suite table has its own NO COUNT flag, and
            #! it used to carry a private copy of the predicate that disagreed
            #! with the verdict. Rendering it here is what keeps them one.
            #! stderr too: e2e-empty-logdir writes a usage line there, and a
            #! reader seeing an alarm above the OK list learns to ignore alarms
            with contextlib.redirect_stdout(buf), \
                    contextlib.redirect_stderr(io.StringIO()):
                rc = main([sys.argv[0], td])
        out = buf.getvalue()
        ok = rc == want_rc
        #! the table and the verdict must agree, always
        if want_rc == 1 and logs and ("NOCOUNT" in out) != ("NO COUNT" in out):
            ok = False
            why += "  [table flag and verdict DISAGREE]"
        #! ...and the OUTPUT itself is asserted, not just the exit code. The
        #! headline numbers and the skip listing were both mutable in silence:
        #! the listing is the declared marker's ONLY remaining purpose, so a
        #! deleted listing makes the marker pointless without failing anything.
        if want_out is not None and want_out not in out:
            ok = False
            why += f"  [expected {want_out!r} in the output]"
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} rc={rc}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected rc={want_rc}")

    # --- SHARDED INVENTORY --------------------------------------------------
    # Parallel workers are only faster if their union is still the serial
    # sweep. These cases reach the exact multi-directory CLI the aggregate
    # GitHub job uses and prove that omissions, additions, and double ownership
    # all fail before a combined headline can be trusted.
    for name, layout, want_rc, want_out, why in (
        ("inventory-exact",
         ({"left": {"a": "checks: 2   failures: 0\n"},
                    "right": {"b": "checks: 3   failures: 0\n"}},
          ("a", "b")),
         0, "checks: 5   in-suite failures: 0",
         "disjoint shard logs reproduce the serial tally"),
        ("inventory-missing",
         ({"left": {"a": "checks: 2   failures: 0\n"}}, ("a", "b")),
         1, "MISSING     b", "one omitted serial suite fails closed"),
        ("inventory-unexpected",
         ({"left": {"a": "checks: 2   failures: 0\n",
                     "c": "checks: 4   failures: 0\n"}}, ("a", "b")),
         1, "UNEXPECTED  c", "a stale or invented suite log fails closed"),
        ("inventory-duplicate",
         ({"left": {"a": "checks: 2   failures: 0\n"},
                    "right": {"a": "checks: 2   failures: 0\n",
                              "b": "checks: 3   failures: 0\n"}},
          ("a", "b")),
         1, "DUPLICATE   a", "two workers owning one suite fails closed"),
    ):
        log_layout, expected = layout
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            suite_root = base / "suites"
            suite_root.mkdir()
            for suite in expected:
                suite_dir = suite_root / suite
                suite_dir.mkdir()
                (suite_dir / "Makefile").write_text("all:\n\t@true\n")
            logdirs = []
            for dirname, logs in log_layout.items():
                logdir = base / dirname
                logdir.mkdir()
                logdirs.append(logdir)
                for stem, body in logs.items():
                    (logdir / f"{stem}.log").write_text(body)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), \
                    contextlib.redirect_stderr(io.StringIO()):
                rc = main([sys.argv[0], *map(str, logdirs), "--quiet",
                           "--expect-suite-root", str(suite_root)])
        out = buf.getvalue()
        ok = rc == want_rc and want_out in out
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} rc={rc}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected rc={want_rc} and {want_out!r} in output")

    # --- the CAMPAIGN GUARD --------------------------------------------------
    # The guard protects 164 checks that nothing else protects, because the
    # suite's own 2-check floor lifts it clear of NOCOUNT. A review pointed out
    # the guard itself had no test: revert it and reword the summary, and both
    # the self-test and the sweep stay green.
    for name, text, want_ok, why in (
        ("guard-real-tally",
         "== AAF campaign (tsn-gen driven): 164 pass, 0 fail, 0 known gaps ==\n",
         True, "a campaign that measured something is accounted for"),
        ("guard-other-shapes",
         "aaf: 164 checks, 0 failures\n", True,
         "...in ANY shape the sweep reads, not just the campaign one"),
        ("guard-declared-skip",
         "SUITE-SKIP: AAF campaign (tsn-gen absent)\n", True,
         "...and so is one that declared it ran nothing"),
        ("guard-reworded-summary",
         "== AAF campaign: 164 ok / 0 bad ==\n", False,
         "a summary past every shape is NOT, though it looks fine to a human"),
        ("guard-zero-tally",
         "== AAF campaign (tsn-gen driven): 0 pass, 0 fail, 0 known gaps ==\n",
         False, "neither is one that ran and measured nothing"),
        ("guard-silence", "building...\n", False, "nor silence"),
        #! a marker excuses a campaign only when it is the WHOLE story. A
        #! review found a bare `if skipped:` here, so a log carrying a marker
        #! ANYWHERE passed regardless of what else it printed.
        #!
        #! THE LIMIT, pinned rather than hidden: a marker beside a REWORDED
        #! tally still passes, because a reworded line is indistinguishable
        #! from ordinary log chatter -- there is nothing for the parser to see.
        #! Unreachable today (require_tsn_gen prints the marker and exits, so a
        #! campaign cannot both skip and report), and the case is here so that
        #! stops being an accident.
        ("guard-skip-beside-a-reword-is-the-known-limit",
         "SUITE-SKIP: half of it was skipped\n== c: 164 ok / 0 bad ==\n",
         True, "a reworded line is invisible to the parser -- documented limit"),
        ("guard-skip-does-not-launder-a-zero",
         "SUITE-SKIP: half of it was skipped\n== c: 0 pass, 0 fail ==\n",
         False, "...nor a tally that measured nothing"),
        ("guard-skip-plus-real-tally-is-fine",
         "SUITE-SKIP: one part skipped\n== c: 164 pass, 0 fail ==\n",
         True, "...but a real tally beside a marker is still accounted for"),
    ):
        reason, got = campaign_accounted_for(text)
        ok = got == want_ok
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} "
              f"accounted={got}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected accounted={want_ok}, got reason: {reason}")

    # --- the guard's CLI, and --quiet ----------------------------------------
    # campaign_accounted_for() is tested above as a FUNCTION. Its command-line
    # wiring is the half the Makefile actually consumes, and a review disabled
    # the guard two ways -- `if ok:` -> `if True:`, and `return 1` -> `return 0`
    # -- with every case above still green. The second is the nastier: the
    # alarm still PRINTS, so the suite log looks alarming and make passes.
    #
    # --quiet is here for the same reason: run_all_suites.sh:173 is the only
    # production caller and passes it, and returning 0 early under --quiet
    # survived everything.
    for name, argv_extra, text, want_rc, want_out, why in (
        ("cli-guard-accepts",
         ["--campaign-guard"], "== c: 164 pass, 0 fail ==\n", 0, None,
         "the guard's CLI passes a campaign that measured something"),
        ("cli-guard-rejects",
         ["--campaign-guard"], "== c: 164 ok / 0 bad ==\n", 1,
         "CAMPAIGN UNACCOUNTED FOR",
         "...and REJECTS one that did not, with a non-zero exit"),
        ("cli-guard-rejects-zero",
         ["--campaign-guard"], "== c: 0 pass, 0 fail ==\n", 1,
         "measured nothing",
         "...including one that ran and measured nothing"),
    ):
        with tempfile.TemporaryDirectory() as td:
            log = Path(td, "campaign.out")
            log.write_text(text)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), \
                    contextlib.redirect_stderr(io.StringIO()):
                rc = main([sys.argv[0], *argv_extra, str(log)])
        out = buf.getvalue()
        ok = rc == want_rc and (want_out is None or want_out in out)
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} rc={rc}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected rc={want_rc}"
                  + (f" and {want_out!r} in the output" if want_out else ""))

    with tempfile.TemporaryDirectory() as td:
        Path(td, "a.log").write_text("building...\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            rc = main([sys.argv[0], td, "--quiet"])
    ok = rc == 1
    print(f"  {'ok  ' if ok else 'FAIL'} {'quiet-still-gates':<32} rc={rc}  "
          f"-- --quiet is the mode CI uses, and it still fails a silent suite")
    if not ok:
        bad += 1
        print("       expected rc=1")

    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv[1:]:
        return selftest()
    if "--campaign-guard" in argv[1:]:
        #! One campaign log, checked against the same recognisers the sweep
        #! uses. See campaign_accounted_for().
        path = argv[argv.index("--campaign-guard") + 1]
        reason, ok = campaign_accounted_for(
            Path(path).read_text(errors="replace"))
        if ok:
            return 0
        print(f"CAMPAIGN UNACCOUNTED FOR -- {reason}.")
        print("  Its checks would leave the sweep's headline in silence: the")
        print("  suite prints an unconditional floor of its own, so this does")
        print("  NOT show up as a NOCOUNT. Print a tally in one of the shapes")
        print("  in scripts/suite_tally.py, or a SUITE-SKIP: line saying why")
        print("  the campaign ran nothing.")
        return 1
    quiet = False
    expected_root = None
    logdir_args = []
    pos = 1
    while pos < len(argv):
        arg = argv[pos]
        if arg == "--quiet":
            quiet = True
            pos += 1
        elif arg == "--expect-suite-root":
            if pos + 1 >= len(argv):
                sys.stderr.write("suite_tally: --expect-suite-root needs a path\n")
                return 2
            expected_root = Path(argv[pos + 1])
            pos += 2
        elif arg.startswith("-"):
            sys.stderr.write(f"suite_tally: unknown option {arg}\n")
            return 2
        else:
            logdir_args.append(arg)
            pos += 1
    if not logdir_args:
        sys.stderr.write("usage: suite_tally.py <logdir>... [--quiet] "
                         "[--expect-suite-root <dir>]\n")
        return 2

    logdirs = [Path(arg) for arg in logdir_args]
    logs = sorted((log for logdir in logdirs for log in logdir.glob("*.log")),
                  key=lambda path: (path.stem, str(path)))
    if not logs:
        rendered = ", ".join(map(str, logdirs))
        sys.stderr.write(f"suite_tally: no *.log under {rendered} -- nothing to "
                         f"tally, which is an unknown, not a zero\n")
        return 2

    inventory_findings = []
    counts = Counter(log.stem for log in logs)
    for suite, count in sorted(counts.items()):
        if count > 1:
            inventory_findings.append(
                ("DUPLICATE", suite, f"appears in {count} shard log directories"))
    if expected_root is not None:
        try:
            expected = {
                path.name for path in expected_root.iterdir()
                if path.is_dir() and (path / "Makefile").is_file()
            }
        except OSError as exc:
            sys.stderr.write(f"suite_tally: cannot read expected suite root "
                             f"{expected_root}: {exc}\n")
            return 2
        if not expected:
            sys.stderr.write(f"suite_tally: no suite Makefiles under expected "
                             f"root {expected_root}\n")
            return 2
        actual = set(counts)
        inventory_findings.extend(
            ("MISSING", suite, "no shard produced its log")
            for suite in sorted(expected - actual)
        )
        inventory_findings.extend(
            ("UNEXPECTED", suite, "not present in the serial suite inventory")
            for suite in sorted(actual - expected)
        )

    total_checks = total_fails = 0
    nocount = []
    zero_tally = set()
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
            if matched:
                zero_tally.add(suite)
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

    if inventory_findings:
        print()
        print("ACCOUNTING FAILURE -- shard logs do not equal the serial suite "
              "inventory:")
        for finding, suite, reason in inventory_findings:
            print(f"  {finding:<11} {suite}: {reason}")
        print("  The combined check total is not exhaustive and must not be "
              "treated as the serial sweep.")

    #! Printed ALWAYS, including --quiet, and above the accounting verdicts:
    #! the total being smaller than usual is the thing a reader most needs
    #! told, and it is not a failure so nothing else would say it.
    if skip_findings:
        print()
        print(f"declared skips ({len(skip_findings)}) -- these ran NOTHING and "
              f"contribute 0 to the total above:")
        for suite, reason in skip_findings:
            print(f"  SKIPPED  {suite}: {reason}")

    bad = bool(inventory_findings)
    if nocount:
        bad = True
        print()
        print("ACCOUNTING FAILURE -- nothing was measured by "
              f"{len(nocount)} suite log(s):")
        #! The two causes need different advice. Telling someone whose suite
        #! printed "0 pass, 0 fail" to "print one of the shapes" sends them to
        #! fix the thing they already did right.
        for suite in nocount:
            zero = suite in zero_tally
            why = ("reported a tally, but it measured 0 checks and 0 failures"
                   if zero else "printed no tally line at all")
            print(f"  NOCOUNT  {suite}: {why}")
        print("  A suite that measured nothing is an UNKNOWN, not agreement.")
        print("  If it printed no tally: make it print one of the shapes in")
        print("  scripts/suite_tally.py. If it tallied zero: make it assert")
        print("  something, or say why it ran nothing with a SUITE-SKIP: line")
        print("  AND still report the checks it did run.")
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
