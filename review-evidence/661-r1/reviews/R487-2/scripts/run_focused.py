#!/usr/bin/env python3
"""Run independent focused campaigns concurrently; foreground coordinator."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root, packet, compiler = (Path(arg).resolve() for arg in sys.argv[1:])
scratch = packet / "scratch"
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(scratch),
       "VERILATOR": str(compiler), "PATH": str(compiler.parent) + os.pathsep + os.environ["PATH"]}
identity = subprocess.check_output([str(compiler), "--version"], env=env, text=True)
assert "Verilator 5.050" in identity, identity
(packet / "receipts/compiler-identity.txt").write_text(identity)
jobs = {
    "wire-selftest": [sys.executable, "tb/tools/avtp_wire_truth.py", "--self-test"],
    "adp-probe": [sys.executable, str(packet / "scripts/adp_probe.py"), str(root), str(scratch)],
    "focused-builder": [sys.executable, str(packet / "scripts/focused_builder.py"), str(root), str(scratch)],
    "source-lists": [sys.executable, "scripts/check_rtl_source_lists.py"],
    "source-lists-selftest": [sys.executable, "scripts/check_rtl_source_lists.py", "--selftest"],
    "pp-source-lists": [sys.executable, "scripts/pp_srcs.py", "--check", "--selftest"],
    "resource-policy": [sys.executable, "syn/ooc/pp_resource_gate.py", "check-baseline"],
    "resource-sweep-selftest": [sys.executable, "syn/resmap/yosys_sweep.py", "--selftest"],
    "resource-model-selftest": [sys.executable, "syn/resmap/resmap_models.py", "--selftest"],
    "resource-table-selftest": [sys.executable, "syn/resmap/resmap_tables.py", "--selftest"],
    "capture-receipt": [sys.executable, "scripts/check_nvm_capture.py"],
}


def run(item):
    name, command = item
    raw = scratch / (name + ".raw.log")
    start = time.monotonic()
    with raw.open("w") as log:
        result = subprocess.run(command, cwd=root, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=590)
    text = raw.read_text()
    for old, new in ((str(root), "$REPO"), (str(packet), "$PACKET"),
                     (str(compiler.parent), "$COMPILER_DIR")):
        text = text.replace(old, new)
    (packet / "receipts" / (name + ".log")).write_text(text)
    (packet / "receipts" / (name + ".rc")).write_text(str(result.returncode) + "\n")
    receipt = {"campaign": name, "rc": result.returncode,
               "seconds": round(time.monotonic() - start, 3)}
    print(json.dumps(receipt), flush=True)
    return receipt


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(run, jobs.items()))
(packet / "receipts/focused-results.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(row["rc"] == 0 for row in results), results
