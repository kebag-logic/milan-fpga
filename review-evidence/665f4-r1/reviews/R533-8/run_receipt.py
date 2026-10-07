#!/usr/bin/env python3
"""Run one foreground validation command and retain a public receipt.

Run from the reviewed checkout. Supply REVIEW_VERILATOR when using the scoped
mailbox gate. The SDK must already be installed at scratch/sdk with the
repository's checksum-verifying installer. No detached process is created.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

packet = Path(__file__).resolve().parent
root = Path.cwd()
label, *command = sys.argv[1:]
scratch = packet / "scratch"
receipts = packet / "receipts"
receipts.mkdir(exist_ok=True)
env = os.environ.copy()
env.update(TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE="1",
           PYTHONUNBUFFERED="1", GIT_NO_REPLACE_OBJECTS="1",
           MILAN_RV32_CC=str(scratch / "sdk/bin/riscv32-linux-gcc"))
if "REVIEW_VERILATOR" in env:
    env["VERILATOR"] = env["REVIEW_VERILATOR"]
    env["PATH"] = str(Path(env["VERILATOR"]).parent) + ":" + env["PATH"]
raw = scratch / (label + ".raw.log")
start = time.monotonic()
with raw.open("wb") as stream:
    rc = subprocess.run(command, env=env, stdout=stream,
                        stderr=subprocess.STDOUT).returncode
def public(value):
    return (value.replace(str(packet), "$PACKET")
            .replace(str(root), "$CHECKOUT")
            .replace(str(Path.home()), "$USER_HOME"))
data = raw.read_bytes()
log = receipts / (label + ".log")
log.write_text(public(data.decode(errors="replace")))
(receipts / (label + ".rc")).write_text(str(rc) + "\n")
record = dict(command=[public(x) for x in command], cwd=public(str(root)),
              rc=rc, seconds=round(time.monotonic() - start, 3),
              raw_bytes=len(data), raw_sha256=hashlib.sha256(data).hexdigest(),
              published_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
(receipts / (label + ".json")).write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record), flush=True)
print("\n".join(log.read_text().splitlines()[-12:]), flush=True)
raise SystemExit(rc)
