#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Control: the runner self-test passes on a host with fewer CPUs than it books.

The runner self-test books the synthetic CPU ranges 0-15 to 48-63, and the
production range parser refuses any range that ends at or past
`os.cpu_count()`. So every self-test arm that reaches that parser must pin
the count it needs. An arm that does not passes on a large workstation and
fails on GitHub's four-CPU standard runner, which is how the main-entry probe
failed the hosted docs gate (R636-6-F1).

This control runs an installed copy of the runner's self-test in a child
interpreter whose `os.cpu_count()` is forced below the highest booked CPU, so
its result no longer depends on the host it runs on. It then runs the same
self-test on a copy whose production `main` no longer contains its PR run in
the cleanup-signal handlers. That copy must fail on the main-entry probe
after reaching the lookup, not by refusing its CPU booking: forcing the count
must not make that probe vacuous.

The child runs isolated, exactly as the hosted gate's second invocation runs
the runner. A non-isolated self-test would also launch its flat-install child,
a fresh interpreter the forced count cannot reach. The isolated run skips only
that launcher, and executes every other arm under the forced count.

    python3 -I scripts/act_ci_small_host_selftest.py
"""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "act_ci.py"
#: The last CPU of the self-test's synthetic booking (`selftest_configured`).
HIGHEST_BOOKED_CPU = 63
ENTRY_PROBE = "FAIL production main contains an interrupted early repository lookup"
CONTAINED = "        return run_with_cleanup_signals(execute_pr_run)\n"
UNCONTAINED = "        return execute_pr_run()\n"
CPU_REFUSAL = "exceeds this host's"
#: Forces the count, then runs the runner as `__main__`, the way `python3 -I` would.
BOOTSTRAP = (
    "import os, runpy, sys\n"
    "cpus = int(sys.argv[1])\n"
    "os.cpu_count = lambda: cpus\n"
    "print('forced os.cpu_count() =', os.cpu_count(), flush=True)\n"
    "sys.argv = sys.argv[2:]\n"
    "runpy.run_path(sys.argv[0], run_name='__main__')\n"
)


def run_selftest(source: str, worktree: Path, cpus: int) -> subprocess.CompletedProcess:
    """Install `source` read-only and run its self-test isolated, with `cpus` CPUs reported."""
    with tempfile.TemporaryDirectory(prefix="act-ci-small-host-") as raw:
        installed = Path(raw) / "act_ci.py"
        installed.write_text(source, encoding="utf-8")
        installed.chmod(0o555)
        result = subprocess.run(
            [sys.executable, "-I", "-c", BOOTSTRAP, str(cpus), str(installed),
             "--selftest", "--worktree", str(worktree)],
            cwd=raw, capture_output=True, text=True, check=False,
        )
    print(result.stdout + result.stderr, end="")
    return result


def main() -> int:
    """Require the clean self-test to pass, and the planted copy to fail its entry probe."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--cpus", type=int, default=4, help="the CPU count the child reports (default 4)")
    parser.add_argument("--runner", type=Path, default=RUNNER, help="the runner to test (default this tree's)")
    parser.add_argument("--worktree", type=Path, default=ROOT, help="the shipping worktree (default this tree)")
    args = parser.parse_args()
    if not 1 <= args.cpus <= HIGHEST_BOOKED_CPU:
        parser.error(f"--cpus must be 1 to {HIGHEST_BOOKED_CPU}: the booking must exceed the forced count")
    source = args.runner.read_text(encoding="utf-8")
    if source.count(CONTAINED) != 1:
        print("FAIL the runner's main does not end in one contained PR run to plant against")
        return 1
    worktree = args.worktree.expanduser().resolve()
    failures = 0
    clean = run_selftest(source, worktree, args.cpus)
    if clean.returncode or "selftest: PASS" not in clean.stdout:
        print(f"FAIL runner self-test at {args.cpus} CPUs (rc {clean.returncode})")
        failures += 1
    else:
        print(f"ok   runner self-test passes at {args.cpus} CPUs")
    planted = run_selftest(source.replace(CONTAINED, UNCONTAINED), worktree, args.cpus)
    if planted.returncode and ENTRY_PROBE in planted.stdout and CPU_REFUSAL not in planted.stderr:
        print(f"ok   uncontained entry lookup fails the main-entry probe at {args.cpus} CPUs")
    else:
        print(f"FAIL uncontained entry lookup at {args.cpus} CPUs was not caught by the main-entry probe")
        failures += 1
    print("small-host runner control: " + ("PASS" if not failures else f"{failures} FAILURE(S)"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
