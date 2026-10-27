"""Check every MANIFEST.json entry's published_sha256 and list unlisted files. Usage: verify_manifest.py <packet-root>"""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
m = json.loads((root / "MANIFEST.json").read_text())
listed = {e["file"] for e in m}
bad = [e["file"] for e in m if not (root / e["file"]).is_file() or
       hashlib.sha256((root / e["file"]).read_bytes()).hexdigest() != e["published_sha256"]]
files = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
print(f"entries={len(m)} mismatched_or_missing={len(bad)} unlisted={len(files - listed)}")
for b in bad[:20]: print("BAD", b)
for u in sorted(files - listed)[:20]: print("UNLISTED", u)
r6 = [e for e in m if e["file"].startswith("author-r6/")]
print(f"author-r6 entries={len(r6)} mismatched={sum(1 for e in r6 if e['file'] in bad)}")
