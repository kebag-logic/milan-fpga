#!/usr/bin/env python3
"""Read public source receipts and bind their input hashes to the source commit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

p = argparse.ArgumentParser()
p.add_argument("root", type=Path)
p.add_argument("scratch", type=Path)
a = p.parse_args()
base = ("https://raw.githubusercontent.com/kebag-logic/milan-fpga/"
        "4c97887dc83f46703b8d767dec671afcb9ebe206/"
        "review-evidence/544-r1/author-r3/")
for mode in ("sdk", "absent"):
    run_name = f"full-builder-{mode}-run.json"
    raw = urllib.request.urlopen(base + run_name).read()
    meta = json.loads(raw)
    assert meta["head"] == "8383e929fab3ff57a768c88b8b1ff9b568afcf14"
    assert meta["rc"] == 0 and meta["source_unchanged"] is True
    for path, expected in meta["sha256"].items():
        data = subprocess.check_output(["git", "-C", str(a.root), "show", meta["head"] + ":" + path])
        assert hashlib.sha256(data).hexdigest() == expected
    print("PUBLIC SOURCE RUN", base + run_name)
    print(json.dumps({k: meta[k] for k in ("head", "rc", "elapsed_seconds", "sha256", "source_unchanged")}, sort_keys=True))
    log_name = f"full-builder-{mode}.log"
    data = urllib.request.urlopen(base + log_name).read()
    (a.scratch / log_name).write_bytes(data)
    print("PUBLIC LOG", base + log_name, "sha256", hashlib.sha256(data).hexdigest())
    print("Verbatim result excerpts:")
    for line in data.decode().splitlines():
        if ("ALL GATES PASS" in line or "GATE ARM(S) DID NOT RUN" in line
                or "[gate 11]" in line
                or "[gate 1b] boot-unit asm forms" in line
                or "[gate 1b] identity storage" in line):
            print(line)
print("Source receipts are source evidence only, not the composition head or a future current-dev candidate.")
