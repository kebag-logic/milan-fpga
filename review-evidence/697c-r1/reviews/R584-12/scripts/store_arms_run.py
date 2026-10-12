#!/usr/bin/env python3
"""R584-12: run the head's own object-store and configuration pin controls (ctrl_pin_store.store_arms) against the
code in <test-dir>, each after a fresh clone of the stack, as ctrl_pin.pin_controls runs them.

Usage: python3 -I -B store_arms_run.py <test-dir> <stack-checkout> <work-dir>
Prints one [ok]/[ESCAPED] line per control and a summary line; exit 0 when every control holds.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

TEST, STACK, WORK = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(TEST))
from ctrl_pin_store import store_arms  # noqa: E402

GIT = shutil.which("git")
ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "PATH": "/usr/bin:/bin"}
pin = subprocess.run([GIT, "-C", str(STACK), "rev-parse", "HEAD"], capture_output=True, text=True, env=ENV,
                     check=True).stdout.strip()
clone = WORK / "pin-clone"


def fresh() -> None:
    if clone.exists():
        shutil.rmtree(clone)
    subprocess.run([GIT, "clone", "--quiet", "--no-hardlinks", str(STACK), str(clone)], env=ENV, check=True)
    subprocess.run([GIT, "-C", str(clone), "-c", "advice.detachedHead=false", "checkout", "--quiet", pin], env=ENV,
                   check=True)


WORK.mkdir(parents=True, exist_ok=True)
bad = 0
arms = store_arms(clone, pin, WORK, f"differs from the pinned {pin[:8]}: ")
for what, spoil, check, needle in arms:
    fresh()
    spoil()
    accepted, detail = check()
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] {what}: {detail}", flush=True)
    bad += not ok
print(f"SUMMARY {len(arms) - bad} of {len(arms)} held")
sys.exit(1 if bad else 0)
