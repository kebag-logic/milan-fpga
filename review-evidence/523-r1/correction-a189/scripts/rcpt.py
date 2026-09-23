#!/usr/bin/env python3
"""Run one command and keep an exact receipt: argv, cwd, selected env, times, exit, output.

Usage: rcpt.py NAME [--cwd DIR] [--env K=V ...] [--unset K ...] -- COMMAND [ARG ...]
Writes receipts/NAME.json and receipts/NAME.log (stdout+stderr, unfiltered).
Exits with the command's status.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
RECEIPTS = PACKET / "receipts"


def main() -> int:
    args = sys.argv[1:]
    name = args.pop(0)
    cwd = Path.cwd()
    env = dict(os.environ)
    setenv, unset = {}, []
    while args and args[0] != "--":
        flag = args.pop(0)
        if flag == "--cwd":
            cwd = Path(args.pop(0))
        elif flag == "--env":
            key, value = args.pop(0).split("=", 1)
            env[key] = value
            setenv[key] = value
        elif flag == "--unset":
            key = args.pop(0)
            env.pop(key, None)
            unset.append(key)
        else:
            raise SystemExit(f"unknown flag {flag}")
    argv = args[1:]
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    log = RECEIPTS / f"{name}.log"
    started = time.time()
    with log.open("wb") as output:
        status = subprocess.call(argv, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT)
    ended = time.time()
    git_names = sorted(k for k in env if k.startswith("GIT_"))
    receipt = dict(name=name, argv=argv, cwd=str(cwd), set_env=setenv, unset_env=unset,
                   git_env_names=git_names, started=time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(started)),
                   seconds=round(ended - started, 3), exit=status)
    (RECEIPTS / f"{name}.json").write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{name}: exit {status} ({receipt['seconds']} s)")
    return status


if __name__ == "__main__":
    sys.exit(main())
