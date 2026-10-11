#!/usr/bin/env python3
"""Read public evidence and independently verify all ten hosted attempts."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

PACKET = Path(__file__).resolve().parents[1]
OUT = PACKET / "receipts"
SCRATCH = PACKET / "scratch"
HEAD = "f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48"
REF = "3dff3266c96285ad82226beb84721b2622f3ac57"
REPO = "repos/kebag-logic/milan-fpga"
JOBS = ("firmware-unit", "firmware-control-mutants", "firmware-aecp-mutants", "firmware-srp-mutants")
EXPECTED = [(684,682,239,567),(703,841,243,415),(676,823,174,577),
            (667,831,250,595),(660,840,242,482),(538,815,207,610),
            (534,838,169,604),(667,826,260,625),(449,648,203,505),(693,830,244,604)]


def api(path):
    return json.loads(subprocess.check_output(["gh", "api", path], timeout=90))


def attempt(n):
    endpoint = f"{REPO}/actions/runs/38162821680/attempts/{n}"
    run = api(endpoint)
    data = api(endpoint + "/jobs?per_page=100")
    (SCRATCH / f"attempt-{n}-raw.json").write_text(json.dumps({"run": run, "jobs": data}, indent=2))
    assert run["head_sha"] == HEAD and run["run_attempt"] == n
    assert run["event"] == "pull_request" and run["conclusion"] == "success"
    assert len(data["jobs"]) == data["total_count"]
    keep = ("id", "name", "head_sha", "run_attempt", "conclusion", "started_at", "completed_at", "html_url", "steps")
    projected = [{k: j[k] for k in keep if k in j} for j in data["jobs"]]
    row = []
    for name in JOBS:
        matches = [j for j in projected if j["name"] == name]
        assert len(matches) == 1
        j = matches[0]
        assert j["head_sha"] == HEAD and j["run_attempt"] == n and j["conclusion"] == "success"
        duration = int((datetime.fromisoformat(j["completed_at"]) - datetime.fromisoformat(j["started_at"])).total_seconds())
        assert 0 < duration <= 1890
        # At least the named campaign/normal suite step actually executed.
        assert any(s["name"].startswith("Run ") and s["conclusion"] == "success" for s in j["steps"])
        row.append(duration)
    assert tuple(row) == EXPECTED[n-1], (n, row)
    result = {"endpoint": endpoint, "run": {k: run[k] for k in ("id", "head_sha", "run_attempt", "event", "conclusion", "html_url")}, "jobs": projected, "firmware_seconds": dict(zip(JOBS, row))}
    (OUT / f"hosted-attempt-{n:02}.json").write_text(json.dumps(result, indent=2) + "\n")
    return n, row


def download(entry):
    data = api(f"{REPO}/contents/{entry['path']}?ref={REF}")
    content = base64.b64decode(data["content"])
    assert len(content) == entry["size"]
    blob = hashlib.sha1(f"blob {len(content)}\0".encode() + content).hexdigest()
    assert blob == entry["sha"]
    destination = SCRATCH / "public-author" / entry["name"]
    destination.write_bytes(content)
    return {"path": entry["path"], "blob": blob, "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}


def main():
    OUT.mkdir(exist_ok=True)
    (SCRATCH / "public-author").mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(attempt, range(1, 11)))
    print("attempt," + ",".join(JOBS))
    for n, row in rows:
        print(str(n) + "," + ",".join(map(str, row)))
    print("PASS: 40 executed firmware jobs at the exact head; manager table matches API timestamps.")
    print("Maximum 841 / 2700 seconds = %.6f%%; ceiling 1890 seconds." % (841/2700*100))
    entries = api(f"{REPO}/contents/review-evidence/716-r1/author-r1?ref={REF}")
    with ThreadPoolExecutor(max_workers=4) as pool:
        manifest = list(pool.map(download, [e for e in entries if e["type"] == "file"]))
    (OUT / "public-evidence-identity.json").write_text(json.dumps({"commit": REF, "files": manifest}, indent=2) + "\n")
    print("PASS: public author evidence downloaded and checked against API blob identities.")


if __name__ == "__main__":
    main()
