#!/usr/bin/env python3
"""Recompute the published projection and audit source-head receipt coverage."""
import argparse
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("repo", type=Path)
ap.add_argument("packet", type=Path)
a = ap.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
sys.path.insert(0, str(repo / "scripts"))
from ci_gate_workflows import case_inventory, generate, load_template
from ci_builder_legs import inventory, partition
import suite_shards

def load(path):
    return json.loads((packet / "receipts" / path).read_text())

def span(row):
    return (datetime.fromisoformat(row["completed_at"]) -
            datetime.fromisoformat(row["started_at"])).total_seconds()

author = "published/author-r6/"
final = load(author + "round6-final-validation.json")
prior = load(author + "round5-final-gates.json")
measure = load(author + "round6-docs-builder-legs.json")
projection = load(author + "round6-projections.json")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
assert final["head"] == head
jobs = {name: next(j for j in load("hosted-" + name + "-baseline.json")["jobs"]
                   if j["name"] == carrier)
        for name, carrier in (("docs", "docs-check"), ("elaborate", "elaborate"))}
assert all(j["head_sha"] == "f62602531d415d6c1cae1374a3cc2938faf54049" for j in jobs.values())
hosted = {s["name"]: span(s) for s in jobs["docs"]["steps"]}
local = {s["step"]: s.get("seconds") for s in prior["docs_check"]["steps"]}
cases = case_inventory("docs", load_template(repo, "docs"))
rows = []
for case in cases:
    if case["leg"] != 0 or case["name"] in ("CI scheduling and evidence controls", "Upload the HDL reference HTML"):
        continue
    name = case["name"]
    rows.append(dict(step=name, hosted=hosted.get(name, 0), local=local.get(name, 0),
                     maximum=max(hosted.get(name, 0), local.get(name, 0))))
maximum_sum = sum(r["maximum"] for r in rows)
assert abs(maximum_sum - 1246.806) < 0.00001, maximum_sum
names = inventory(repo)
assert len(names) == 103 and list(map(len, partition(names))) == [1, 102]
assert final["docs_builder_union"]["inventory"] == names
assert final["docs_builder_union"]["tree"] == subprocess.check_output(
    ["git", "rev-parse", "HEAD^{tree}"], cwd=repo, text=True).strip()
assert final["docs_builder_union"]["requirements"] == {
    "--require-rv32": ["test_baremetal_profile_contract"]}
assert final["docs_builder_union"]["union"] == "pass"
assert final["docs_builder_union"]["verdicts_sha256"] == measure["aggregate_replay"]["builder_union"]["verdicts_sha256"]

bank_steps = [s for b in final["banks"].values() for s in b.get("steps", [])]
assert all(s["head"] == head and s["returncode"] == 0 for s in bank_steps)
assert all(b["returncode"] == 0 and not any(int(v) for v in b["memory_events"].values())
           for b in final["banks"].values())
actual_docs = [s["step"] for s in bank_steps if s["workflow"] == "docs" and s["job"].startswith("docs-gates-")]
assert sorted(actual_docs + ["Local act runner contract gate", "Upload the HDL reference HTML"]) == sorted(c["name"] for c in cases)
assert final["runner_contract_gate"]["rc"] == 0 and final["runner_contract_gate"]["head"] == head
assert len(actual_docs) == 41 and len(cases) == 43

inp = projection["inputs"]
docs_time = span(jobs["docs"])
elab_time = span(jobs["elaborate"])
assert docs_time == 2682 and elab_time == 2447
assert hosted["End-station builder gates"] == 1400
assert hosted["CI event and SHA contract gate"] == 37
assert hosted["Local act runner contract gate"] == 102
base_case_seconds = sum(r["hosted"] for r in rows)
setup = docs_time - 1400 - 37 - 102 - base_case_seconds
assert setup == 59
elab_steps = {s["name"]: span(s) for s in jobs["elaborate"]["steps"]}
assert elab_steps["Elaboration gates"] == 1763
assert elab_steps["Standalone LiteX simulation aggregate"] == 597
scale = max(1400, local["End-station builder gates"], measure["reference"]["seconds"]) / measure["reference"]["seconds"]
escale = 1763 / inp["elaboration_alone_round5"]
values = {
    "docs-gates-0": setup + maximum_sum + inp["controls"] + 60,
    "docs-gates-1": 120 + measure["legs"][0]["seconds"] * scale,
    "docs-gates-2": 120 + inp["events_step"] + inp["runner_gate"] + 2 + measure["legs"][1]["seconds"] * scale,
    "elaborate-gates-0": elab_time - 597 - 2 - 1763 + inp["elaboration_legs_round5"][0] * escale + 60,
    "elaborate-gates-1": elab_time - 1763 + inp["elaboration_legs_round5"][1] * escale + 60,
}
ceilings = {k: math.ceil(v) for k, v in values.items()}
assert ceilings == {k: v["projected"] for k, v in projection["rows"].items()}
for k, v in ceilings.items():
    workflow = k.split("-")[0]
    limit = generate(workflow, load_template(repo, workflow))["jobs"][k]["timeout-minutes"] * 60
    assert v <= limit * 0.6
workflows = {name: max(v for k,v in ceilings.items() if k.startswith(name))+270
             for name in ("docs", "elaborate")}
assert workflows == {"docs":1665, "elaborate":1745}
assert all(t <= 1800 for t in workflows.values())
suite_problems, suite_loads, suite_bounds = suite_shards.headroom_problems(
    suite_shards.expand_suites(suite_shards.sweep_suites(repo / "tb/verilator")),
    (repo / ".github/workflows/rtl.yml").read_text())
assert not suite_problems, suite_problems
assert suite_loads == [1605,1541,1572,1544,1540,1539,1539,1540,1541,1543,1540,1539,1539,1538,1538,2032]
out = dict(head=head, per_step_maxima=rows, per_step_sum=maximum_sum, setup_and_gaps=setup,
           scales=dict(docs=scale, elaborate=escale), exact=values, rounded=ceilings,
           suite_workers_seconds=suite_loads, suite_worker_bounds_seconds=suite_bounds,
           workflows_seconds=workflows, workflow_margins_seconds={k:1800-v for k,v in workflows.items()},
           gate_counts=dict(builder=103, docs=43, docs_bank=41, separate_runner_gate=1, upload_action_not_executed_by_bank=1),
           docs_union=final["docs_builder_union"],
           limits=["Author summaries bind raw logs and driver receipts by digest; the raw round-six files are not published.",
                   "The elaboration aggregate replay substitutes its unchanged simulation aggregate outcome.",
                   "Final contended source-bank times are execution evidence, not the assigned round-five projection inputs."])
(packet / "receipts/evidence-audit.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(dict(per_step_sum=maximum_sum, rounded=ceilings, workflows=workflows, source_coverage="PASS"), indent=2))
