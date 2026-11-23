#!/usr/bin/env python3
"""Show the round-2 tests fail for the defects they claim to detect.

Usage: python3 -I discriminate.py REPO
1. Gate 42 at this tree, but with the builder blob of 677d605f loaded as
   endstation_builder: the three malformed-board rows must fail (not ConfigError).
2. Gate 41's TSpec check with the host width replaced in memory by the
   current-format width: it must fail.
No tracked file is written.
"""
import subprocess
import sys
import types
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/builder"))
import os
os.chdir(repo)


def load_blob(rev):
    m = types.ModuleType("endstation_builder")
    m.__file__ = str(repo / "sw/builder/endstation_builder.py")
    sys.modules["endstation_builder"] = m
    src = subprocess.check_output(["git", "show", f"{rev}:sw/builder/endstation_builder.py"])
    exec(compile(src, m.__file__, "exec"), m.__dict__)
    return m


ok = True
# 1: old builder, new gate 42 rows
load_blob("677d605f37c3a80654df1dd2cde053b57242845b")
import test_builder as tb
for row in tb.HOST_REFUSALS[:3]:
    label, base, path, value, words = row
    try:
        tb._host_refused(label, tb.CONFIGS["ax7101_1x1_tdm8"], tb._host_mutation(path, value), words)
        print(f"[1] 677d605f {label}: PASSED (not discriminating)")
        ok = False
    except Exception as e:
        print(f"[1] 677d605f {label}: FAILS as required: {type(e).__name__}: {e}")

# 2: new builder, current-format mutant of the host width
for name in ("test_builder", "endstation_builder"):
    sys.modules.pop(name, None)
import endstation_builder as eb
import test_builder as tb2
real = eb.framer_declared_channels


def current_format(cfg):
    w = [eb.fmt_channels(t["formats"][0]) for t in cfg["talkers"]]
    return max([c for c in w if c] or [eb.WIRE_CHANS_MIN])


eb.framer_declared_channels = current_format
try:
    tb2._check_host_tspec()
    print("[2] current-format mutant: PASSED (not discriminating)")
    ok = False
except AssertionError as e:
    print(f"[2] current-format mutant: FAILS as required: {e}")
eb.framer_declared_channels = real
print("[2] unmutated:", tb2._check_host_tspec())
print("DISCRIMINATING" if ok else "NOT DISCRIMINATING")
sys.exit(0 if ok else 1)
