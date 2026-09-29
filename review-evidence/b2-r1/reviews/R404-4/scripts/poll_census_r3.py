#!/usr/bin/env python3
"""Round-3 check of the #606 page's stream-input poll sentences and command census.

Usage: poll_census_r3.py <archived author dir>

1. Every DUT GET_RX_STATE record (role 'dut', what 'state-5-<n>') in every
   controller transcript, split into distinct records and byte-duplicate
   snapshot.jsonl copies of snapshot-after.jsonl.
2. Per action directory (one holding snapshot-before/after.jsonl): exactly one
   Stream Input 1 poll before and one after, and where Stream Input 0 appears.
3. The census files: which DUT stream inputs each polls.
4. Command census: every record addressed to the DUT, grouped by command and
   by descriptor type, to test the page's sentence "No command in the lane
   addressed a DUT stream input". Descriptor type 5 is STREAM_INPUT
   (IEEE 1722.1 Table 7.1); the 'what' label carries <type>-<index>.
Prints no identifier other than record labels.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

A = Path(sys.argv[1])


def recs(p):
    for line in p.read_text().splitlines():
        if line.strip():
            yield json.loads(line)


dup = set()
for p in A.rglob("snapshot.jsonl"):
    if (p.parent / "snapshot-after.jsonl").read_bytes() == p.read_bytes():
        dup.add(p)
files = sorted(A.rglob("*.jsonl"))
print("transcript files:", len(files), "byte-duplicate snapshot.jsonl:", len(dup))

polls_all, polls_distinct, where = Counter(), Counter(), defaultdict(Counter)
bad = []
for p in files:
    for r in recs(p):
        w = r.get("what")
        if r.get("role") == "dut" and isinstance(w, str) and w.startswith("state-5-"):
            polls_all[w] += 1
            if p in dup:
                continue
            polls_distinct[w] += 1
            where[w][p.name] += 1
            resp = r.get("response") or {}
            if resp.get("status") != 0 or resp.get("conn_count") != 0:
                bad.append((p.relative_to(A).as_posix(), w))
print("DUT GET_RX_STATE records, all files:", dict(polls_all), "total", sum(polls_all.values()))
print("DUT GET_RX_STATE records, distinct:", dict(polls_distinct), "total", sum(polls_distinct.values()))
for w in sorted(where):
    print(f"  {w} by file name:", dict(where[w]))
print("distinct polls with status != 0 or conn_count != 0:", bad or "none")

# per action
acts = sorted({p.parent for p in A.rglob("snapshot-after.jsonl")})
shape = Counter()
for d in acts:
    b = [r["what"] for r in recs(d / "snapshot-before.jsonl") if r.get("role") == "dut" and str(r.get("what", "")).startswith("state-5-")]
    a = [r["what"] for r in recs(d / "snapshot-after.jsonl") if r.get("role") == "dut" and str(r.get("what", "")).startswith("state-5-")]
    shape[(tuple(b), tuple(a))] += 1
print("action directories:", len(acts))
for k, v in shape.items():
    print(f"  before={list(k[0])} after={list(k[1])}: {v} actions")
others = [p.relative_to(A).as_posix() for p in files if p not in dup and p.parent not in acts]
print("transcripts outside action directories:", others)

# command census addressed to the DUT
cmd_by_type = Counter()
for p in files:
    if p in dup:
        continue
    for r in recs(p):
        if r.get("role") != "dut":
            continue
        w = str(r.get("what", ""))
        resp = r.get("response") if isinstance(r.get("response"), dict) else {}
        cmd = resp.get("cmd") or ("ACMP GET_RX_STATE" if w.startswith("state-") else "?")
        parts = w.split("-")
        dtype = parts[1] if len(parts) == 3 and parts[1].isdigit() else "-"
        cmd_by_type[(cmd, dtype)] += 1
print("distinct DUT-addressed records (command, descriptor type):")
for k in sorted(cmd_by_type):
    print(f"  {k[0]:20s} type {k[1]:>3s}: {cmd_by_type[k]}")
si = sum(v for (c, t), v in cmd_by_type.items() if t == "5")
print("DUT-addressed commands naming a STREAM_INPUT (type 5):", si)
print("of which state-changing:", sum(v for (c, t), v in cmd_by_type.items()
                                     if t == "5" and not c.startswith(("GET_", "READ_", "ACMP GET_"))))
