#!/usr/bin/env python3
"""Run only the AECP plants introduced by this review delta, in two foreground workers."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import re
import subprocess
import sys
ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("--jobs", type=int, default=8)
ap.add_argument("--worker", type=int)
args = ap.parse_args()
repo = args.repo.resolve()
packet = Path(__file__).resolve().parent
if args.worker is None:
    def run(n):
        cmd = [sys.executable, "-B", __file__, str(repo), "--jobs", str(args.jobs // 2), "--worker", str(n)]
        with (packet / f"plants-{n}.log").open("w") as log:
            result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT,
                env=dict(os.environ, TMPDIR=str(packet / "scratch"), PYTHONDONTWRITEBYTECODE="1"))
        (packet / f"plants-{n}.rc").write_text(str(result.returncode) + "\n")
        print("plants", n, "rc", result.returncode, flush=True)
        return result.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(run, (0, 1)))
    sys.exit(any(results))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_mutants as m
full_table = m.DEFECTS
full_controls = m.controls
def controls():
    selected = m.DEFECTS
    try:
        m.DEFECTS = full_table
        full_controls()
    finally:
        m.DEFECTS = selected
m.controls = controls
diff = subprocess.check_output(["git", "diff", "16ba667d..70c100da", "--",
    "sw/firmware/ctrl/test/aecp_map_mutants.py", "sw/firmware/ctrl/test/aecp_configuration_mutants.py",
    "sw/firmware/ctrl/test/aecp_mutants.py"], cwd=repo, text=True)
names = set(re.findall(r"^\+\s+(?:defect)?\('([^']+)'", diff, re.M))
m.DEFECTS = tuple(d for d in m.DEFECTS if d.name in names)
assert len(m.DEFECTS) == 30, (len(m.DEFECTS), len(names))
print("Selected 30 new plants; shard", args.worker, "of 2; jobs", args.jobs, flush=True)
sys.exit(m.campaign(packet / "scratch" / f"plants-{args.worker}", jobs=args.jobs, shard=(args.worker, 2)))
