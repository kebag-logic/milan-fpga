"""Verify the round-5 author packet: every manifest-*.jsonl entry by size and SHA256,
and every MANIFEST.json entry under author-r5 by published SHA256."""
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])  # .../review-evidence/loopbram-r1
rec = root / "author-r5" / "receipts"
bad = 0; n = 0; listed = set()
for m in sorted(rec.glob("manifest-*.jsonl")):
    for line in m.read_text().splitlines():
        e = json.loads(line); n += 1; listed.add(e["file"])
        f = rec / e["file"]
        if not f.is_file(): print("MISSING", e["file"]); bad += 1; continue
        b = f.read_bytes()
        if len(b) != e["bytes"] or hashlib.sha256(b).hexdigest() != e["sha256"]:
            print("MISMATCH", e["file"]); bad += 1
unlisted = sorted(p.name for p in rec.iterdir() if p.name not in listed and not p.name.startswith("manifest-"))
print("jsonl entries", n, "bad", bad, "unlisted receipts", len(unlisted), unlisted[:12])
man = json.loads((root / "MANIFEST.json").read_text())
r5 = [e for e in man if e["file"].startswith("author-r5/")]
mb = 0
for e in r5:
    f = root / e["file"]
    if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest() != e["published_sha256"]:
        print("MANIFEST.json MISMATCH", e["file"]); mb += 1
files = [p for p in (root / "author-r5").rglob("*") if p.is_file()]
print("MANIFEST.json author-r5 entries", len(r5), "bad", mb, "files on disk", len(files))
sys.exit(1 if bad or mb else 0)
