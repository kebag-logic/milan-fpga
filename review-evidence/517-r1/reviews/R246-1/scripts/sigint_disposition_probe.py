#!/usr/bin/env python3
"""R246-1: does test_sim_pool_backpressure.py's verdict depend on the SIGINT
disposition it inherits? Runs the UNMODIFIED test at the reviewed head twice:
once with SIGINT at its default, once with SIGINT ignored (the state POSIX
gives an asynchronous `cmd &` list in a non-interactive shell).

Usage: python3 sigint_disposition_probe.py <suite-dir> <receipt-dir>
"""
import signal
import subprocess
import sys
from pathlib import Path


def run(suite: Path, disposition, label: str, out: Path) -> int:
    def state() -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, signal.SIG_DFL)
        signal.signal(signal.SIGINT, disposition)
        signal.pthread_sigmask(signal.SIG_SETMASK, set())

    proc = subprocess.run(["timeout", "-k", "5", "180", sys.executable,
                           "test_sim_pool_backpressure.py"], cwd=suite,
                          capture_output=True, text=True, preexec_fn=state)
    (out / f"backpressure_sigint_{label}.log").write_text(
        f"SIGINT inherited as {label}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
    print(f"SIGINT {label}: rc={proc.returncode} :: {proc.stdout.strip().splitlines()[-1]}")
    return proc.returncode


def main() -> int:
    suite, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    run(suite, signal.SIG_DFL, "default", out)
    run(suite, signal.SIG_IGN, "ignored", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
