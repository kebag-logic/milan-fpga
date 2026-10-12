#!/usr/bin/env python3
"""Read-only Actions API check of rtl-fast run RUN_ID, attempts 1..N.

For each attempt: run head SHA, event, conclusion; per job: conclusion, started/completed,
duration (completed - started, seconds), and per-step conclusions for the firmware jobs.
Uses `gh api` (GET only). Writes raw JSON plus a summary table.
Usage: hosted_attempts.py RUN_ID ATTEMPTS EXPECT_SHA OUT_DIR
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = "kebag-logic/milan-fpga"
FW = ("firmware-unit", "firmware-control-mutants", "firmware-srp-mutants", "firmware-aecp-mutants")


def api(path: str):
    return json.loads(subprocess.run(["gh", "api", "-X", "GET", path], check=True,
                                     capture_output=True, text=True).stdout)


def secs(a: str, b: str) -> int:
    f = "%Y-%m-%dT%H:%M:%SZ"
    return int((datetime.strptime(b, f) - datetime.strptime(a, f)).total_seconds())


def main() -> int:
    run_id, n, sha, out = sys.argv[1], int(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    rows, ok = [], True
    for att in range(1, n + 1):
        run = api(f"repos/{REPO}/actions/runs/{run_id}/attempts/{att}")
        jobs = api(f"repos/{REPO}/actions/runs/{run_id}/attempts/{att}/jobs?per_page=100")["jobs"]
        (out / f"attempt{att}.json").write_text(json.dumps({"run": {k: run[k] for k in (
            "id", "name", "head_sha", "event", "status", "conclusion", "run_attempt", "run_started_at",
            "created_at", "updated_at", "head_branch")}, "jobs": jobs}, indent=1))
        row = {"attempt": att, "head_sha": run["head_sha"], "event": run["event"],
               "conclusion": run["conclusion"], "run_attempt": run["run_attempt"]}
        for job in jobs:
            row[job["name"]] = {"conclusion": job["conclusion"],
                                "seconds": secs(job["started_at"], job["completed_at"]) if job["completed_at"] else None,
                                "skipped_steps": [s["name"] for s in job.get("steps", []) if s["conclusion"] == "skipped"]}
        ok &= run["head_sha"] == sha and run["conclusion"] == "success" and run["run_attempt"] == att
        ok &= all(row.get(j, {}).get("conclusion") == "success" for j in FW + ("rtl-fast", "publication-census"))
        rows.append(row)
    table = ["| attempt | head | conclusion | " + " | ".join(FW) + " | publication-census | rtl-fast |",
             "|---|---|---|" + "---|" * (len(FW) + 2)]
    for r in rows:
        table.append(f"| {r['attempt']} | {r['head_sha'][:8]} | {r['conclusion']} | " +
                     " | ".join(f"{r[j]['conclusion']} {r[j]['seconds']} s" for j in FW + ("publication-census", "rtl-fast")) + " |")
    slow = {j: max(r[j]["seconds"] for r in rows) for j in FW}
    table.append("")
    table.append("slowest: " + ", ".join(f"{j} {s} s ({100 * s / 2700:.1f} % of 2700 s)" for j, s in slow.items()))
    (out / "summary.json").write_text(json.dumps({"ok": bool(ok), "rows": rows, "slowest": slow}, indent=1))
    (out / "summary.md").write_text("\n".join(table) + "\n")
    print("\n".join(table))
    for r in rows:
        for j in FW:
            if r[j]["skipped_steps"]:
                print(f"attempt {r['attempt']} {j} skipped steps: {r[j]['skipped_steps']}")
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
