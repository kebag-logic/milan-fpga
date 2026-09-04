#!/usr/bin/env python3
"""Fixture arms for ``scripts/suite_tally.py`` -- one arm per verdict it makes.

This is the ``--selftest`` half of the sweep's accounting, kept beside the
tally rather than inside it: the arms are one long list of independent
fixtures, every case below was copied from a real suite log, and they share no
reader with the rules they exercise.  Run them through the tally, which is the
only supported entry point:

    python3 scripts/suite_tally.py --selftest

``run_arms()`` prints one line per arm in the order the groups below are
called, then ``selftest: PASS`` or the failure count, and returns the exit code
``scripts/run_all_suites.sh`` refuses to start a sweep without.  Adding an arm
to the END of its group is what keeps the printed transcript stable.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from suite_tally import (  # noqa: E402
    campaign_accounted_for,
    is_nocount,
    log_reports_failure,
    main,
    scan,
)


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
    ("labelled-pass-fail",  "link_guard: 40 checks: 40 PASS, 0 FAIL\n", 40, 0, False, 0),
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


def _arms_parse() -> int:
    """Every recorded log shape parses to the checks, failures and skips it must."""
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
    return bad


def _arms_classification() -> int:
    """The NOCOUNT decision itself, which no parse case above can reach."""
    bad = 0
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
    return bad


def _arms_end_to_end() -> int:
    """The whole tool over a temporary log directory: the exit code CI consumes."""
    bad = 0
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
    return bad


def _arms_sharded_inventory() -> int:
    """The multi-directory CLI: a shard union that is not the serial sweep fails."""
    bad = 0
    import contextlib
    import io
    import tempfile
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
    return bad


def _arms_campaign_guard() -> int:
    """The campaign guard as a function: what counts as a campaign accounted for."""
    bad = 0
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
    return bad


def _arms_guard_cli() -> int:
    """The guard's command line and --quiet, the halves production actually calls."""
    bad = 0
    import contextlib
    import io
    import tempfile
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
    return bad


def _arms_log_verdict() -> int:
    """Rule 6's detector - an assertion that only logs - and its command line."""
    bad = 0
    import contextlib
    import io
    import tempfile
    # --- the LOG VERDICT: an assertion that only logs --------------------------
    # Rule 6. A suite that prints [FAIL] and exits 0 used to be a PASS of the
    # sweep, because make cannot read; review crafted exactly that log and the
    # sweep accepted it. These pin the detector, then its CLI and exit code.
    for name, text, want_failed, why in (
        ("verdict-clean", "5 checks: 5 PASS, 0 FAIL\n", False,
         "a clean tally reports no failure"),
        ("verdict-tally-failure", "5 checks: 4 PASS, 1 FAIL\n", True,
         "a tally with a non-zero failure count is a failure, whatever make said"),
        ("verdict-marker-beside-clean-tally",
         "[FAIL] elaboration ACCEPTED illegal TDATA_WIDTH=52\n5 checks: 5 PASS, 0 FAIL\n",
         True, "a [FAIL] line is a failure even when the tally beside it says 0"),
        ("verdict-canonical-failures", "checks: 100   failures: 3\n", True,
         "...in every shape the sweep reads, not just one"),
        ("verdict-prose-is-not-a-marker",
         "note: a [FAIL] here would mean the guard fired\n0 FAIL lines seen\n", False,
         "FAIL mid-line is prose; the marker is anchored"),
        ("verdict-silence-is-not-this-detector", "building...\n", False,
         "a silent log is NOCOUNT's finding, not a reported failure"),
    ):
        reason, got = log_reports_failure(text)
        ok = got == want_failed
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} failed={got}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected failed={want_failed}, got reason: {reason}")

    for name, text, want_rc, want_out, why in (
        ("cli-verdict-accepts", "62 checks: 62 PASS, 0 FAIL\n", 0, None,
         "the verdict CLI passes a log that reports no failure"),
        ("cli-verdict-refuses-marker",
         "62 checks: 62 PASS, 0 FAIL\n[FAIL] elaboration ACCEPTED illegal TDATA_WIDTH=52\n",
         1, "VERDICT CONTRADICTED", "...and refuses one that printed [FAIL], with a non-zero exit"),
        ("cli-verdict-refuses-tally", "5 checks: 4 PASS, 1 FAIL\n", 1,
         "1 failure(s)", "...and one whose tally counts a failure"),
    ):
        with tempfile.TemporaryDirectory() as td:
            log = Path(td, "suite.log")
            log.write_text(text)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), \
                    contextlib.redirect_stderr(io.StringIO()):
                rc = main([sys.argv[0], "--verdict", str(log)])
        out = buf.getvalue()
        ok = rc == want_rc and (want_out is None or want_out in out)
        print(f"  {'ok  ' if ok else 'FAIL'} {name:<32} rc={rc}  -- {why}")
        if not ok:
            bad += 1
            print(f"       expected rc={want_rc}"
                  + (f" and {want_out!r} in the output" if want_out else ""))
    with tempfile.TemporaryDirectory() as td:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            rc = main([sys.argv[0], "--verdict", str(Path(td, "absent.log"))])
    ok = rc == 2
    print(f"  {'ok  ' if ok else 'FAIL'} {'cli-verdict-unreadable-log':<32} rc={rc}  "
          f"-- a log that cannot be read is an unknown, never a pass")
    if not ok:
        bad += 1
        print("       expected rc=2")
    return bad




def run_arms() -> int:
    """Demonstrate both loud verdicts and every parse shape; 0 when all hold."""
    bad = sum(arms() for arms in (
        _arms_parse, _arms_classification, _arms_end_to_end,
        _arms_sharded_inventory, _arms_campaign_guard, _arms_guard_cli,
        _arms_log_verdict))
    print("selftest:", "PASS" if bad == 0 else f"{bad} FAILURE(S)")
    return 1 if bad else 0
