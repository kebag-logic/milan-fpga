#!/usr/bin/env python3
"""Run a foreground command and retain its exit code and elapsed time."""
import argparse, os, subprocess, time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument("prefix", type=Path); p.add_argument("command", nargs=argparse.REMAINDER)
a=p.parse_args(); start=time.monotonic()
a.prefix.parent.mkdir(parents=True, exist_ok=True)
with a.prefix.with_suffix(".log").open("w") as log:
    result=subprocess.run(a.command, stdout=log, stderr=subprocess.STDOUT, check=False)
a.prefix.with_suffix(".rc").write_text(str(result.returncode)+"\n")
a.prefix.with_suffix(".time").write_text(f"elapsed_seconds={time.monotonic()-start:.3f}\n")
print(a.prefix.name, "rc",result.returncode,flush=True)
raise SystemExit(result.returncode)
