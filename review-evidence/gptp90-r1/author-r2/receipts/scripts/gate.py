"""Run ONE recorded gate in the foreground and keep its log and result row.

usage: gate.py <out-dir> <label> <cwd> <cmd> [args...]

The command runs under the lane's pinned environment (scripts/env.sh values),
unpiped, with stdout and stderr in <out-dir>/<label>.log. The row
<out-dir>/<label>.json records the command, the checkout's HEAD before and
after (they must agree), the exit status and the wall time. The exit status
of this script is the gate's own.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PINNED = {
    "PATH": "<pinned-verilator>:<pinned-sv2v>:"
            "<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
    "VERILATOR_ROOT": "<home>/.local/share/containers/storage/overlay/"
                      "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator",
    "TMPDIR": "<scratch>/tmp",
}


def head(cwd):
    return subprocess.run(["git", "-C", cwd, "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


def main():
    out, label, cwd, *cmd = sys.argv[1:]
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, **PINNED)
    Path(PINNED["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    before = head(cwd)
    start = time.monotonic()
    with (out / f"{label}.log").open("w") as log:
        rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=log,
                            stderr=subprocess.STDOUT).returncode
    secs = round(time.monotonic() - start, 1)
    after = head(cwd)
    row = dict(label=label, command=cmd, head=before, exit_code=rc,
               seconds=secs, head_unchanged=before == after)
    (out / f"{label}.json").write_text(json.dumps(row, indent=1) + "\n")
    print(json.dumps(row))
    raise SystemExit(rc if before == after else 3)


if __name__ == "__main__":
    main()
