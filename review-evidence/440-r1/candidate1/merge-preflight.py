#!/usr/bin/env python3
"""Read-only PR507 preflight; source-head and current-base evidence stay distinct."""
import datetime
import json
from pathlib import Path
import subprocess

REPO = "kebag-logic/milan-fpga"
HEAD = "9d6109ccf924c03308cb8aa202ce68a435cd4f8d"
OLD_BASE = "b17580b91deb11f3441dfc5d7f9fafe539d929b8"
BASE = "ec34fcdee0ca9ffa63564a9af8ad70a3a618de29"
CANDIDATE = "0e8cd2325a0d3b15201907372d708428a61044fd"
TREE = "c23dff6c0eafdf5ae89bb3e8a9416c55533a2332"
CWD = Path("$VALIDATION")
ROOT = Path("$VALIDATION_STORAGE/440-manager-candidate1")
SOURCE_RECEIPTS = Path("$VALIDATION_STORAGE/440-manager-r2")
MANAGER = Path("$WORKSPACE_HOME/milan-fpga-management")


def command(*argv):
    return subprocess.check_output(argv, cwd=CWD, text=True).strip()


def github(*argv):
    return json.loads(command("gh", *argv, "--repo", REPO))


receipts = {}
for root, expected_head, expected_base, groups in (
    (ROOT, CANDIDATE, BASE, (("manager-builder", 43), ("full-native", 5))),
    (SOURCE_RECEIPTS, HEAD, OLD_BASE,
     (("manager-builder", 43), ("full-native", 5), ("act-ready", 1))),
):
    for name, count in groups:
        complete = json.loads((root / name / "complete.json").read_text())
        result = json.loads((root / name / "results.json").read_text())
        assert complete["head"] == result["head"] == expected_head
        assert result["base"] == expected_base and complete["exit_code"] == 0
        assert len(result["results"]) == count
        assert all(row["exit_code"] == 0 for row in result["results"])
        receipts[f"{root.name}/{name}"] = {"complete": complete, "results": result}

for name in ("builder-integrity.json", "native-integrity.json"):
    record = json.loads((ROOT / name).read_text())
    assert record["result"] == "PASS"
    assert record["parent"]["head"] == CANDIDATE and record["parent"]["tree"] == TREE
    receipts[name] = record

assert command("git", "rev-parse", "HEAD") == CANDIDATE
assert not command("git", "status", "--porcelain=v1")
assert command("git", "ls-remote", "origin", "refs/heads/dev").split()[0] == BASE
assert command("git", "ls-remote", "origin", "refs/heads/440-markdown-closers").split()[0] == HEAD
assert command("git", "rev-parse", "HEAD^{tree}") == TREE
assert command("git", "merge-tree", "--write-tree", "--no-messages", BASE, HEAD) == TREE
assert command("git", "diff", "--binary", OLD_BASE, HEAD) == command("git", "diff", "--binary", BASE, CANDIDATE)
assert not (set(command("git", "diff", "--name-only", OLD_BASE, HEAD).splitlines()) &
            set(command("git", "diff", "--name-only", OLD_BASE, BASE).splitlines()))

pr = github("pr", "view", "507", "--json",
            "headRefOid,isDraft,state,mergeable,mergeStateStatus,statusCheckRollup")
assert pr["headRefOid"] == HEAD and not pr["isDraft"]
assert pr["state"] == "OPEN" and pr["mergeable"] == "MERGEABLE"
assert pr["mergeStateStatus"] == "CLEAN", pr["mergeStateStatus"]
run = github("run", "view", "35715877831", "--json", "headSha,status,conclusion,event,jobs,url")
assert run["headSha"] == HEAD and run["event"] == "workflow_dispatch"
jobs = {job["name"]: job for job in run["jobs"]}
required_full = {"full-ci-gate", "verilator-suites", "yosys-portability"}
required_full |= {f"Verilator shard {n}/5" for n in range(5)}
required_full |= {f"Yosys shard {n}/4" for n in range(4)}
for name in required_full:
    assert jobs[name]["status"] == "completed" and jobs[name]["conclusion"] == "success", name
# The policy excludes the nightly/manual physical-rate job from PR aggregates.
# Its actual status is retained in the complete run metadata, never called PASS by omission.
required_checks = {"rtl-fast", "docs-check", "wire-accountability", "docs-check-no-git",
                   "elaborate", "verilator-suites", "yosys-portability"}
latest = {}
check_pages = json.loads(command("gh", "api", "--paginate", "--slurp",
                                f"repos/{REPO}/commits/{HEAD}/check-runs?per_page=100"))
# PR-specific rollup retains the earlier draft run. Read every check on the exact
# commit so the successful manual recovery is judged, without accepting a skip.
for check in [check for page in check_pages for check in page["check_runs"]]:
    assert check["head_sha"] == HEAD
    if check.get("name") not in required_checks:
        continue
    stamp = (check.get("started_at") or "", check.get("completed_at") or "")
    name = check["name"]
    if name not in latest or stamp > latest[name][0]:
        latest[name] = (stamp, check)
assert set(latest) == required_checks
for name, (_, check) in latest.items():
    assert check.get("conclusion") == "success", (name, check)
for name in ("verilator-suites", "yosys-portability"):
    assert "/runs/35715877831/" in latest[name][1]["details_url"]

pages = json.loads(command("gh", "api", "--paginate", "--slurp", f"repos/{REPO}/issues/507/comments"))
comments = [comment for page in pages for comment in page]
reviews = {}
for who, day in (("R225", "2026-09-21"), ("R226", "2026-09-19")):
    current = [c for c in comments if c["body"].startswith(f"[{who}]")][-1]
    assert current["body"].splitlines()[0] == f"[{who}] POSITIVE - exact head {HEAD}"
    report = Path("$VALIDATION_STORAGE/lanes/440-review-evidence/review-evidence/440-r1/round2/reviews") / (who + "-2") / "REPORT.md"
    assert current["body"].strip() == report.read_text().strip()
    key = f"507-r2-{who.lower()}"
    execution = json.loads((MANAGER / day / (key + "-execution.json")).read_text())
    assert execution["exit_code"] == 0 and execution.get("is_error") is False
    assert not execution.get("credit_exhausted", False)
    assert subprocess.run(["systemctl", "--user", "is-active", "--quiet", "milan-" + key]).returncode != 0
    reviews[who] = {"comment": current, "execution": execution}
assert subprocess.run(["systemctl", "--user", "is-active", "--quiet", "milan-440-r2-act-ready"]).returncode != 0

result = {
    "checked_at": datetime.datetime.now().astimezone().isoformat(),
    "reviewed_head": HEAD, "source_validation_base": OLD_BASE,
    "live_base": BASE, "candidate_commit": CANDIDATE, "candidate_tree": TREE,
    "receipts": receipts, "hosted_recovery_run": run, "pr": pr,
    "latest_required_checks": {k: v[1] for k, v in latest.items()},
    "exact_commit_check_pages": check_pages, "reviews": reviews,
    "merge_performed": False,
    "authorization": "Standing maintainer authorization at PR503 comment5764802190",
    "limits": "Manager confirms reviewer-owned clean ledgers and finding dispositions. Physical calibration and four field-campaign skips stay disclosed. Nightly/manual physical-rate simulation is separate from mandatory PR contexts; its actual status remains recorded. Source and current-candidate validation retain distinct identities.",
}
(ROOT / "merge-preflight.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"Read-only preflight passed: source {HEAD}, live dev {BASE}, candidate tree {TREE}")
