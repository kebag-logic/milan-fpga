"""Check a published evidence tree against its MANIFEST.json, and explain each
SHA256SUMS mismatch of one sub-packet by the manifest's redaction record.
Usage: python3 -I verify_manifest.py <packet root> <sub-packet dir relative to root>"""
import hashlib, json, sys
from pathlib import Path
root, sub = Path(sys.argv[1]), sys.argv[2]
man = json.load(open(root / "MANIFEST.json"))
by = {e["file"]: e for e in man}
bad = 0
for e in man:
    p = root / e["file"]
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]:
        bad += 1; print("MANIFEST MISMATCH", e["file"])
on_disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
extra = sorted(on_disk - set(by))
for x in extra: print("NOT IN MANIFEST", x)
print("manifest entries", len(man), "mismatches", bad, "unlisted files", len(extra))
sums = root / sub / "SHA256SUMS"
unexplained = 0
for line in sums.read_text().splitlines():
    h, name = line.split(None, 1); name = name.lstrip("*").removeprefix("./")
    rel = f"{sub}/{name}"; e = by.get(rel)
    if e is None: print("SUMS ENTRY NOT PUBLISHED", rel); continue
    if h == e["published_sha256"]: continue
    if h == e["original_sha256"] and e["path_redacted"]: print("redacted, original matches SUMS:", rel); continue
    unexplained += 1; print("UNEXPLAINED", rel)
print(sub, "SHA256SUMS unexplained mismatches", unexplained)
