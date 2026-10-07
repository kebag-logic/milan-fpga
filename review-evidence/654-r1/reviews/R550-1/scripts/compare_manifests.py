#!/usr/bin/env python3
"""Compare two export_ax.py manifests file by file (raw-byte digests).

Usage: compare_manifests.py BASE.json HEAD.json
Exit 0 only when the artifact populations (paths, sizes, SHA-256) are identical.
Prints the population size, total bytes and a population digest (SHA-256 over
sorted "path size sha256" lines) so independent runs can be cross-checked.
"""
import hashlib, json, sys

a, b = (json.load(open(p)) for p in sys.argv[1:3])
fa, fb = a["files"], b["files"]
diff = sorted(k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k))
lines = "".join(f"{k} {v['bytes']} {v['sha256']}\n" for k, v in sorted(fa.items()))
print(f"config={a['config']} mode={a['mode']}/{b['mode']} artifacts={len(fa)}/{len(fb)} "
      f"bytes={sum(v['bytes'] for v in fa.values())} "
      f"population_sha256={hashlib.sha256(lines.encode()).hexdigest()}")
print("argv_equal=", a["argv"] == b["argv"])
for k in diff:
    print("DIFF", k, fa.get(k), fb.get(k))
ldiff = sorted(k for k in set(a["logs"]) | set(b["logs"]) if a["logs"].get(k) != b["logs"].get(k))
print("diagnostic logs differing:", ldiff)
sys.exit(1 if diff or a["argv"] != b["argv"] else 0)
