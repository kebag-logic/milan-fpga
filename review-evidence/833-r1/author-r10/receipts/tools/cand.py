#!/usr/bin/env python3
"""Candidate mutants on copies: which listings of owner_stated_seconds each misses, every listing checked.

usage: python3 -I -B cand.py <tree> <jobs> <candidates.py> [NAME ...]
<candidates.py> defines CANDIDATES = {name: ((old, new), ...)}. Each tree is a copy of <tree>/scripts with the
edits applied to owned_process.py (each old text exactly once); per_listing.py runs from it.
"""
import concurrent.futures
import runpy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

tree, jobs, source = Path(sys.argv[1]).resolve(), int(sys.argv[2]), Path(sys.argv[3]).resolve()
CANDIDATES = runpy.run_path(str(source))["CANDIDATES"]
names = sys.argv[4:] or list(CANDIDATES)
probe = Path(__file__).resolve().parent.parent / "probes/per_listing.py"


def run(scratch: Path, name: str) -> str:
    root = scratch / name
    shutil.copytree(tree / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    product = root / "scripts/owned_process.py"
    text = product.read_text()
    for old, new in CANDIDATES[name]:
        if text.count(old) != 1:
            return f"{name}: DOES NOT APPLY ({text.count(old)}x): {old!r}"
        text = text.replace(old, new)
    product.write_text(text)
    done = subprocess.run([sys.executable, "-I", "-B", str(probe), str(root)], capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
    lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
    missed = [line.split(": MISSED")[0] for line in lines if ": MISSED" in line]
    first = next((line for line in lines if ": MISSED" in line), "")
    return f"{name}: rc {done.returncode} missed {len(missed)}: {missed}\n    first: {first[:260]}"


with tempfile.TemporaryDirectory(prefix="cand-", dir="$VALIDATION_STORAGE/833-a726j/tmp") as scratch:
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        for line in pool.map(lambda name: run(Path(scratch), name), names):
            print(line, flush=True)
