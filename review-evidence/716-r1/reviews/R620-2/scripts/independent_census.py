#!/usr/bin/env python3
"""Independent firmware command census: dev 09c7231e firmware-unit vs head's four jobs.

Reads both workflow files straight from git objects (no repository code imported),
splits every `run:` into non-blank, non-comment lines, and records each with its
job `if`, step `if` and step name. Compares after removing only a terminal
` --shard N/4`. Also checks the aggregate's needs and result loop at head.
Usage: independent_census.py CLONE DEV_SHA HEAD_SHA OUT_JSON
"""
import json
import re
import subprocess
import sys

import yaml

FW = ("firmware-unit", "firmware-control-mutants", "firmware-aecp-mutants", "firmware-srp-mutants")


def workflow(clone: str, sha: str) -> dict:
    text = subprocess.run(["git", "-C", clone, "show", f"{sha}:.github/workflows/rtl-fast.yml"],
                          check=True, capture_output=True, text=True).stdout
    return yaml.safe_load(text)


def rows(wf: dict, jobs: tuple) -> list:
    out = []
    for jid in jobs:
        job = wf["jobs"].get(jid)
        if job is None:
            continue
        for step in job["steps"]:
            for line in str(step.get("run", "")).splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    out.append({"job": jid, "job_if": str(job.get("if")), "step": step.get("name", step.get("uses")),
                                "step_if": str(step.get("if")), "command": line})
            if "uses" in step:
                out.append({"job": jid, "job_if": str(job.get("if")), "step": step.get("name", step["uses"]),
                            "step_if": str(step.get("if")), "command": "uses:" + step["uses"] +
                            json.dumps(step.get("with", {}), sort_keys=True)})
    return out


def key(row: dict) -> tuple:
    return (re.sub(r" --shard [0-3]/4$", "", row["command"]), row["job_if"], row["step_if"])


def main() -> int:
    clone, dev, head, out = sys.argv[1:5]
    before = rows(workflow(clone, dev), ("firmware-unit",))
    wf = workflow(clone, head)
    after = rows(wf, FW)
    bset, aset = {key(r) for r in before}, {key(r) for r in after}
    shard_cmds = [(r["job"], r["command"]) for r in after if "--shard" in r["command"]]
    agg = wf["jobs"]["rtl-fast"]
    agg_run = agg["steps"][0]["run"]
    agg_env = agg["steps"][0]["env"]
    result = {
        "before_lines": len(before), "after_lines": len(after),
        "missing": sorted(map(list, bset - aset)), "added": sorted(map(list, aset - bset)),
        "shard_commands": shard_cmds,
        "timeouts": {j: wf["jobs"][j].get("timeout-minutes") for j in FW},
        "needs_changes": {j: wf["jobs"][j].get("needs") for j in FW},
        "job_if": {j: wf["jobs"][j].get("if") for j in FW},
        "aggregate_needs": agg["needs"],
        "aggregate_loop_names": re.findall(r'"([a-z0-9-]+):\$', agg_run),
        "aggregate_env": sorted(agg_env),
        "publication_census_job_identical_to_dev":
            workflow(clone, dev)["jobs"]["publication-census"] == wf["jobs"]["publication-census"],
        "caches": {j: [s.get("with", {}).get("path") for s in wf["jobs"][j]["steps"]
                       if str(s.get("uses", "")).startswith("actions/cache")] for j in FW},
    }
    ok = (not result["missing"] and not result["added"]
          and sorted(c.rsplit(" ", 1)[1] for _, c in shard_cmds) == ["0/4", "1/4", "2/4", "3/4"]
          and len({j for j, _ in shard_cmds}) == 4
          and all(v == 45 for v in result["timeouts"].values())
          and all(n == "changes" for n in result["needs_changes"].values())
          and set(FW) | {"publication-census"} <= set(result["aggregate_needs"])
          and set(FW) | {"publication-census"} <= set(result["aggregate_loop_names"])
          and result["publication_census_job_identical_to_dev"]
          and all(v == ["~/br-milan-rv32/host"] for v in result["caches"].values()))
    result["ok"] = ok
    with open(out, "w") as fh:
        json.dump({"result": result, "before": before, "after": after}, fh, indent=1)
    print(json.dumps(result, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
