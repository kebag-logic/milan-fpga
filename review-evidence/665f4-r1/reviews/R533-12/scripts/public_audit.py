#!/usr/bin/env python3
"""Verify published gate receipts by their immutable Git blobs and SHA256."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--packet", type=Path, required=True)
p.add_argument("--jobs", type=int, default=4)
a = p.parse_args()
packet = a.packet.resolve()
commit = "30357b9239a8a5e88298e662b65a20fda1a8b9a2"
prefix = "review-evidence/665f4-r1/author-r12/"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/" + path]))
tree = {x["path"]: x for x in api("git/trees/" + commit + "?recursive=1")["tree"]}
out = packet / "scratch/public-evidence"
out.mkdir(parents=True, exist_ok=True)
def blob(path):
    entry = tree[prefix + path]
    target = out / path
    if target.exists():
        data = target.read_bytes()
    else:
        data = base64.b64decode(api("git/blobs/" + entry["sha"])["content"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    assert hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() == entry["sha"]
    return data
gates = json.loads(blob("ROUND12-GATES.json"))
def check(row):
    retained = row.get("retained_log")
    result = {"label": row.get("label"), "command": row["command"], "rc": row["rc"]}
    if retained:
        data = blob(retained["path"])
        result.update(path=prefix + retained["path"], bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest())
        result["hash_matches"] = result["sha256"] == retained["sha256"] and len(data) == retained["size"]
    else:
        result["metadata_only"] = True
    return result
with ThreadPoolExecutor(max_workers=a.jobs) as ex:
    rows = list(ex.map(check, gates["receipts"]))
result = {"commit": commit, "head": gates["head"], "gate_count": len(rows),
          "all_rc_zero": all(r["rc"] == 0 for r in rows),
          "all_retained_hashes_match": all(r.get("hash_matches", True) for r in rows),
          "metadata_only_count": sum(r.get("metadata_only", False) for r in rows), "rows": rows}
(packet / "receipts/public-gates-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "rows"}, indent=2))
raise SystemExit(0 if result["all_rc_zero"] and result["all_retained_hashes_match"] else 1)
