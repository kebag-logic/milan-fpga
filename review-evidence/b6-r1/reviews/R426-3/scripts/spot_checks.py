#!/usr/bin/env python3
"""R426-3 spot checks. Usage: spot_checks.py <archive-root> <page-file>
(1) A2 cluster 56 sits just after the 13.3 s stall's cluster; (2) every raw hash the
round-2 attribution receipt records equals the page's Artifact hashes row."""
import json, re, sys, pathlib
root = pathlib.Path(sys.argv[1]); page = open(sys.argv[2]).read()
g = json.loads((root / "author/summary/a2/grade.json").read_text())["skip_clusters"]
big = max(g, key=lambda k: k["lost_ms"])
c56 = [k for k in g if k["cluster"] == 56][0]
print(f"A2 largest-loss cluster {big['cluster']}: first_frame {big['first_frame']}, lost {big['lost_ms']:.1f} ms")
print(f"A2 cluster 56: first_frame {c56['first_frame']}, net {c56['net_step']}, lost {c56['lost_frames']}, "
      f"rise {c56['read_rise_ms']}, gap {c56['recent_read_gap_ms']}, basis {c56['basis']}")
d = c56["first_frame"] - big["first_frame"]
between = [k["cluster"] for k in g if big["first_frame"] < k["first_frame"] < c56["first_frame"]]
print(f"  cluster 56 is {d} capture frames ({d/48000:.3f} s) after it; clusters between: {between}")
ok1 = 0 < d < 48000 * 2 and between == []
rec = (root / "author-r2/receipts/attribution-checks.txt").read_text()
pairs = re.findall(r"^  (\w+/(?:grade-full\.json|cap-ts\.bin)) ([0-9a-f]{64})$", rec, re.M)
bad = []
for f, h in pairs:
    m = re.search(r"\| `" + re.escape(f) + r"`[^|]*\| [0-9,]+ \| `([0-9a-f]{64})` \|", page)
    if not m or m.group(1) != h:
        bad.append(f)
print(f"round-2 receipt raw hashes: {len(pairs)} recorded, {len(pairs)-len(bad)} equal to the page, mismatched {bad}")
ok2 = len(pairs) == 10 and not bad
print("RESULT", "PASS" if ok1 and ok2 else "FAIL")
