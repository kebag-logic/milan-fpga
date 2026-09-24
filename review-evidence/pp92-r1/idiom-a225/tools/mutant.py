#!/usr/bin/env python3
"""Apply one exact RTL edit in the SCRATCH processor checkout, build a suite,
run its binaries, keep each binary's raw output, restore the file.

usage: mutant.py TAG NAME SUITE FILE OLD NEW BIN[,BIN...]

Runs only in the scratch parent clone's protocol-processor checkout, never in
the lane. The same mutant is run at the base head and at the fixed head; the
bench outputs are then compared byte for byte (the RTL is identical at both).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("$REVIEWS/pp92-a225-packet/scratch/parent/protocol-processor")
OUT = Path("$REVIEWS/pp92-a225-packet/logs/mutants")
PIN = "$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin"

tag, name, suite, rel, old, new, bins = sys.argv[1:8]
OUT.mkdir(parents=True, exist_ok=True)
path = ROOT / rel
orig = path.read_text()
if orig.count(old) != 1:
    sys.exit(f"{name}: anchor occurs {orig.count(old)} times: {old!r}")
head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                      text=True, check=True).stdout.strip()
env = dict(os.environ, PATH=PIN + ":" + os.environ["PATH"])
tdir = ROOT / "tb" / suite
bak = path.with_suffix(path.suffix + ".a225bak")
shutil.copy2(path, bak)
try:
    path.write_text(orig.replace(old, new, 1))
    subprocess.run(["make", "clean"], cwd=tdir, env=env, capture_output=True)
    b = subprocess.run(["make"], cwd=tdir, env=env, capture_output=True, text=True)
    for binary in bins.split(","):
        exe = tdir / binary
        if not exe.exists():
            sys.exit(f"{name}: {binary} was not built (make exit {b.returncode})")
        r = subprocess.run([str(exe)], cwd=tdir, env=env, capture_output=True, text=True)
        log = OUT / f"{tag}-{suite}-{name}-{exe.name}.txt"
        log.write_text(r.stdout + r.stderr)
        fails = sum(1 for line in r.stdout.splitlines() if line.startswith("FAIL"))
        print(f"{tag} {name} {suite}/{binary} at {head[:8]}: exit {r.returncode}, "
              f"{fails} FAIL lines, last: {(r.stdout.strip().splitlines() or [''])[-1]}")
finally:
    shutil.move(bak, path)
    subprocess.run(["make", "clean"], cwd=tdir, env=env, capture_output=True)
st = subprocess.run(["git", "status", "--short"], cwd=ROOT, capture_output=True, text=True).stdout
if st.strip():
    sys.exit(f"scratch checkout not clean after {name}:\n{st}")
