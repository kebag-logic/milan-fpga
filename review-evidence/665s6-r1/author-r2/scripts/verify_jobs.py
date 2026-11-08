#!/usr/bin/env python3
"""Fail unless every run: step of every job a pull_request to dev-soft-core triggers has an rc of 0 or a rule.

usage: verify_jobs.py <head sha> <replay root> [--table OUT.md] [--json OUT.json]

The rows come from the four workflows at the head, matrix jobs expanded, so a job or step left out
of the replay is a red here, not a missing row. A step ran when <root>/logs/<job>__<id>.rc exists and
its log's first line names the head; it passes at rc 0. A step not run must match a rule of
not_run.json (beside this file), printed beside it. A job whose if: excludes a pull_request event
must have a rule for each of its steps too.
"""
import argparse
import itertools
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

LANE = "$LANES/665-s6-placement"
WORKFLOWS = ("docs.yml", "elaborate.yml", "rtl-fast.yml", "rtl.yml")
RULES = json.loads(Path(__file__).with_name("not_run.json").read_text())["rules"]


def rule_for(wf: str, job: str, sid: str, name: str) -> dict | None:
    for rule in RULES:
        if re.fullmatch(rule["workflow"], wf) and re.fullmatch(rule["job"], job) and (
                re.fullmatch(rule.get("id", "(?!)"), sid) or re.fullmatch(rule.get("name", "(?!)"), name)):
            return rule
    return None


def expansions(body: dict) -> list[dict]:
    matrix = (body.get("strategy") or {}).get("matrix") or {}
    keys = [k for k in matrix if isinstance(matrix[k], list)]
    return [dict(zip(keys, combo)) for combo in itertools.product(*(matrix[k] for k in keys))] or [{}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("head")
    ap.add_argument("root", type=Path)
    ap.add_argument("--table", type=Path)
    ap.add_argument("--json", type=Path)
    a = ap.parse_args()
    logs = a.root / "logs"
    rows, bad, ran, skipped, instead = [], 0, 0, 0, 0
    for wf in WORKFLOWS:
        text = subprocess.run(["git", "-C", LANE, "show", f"{a.head}:.github/workflows/{wf}"],
                              check=True, capture_output=True, text=True).stdout
        doc = yaml.safe_load(text)
        for job, body in doc["jobs"].items():
            for matrix in expansions(body):
                tag = job + "".join(f"-{k}{v}" for k, v in sorted(matrix.items()))
                for n, step in enumerate(body.get("steps", [])):
                    if "run" not in step:
                        continue
                    sid = step.get("id") or f"step{n}"
                    name = (step.get("name") or "").replace("|", "/")
                    rule = rule_for(wf, job, sid, step.get("name") or "")
                    rc_file, log = logs / f"{tag}__{sid}.rc", logs / f"{tag}__{sid}.log"
                    row = {"workflow": wf, "job": tag, "step": sid, "name": name}
                    if rule and not rule.get("instead") and not rule.get("drop"):
                        skipped += 1
                        row.update(result="NOT RUN", detail=rule["reason"])
                    elif not rc_file.exists():
                        bad += 1
                        row.update(result="MISSING", detail="no rc file")
                    else:
                        rc = rc_file.read_text().strip()
                        first = log.read_text(errors="replace").splitlines()[0] if log.exists() else ""
                        ok = rc == "0" and a.head in first
                        bad += not ok
                        ran += 1
                        instead += bool(rule)
                        row.update(result=("rc 0" if ok else f"BAD rc {rc}") + (" (instead)" if rule else ""),
                                   detail=(rule["reason"] + "; " if rule else "") + f"`{log.name}`")
                    rows.append(row)
    lines = ["| Workflow | Job | Step | Name | Result | Reason or log |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['workflow']} | {r['job']} | {r['step']} | {r['name']} | {r['result']} | {r['detail']} |"
              for r in rows]
    summary = (f"{ran} steps ran ({instead} of them as the stated command instead), {skipped} not run with a "
               f"reason, {bad} bad")
    lines += ["", summary]
    out = "\n".join(lines) + "\n"
    if a.table:
        a.table.write_text(f"head {a.head}\n\n" + out)
    if a.json:
        a.json.write_text(json.dumps({"head": a.head, "rows": rows, "summary": summary}, indent=1) + "\n")
    print(out if not a.table else summary)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
