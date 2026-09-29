#!/usr/bin/env python3
"""R405-2: count DUT stream-input state polls (role dut, what state-5-N) in the
archived B2 controller transcripts, with and without byte-identical duplicate
files.  Usage: r405_poll_count.py <author-dir>"""
import collections, glob, hashlib, json, os, sys
root = sys.argv[1]
files = sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True))
dup = collections.Counter()
for d in sorted({os.path.dirname(p) for p in files if p.endswith("/snapshot.jsonl")}):
    hs = {n: hashlib.sha256(open(os.path.join(d, n), "rb").read()).hexdigest() for n in ("snapshot.jsonl", "snapshot-before.jsonl", "snapshot-after.jsonl")}
    dup["snapshot.jsonl == snapshot-after.jsonl" if hs["snapshot.jsonl"] == hs["snapshot-after.jsonl"] else
        ("snapshot.jsonl == snapshot-before.jsonl" if hs["snapshot.jsonl"] == hs["snapshot-before.jsonl"] else "distinct")] += 1
print("action dirs with snapshot.jsonl:", sum(dup.values()), dict(dup))
def polls(fs):
    c = collections.Counter(); seen = set()
    for p in fs:
        for line in open(p):
            if not line.startswith("{"): continue
            d = json.loads(line)
            if d.get("role") == "dut" and str(d.get("what", "")).startswith("state-5-"):
                c[(d["what"], d["response"].get("conn_count"))] += 1; seen.add((d["what"], d["t"]))
    return c, seen
all_c, all_seen = polls(files)
print("counting every *.jsonl file:", sum(all_c.values()), dict(all_c))
nodup = [p for p in files if not p.endswith("/snapshot.jsonl")]
c2, _ = polls(nodup)
print("excluding the duplicate snapshot.jsonl copies:", sum(c2.values()), dict(c2))
print("distinct (input, timestamp) polls:", len(all_seen))
