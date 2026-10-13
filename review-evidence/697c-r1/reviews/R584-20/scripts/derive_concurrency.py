#!/usr/bin/env python3
"""derive_concurrency.py <tree>: an independent restatement (it imports nothing from <tree>)
of the CPU-range rule CI_WORKFLOWS.md states for the act replica (#730): a job without a
matrix is one container, a matrix job is its literal max-parallel wide or act's default 4,
and a workflow's concurrency is its CONCURRENT_JOB_LIMIT (1) widest jobs added up. Prints
each shipping workflow's jobs, their widths and the derived concurrency, so the document's
"rtl-full derives 4; docs, elaborate and rtl-fast derive 1" can be checked on the composed tree."""
import sys
from pathlib import Path
import yaml

tree = Path(sys.argv[1])
LIMIT, DEFAULT = 1, 4
expect = {"docs.yml": 1, "elaborate.yml": 1, "rtl-fast.yml": 1, "rtl.yml": 4}
bad = 0
for name, want in expect.items():
    jobs = yaml.safe_load((tree / ".github/workflows" / name).read_text())["jobs"]
    widths = {}
    for job_id, job in jobs.items():
        strategy = job.get("strategy")
        if not strategy or "matrix" not in strategy:
            widths[job_id] = 1
        else:
            raw = strategy.get("max-parallel")
            widths[job_id] = DEFAULT if raw is None else max(1, int(raw))
    derived = sum(sorted(widths.values(), reverse=True)[:LIMIT])
    ok = derived == want
    bad += not ok
    print(f"{name}: {len(jobs)} jobs, widths {widths}, derived {derived}, documented {want}: {'OK' if ok else 'DIFFERS'}")
sys.exit(1 if bad else 0)
