#!/usr/bin/env python3
"""Compare a recipe input manifest's non-generated files with a checkout's bytes.

Usage: python3 -I verify_route_manifest.py <manifest.json> <repo checkout> [<second manifest.json>]
Prints one line per file that is missing or differs, then a summary.  With a
second manifest, also prints the files whose digests differ between the two.
Exit 0 when every non-generated file matches the checkout.
"""
import hashlib
import json
import sys
from pathlib import Path


def entries(path):
    m = json.loads(Path(path).read_text())
    out = {}
    for e in m["files"]:
        name = e["file"].split("/", 1)[1] if e["file"].startswith("$ROOT") else e["file"]
        out[name] = e
    return m, out


man, files = entries(sys.argv[1])
repo = Path(sys.argv[2])
bad = gen = ok = 0
for name, e in sorted(files.items()):
    if e.get("generated"):
        gen += 1
        continue
    p = repo / name
    if not p.is_file():
        print("MISSING", name)
        bad += 1
        continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["sha256"]:
        print("DIFFERS", name)
        bad += 1
    else:
        ok += 1
print(f"manifest {sys.argv[1]}: {ok} match, {bad} differ/missing, {gen} generated (not checked), "
      f"{len(man['images'])} images, inputs_sha256 {man['inputs_sha256']}")
if len(sys.argv) > 3:
    man2, files2 = entries(sys.argv[3])
    for name in sorted(set(files) | set(files2)):
        a, b = files.get(name), files2.get(name)
        if a is None or b is None or a["sha256"] != b["sha256"]:
            print("BETWEEN-MANIFESTS", name, "only-first" if b is None else "only-second" if a is None else "digest")
    im1 = {i["name"]: i["sha256"] for i in man["images"]}
    im2 = {i["name"]: i["sha256"] for i in man2["images"]}
    print("images equal between manifests:", im1 == im2, "generics equal:", man["generics"] == man2["generics"])
sys.exit(1 if bad else 0)
