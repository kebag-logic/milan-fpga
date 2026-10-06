#!/usr/bin/env python3
"""Run four isolated focused builds concurrently under a foreground supervisor."""
import concurrent.futures
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import time

packet = Path(__file__).resolve().parents[1]
repo = Path(sys.argv[1]).resolve()
verilator = Path(os.environ.get("REVIEW_VERILATOR", "$VALIDATION_TOOLS/pinned-verilator-5.050/verilator"))
version = subprocess.check_output([str(verilator), "--version"], text=True).strip()
assert re.search(r"^Verilator 5\.050\b", version), version
identity = {"path": str(verilator), "resolved": str(verilator.resolve()), "version": version, "sha256": hashlib.sha256(verilator.read_bytes()).hexdigest()}
(packet / "receipts/simulator-identity.json").write_text(json.dumps(identity, indent=2) + "\n")
pins = {"base": "e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8", "head": "2139f3dc10161b456dfbd51d2f73a63f9164e041"}
roots = {}
for label, pin in pins.items():
    dest = packet / "scratch" / ("suites-" + label)
    dest.mkdir(parents=True, exist_ok=False)
    data = subprocess.check_output(["git", "-C", str(repo), "archive", pin])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(dest, filter="data")
    roots[label] = dest

def run(task):
    label, suite = task
    cwd = roots[label] / "tb" / suite
    stem = packet / "receipts" / (label + "-" + suite)
    # Each outer make has one recipe. Four translators get three workers each.
    flags = '--cc --exe --build -j 3 --top-module ' + {"originator": "KL_pp_originator", "rx_validator": "KL_pp_rx_validator"}[suite]
    flags += ' -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM'
    flags += ' -CFLAGS "-std=c++17 -O2 -I' + str(cwd) + ' -Wall -Wextra"'
    command = ["make", "-j16", "VERILATOR=" + str(verilator), "VFLAGS=" + flags, "run"]
    start = time.monotonic()
    with stem.with_suffix(".log").open("w") as log:
        proc = subprocess.run(command, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=540)
    stem.with_suffix(".rc").write_text(str(proc.returncode) + "\n")
    log = stem.with_suffix(".log").read_text()
    records = [line for line in log.splitlines() if re.search(r"\bchecks:|RND|divergence|PASS|FAIL", line)]
    result = {"revision": label, "pin": pins[label], "suite": suite, "rc": proc.returncode, "seconds": round(time.monotonic()-start, 3), "command": command, "records": records}
    assert proc.returncode == 0, result
    assert any("checks:" in row and "0 FAIL" in row for row in records), result
    return result

tasks = [(label, suite) for label in pins for suite in ["originator", "rx_validator"]]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, tasks))
for suite in ["originator", "rx_validator"]:
    records = [r["records"] for r in results if r["suite"] == suite]
    assert records[0] == records[1], (suite, records)
(packet / "receipts/focused-suites.json").write_text(json.dumps({"version": version, "max_compile_workers": 12, "identical_records": True, "results": results}, indent=2) + "\n")
print(json.dumps({"identical_records": True, "results": [{k:v for k,v in r.items() if k != "command"} for r in results]}, indent=2))
