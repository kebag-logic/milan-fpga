#!/usr/bin/env python3
"""Run named gate commands in a checkout, one log and one rc file per gate, never piped.

usage: gates.py <checkout> <python> <logdir> <name>=<command> ...
Each <command> is split with shlex; a leading "python3" is replaced by <python>.
A command that needs a shell (cd, rm, install) is given as "sh -c '...'".
Prints one table row per gate and exits 1 if any gate is nonzero.
"""

import os
import pathlib
import shlex
import subprocess
import sys
import time


def main() -> int:
    checkout, python, logdir, *specs = sys.argv[1:]
    out = pathlib.Path(logdir)
    out.mkdir(parents=True, exist_ok=True)
    failed = 0
    rows = []
    for spec in specs:
        name, command = spec.split("=", 1)
        argv = shlex.split(command)
        if argv[0] == "python3":
            argv[0] = python
        start = time.monotonic()
        with open(out / f"{name}.log", "w", encoding="utf-8") as log:
            log.write("$ " + command + "\n")
            log.flush()
            env = {**os.environ, "PATH": str(pathlib.Path(python).parent) + ":/usr/bin:/bin"}
            rc = subprocess.run(argv, cwd=checkout, stdout=log, stderr=subprocess.STDOUT,
                                env=env).returncode
        seconds = time.monotonic() - start
        (out / f"{name}.rc").write_text(f"{rc}\n", encoding="utf-8")
        rows.append(f"| {name} | `{command}` | {rc} | {seconds:.1f} s |")
        print(rows[-1], flush=True)
        failed |= rc != 0
    with open(out / "table.md", "a", encoding="utf-8") as table:
        table.write("\n".join(rows) + "\n")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
