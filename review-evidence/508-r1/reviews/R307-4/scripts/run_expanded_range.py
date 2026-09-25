#!/usr/bin/env python3
"""Run a slice of an expanded `make -n` recipe, one logical command at a time.

Usage: run_expanded_range.py <expanded.txt> <workdir> <first> <last> <logdir>
Lines ending in a backslash are joined into one logical command. Commands are
numbered from 1. Each command runs under `bash -c` in <workdir>; its output
goes to <logdir>/cmdNN.log and a line `NN rc seconds command` is appended to
<logdir>/SUMMARY.tsv. With `list` in place of <first> the numbered commands
are printed instead. Exit status: 1 if any command in the slice failed.
"""
import subprocess
import sys
import time
from pathlib import Path


def logical(path: Path) -> list[str]:
    """The recipe's logical commands, continuation lines joined."""
    cmds, cur = [], ""
    for line in path.read_text().splitlines():
        if line.endswith("\\"):
            cur += line[:-1] + " "
            continue
        cur += line
        if cur.strip():
            cmds.append(cur.strip())
        cur = ""
    if cur.strip():
        cmds.append(cur.strip())
    return cmds


def main() -> int:
    """Run or list the requested slice."""
    cmds = logical(Path(sys.argv[1]))
    work = Path(sys.argv[2])
    if sys.argv[3] == "list":
        for i, c in enumerate(cmds, 1):
            print(f"{i:02d} {c[:160]}")
        return 0
    first, last = int(sys.argv[3]), int(sys.argv[4])
    logdir = Path(sys.argv[5])
    logdir.mkdir(parents=True, exist_ok=True)
    bad = 0
    with open(logdir / "SUMMARY.tsv", "a") as summary:
        for i in range(first, min(last, len(cmds)) + 1):
            t0 = time.time()
            with open(logdir / f"cmd{i:02d}.log", "w") as log:
                log.write(f"$ {cmds[i - 1]}\ncwd: {work}\n")
                log.flush()
                rc = subprocess.run(["bash", "-c", cmds[i - 1]], cwd=work,
                                    stdout=log, stderr=subprocess.STDOUT,
                                    check=False).returncode
                log.write(f"rc={rc}\n")
            dt = int(time.time() - t0)
            summary.write(f"{i:02d}\t{rc}\t{dt}\t{cmds[i - 1][:200]}\n")
            summary.flush()
            print(f"{i:02d} rc={rc} {dt}s {cmds[i - 1][:100]}")
            bad |= rc != 0
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
