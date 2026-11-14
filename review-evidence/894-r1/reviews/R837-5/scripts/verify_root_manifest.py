"""Check the archive's root MANIFEST.json rows under a prefix (file, original_sha256, published_sha256, path_redacted)
against the published bytes. usage: verify_root_manifest.py MANIFEST.json ROOT PREFIX"""
import hashlib, json, sys
from pathlib import Path
rows = [r for r in json.load(open(sys.argv[1])) if r["file"].startswith(sys.argv[3])]
root = Path(sys.argv[2]); bad = 0
for r in rows:
    f = root / r["file"]; h = hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None
    ok = h == r["published_sha256"]; bad += not ok
    if not ok or r["path_redacted"] or r["original_sha256"] != r["published_sha256"]:
        print(("ok  " if ok else "BAD ") + r["file"] + f" redacted={r['path_redacted']} original={r['original_sha256'][:12]} published={r['published_sha256'][:12]}")
print(f"rows {len(rows)} bad {bad}")
sys.exit(1 if bad else 0)
