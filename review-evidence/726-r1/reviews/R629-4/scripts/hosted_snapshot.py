#!/usr/bin/env python3
"""Read hosted run metadata without changing repository state."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import zipfile

packet = pathlib.Path(sys.argv[1])
repo = "repos/kebag-logic/milan-fpga"
head = "1add0cfbcc778c5292a5935631ca7b47c612b990"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", repo + path]))

def read_run(run_id):
    run = api(f"/actions/runs/{run_id}")
    assert run["head_sha"] == head
    record = {key: run[key] for key in ("id", "name", "head_sha", "status", "conclusion", "html_url", "updated_at")}
    jobs = api(f"/actions/runs/{run_id}/jobs?per_page=100")["jobs"]
    record["jobs"] = [{key: job[key] for key in ("id", "name", "status", "conclusion", "html_url", "steps")} for job in jobs]
    record["artifacts"] = [{key: artifact[key] for key in ("id", "name", "expired", "digest")}
                           for artifact in api(f"/actions/runs/{run_id}/artifacts?per_page=100")["artifacts"]]
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    runs = list(pool.map(read_run, (38311300974, 38311301025, 38311301106, 38311300993)))
receipt = {"observed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "runs": runs}
(packet / "receipts/hosted-final.json").write_text(json.dumps(receipt, indent=2) + "\n")
for run in runs:
    print(run["name"], run["status"], run["conclusion"])
    for job in run["jobs"]:
        print(" ", job["name"], job["status"], job["conclusion"])
    for artifact in run["artifacts"]:
        if artifact["name"] != "suite-logs-4":
            continue
        raw = subprocess.check_output(["gh", "api", repo + f'/actions/artifacts/{artifact["id"]}/zip'])
        assert "sha256:" + hashlib.sha256(raw).hexdigest() == artifact["digest"]
        archive = packet / "scratch/suite-logs-4.zip"
        archive.write_bytes(raw)
        destination = packet / "receipts/hosted-suite-logs-4"
        destination.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive) as zip_file:
            for name in zip_file.namelist():
                if "milan_dp" in name and not name.endswith("/"):
                    target = destination / pathlib.Path(name).name
                    target.write_bytes(zip_file.read(name))
                    print("retained", target.name)
