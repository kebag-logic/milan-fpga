#!/usr/bin/env python3
"""R246-1: repeat the unmodified shipped pool tests with a normalized signal
state (SIGINT/SIGTERM/SIGHUP default, nothing blocked) and count failures.

Usage: python3 flake_repeat.py <suite-dir> <receipt-dir> <test-file> <runs>
Each run keeps its fixtures (--output) when the test supports it.
"""
import signal
import subprocess
import sys
from pathlib import Path


def state() -> None:
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, signal.SIG_DFL)
    signal.pthread_sigmask(signal.SIG_SETMASK, set())


def main() -> int:
    suite, out, test, runs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    fails = 0
    for k in range(runs):
        argv = ["timeout", "-k", "5", "180", sys.executable, test]
        if "backpressure" in test:
            argv += ["--output", str((out / f"fixtures-{k:02d}").resolve())]
        proc = subprocess.run(argv, cwd=suite, capture_output=True, text=True, preexec_fn=state)
        (out / f"run-{k:02d}.log").write_text(f"rc={proc.returncode}\n{proc.stdout}{proc.stderr}")
        bad = [line for line in proc.stdout.splitlines() if line.startswith("[FAIL]")]
        fails += proc.returncode != 0
        print(f"run {k:02d} rc={proc.returncode} {'; '.join(bad)}", flush=True)
    print(f"{test}: {fails}/{runs} runs failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
