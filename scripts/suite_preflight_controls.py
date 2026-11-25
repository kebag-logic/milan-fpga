#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The sweep's preflight-only and no-preflight modes, run by test_suite_cancellation.py's main.

The hosted run's preflight job runs the sweep with --preflight-only, and its workers with
--ci-pieces --no-preflight. Each control here starts the production driver in
test_suite_cancellation.py's disposable fixture, which `harness` is."""

import signal
from pathlib import Path
from types import ModuleType

#: Every log the preflight writes, one per self-test, in run_preflight_gates order.
PREFLIGHT_LOGS = ("test_suite_cancellation", "suite_tally", "suite_shards", "check_merge_containment",
                  "check_results_fresh", "check_list_hermetic", "xvlog_gate", "check_merge_review_integrity")


def preflight_only(harness: ModuleType, parent: Path, fail: bool) -> None:
    """--preflight-only runs every self-test and no suite, and a failing one still aborts (exit 2)."""
    root, probe = harness.fixture(parent, "preflight-only" + ("-fail" if fail else ""))
    for relative, text in harness.PREVIOUS.items():
        harness.write(root / "logs" / relative, text)
    if fail:
        probe.env["PROBE_OWNER_FAIL"] = "1"
    harness.start(probe, "--preflight-only")
    status, output = probe.finish()
    assert (probe.control / "owner-ran").exists(), output
    assert not (root / "logs/alpha.log").exists() and not (probe.control / "next-suite").exists(), output
    assert not (root / "logs/omega.log").exists(), "stale suite log survived"
    assert not (root / "logs/preflight/old.log").exists(), "stale prerequisite log survived"
    assert "\nsuites:" not in output, output
    if fail:
        assert status == 2 and "ABORTING: sweep cancellation controls failed" in output, output
        assert "preflight: every self-test passed" not in output, output
    else:
        assert status == 0 and "preflight: every self-test passed; no suite was selected" in output, output
        logs = sorted(path.stem for path in (root / "logs/preflight").iterdir())
        assert logs == sorted(PREFLIGHT_LOGS), logs
    assert not (root / ".run_all_suites.lock.owner").exists()
    probe.save(dict(exit=status, preflight_only=True, failing_selftest=fail, suite_started=False))


def no_preflight(harness: ModuleType, parent: Path) -> None:
    """A --ci-pieces --no-preflight worker runs its suites and none of the self-tests."""
    root, probe = harness.fixture(parent, "no-preflight")
    for relative, text in harness.PREVIOUS.items():
        harness.write(root / "logs" / relative, text)
    harness.start(probe, "--ci-pieces", "--no-preflight")
    status, output = probe.finish()
    assert status == 0 and "PASS     omega" in output and "suites: 2" in output, output
    assert "preflight: not run here" in output, output
    assert not (probe.control / "owner-ran").exists(), "a no-preflight worker ran the self-tests"
    assert list((root / "logs/preflight").iterdir()) == [], "a no-preflight worker kept or wrote preflight logs"
    probe.save(dict(exit=status, no_preflight=True, owner_ran=False))


def preflight_refusals(harness: ModuleType, parent: Path) -> None:
    """The serial sweep, the physical leg and a selected shard cannot drop or isolate the preflight."""
    for options in (("--no-preflight",), ("--no-preflight", "--physical-gptp"),
                    ("--preflight-only", "--shard", "0/1"), ("--preflight-only", "--list"),
                    ("--preflight-only", "--ci-pieces"), ("--preflight-only", "--physical-gptp"),
                    ("--preflight-only", "--no-preflight")):
        label = "refused" + "".join(option.replace("--", "-").replace("/", "_") for option in options)
        root, probe = harness.fixture(parent, label)
        harness.start(probe, *options)
        status, output = probe.finish()
        assert status == 2 and not (root / "logs").exists(), (options, output)
        assert not (probe.control / "owner-ran").exists(), (options, output)
        probe.save(dict(exit=status, refused=list(options)))


def run(parent: Path, harness: ModuleType) -> None:
    """Both modes, their refusals, and their INT/TERM boundaries through the shared traps."""
    preflight_only(harness, parent, fail=False)
    preflight_only(harness, parent, fail=True)
    no_preflight(harness, parent)
    preflight_refusals(harness, parent)
    for signum in (signal.SIGINT, signal.SIGTERM):
        harness.cancellation(parent, "preflight", signum, options=("--preflight-only",))
    for phase in ("selection", "command", "transition"):
        harness.cancellation(parent, phase, signal.SIGTERM, options=("--ci-pieces", "--no-preflight"))
    print("suite preflight modes: PASS (preflight-only and no-preflight sweeps, their refusals, "
          "INT/TERM in each)", flush=True)
