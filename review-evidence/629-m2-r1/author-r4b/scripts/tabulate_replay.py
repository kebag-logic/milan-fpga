#!/usr/bin/env python3
"""Tabulate every replayed job's summary.json: steps by kind, make calls, result.

Usage: tabulate_replay.py <replay dir> [job-dir ...]
"""

import json
import sys
from pathlib import Path


def row(job_dir: Path) -> str:
    """One Markdown table row for one replayed job."""
    summary = json.loads((job_dir / "summary.json").read_text())
    steps = summary["steps"]
    run = [s for s in steps if s["result"].startswith(("PASS", "FAIL"))]
    subst = [s for s in run if "SUBSTITUTED" in s["result"]]
    mapped = [s for s in run if "mapped" in s["result"]]
    actions = [s for s in steps if s["result"].startswith("ACTION")]
    skipped = [s for s in steps if s["result"].startswith("SKIPPED")]
    failed = [s for s in run if s["rc"] != 0]
    calls = {}
    tsv = job_dir / "make_invocations.tsv"
    if tsv.exists():
        for line in tsv.read_text().splitlines():
            tag = line.split("\t", 1)[0]
            calls[tag] = calls.get(tag, 0) + 1
    make = sum(calls.values())
    where = ", ".join(f"{int(t)}: {n:,}" for t, n in sorted(calls.items()))
    verdict = "rc 0" if not failed else "FAILED " + ", ".join(s["step"] for s in failed)
    return (f"| {summary['workflow'].split('/')[-1]} `{summary['job']}` ({job_dir.name}) | "
            f"{len(steps)}: {len(run) - len(subst)} ({len(mapped)}) / {len(subst)}; "
            f"{len(actions)}; {len(skipped)} | {make:,}{' (' + where + ')' if make else ''} | "
            f"{verdict}, head `{summary['head'][:8]}` |")


def main() -> int:
    """Print the table for the named job directories, or every one found."""
    root = Path(sys.argv[1])
    names = sys.argv[2:] or sorted(p.name for p in root.iterdir()
                                   if (p / "summary.json").exists())
    print("| Job | Steps: verbatim (of them path-mapped) / substituted; actions; "
          "skipped by `if:` | make calls, all GNU make 4.3 | Result |")
    print("|---|---|---|---|")
    for name in names:
        print(row(root / name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
