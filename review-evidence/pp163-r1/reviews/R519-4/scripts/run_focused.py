#!/usr/bin/env python3
"""Run the digest review and the small arbiter suite concurrently, join both.

Usage: python3 scripts/run_focused.py PROCESSOR_CLONE PACKET PINNED_VERILATOR
The suite runs from a disposable exact-head archive, never the source checkout.
"""
import argparse
import concurrent.futures
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import time

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("source", type=Path)
ap.add_argument("packet", type=Path)
ap.add_argument("verilator", type=Path)
args = ap.parse_args()
source, packet, executable = args.source.resolve(), args.packet.resolve(), args.verilator.resolve()
assert subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip() == "c4539ff107a6a4c7d2e4a4844182b00a2bf33c82"
version = subprocess.check_output([str(executable), "--version"], text=True).strip()
assert version.startswith("Verilator 5.050 "), version
identity = dict(requested_path=str(args.verilator), resolved_path=str(executable),
                sha256=hashlib.sha256(executable.read_bytes()).hexdigest(), version=version)
(packet / "receipts/simulator-identity.json").write_text(json.dumps(identity, indent=2) + "\n")
suite = packet / "scratch/focused-source"
suite.mkdir(exist_ok=True)
archive = subprocess.check_output(["git", "-C", str(source), "archive", "HEAD", "hdl", "tb/tx_arbiter", "tb/common"])
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
    tar.extractall(suite, filter="data")
flags = '--cc --exe --build -j 8 --top-module tx_arbiter_harness -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
jobs = [
    ("independent-inputs", ["python3", str(packet / "scripts/verify_inputs.py"), str(source), str(packet)], source),
    ("tx-arbiter", ["make", "-j16", "run", "VERILATOR=" + str(executable), "VFLAGS=" + flags], suite / "tb/tx_arbiter"),
]


def run(item):
    name, argv, cwd = item
    start = time.monotonic()
    log_path = packet / ("scratch" if name == "tx-arbiter" else "receipts") / (name + ".log")
    with log_path.open("w") as log:
        rc = subprocess.run(argv, cwd=cwd, stdout=log, stderr=subprocess.STDOUT, timeout=540).returncode
    if name == "tx-arbiter" and rc == 0:
        capture = log_path.read_bytes()
        marker = b"./obj_dir/Vtx_arbiter_sim\n"
        assert marker in capture
        (packet / "receipts/tx-arbiter.log").write_bytes(capture.split(marker, 1)[1])
        (packet / "receipts/tx-arbiter-capture.json").write_text(json.dumps(dict(full_capture_sha256=hashlib.sha256(capture).hexdigest(), full_capture_bytes=len(capture), published="Verbatim executable output after the build; full compiler capture is scratch only."), indent=2) + "\n")
    (packet / "receipts" / (name + ".rc")).write_text(str(rc) + "\n")
    return dict(name=name, argv=argv, cwd=str(cwd.relative_to(packet)) if cwd.is_relative_to(packet) else "processor clone", rc=rc, seconds=round(time.monotonic() - start, 3))


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, jobs))
(packet / "receipts/focused-runs.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
raise SystemExit(0 if all(r["rc"] == 0 for r in results) else 1)
