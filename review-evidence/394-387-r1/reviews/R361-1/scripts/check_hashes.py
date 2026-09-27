"""Compare the findings page's artifact-hash table with the packet's
RAW-ARTIFACTS.json and per-cycle raw-artifacts.json, and report every raw
path prefix the packet indexes.

Usage: python3 -B check_hashes.py <packet author dir> <page path>
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

pkt = Path(sys.argv[1])
page = Path(sys.argv[2]).read_text()
rows = re.findall(r"^\| (\d+) \| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$", page, re.M)
print("page hash rows:", len(rows))
top = json.loads((pkt / "RAW-ARTIFACTS.json").read_text())
flat = top if isinstance(top, list) else [x for v in top.values() for x in (v if isinstance(v, list) else [v])]
print("RAW-ARTIFACTS.json entries:", len(flat), "bytes:", sum(int(e.get("size", e.get("bytes", 0))) for e in flat if isinstance(e, dict)))
prefixes = Counter()
for e in flat:
    if isinstance(e, dict) and "path" in e:
        prefixes["/".join(e["path"].split("/")[:3])] += 1
print("raw path prefixes:", dict(prefixes))
bad = 0
for cyc, name, size, sha in rows:
    per = json.loads((pkt / f"cycle{int(cyc):02d}" / "raw-artifacts.json").read_text())
    hit = [e for e in per if e["path"].endswith("/" + name)]
    top_hit = [e for e in flat if isinstance(e, dict) and e.get("sha256") == sha]
    ok = len(hit) == 1 and hit[0]["sha256"] == sha and hit[0]["size"] == int(size) and top_hit
    bad += not ok
    print(("OK " if ok else "BAD"), cyc, name, size, sha[:12], "per-cycle path:", hit[0]["path"] if hit else None)
print("FAILURES", bad)
sys.exit(1 if bad else 0)
