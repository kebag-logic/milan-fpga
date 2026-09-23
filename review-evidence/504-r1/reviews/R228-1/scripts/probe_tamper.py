#!/usr/bin/env python3
"""Tamper/foreign-cache probes against the candidate installer's verify path.

Usage: probe_tamper.py <clone> <victim-prefix> <foreign-prefix>
Each probe changes the victim prefix, runs `ci_rv32_sdk.py --verify-only`
(and the cache-hit `install` path for one probe), records the exit status,
the last line and how many SDK tools executed, then restores the bytes.
"""

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

clone, victim, foreign = (Path(a).resolve() for a in sys.argv[1:4])
RECEIPT = victim / ".milan-rv32-sdk.json"
CC1 = next(victim.glob("libexec/gcc/riscv32-buildroot-linux-gnu/14.3.0/cc1"))


def run(extra=("--verify-only",)):
    """Run the candidate installer from the clone at the exact head."""
    done = subprocess.run(
        [sys.executable, str(clone / "scripts/ci_rv32_sdk.py"),
         "--destination", str(victim), *extra],
        capture_output=True, text=True, cwd=clone)
    lines = (done.stdout + done.stderr).strip().splitlines()
    tools = sum(1 for line in lines if line.startswith("SDK argv"))
    return done.returncode, (lines[-1] if lines else ""), tools


def probe(label, change, restore, extra=("--verify-only",)):
    change()
    try:
        code, last, tools = run(extra)
    finally:
        restore()
    print(json.dumps({"probe": label, "exit": code, "tools_executed": tools,
                      "last": last[:200]}))


def digest(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()


receipt_bytes = RECEIPT.read_bytes()
cc1_bytes = CC1.read_bytes()


def restore_receipt():
    RECEIPT.write_bytes(receipt_bytes)


def restore_cc1():
    CC1.write_bytes(cc1_bytes)
    CC1.chmod(0o755)


print(json.dumps({"baseline": run()[:2]}))

# 1. one flipped byte in the compiler proper
def flip():
    data = bytearray(cc1_bytes)
    data[len(data) // 2] ^= 0xFF
    CC1.write_bytes(bytes(data))
probe("cc1 byte flipped", flip, restore_cc1)

# 2. same flip with a consistently forged receipt (hostile cache writer)
def forged():
    flip()
    receipt = json.loads(receipt_bytes)
    rel = CC1.relative_to(victim).as_posix()
    receipt["inventory"][rel]["sha256"] = digest(CC1)
    RECEIPT.write_text(json.dumps(receipt, sort_keys=True) + "\n")
probe("cc1 flipped + receipt forged consistently", forged,
      lambda: (restore_cc1(), restore_receipt()))

# 3. foreign cache: another prefix's genuine receipt
probe("foreign prefix receipt", lambda: RECEIPT.write_bytes(
    (foreign / ".milan-rv32-sdk.json").read_bytes()), restore_receipt)

# 4. stale installer: receipt from a different installer source
def stale():
    receipt = json.loads(receipt_bytes)
    receipt["provenance"]["installer_sha256"] = "0" * 64
    RECEIPT.write_text(json.dumps(receipt))
probe("stale installer digest", stale, restore_receipt)

# 5. setuid bit on the compiler proper
probe("cc1 setuid bit", lambda: CC1.chmod(0o4755), restore_cc1)

# 6. extra executable dropped next to the selector
extra = victim / "bin/riscv32-linux-extra"
probe("extra file in bin", lambda: extra.write_text("#!/bin/sh\n"),
      lambda: extra.unlink())

# 7. an extra EMPTY directory (directories carry no record)
empty = victim / "include/r228-empty-dir"
probe("extra empty directory", lambda: empty.mkdir(), lambda: empty.rmdir())

# 8. a FIFO where a file could be
fifo = victim / "bin/r228-fifo"
probe("fifo entry", lambda: os.mkfifo(fifo), lambda: fifo.unlink())

# 9. selector symlink retargeted inside the prefix
sel = victim / "bin/riscv32-linux-gcc"
target = os.readlink(sel)
def retarget():
    sel.unlink()
    sel.symlink_to("riscv32-linux-cpp")
def untarget():
    sel.unlink()
    sel.symlink_to(target)
probe("selector symlink retargeted", retarget, untarget)

# 10. receipt removed on a restored cache (cache-hit install path)
probe("receipt removed (install path)", lambda: RECEIPT.unlink(),
      restore_receipt, extra=())

print(json.dumps({"final": run()[:2]}))
