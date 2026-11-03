#!/usr/bin/env python3
"""For each named MUTANTS entry, which listings of owner_stated_seconds miss their stated seconds.

usage: python3 -I -B per_listing_mutants.py <tree> <jobs> NAME ...
Each mutant tree is the repository's own mutant_tree; per_listing.py runs from it, every listing checked.
"""
import concurrent.futures
import subprocess
import sys
import tempfile
from pathlib import Path

tree, jobs, names = Path(sys.argv[1]).resolve(), int(sys.argv[2]), sys.argv[3:]
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402

probe = Path(__file__).resolve().parent / "per_listing.py"


def run(root: Path) -> str:
    """The probe's last line from one tree."""
    done = subprocess.run([sys.executable, "-I", "-B", str(probe), str(root)], capture_output=True, text=True,
                          timeout=300, stdin=subprocess.DEVNULL)
    lines = [line for line in (done.stdout + done.stderr).splitlines() if line.strip()]
    return f"rc {done.returncode}: {lines[-1] if lines else ''}"


with tempfile.TemporaryDirectory(prefix="per-listing-", dir="$VALIDATION_STORAGE/833-a726i/tmp") as scratch:
    trees = {name: pts.mutant_tree(Path(scratch), name) for name in names}
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        results = dict(zip(names, pool.map(run, (trees[name] for name in names))))
for name in names:
    print(f"{name} ({pts.MUTANTS[name][0]}, {pts.MUTANTS[name][1]!r}): {results[name]}", flush=True)
