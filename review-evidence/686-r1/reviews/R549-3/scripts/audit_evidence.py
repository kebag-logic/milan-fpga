#!/usr/bin/env python3
"""Audit downloaded public resource and candidate receipts without running their commands."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
public = packet / "scratch/public-evidence"
resource = public / "fixed/author-r2/resource-receipts"
candidate = public / "candidate/manager-candidate"
receipts = packet / "receipts"
head = "9c601b5983acfd60fb269b9a88c27b48cab7cf65"
candidate_head = "1351f398f9e0c246888b9ac5286db8370a3bc1f3"
candidate_tree = "140c3b838ef3a1f72e2669744871a48b83911311"
parent = "b959830acd53a868febfe362974e33e144481aa7"

def read(path):
    return json.loads(path.read_text())

def snapshot(filename, endpoint):
    path = packet / "scratch" / filename
    if not path.exists():
        path.write_bytes(subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/" + endpoint]))
    return read(path)

check = subprocess.run(["sha256sum", "-c", "MANIFEST.sha256"], cwd=resource,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
(receipts / "resource-checksums.log").write_text(check.stdout)
(receipts / "resource-checksums.rc").write_text(f"{check.returncode}\n")
assert check.returncode == 0
baseline = read(a.repo / "syn/ooc/pp_resource_baseline.json")["endpoints"]
resources = []
for endpoint in ("route-1x1", "ooc-1x1", "ooc-8x8"):
    root = resource / "r2-48f12dc1" / endpoint
    record = read(root / "record.json")
    assert baseline[endpoint]["record"] == record
    manifest = read(root / "inputs.manifest.json")
    matched = 0
    for entry in manifest["files"]:
        if entry["role"] == "repo":
            path = a.repo / entry["path"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
            matched += 1
    resources.append(dict(endpoint=endpoint, record_equals_head=True,
                          repository_input_hashes_verified=matched,
                          inputs_sha256=record["inputs_sha256"], figures=record["figures"]))

banks = []
dest = receipts / "public-candidate"
dest.mkdir(exist_ok=True)
for bank, total, integrity_file in (("manager-builder",48,"manager-builder-initial-integrity.json"),
                                    ("full-native",5,"full-native-initial-integrity.json")):
    result = read(candidate / bank / "results.json")
    complete = read(candidate / bank / "complete.json")
    integrity = read(candidate / integrity_file)
    assert result["head"] == complete["head"] == integrity["parent"]["head"] == candidate_head
    assert result["base"] == parent
    assert integrity["parent"]["tree"] == candidate_tree
    assert integrity["result"] == "PASS" and complete["exit_code"] == 0
    assert len(result["results"]) == total
    assert all(row["exit_code"] == 0 for row in result["results"])
    for i in range(1,total+1):
        assert (candidate / bank / f"{i:02d}.log").is_file()
    shutil.copytree(candidate / bank, dest / bank, dirs_exist_ok=True)
    shutil.copyfile(candidate / integrity_file, dest / integrity_file)
    banks.append(dict(bank=bank, rows=total, zero_statuses=total,
                      commit=candidate_head, tree=candidate_tree, base=parent))

calibration = (candidate / "manager-builder/48.log").read_text()
assert "ALL GATES PASS EXCEPT 1 NOT RUN" in calibration
checks = snapshot("check-runs.json", f"commits/{head}/check-runs?per_page=100")
hosted = [{k:c[k] for k in ("name","status","conclusion","head_sha","details_url","started_at","completed_at")}
          for c in checks["check_runs"]]
assert all(c["head_sha"] == head for c in hosted)
(receipts / "hosted-checks.json").write_text(json.dumps(hosted, indent=2) + "\n")
jobs = snapshot("hosted-jobs.json", "actions/runs/37719245522/jobs?per_page=100")["jobs"]
slim_jobs = [{k:j[k] for k in ("id","name","head_sha","conclusion","started_at","completed_at","steps")}
             for j in jobs]
(receipts / "hosted-job-steps.json").write_text(json.dumps(slim_jobs, indent=2) + "\n")

summary = dict(resource_files_checked=check.stdout.count(": OK"), resources=resources, candidate_banks=banks,
    candidate_association="Cross-checked published integrity/results/completion receipts; candidate Git objects not available through public commit API",
    source_bank_scope="No exact-source manager bank logs in the supplied archive; candidate receipts explicitly validate another commit/tree",
    calibration="NOT RUN", physical_interop="NOT RUN",
    hosted_success=sum(c["conclusion"]=="success" for c in hosted),
    hosted_skipped=[c["name"] for c in hosted if c["conclusion"]=="skipped"])
(receipts / "evidence-audit.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
