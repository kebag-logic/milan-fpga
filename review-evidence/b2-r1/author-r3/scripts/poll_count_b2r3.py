#!/usr/bin/env python3
"""[A447] Round 3 of PR #622 (F5): the DUT stream-input polls as recorded.

Counts every DUT GET_RX_STATE record (role "dut", what "state-5-<input>") in the
archived lane B2 controller transcripts, per input and per file role. The
snapshot.jsonl file of each action directory is checked against
snapshot-before.jsonl and snapshot-after.jsonl, and a byte-identical copy is left
out of the count. A poll is one (input, timestamp) record.

Usage: poll_count_b2r3.py <round-1 author dir> [<archive MANIFEST.json>]
With the manifest, every transcript read is checked against its
original_sha256 under author/. Prints counts and relative paths only; no
identifier is printed.
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

A = Path(sys.argv[1])
FAILURES = []


def check(ok, what):
    print(("PASS " if ok else "FAIL ") + what)
    if not ok:
        FAILURES.append(what)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def role_of(rel):
    name = rel.rsplit("/", 1)[-1]
    if name in ("census-start.jsonl", "census-end.jsonl"):
        return name[:-6]
    if name in ("snapshot-before.jsonl", "snapshot-after.jsonl", "snapshot.jsonl"):
        return name[:-6]
    return "other"


files = sorted(A.rglob("*.jsonl"))
print(f"transcript files: {len(files)}")

print("\n== snapshot.jsonl against its siblings, per action directory")
dirs = sorted({f.parent for f in files if f.name == "snapshot.jsonl"})
same = Counter()
for d in dirs:
    h = {n: sha(d / n) for n in ("snapshot.jsonl", "snapshot-before.jsonl", "snapshot-after.jsonl")}
    if h["snapshot.jsonl"] == h["snapshot-after.jsonl"]:
        same["byte-identical to snapshot-after.jsonl"] += 1
    elif h["snapshot.jsonl"] == h["snapshot-before.jsonl"]:
        same["byte-identical to snapshot-before.jsonl"] += 1
    else:
        same["distinct"] += 1
print(f"action directories: {len(dirs)}", dict(same))
check(len(dirs) == 112 and same["byte-identical to snapshot-after.jsonl"] == 112,
      "all 112 action directories: snapshot.jsonl is a byte copy of snapshot-after.jsonl")

print("\n== DUT GET_RX_STATE records")
records = Counter()          # (input, role) -> records, every file
polls = defaultdict(set)     # input -> {timestamp}, duplicates excluded
by_role = Counter()          # (input, role) -> polls, duplicates excluded
values = Counter()
per_dir = defaultdict(Counter)
for f in files:
    rel = f.relative_to(A).as_posix()
    role = role_of(rel)
    for line in f.read_text().splitlines():
        if not line.startswith("{"):
            continue
        r = json.loads(line)
        what = r.get("what")
        if r.get("role") != "dut" or not (isinstance(what, str) and what.startswith("state-5-")):
            continue
        inp = int(what.rsplit("-", 1)[1])
        resp = r.get("response") or {}
        records[(inp, role)] += 1
        if role == "snapshot":
            continue
        polls[inp].add(r["t"])
        by_role[(inp, role)] += 1
        values[(inp, resp.get("status"), resp.get("conn_count"))] += 1
        if role in ("snapshot-before", "snapshot-after"):
            per_dir[f.parent.relative_to(A).as_posix()][(inp, role)] += 1

print("records in every *.jsonl, by (input, file role):", dict(sorted(records.items())))
print("  total:", sum(records.values()))
print("polls with the snapshot.jsonl copies left out, by (input, file role):", dict(sorted(by_role.items())))
print("  total:", sum(by_role.values()))
print("distinct (input, timestamp) polls per input:", {k: len(v) for k, v in sorted(polls.items())})
print("values (input, status, conn_count):", dict(sorted(values.items(), key=str)))

check(sum(records.values()) == 340 and records[(1, "snapshot")] == 112 and records[(0, "snapshot")] == 0,
      "every *.jsonl gives 340 records, 112 of them in the snapshot.jsonl copies")
check(len(polls[1]) == 226 and sum(v for (i, _), v in by_role.items() if i == 1) == 226,
      "Stream Input 1: 226 distinct polls")
check(by_role[(1, "snapshot-before")] == 112 and by_role[(1, "snapshot-after")] == 112
      and all(c[(1, "snapshot-before")] == 1 and c[(1, "snapshot-after")] == 1 for c in per_dir.values())
      and len(per_dir) == 112,
      "Stream Input 1 polled once before and once after each of the 112 actions")
check(by_role[(1, "census-start")] == 1 and by_role[(1, "census-end")] == 1,
      "Stream Input 1 polled once at each census")
check(len(polls[0]) == 2 and by_role[(0, "census-start")] == 1 and by_role[(0, "census-end")] == 1
      and sum(v for (i, _), v in by_role.items() if i == 0) == 2,
      "Stream Input 0: 2 polls, one at each census and none elsewhere")
check(set(polls) == {0, 1}, "no other DUT stream input was polled")
check(all(k[1] == 0 and k[2] == 0 for k in values), "every poll: status 0, connection count 0")
check(sum(len(v) for v in polls.values()) == 228, "228 distinct polls in all")

if len(sys.argv) > 2:
    print("\n== transcripts read against the archive MANIFEST.json (author/ prefix)")
    man = {e["file"]: e for e in json.loads(Path(sys.argv[2]).read_text())}
    ok = redacted = missing = 0
    for f in files:
        e = man.get("author/" + f.relative_to(A).as_posix())
        if e is None:
            missing += 1
            continue
        ok += e["original_sha256"] == sha(f)
        redacted += e["original_sha256"] != e["published_sha256"]
    print(f"files {len(files)}, original_sha256 equal {ok}, archived as redacted copies {redacted}, "
          f"absent from the manifest {missing}")
    check(ok == len(files) and missing == 0, "every transcript read equals the archive's original_sha256")

print(f"\nFAILURES {len(FAILURES)}")
sys.exit(1 if FAILURES else 0)
