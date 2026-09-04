#!/usr/bin/env python3
"""Tally the check counts out of a Verilator sweep's per-suite logs.

    python3 scripts/suite_tally.py <logdir>... [--quiet]
        [--expect-suite-root <tb/verilator>]
    python3 scripts/suite_tally.py --verdict <suite.log>

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
``run_all_suites.sh`` gates that on the suite's exit status, plus one more
reading of the same log: ``--verdict`` (``log_reports_failure()``) refuses a
suite that exited 0 while its log carries a ``[FAIL]`` line or a tally with a
non-zero failure count.  An assertion that only logs is Rule 6's masked
verdict, and make cannot see it.

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

THE SELF-TEST IS NOT HERE
-------------------------
``--selftest`` still runs from this file and prints the same transcript, but
its arms live in ``scripts/suite_tally_selftest.py``: one long list of log
fixtures that share no reader with the shapes above, imported only when the
flag is passed.  What that transcript proves -- and why a gate that cannot fail
is not a gate -- is that file's docstring.
"""

import re
import sys
from collections import Counter
from pathlib import Path
from typing import NamedTuple

# --- the recognised summary shapes -------------------------------------------
#
# Each entry: (name, compiled regex, checks-group, failures-group).
# Every regex must capture BOTH the total and the failure count, so the two
# halves of the headline can never drift apart.
SHAPES = (
    # "73 checks: 73 PASS, 0 FAIL"                 aaf_latency_taps, eth_tx_reset,
    # "link_guard: 40 checks: 40 PASS, 0 FAIL"     link_guard
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


def scan(text: str) -> tuple[int, int, list[tuple[str, int, int, str]], list[str], list[str]]:
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


def is_nocount(checks: int, failures: int, matched: list[tuple[str, int, int, str]], skipped: list[str]) -> bool:
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


def campaign_accounted_for(text: str) -> tuple[str, bool]:
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


# A line a harness prints for a check that FAILED. Anchored at the start of the
# line: the shape every sim_main.cpp here prints from its check() helper, and
# the shape the negative arms print. Prose mentioning FAIL mid-line is not it.
FAIL_MARKER = re.compile(r"^\s*\[FAIL\]")


def log_reports_failure(text: str) -> tuple[str, bool]:
    """(reason, failed) - does one suite log say that something FAILED?

    Rule 6's other inventory: an assertion that only logs. A harness whose
    check() prints `[FAIL]` and counts it, but whose main() returns 0 anyway,
    hands make a green it did not earn; so does a tally reading `4 PASS, 1
    FAIL` above an `exit 0`. ``run_all_suites.sh`` calls this for every suite
    that exited 0 and refuses the pass when its log contradicts it. Two
    detectors: a tally in any shape above with a non-zero failure count, and a
    line that starts with ``[FAIL]``. Silence is not this function's business
    (that is ``NOCOUNT``), and a suite that exited non-zero has already failed.
    """
    checks, failures, _matched, _unparsed, _skipped = scan(text)
    markers = [line.strip() for line in text.splitlines() if FAIL_MARKER.match(line)]
    if failures:
        return (f"its tallies report {failures} failure(s) across {checks} checks", True)
    if markers:
        return (f"it carries {len(markers)} [FAIL] line(s), first: {markers[0][:80]}", True)
    return ("no failure reported", False)


class _Tally(NamedTuple):
    """What one pass over the suite logs measured."""

    checks: int
    failures: int
    nocount: list
    zero_tally: set
    unparsed: list
    skips: list
    rows: list


def _campaign_guard_command(path) -> int:
    """The --campaign-guard arm: one campaign log, accounted for or not.

    Checked against the same recognisers the sweep uses; see
    campaign_accounted_for().
    """
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


def _verdict_command(path) -> int:
    """The --verdict arm: one suite log, asked whether it REPORTS a failure.

    run_all_suites.sh consults it for every suite that exited 0; see
    log_reports_failure().
    """
    try:
        text = Path(path).read_text(errors="replace")
    except OSError as exc:
        sys.stderr.write(f"suite_tally: cannot read {path}: {exc}\n")
        return 2
    reason, failed = log_reports_failure(text)
    if not failed:
        return 0
    print(f"VERDICT CONTRADICTED -- {reason}.")
    print("  The suite exited 0 while its own log reports a failure: an")
    print("  assertion that only logs is a masked verdict (Rule 6). Make the")
    print("  harness return non-zero when a check fails.")
    return 1


def _parse_options(argv):
    """(quiet, expected_root, logdirs, exit_code); the code is set on a usage error."""
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
                return False, None, [], 2
            expected_root = Path(argv[pos + 1])
            pos += 2
        elif arg.startswith("-"):
            sys.stderr.write(f"suite_tally: unknown option {arg}\n")
            return False, None, [], 2
        else:
            logdir_args.append(arg)
            pos += 1
    if not logdir_args:
        sys.stderr.write("usage: suite_tally.py <logdir>... [--quiet] "
                         "[--expect-suite-root <dir>]\n")
        return False, None, [], 2
    return quiet, expected_root, [Path(arg) for arg in logdir_args], None


def _inventory_findings(logs, expected_root):
    """(findings, exit_code): where the shard logs are not the serial inventory."""
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
            return [], 2
        if not expected:
            sys.stderr.write(f"suite_tally: no suite Makefiles under expected "
                             f"root {expected_root}\n")
            return [], 2
        actual = set(counts)
        inventory_findings.extend(
            ("MISSING", suite, "no shard produced its log")
            for suite in sorted(expected - actual)
        )
        inventory_findings.extend(
            ("UNEXPECTED", suite, "not present in the serial suite inventory")
            for suite in sorted(actual - expected)
        )
    return inventory_findings, None


def _scan_logs(logs) -> _Tally:
    """One pass over every log: the totals, the per-suite rows and the findings."""
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
    return _Tally(total_checks, total_fails, nocount, zero_tally,
                  unparsed_findings, skip_findings, rows)


def _print_table(rows) -> None:
    """The per-suite table, which --quiet suppresses."""
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


def _print_inventory(inventory_findings) -> None:
    """The accounting failure a shard inventory mismatch is."""
    print()
    print("ACCOUNTING FAILURE -- shard logs do not equal the serial suite "
          "inventory:")
    for finding, suite, reason in inventory_findings:
        print(f"  {finding:<11} {suite}: {reason}")
    print("  The combined check total is not exhaustive and must not be "
          "treated as the serial sweep.")


def main(argv: list[str]) -> int:
    """Dispatch the CLI to a self-test, a campaign guard, a verdict, or the tally."""
    if "--selftest" in argv[1:]:
        # The arms live in ``suite_tally_selftest``: one long list of
        # independent log fixtures that share no reader with the shapes above,
        # and importing them only when --selftest is asked for keeps the
        # import every sweep pays free of them.
        from suite_tally_selftest import run_arms
        return run_arms()
    if "--campaign-guard" in argv[1:]:
        return _campaign_guard_command(argv[argv.index("--campaign-guard") + 1])
    if "--verdict" in argv[1:]:
        return _verdict_command(argv[argv.index("--verdict") + 1])
    quiet, expected_root, logdirs, usage_failure = _parse_options(argv)
    if usage_failure is not None:
        return usage_failure

    logs = sorted((log for logdir in logdirs for log in logdir.glob("*.log")),
                  key=lambda path: (path.stem, str(path)))
    if not logs:
        rendered = ", ".join(map(str, logdirs))
        sys.stderr.write(f"suite_tally: no *.log under {rendered} -- nothing to "
                         f"tally, which is an unknown, not a zero\n")
        return 2

    inventory_findings, root_failure = _inventory_findings(logs, expected_root)
    if root_failure is not None:
        return root_failure

    tally = _scan_logs(logs)
    total_checks, total_fails = tally.checks, tally.failures
    nocount, zero_tally = tally.nocount, tally.zero_tally
    unparsed_findings, skip_findings = tally.unparsed, tally.skips

    if not quiet:
        _print_table(tally.rows)

    print(f"checks: {total_checks}   in-suite failures: {total_fails}")

    if inventory_findings:
        _print_inventory(inventory_findings)

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
