#!/usr/bin/env python3
"""R246-2: repeat an UNMODIFIED shipped pool test under a chosen inherited
SIGINT disposition and count failing runs.

Usage: python3 repeat_disposition.py <suite-dir> <receipt-dir> <test-file> <runs>
                                     <default|ignored> [parallel]

`ignored` reproduces the state POSIX gives an asynchronous `cmd &` list in a
non-interactive shell (SIGINT ignored); `default` is a foreground terminal.
SIGTERM/SIGHUP are default and nothing is blocked in both. Each run's stdout
is kept; backpressure runs keep their fixtures with --output.
"""
import concurrent.futures
import signal
import subprocess
import sys
from pathlib import Path


def main() -> int:
    suite, out, test = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    runs, label = int(sys.argv[4]), sys.argv[5]
    parallel = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    disposition = {"default": signal.SIG_DFL, "ignored": signal.SIG_IGN}[label]
    out.mkdir(parents=True, exist_ok=True)

    def state() -> None:
        for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
            signal.signal(sig, signal.SIG_DFL)
        signal.signal(signal.SIGINT, disposition)
        signal.pthread_sigmask(signal.SIG_SETMASK, set())

    def one(k: int) -> tuple[int, int, list[str], str]:
        argv = ["timeout", "-k", "5", "300", sys.executable, test]
        if "backpressure" in test:
            argv += ["--output", str((out / f"fixtures-{label}-{k:02d}").resolve())]
        proc = subprocess.run(argv, cwd=suite, capture_output=True, text=True, preexec_fn=state)
        (out / f"run-{label}-{k:02d}.log").write_text(
            f"SIGINT inherited {label}\nrc={proc.returncode}\n{proc.stdout}{proc.stderr}")
        bad = [line for line in proc.stdout.splitlines() if line.startswith("[FAIL]")]
        last = (proc.stdout.strip().splitlines() or ["<no output>"])[-1]
        return k, proc.returncode, bad, last

    fails = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as pool:
        for k, rc, bad, last in pool.map(one, range(runs)):
            fails += rc != 0
            print(f"run {k:02d} SIGINT={label} rc={rc} :: {last} {'; '.join(bad)}", flush=True)
    print(f"{test} SIGINT={label}: {fails}/{runs} runs failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
