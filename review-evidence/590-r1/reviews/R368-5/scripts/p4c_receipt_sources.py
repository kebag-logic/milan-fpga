#!/usr/bin/env python3
"""P4c: every tracked-source hash bound in every receipt of the second merge-dev
packet must equal the exact bytes at head 4c2a30de (submodules read at their
gitlinks). Run from the review clone. Usage: p4c_receipt_sources.py <packet dir>"""
import glob, hashlib, json, os, subprocess, sys
HEAD = "4c2a30debb031595b81c5c4bfc53b601a0fec528"
SUBS = {}
for line in subprocess.run(["git", "ls-tree", "-r", HEAD], capture_output=True, text=True, check=True).stdout.splitlines():
    meta, path = line.split("\t")
    if meta.split()[1] == "commit":
        SUBS[path] = meta.split()[2]
def blob(path):
    for sub, pin in SUBS.items():
        if path.startswith(sub + "/"):
            return subprocess.run(["git", "-C", sub, "show", f"{pin}:{path[len(sub)+1:]}"],
                                  capture_output=True, check=True).stdout
    return subprocess.run(["git", "show", f"{HEAD}:{path}"], capture_output=True, check=True).stdout
root = sys.argv[1]
files = sorted(glob.glob(root + "/native-evidence/*-receipt.json") + glob.glob(root + "/uncompressed/native-evidence/*-receipt.json"))
n = bad = 0
unavailable = set()
for f in files:
    d = json.load(open(f))
    for sec in ("build_hashes", "input_hashes"):
        for k, v in d.get(sec, {}).items():
            if k.startswith("build/"):
                continue
            try:
                data = blob(k)
            except subprocess.CalledProcessError:
                unavailable.add(k); continue
            n += 1
            if hashlib.sha256(data).hexdigest() != v:
                bad += 1; print("MISMATCH", os.path.basename(f), k)
print(f"unavailable here (uninitialised submodule; unchanged between packets per P4): {sorted(unavailable)}")
print(f"receipts={len(files)} tracked-source hashes checked={n} mismatched={bad} (submodule pins: {SUBS})")
