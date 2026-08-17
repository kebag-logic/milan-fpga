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

THE THIRD STATE: SKIPPED
------------------------
A campaign whose *optional* dependency is absent has run nothing, and that is
neither a measurement nor silence -- it is a **fourth** thing, and collapsing it
into any of the other three loses information:

* counting it as ``0 pass, 0 fail`` makes it look like a campaign that ran and
  found nothing to check.  The suite total then reads as complete when it is
  not, and the sweep goes quiet -- the exact false green this file exists to
  prevent, arrived at from the other direction.
* leaving it silent makes it a ``NOCOUNT``, which is loud and correct but
  unactionable: CI cannot pass on a machine without the optional tool.

So a suite may declare the skip explicitly, with a ``SUITE-SKIP:`` line.  That
is not a tally and adds nothing to the total; it only says *why* the total is
smaller, and it keeps the suite out of ``NOCOUNT``.  Every skip is listed in
this tool's output, so a campaign that silently stopped running cannot hide
behind a green sweep.

The limit of this, stated honestly: a suite that prints ``SUITE-SKIP:`` and
*then* runs checks whose summary matches no shape has those checks dropped
without a ``NOCOUNT``.  ``UNPARSED`` still covers that when the summary looks
tally-shaped.  The marker is deliberately an explicit, anchored token rather
than prose so it cannot be tripped by a log merely mentioning a skip.

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
# An explicit declaration that an optional campaign did not run.  Anchored and
# all-caps on purpose: it must be something a suite states deliberately, never
# something prose can trip.  "campaign skipped", "SKIP: ..." and friends appear
# in ordinary log chatter and are NOT this.
SKIP_DECLARED = re.compile(r"^\s*SUITE-SKIP:\s*(\S.*?)\s*$")

# NOTE the limit of this net, honestly: it only catches vocabularies that
# overlap the ones above. A suite inventing wording that shares NOTHING with
# them slips past it -- and is then caught by the NOCOUNT detector instead,
# which is why both exist. That is exactly how tsn_fuzz was found: it printed
# "222 pass, 0 fail" per campaign and the word "checks" nowhere, so it read as
# a silent zero for as long as the sweep only grepped for `checks:`.


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


# --- self-test ---------------------------------------------------------------
# A gate that cannot fail is not a gate. These cases exist so the two loud
# verdicts are demonstrated rather than assumed -- run `suite_tally.py
# --selftest`. Every shape below was copied from a real suite log.
SELFTEST = [
    # (name, log text, expected checks, expected failures, expected unparsed?)
    ("n-checks-pass-fail",  "73 checks: 70 PASS, 3 FAIL\n",          73, 3, False),
    ("labelled-pass-fail",  "pcm_playback: 40 checks: 40 PASS, 0 FAIL\n", 40, 0, False),
    ("labelled",            "aaf: 27 checks, 2 failures\n",          27, 2, False),
    ("eqeq",                "== 43 checks, 1 failures ==\n",         43, 1, False),
    ("result-suffix",       "31 checks, 0 failures, RESULT: PASS\n", 31, 0, False),
    ("cbs-mismatches",      "cycle checks: 1000   mismatches: 4\n", 1000, 4, False),
    ("canonical",           "checks: 228   failures: 5\n",          228, 5, False),
    ("clkvalid-decorated",  "== clkvalid: checks: 74  failures: 0 ==\n", 74, 0, False),
    ("extras-after",        "checks: 26   failures: 0   (data=4 adp=3 frames)\n", 26, 0, False),
    ("multi-executable",    "checks: 10   failures: 0\nchecks: 5   failures: 1\n", 15, 1, False),
    ("tsn-fuzz-campaign",   "== ADP discovery field campaign: 222 pass, 0 fail, 0 known gaps ==\n"
                            "== co-sim: 42 pass, 1 fail ==\n",      264, 1, False),
    # ORDERING GUARD: this line contains BOTH "73 checks: ... " and
    # "73 PASS, 0 FAIL". If campaign-pass-fail were tried first, or if both
    # shapes were allowed to match, it would count 146 instead of 73.
    ("no-double-count",     "73 checks: 73 PASS, 0 FAIL\n",          73, 0, False),
    # prose that merely contains the word must NOT be read as a tally
    ("prose-not-a-tally",   "[15] new descriptor spot checks\n"
                            "== KL_mac_rmon_events (no MAC checks) ==\n",  0, 0, False),
    # THE POINT OF THE GATE: a shape nobody taught it must be LOUD, never zero
    ("novel-shape",         "assertions=419 errors=0\ntotal 419 checks OK\n", 0, 0, True),
    # A declared skip is not a tally: it must add NOTHING to the total. The
    # regression this guards is a skip note worded as "0 pass, 0 fail", which
    # the campaign shape WOULD match and which would read as a campaign that
    # ran and checked nothing.
    ("skip-adds-nothing",   "SUITE-SKIP: aaf campaign (tsn-gen absent)\n"
                            "1 checks: 1 PASS, 0 FAIL\n",                1, 0, False),
    # ...and a skip must not launder an unparseable tally sitting beside it
    ("skip-does-not-hide-unparsed",
                            "SUITE-SKIP: aaf campaign (tsn-gen absent)\n"
                            "total 419 checks OK\n",                     0, 0, True),
    # prose about skipping is NOT the marker -- the marker is deliberate
    ("skip-prose-is-not-a-marker",
                            "  ..... campaign skipped (tsn-gen absent)\n"
                            "  SKIP: tsn-gen not found\n",               0, 0, False),
]


def selftest():
    bad = 0
    for name, text, want_c, want_f, want_unparsed in SELFTEST:
        c, f, matched, unparsed, _skipped = scan(text)
        got_unparsed = bool(unparsed)
        ok = (c == want_c and f == want_f and got_unparsed == want_unparsed)
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<22} "
              f"checks={c} failures={f} unparsed={got_unparsed}")
        if not ok:
            bad += 1
            print(f"       expected checks={want_c} failures={want_f} "
                  f"unparsed={want_unparsed}")

    # An empty log is a NOCOUNT, not a zero -- the whole reason this file exists.
    c, f, matched, unparsed, skipped = scan("Verilating...\nbuild finished\n")
    if matched or skipped:
        print("  FAIL nocount               a silent log produced a tally")
        bad += 1
    else:
        print("  ok   nocount               a silent log yields NO tally "
              "(-> NOCOUNT, not 0)")

    # ...and a log that ONLY declares a skip is the third state: still no
    # tally, but it explained itself, so it is SKIPPED rather than NOCOUNT.
    c, f, matched, unparsed, skipped = scan(
        "== AAF campaign ==\nSUITE-SKIP: aaf campaign (tsn-gen absent)\n")
    if matched or c or not skipped:
        print("  FAIL skipped               a skip-only log did not read as SKIPPED")
        bad += 1
    else:
        print("  ok   skipped               a skip-only log is SKIPPED, "
              "contributes 0, and is NOT a NOCOUNT")

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
        rows.append((suite, c, f, len(matched), len(skipped)))
        #! a declared skip keeps a suite out of NOCOUNT, and ONLY that: it adds
        #! no checks, and it is reported below so a campaign that quietly
        #! stopped running cannot hide behind a green sweep
        if not matched and not skipped:
            nocount.append(suite)
        for line in unparsed:
            unparsed_findings.append((suite, line))
        for reason in skipped:
            skip_findings.append((suite, reason))

    if not quiet:
        print("suite                        checks   failures  tallies")
        for suite, c, f, n, s in rows:
            flag = "  <- NO COUNT" if (n == 0 and s == 0) else ""
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
