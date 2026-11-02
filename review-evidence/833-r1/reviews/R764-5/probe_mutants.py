#!/usr/bin/env python3
"""Reviewer probe for #833 at the head under review: new mutants of scripts/owned_process.py.

Adds this round's own mutants to the committed MUTANTS list in memory (the clone is not
edited), then runs the committed campaign driver with --matrix semantics: every mutant
against every owner control and the whole test, each in a copied scripts/ tree.

usage: python3 -I probe_mutants.py <clone> <jobs> [name ...]
"""
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402
from owned_process import OwnedProcesses  # noqa: E402

OWN = {
    # TESTING.md:232: a listing that dies inside every census waits 10 s more.
    "rv-vanishing-waits-no-more": (None, "probe",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit)")),
    "rv-vanishing-waits-30s-more": (None, "probe",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit + 3 * REAP_SECONDS)")),
    # TESTING.md:219: stable process handles prevent signalling reused numeric identities.
    "rv-signal-by-number": (None, "probe",
        ("            self._signal(fd, signum)\n            self._signal(fd, signal.SIGCONT)\n",
         "            os.kill(pid, signum)\n            os.kill(pid, signal.SIGCONT)\n")),
    # TESTING.md:224: two seconds after grace SIGKILL has reached every other descendant.
    "rv-parent-spared-past-kill-all": (None, "probe",
        ("                elif clock < kill_all:\n",
         "                elif clock < kill_all or any(parent == pid and child in live"
         " for child, (parent, _start) in owned.items()):\n")),
    # TESTING.md:235: wall time runs ahead of the owner's clock only while a pass takes longer than 0.5 s.
    "rv-clock-always-cap": (None, "probe",
        ("clock += min(now - last, MAX_PASS_SECONDS)", "clock += MAX_PASS_SECONDS")),
    # Not stated in TESTING.md: SIGCONT after each signal so a stopped descendant acts on SIGTERM.
    "rv-no-sigcont-after-send": (None, "probe",
        ("            self._signal(fd, signal.SIGCONT)\n            return True\n",
         "            return True\n")),
    # Not stated in TESTING.md: SIGTERM during grace only to the first census's members.
    "rv-sigterm-to-new": (None, "probe",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    pass\n                elif")),
    # Comment-level: parents spared for their stubborn leaf until grace + 1 s.
    "rv-no-leaf-first": (None, "probe",
        ("if clock < deadline + 1.0 and pid in initial.values():", "if False:")),
    # TESTING.md:277 via owner_survivor's 'sent SIGKILL' field.
    "rv-killed-not-recorded": (None, "probe",
        ("                        killed.setdefault(pid, time.monotonic())\n", "                        pass\n")),
}
pts.MUTANTS.update(OWN)
names = sys.argv[3:] or list(OWN)
with OwnedProcesses():
    sys.exit(pts.mutation_campaign(tsc.OWNER_CONTROLS, names, True, jobs))
