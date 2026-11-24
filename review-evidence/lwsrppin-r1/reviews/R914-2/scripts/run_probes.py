"""Replay focused probes concurrently; all subprocesses finish before returning.

Usage: python3 -I -B scripts/run_probes.py <candidate-root>
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent.parent
root = Path(sys.argv[1]).resolve()
jobs = [
    ("mutants", ["scripts/twin_mutants.py", str(root), str(packet / "scratch/mutants")], 0),
    ("legacy-census", ["scripts/probe_twin.py", str(root)], 1),
    ("adapted-probe", ["scripts/probe_twin_11.py", str(root)], 0),
    ("runtime-census", ["scripts/census.py", str(root)], 0),
]

def run(job):
    name, args, expected = job
    result = subprocess.run([sys.executable, "-I", "-B", *args], cwd=packet,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    (packet / f"receipts/{name}.log").write_bytes(result.stdout)
    (packet / f"receipts/{name}.rc").write_text(str(result.returncode) + "\n")
    return name, result.returncode, expected

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs))
for name, rc, expected in results:
    print(f"{name}: rc={rc}, expected={expected}")
assert all(rc == expected for _, rc, expected in results)
