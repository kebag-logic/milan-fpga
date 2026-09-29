#!/usr/bin/env python3
"""R405-3: locate every DUT stream-input state poll (role dut, what state-5-N)
in the archived B2 controller transcripts, by file kind, to check the wording
"Stream Input 1 in 226 distinct polls, before and after every action and at
both censuses; Stream Input 0 at the two censuses only; snapshot.jsonl is a
byte copy of snapshot-after.jsonl and is not counted".
Usage: r405_3_polls.py <author-dir>"""
import collections, glob, hashlib, json, os, sys

root = sys.argv[1]
files = sorted(glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True))

def polls(p):
    out = []
    for line in open(p, encoding="utf-8"):
        if not line.startswith("{"):
            continue
        d = json.loads(line)
        if d.get("role") == "dut" and str(d.get("what", "")).startswith("state-5-"):
            out.append((d["what"], d["t"], d["response"].get("conn_count")))
    return out

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

by_kind = collections.Counter()
per_dir = collections.defaultdict(lambda: collections.Counter())
all_polls, counted = [], []
for p in files:
    rel = os.path.relpath(p, root)
    base = os.path.basename(p)
    for w, t, cc in polls(p):
        all_polls.append((rel, w, t, cc))
        by_kind[(os.path.dirname(rel).split("/")[0], base, w, cc)] += 1
        if base != "snapshot.jsonl":
            counted.append((rel, w, t, cc))
            per_dir[os.path.dirname(rel)][(base, w)] += 1

print("jsonl files:", len(files))
print("polls by (top dir, file, input, conn_count):")
for k, v in sorted(by_kind.items()):
    print("  ", k, v)

# snapshot.jsonl duplicates
dirs = sorted({os.path.dirname(p) for p in files if p.endswith("/snapshot.jsonl")})
eq = collections.Counter()
for d in dirs:
    eq[sha(os.path.join(d, "snapshot.jsonl")) == sha(os.path.join(d, "snapshot-after.jsonl"))] += 1
print("dirs with snapshot.jsonl:", len(dirs), "byte-equal to snapshot-after.jsonl:", dict(eq))

# action dirs: every dir that carries snapshot-before/after
act = sorted({os.path.relpath(os.path.dirname(p), root) for p in files
              if os.path.basename(p) in ("snapshot-before.jsonl", "snapshot-after.jsonl")})
bad = [d for d in act if per_dir[d] != collections.Counter({("snapshot-before.jsonl", "state-5-1"): 1,
                                                         ("snapshot-after.jsonl", "state-5-1"): 1})]
print("dirs with a before/after snapshot:", len(act),
      "cycles:", sum(d.startswith("cycles/") for d in act),
      "bind/:", sorted(d for d in act if d.startswith("bind/")))
print("dirs whose before/after polls are not exactly one Stream Input 1 each:", bad)
missing_before = [d for d in act if not os.path.exists(os.path.join(root, d, "snapshot-before.jsonl"))]
missing_after = [d for d in act if not os.path.exists(os.path.join(root, d, "snapshot-after.jsonl"))]
print("missing before:", missing_before, "missing after:", missing_after)

# other controller-action dirs that have no snapshots at all (would break "every action")
acts_all = sorted({os.path.relpath(os.path.dirname(p), root) for p in files
                   if os.path.basename(p) in ("cycle.jsonl", "unbind.jsonl", "bind.jsonl", "connect.jsonl")})
print("dirs with an action transcript:", len(acts_all), "without before/after snapshot:",
      [d for d in acts_all if d not in act])
print("bind/ subdirs:", sorted(os.listdir(os.path.join(root, "bind"))))
for d in sorted(os.listdir(os.path.join(root, "bind"))):
    print("   bind/%s:" % d, sorted(os.listdir(os.path.join(root, "bind", d))))

cen = [(r, w, t, cc) for r, w, t, cc in counted if r.startswith("restore/census")]
print("census polls:", cen)
si = collections.Counter((w, cc) for _, w, _, cc in counted)
print("counted polls (snapshot.jsonl excluded):", len(counted), dict(si))
print("distinct (input, t) among counted:", len({(w, t) for _, w, t, _ in counted}),
      " among all:", len({(w, t) for _, w, t, _ in all_polls}), " all incl. copies:", len(all_polls))
print("Stream Input 0 outside census files:", [r for r, w, _, _ in all_polls if w == "state-5-0" and not r.startswith("restore/census")])
print("non-zero conn_count anywhere:", [x for x in all_polls if x[3] != 0])
