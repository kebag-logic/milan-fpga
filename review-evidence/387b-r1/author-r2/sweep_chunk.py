#!/usr/bin/env python3
"""Replay `make -C tb/verilator/milan_dp run` in chunks that each fit one
foreground command: `list` runs `make clean` and records the `make -n run`
listing; `run A B` executes listed commands A..B-1 in order (shell, suite
directory), appending their output to receipts/sweep/sweep.log and one line
per command (index, exit code, seconds) to receipts/sweep/sweep-state.txt.
A command that fails stops the chunk, as make would. Nothing is skipped or
reordered: a chunk refuses to start anywhere but the next unrun index.

Usage: sweep_chunk.py <repo> list | run <first> <end>"""
import os
import subprocess
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "receipts" / "sweep"
VERILATOR = "$VALIDATION_TOOLS/verilator-v5.050/bin/verilator"
JOBS = "8"


def env() -> dict[str, str]:
    e = os.environ.copy()
    e["PATH"] = str(Path(VERILATOR).parent) + os.pathsep + e["PATH"]
    e["VERILATOR"] = VERILATOR
    e["VERILATOR_JOBS"] = JOBS
    return e


def listing() -> list[str]:
    lines = (OUT / "run-recipe.txt").read_text().splitlines()
    commands, cur = [], ""
    for line in lines:
        cur = cur + "\n" + line if cur else line
        if not line.endswith("\\"):
            commands.append(cur)
            cur = ""
    assert not cur, "dangling continuation"
    return commands


def main() -> int:
    repo, mode = Path(sys.argv[1]).resolve(), sys.argv[2]
    suite = repo / "tb/verilator/milan_dp"
    OUT.mkdir(parents=True, exist_ok=True)
    if mode == "list":
        with (OUT / "make-clean.log").open("wb") as s:
            rc = subprocess.run(["make", "clean"], cwd=suite, env=env(), stdout=s,
                                stderr=subprocess.STDOUT, check=False).returncode
        print(f"make clean rc={rc}")
        if rc:
            return rc
        with (OUT / "run-recipe.txt").open("wb") as s:
            rc = subprocess.run(["make", "-n", "run", f"VERILATOR={VERILATOR}",
                                 f"VERILATOR_JOBS={JOBS}"], cwd=suite, env=env(),
                                stdout=s, stderr=subprocess.PIPE, check=False).returncode
        print(f"make -n run rc={rc}; {len(listing())} commands")
        return rc
    first, end = int(sys.argv[3]), int(sys.argv[4])
    state = OUT / "sweep-state.txt"
    done = state.read_text().splitlines() if state.exists() else []
    assert len(done) == first, f"next unrun index is {len(done)}, not {first}"
    assert all(line.split()[1] == "rc=0" for line in done), "an earlier command failed"
    commands = listing()
    end = min(end, len(commands))
    with (OUT / "sweep.log").open("ab") as log:
        for i in range(first, end):
            header = f"\n==== [{i + 1}/{len(commands)}] {commands[i]}\n"
            log.write(header.encode())
            log.flush()
            t0 = time.time()
            rc = subprocess.run(["sh", "-c", commands[i]], cwd=suite, env=env(),
                                stdout=log, stderr=subprocess.STDOUT,
                                check=False).returncode
            dt = time.time() - t0
            log.write(f"==== [{i + 1}/{len(commands)}] rc={rc} {dt:.1f} s\n".encode())
            with state.open("a") as s:
                s.write(f"{i} rc={rc} {dt:.1f}s\n")
            print(f"[{i + 1}/{len(commands)}] rc={rc} {dt:.1f} s  {commands[i][:90]}")
            if rc:
                return rc
    print(f"chunk {first}..{end} done; {len(commands) - end} left")
    return 0


if __name__ == "__main__":
    sys.exit(main())
