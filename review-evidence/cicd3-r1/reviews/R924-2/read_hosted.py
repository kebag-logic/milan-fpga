#!/usr/bin/env python3
"""R924: retain read-only Actions API receipts and calculate job wall times."""
import concurrent.futures
import datetime
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = "repos/kebag-logic/milan-fpga"
RUNS = (45528737977, 45528738009, 45528738040, 45528738049)


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", f"{REPO}/{path}"]))


def fetch(run):
    metadata = api(f"actions/runs/{run}")
    jobs, page = [], 1
    while True:
        response = api(f"actions/runs/{run}/jobs?per_page=100&page={page}")
        jobs.extend(response["jobs"])
        if len(jobs) >= response["total_count"]:
            break
        assert response["jobs"]
        page += 1
    fields = ("id", "name", "head_sha", "event", "status", "conclusion", "run_attempt", "created_at", "updated_at", "html_url")
    # Omit account identities, runner identities, and repository metadata.
    value = {key: metadata.get(key) for key in fields}
    value["jobs"] = [{key: job.get(key) for key in
                      ("id", "name", "head_sha", "status", "conclusion", "started_at", "completed_at", "html_url", "steps")}
                     for job in jobs]
    (ROOT / f"hosted-{run}.json").write_text(json.dumps(value, indent=2) + "\n")
    return value


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        runs = list(pool.map(fetch, RUNS))
    lines = ["[R924] Actions jobs API; minutes = (completed_at - started_at) / 60", "run\tjob_id\tjob\tconclusion\tminutes"]
    for run in runs:
        assert run["head_sha"] == "9c62539365fea8316dae2b9fd7c68defeff5cb31"
        for job in run["jobs"]:
            start, end = (datetime.datetime.fromisoformat(job[key]) for key in ("started_at", "completed_at"))
            minutes = (end - start).total_seconds() / 60
            lines.append(f'{run["id"]}\t{job["id"]}\t{job["name"]}\t{job["conclusion"]}\t{minutes:.3f}')
    (ROOT / "hosted-minutes.tsv").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
