#!/usr/bin/env python3
"""Read-only final public snapshot; usage: capture_public.py OUTPUT_DIR."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

REPO = "repos/kebag-logic/milan-fpga"
HEAD = "2bef9e50489a60f216a8073a9f5ea0645752b33f"


def get(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", f"{REPO}/{endpoint}"]))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    observed = datetime.now(timezone.utc).isoformat()
    pr = get("pulls/722")
    dev = get("git/ref/heads/dev")
    runs = get(f"actions/runs?head_sha={HEAD}&per_page=100")
    selected = runs["workflow_runs"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = list(pool.map(lambda run: get(f'actions/runs/{run["id"]}/jobs?per_page=100'), selected))
    for name, data in (("pr-final", pr), ("dev-final", dev),
                       ("hosted-runs-final", runs), ("hosted-jobs-final", jobs)):
        (out / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n")
    lines = [f"Observed UTC: {observed}", f'PR head: {pr["head"]["sha"]}',
             f'Live dev: {dev["object"]["sha"]}',
             "workflow\tjob\tstatus\tconclusion\tsteps\thead"]
    for run, packet in zip(selected, jobs):
        assert packet["total_count"] == len(packet["jobs"]), "pagination needed"
        for job in packet["jobs"]:
            assert job["head_sha"] == HEAD
            lines.append("\t".join(map(str, (run["name"], job["name"], job["status"],
                                                job["conclusion"], len(job["steps"]), job["head_sha"]))))
    (out / "public-final.log").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
