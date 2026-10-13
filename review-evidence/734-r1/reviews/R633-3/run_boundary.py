#!/usr/bin/env python3
"""Run one offline review gate in a disposable, networkless user namespace."""
import argparse
import os
from pathlib import Path
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--work-name")
parser.add_argument("candidate", type=Path)
parser.add_argument("name")
parser.add_argument("command", nargs=argparse.REMAINDER)
a = parser.parse_args()
packet = Path(__file__).resolve().parent
work = packet / "scratch" / (a.work_name or a.name)
work.mkdir(parents=True, exist_ok=True)
for name in ("home", "tmp", "install"):
    (work / name).mkdir(exist_ok=True)
argv = ["bwrap", "--unshare-all", "--die-with-parent", "--new-session",
        "--ro-bind", "/usr", "/usr", "--symlink", "/usr/bin", "/bin",
        "--symlink", "/usr/lib", "/lib", "--symlink", "/usr/lib64", "/lib64",
        "--proc", "/proc", "--dev", "/dev", "--dir", "/tmp",
        "--ro-bind", str(a.candidate.resolve()), "/candidate",
        "--ro-bind", str(packet), "/packet", "--bind", str(work), "/work",
        "--clearenv", "--setenv", "PATH", "/usr/bin:/bin",
        "--setenv", "HOME", "/work/home", "--setenv", "TMPDIR", "/work/tmp",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "GIT_CONFIG_GLOBAL", "/dev/null",
        "--setenv", "GIT_CONFIG_SYSTEM", "/dev/null",
        "--setenv", "GIT_CONFIG_COUNT", "1",
        "--setenv", "GIT_CONFIG_KEY_0", "safe.directory",
        "--setenv", "GIT_CONFIG_VALUE_0", "*",
        "--setenv", "GIT_NO_REPLACE_OBJECTS", "1",
        "--chdir", "/candidate", "--", *a.command]
start = time.monotonic()
with (packet / (a.name + ".log")).open("w") as log:
    log.write("Networkless disposable boundary; candidate read-only; no credentials or daemon socket.\n")
    log.write("COMMAND " + repr(a.command) + "\n")
    log.flush()
    result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    log.write(f"\nEXIT {result.returncode} elapsed_seconds={time.monotonic()-start:.3f}\n")
(packet / (a.name + ".rc")).write_text(str(result.returncode) + "\n")
print(a.name, "exit", result.returncode)
raise SystemExit(result.returncode)
