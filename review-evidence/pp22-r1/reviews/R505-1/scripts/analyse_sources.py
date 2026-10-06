#!/usr/bin/env python3
"""Analyze both isolated revisions, each package-first, with all raw receipts."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

packet = Path(__file__).resolve().parents[1]
sources = json.loads((packet / "receipts/derived-sources.json").read_text())
contract = json.loads((packet / "receipts/parent-contract.json").read_text())
binary = os.environ.get("XVLOG") or contract["xvlog_path"]
assert binary and Path(binary).is_file(), "analysis front-end unavailable"
identity_dir = packet / "scratch/analysis-identity"
identity_dir.mkdir(parents=True, exist_ok=True)
version = subprocess.run([binary, "--version"], cwd=identity_dir, capture_output=True, text=True, timeout=30)
(packet / "receipts/analysis-identity.json").write_text(json.dumps({"path": binary, "sha256": hashlib.sha256(Path(binary).read_bytes()).hexdigest(), "version_rc": version.returncode, "version_stdout": version.stdout, "version_stderr": version.stderr}, indent=2) + "\n")

def analyse(label):
    work = packet / "scratch" / ("analysis-" + label)
    work.mkdir(parents=True, exist_ok=False)
    out = packet / "receipts/xvlog" / label
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    start = time.monotonic()
    for path in sources:
        source = packet / "scratch" / ("suites-" + label) / path
        command = [binary, "-sv", "--work", "work", str(source)]
        logfile = out / (Path(path).stem + ".log")
        with logfile.open("w") as log:
            proc = subprocess.run(command, cwd=work, stdout=log, stderr=subprocess.STDOUT, timeout=60)
        logfile.with_suffix(".rc").write_text(str(proc.returncode) + "\n")
        text = logfile.read_text(errors="replace")
        row = {"file": path, "rc": proc.returncode, "VRFC 10-3380": text.count("[VRFC 10-3380]"), "VRFC 10-8530": text.count("[VRFC 10-8530]")}
        rows.append(row)
    (packet / "receipts" / (label + "-analysis-table.json")).write_text(json.dumps(rows, indent=2) + "\n")
    expected = json.loads((packet / "public/evidence/author" / (label + "-analysis-table.json")).read_text())
    assert rows == expected, (label, rows)
    return {"revision": label, "files": len(rows), "seconds": round(time.monotonic()-start,3), "expected_table_matches": True, "nonzero_rc": sum(r["rc"] != 0 for r in rows), "VRFC 10-3380": sum(r["VRFC 10-3380"] for r in rows), "VRFC 10-8530": sum(r["VRFC 10-8530"] for r in rows)}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(analyse, ["base", "head"]))
(packet / "receipts/analysis-summary.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
