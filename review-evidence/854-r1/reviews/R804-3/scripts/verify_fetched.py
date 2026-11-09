#!/usr/bin/env python3
"""Check fetched files of the published evidence directory against its MANIFEST.json.
Usage: verify_fetched.py <directory holding MANIFEST.json and the fetched files>
Exit 0 iff every fetched file is listed with a matching published_sha256."""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
rows = {r["file"]: r for r in json.loads((root / "MANIFEST.json").read_text())}
bad = 0
for p in sorted(root.rglob("*")):
    if p.is_file() and p.name != "MANIFEST.json":
        k = str(p.relative_to(root)); h = hashlib.sha256(p.read_bytes()).hexdigest()
        ok = rows.get(k, {}).get("published_sha256") == h
        bad += not ok
        print("MATCH" if ok else "MISMATCH", h, "review-evidence/854-r1/" + k)
print(f"MANIFEST.json sha256 {hashlib.sha256((root / 'MANIFEST.json').read_bytes()).hexdigest()}, fetched at commit edebc85d43b99d3936774e5902df4142deea5bf4; {bad} problems")
sys.exit(1 if bad else 0)
