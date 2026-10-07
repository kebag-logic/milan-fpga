#!/usr/bin/env python3
"""Run one foreground command and preserve its raw output and exit status."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
ap = argparse.ArgumentParser()
ap.add_argument("packet", type=Path)
ap.add_argument("name")
ap.add_argument("command", nargs=argparse.REMAINDER)
a = ap.parse_args()
env = dict(os.environ, TMPDIR=str(a.packet.resolve() / "scratch"), PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
with (a.packet / "receipts" / (a.name + ".log")).open("w") as f:
    rc = subprocess.call(a.command, stdout=f, stderr=subprocess.STDOUT, env=env)
(a.packet / "receipts" / (a.name + ".rc")).write_text(str(rc) + "\n")
print(a.name, "rc", rc)
sys.exit(rc)
