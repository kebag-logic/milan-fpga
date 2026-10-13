"""Independent re-derivation of the replay concurrency of each shipping workflow.

Reads the four workflow files the runner replays from a tree given on the
command line, with YAML's base loader (every scalar a string), and applies
the rule CI_WORKFLOWS.md states: a job without a matrix runs one container,
a matrix job runs its literal max-parallel or act's default of 4, and a
workflow's concurrency is its CONCURRENT_JOB_LIMIT (1) widest jobs added up.
Prints each job's width and each workflow's derived concurrency. Does not
import or execute the repository's runner.

usage: python3 -I derive_concurrency.py <tree> [<tree> ...]
"""
import pathlib
import sys

import yaml

WORKFLOWS = {
    "docs": ".github/workflows/docs.yml",
    "elaborate": ".github/workflows/elaborate.yml",
    "rtl-fast": ".github/workflows/rtl-fast.yml",
    "rtl-full": ".github/workflows/rtl.yml",
}
DEFAULT_WIDTH = 4
CONCURRENT_JOB_LIMIT = 1


def width(job: dict) -> int:
    strategy = job.get("strategy")
    if not isinstance(strategy, dict) or "matrix" not in strategy:
        return 1
    raw = strategy.get("max-parallel")
    return DEFAULT_WIDTH if raw is None else max(1, int(raw))


def main() -> int:
    for tree in sys.argv[1:]:
        print(f"tree {tree}")
        for name, relative in WORKFLOWS.items():
            text = (pathlib.Path(tree) / relative).read_text(encoding="utf-8")
            jobs = yaml.load(text, Loader=yaml.BaseLoader)["jobs"]
            widths = {job_id: width(job) for job_id, job in jobs.items()}
            derived = sum(sorted(widths.values(), reverse=True)[:CONCURRENT_JOB_LIMIT])
            wide = {k: v for k, v in widths.items() if v > 1}
            print(f"  {name}: {len(widths)} jobs, wider than one: {wide or 'none'}, derives {derived}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
