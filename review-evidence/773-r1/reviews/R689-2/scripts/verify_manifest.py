"""Verify every published_sha256 in an evidence MANIFEST.json against the extracted tree.
Usage: python3 -I verify_manifest.py <evidence_root>"""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
man = json.loads((root / "MANIFEST.json").read_text())
listed = set(); bad = []
for e in man:
    p = root / e["file"]; listed.add(e["file"])
    if not p.is_file():
        bad.append(("missing", e["file"])); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]:
        bad.append(("mismatch", e["file"]))
on_disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
unlisted = sorted(on_disk - listed)
r2 = [f for f in listed if f.startswith("author-r2/receipts/round2/") or f.startswith("author-r2/scripts/")]
print(f"entries {len(man)} verified {len(man)-len(bad)} bad {len(bad)} unlisted {len(unlisted)} round2+scripts listed {len(r2)}")
for b in bad: print("BAD", *b)
for u in unlisted: print("UNLISTED", u)
sys.exit(1 if bad else 0)
