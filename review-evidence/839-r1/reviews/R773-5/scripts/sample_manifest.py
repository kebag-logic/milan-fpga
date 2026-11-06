#!/usr/bin/env python3
"""Usage: sample_manifest.py <MANIFEST.json> <evidence-commit> <n>: fetch a seeded sample and compare published_sha256."""
import hashlib, json, random, subprocess, sys
m = json.load(open(sys.argv[1])); ev = sys.argv[2]; n = int(sys.argv[3])
rng = random.Random(841)
sample = rng.sample(m, n)
bad = 0
for e in sample:
    url = f"repos/kebag-logic/milan-fpga/contents/review-evidence/839-r1/{e['file']}?ref={ev}"
    body = subprocess.run(["gh", "api", url, "-H", "Accept: application/vnd.github.raw"], capture_output=True).stdout
    ok = hashlib.sha256(body).hexdigest() == e["published_sha256"]
    bad += not ok
    print("OK " if ok else "BAD", e["published_sha256"][:16], e["file"][:90])
print(f"sampled {n}, mismatches {bad}, seed 841")
