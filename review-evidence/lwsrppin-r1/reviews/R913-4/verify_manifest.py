#!/usr/bin/env python3
"""Check a published evidence tree against its MANIFEST.json (file, original_sha256, published_sha256, path_redacted)
and against the author's INDEX.md prefixes (which hash the originals).

Usage: python3 -I verify_manifest.py <MANIFEST.json> <evidence-root> <subdir-prefix e.g. author-r3/>
"""
import hashlib, json, pathlib, re, sys
man = json.load(open(sys.argv[1])); root = pathlib.Path(sys.argv[2]); pre = sys.argv[3]
rows = [r for r in man if r["file"].startswith(pre)]
idx = {}
ip = root / pre / "receipts/INDEX.md"
if ip.is_file():
    idx = {p: h for p, _, h in re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{16})` \|", ip.read_text(), re.M)}
bad = 0
for r in rows:
    f = root / r["file"]
    h = hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file() else None
    ok = h == r["published_sha256"]
    rel = r["file"][len(pre) + len("receipts/"):] if r["file"].startswith(pre + "receipts/") else None
    iok = "n/a" if rel not in idx else ("orig-match" if r["original_sha256"].startswith(idx[rel]) else "ORIG-MISMATCH")
    if not ok or iok == "ORIG-MISMATCH" or r["path_redacted"] != (r["original_sha256"] != r["published_sha256"]):
        bad += 1
    print(f"{'OK' if ok else 'BAD'} redacted={r['path_redacted']} index={iok} {r['file']}")
on_disk = {str(p.relative_to(root)) for p in (root / pre).rglob("*") if p.is_file()}
missing = sorted(on_disk - {r['file'] for r in rows})
for m in missing: print("NOT-IN-MANIFEST", m)
print(f"rows={len(rows)} bad={bad} not_in_manifest={len(missing)} redacted={sum(r['path_redacted'] for r in rows)}")
sys.exit(1 if bad or missing else 0)
