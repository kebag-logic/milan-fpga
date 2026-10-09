#!/usr/bin/env python3
"""Fetch only published source authorities and portable-core comparison inputs."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("tree", type=Path)
p.add_argument("destination", type=Path)
a = p.parse_args()
revision = "6aa25dec977c6ad78bf4ff6275de47fb81d0c246"
files = ["AGENTS.md", "CONTRIBUTING.md", "REQUIREMENTS.md", "docs/README.md", "sw/firmware/ctrl/README.md", "sw/firmware/gtest/README.md", "sw/firmware/gtest/fw_coverage.py", "sw/firmware/gtest/coverage.ratchet", "docs/design/SAVED_STATE_FASTCONNECT.md"]
files += ["sw/firmware/ctrl/" + s for s in ["adp/adp.c", "adp/adp.h", "acmp/acmp.c", "acmp/acmp.h", "acmp/acmp_nvm.c", "acmp/acmp_nvm.h", "maap/maap.c", "maap/maap.h", "maap/README.md", "wire/wire.h"]]
files += ["sw/firmware/ctrl/test/" + s for s in ["test_adp.cpp", "test_adp_reentry.cpp", "test_acmp.cpp", "acmp_fake.hpp", "test_maap.cpp", "test_maap_debug.cpp", "acmp_mutants.py", "acmp_review_mutants.py", "maap_mutants.py", "ctrl_mutant.py", "ctrl_mutants.py"]]
tree = {x["path"]: x for x in json.loads(a.tree.read_text())["tree"]}
def fetch(name):
    entry = tree[name]
    data = subprocess.check_output(["gh", "api", "-H", "Accept: application/vnd.github.raw+json", f"repos/kebag-logic/milan-fpga/git/blobs/{entry['sha']}"])
    oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert oid == entry["sha"], (name, oid)
    target = a.destination / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {"path": name, "blob": oid, "bytes": len(data), "mode": entry["mode"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(fetch, files))
print(json.dumps({"source": revision, "verified": records}, indent=2))
