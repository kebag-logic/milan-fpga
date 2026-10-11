#!/usr/bin/env python3
"""Independent firmware command census: base workflow vs head workflow.

Usage: python3 -I independent_census.py BASE_WORKFLOW_YAML HEAD_WORKFLOW_YAML
Does not import the repository's ci_events.py. For every job whose name starts
with `firmware`, splits each `run` into lines (dropping blanks/comments, joining
backslash continuations) and records (command, job if, step if, step env,
continue-on-error, shell, working-directory, timeout-minutes). Compares the
base set with the head set after removing ONLY a trailing ` --shard N/4`.
"""
import json
import re
import sys

import yaml


def lines(script):
    out, buf = [], ""
    for raw in script.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        if s.endswith("\\"):
            buf += s[:-1].strip() + " "
            continue
        out.append((buf + s).strip())
        buf = ""
    return out


def census(path):
    wf = yaml.safe_load(open(path))
    rows = []
    for jid, job in wf["jobs"].items():
        if not jid.startswith("firmware"):
            continue
        for step in job.get("steps", []):
            if "uses" in step:
                rows.append({"job": jid, "uses": step["uses"], "with": json.dumps(step.get("with"), sort_keys=True),
                             "job_if": str(job.get("if")), "step_if": str(step.get("if"))})
                continue
            for cmd in lines(step.get("run", "")):
                rows.append({"job": jid, "step": step.get("name"), "command": cmd,
                             "job_if": str(job.get("if")), "step_if": str(step.get("if")),
                             "env": json.dumps(step.get("env"), sort_keys=True),
                             "coe": str(step.get("continue-on-error")), "shell": str(step.get("shell")),
                             "wd": str(step.get("working-directory")),
                             "job_timeout": job.get("timeout-minutes"), "job_needs": str(job.get("needs"))})
    return wf, rows


def key(row, strip):
    cmd = row.get("command")
    if cmd is not None and strip:
        cmd = re.sub(r" --shard [0-9]+/[0-9]+$", "", cmd)
    return (cmd, row.get("uses"), row.get("with"), row["job_if"], row["step_if"], row.get("env"),
            row.get("coe"), row.get("shell"), row.get("wd"))


def main():
    base_wf, base = census(sys.argv[1])
    head_wf, head = census(sys.argv[2])
    want = {key(r, False) for r in base}
    got = {key(r, True) for r in head}
    shard_args = sorted(re.search(r"--shard (\S+)$", r["command"]).group(1)
                        for r in head if r.get("command") and re.search(r"--shard \S+$", r["command"]))
    changed = sorted({r["command"] for r in head if r.get("command")} - {r["command"] for r in base if r.get("command")})
    agg_needs = head_wf["jobs"]["rtl-fast"]["needs"]
    result = {
        "base_firmware_jobs": sorted({r["job"] for r in base}),
        "head_firmware_jobs": sorted({r["job"] for r in head}),
        "base_rows": len(base), "head_rows": len(head),
        "missing_from_head": sorted(map(str, want - got)),
        "added_in_head": sorted(map(str, got - want)),
        "shard_arguments": shard_args,
        "head_command_lines_not_in_base": changed,
        "head_timeouts": {j: head_wf["jobs"][j].get("timeout-minutes") for j in head_wf["jobs"] if j.startswith("firmware")},
        "head_needs": {j: head_wf["jobs"][j].get("needs") for j in head_wf["jobs"] if j.startswith("firmware")},
        "aggregate_needs": agg_needs,
        "head_cache_paths": sorted({r["with"] for r in head if r.get("uses", "").startswith("actions/cache")}),
        "base_cache_paths": sorted({r["with"] for r in base if r.get("uses", "").startswith("actions/cache")}),
    }
    ok = (not result["missing_from_head"] and not result["added_in_head"]
          and shard_args == ["0/4", "1/4", "2/4", "3/4"]
          and all(j in agg_needs for j in result["head_firmware_jobs"])
          and set(result["head_timeouts"].values()) == {45}
          and result["head_cache_paths"] == result["base_cache_paths"])
    result["preserved"] = ok
    print(json.dumps(result, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
