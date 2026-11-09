"""Check downloaded evidence files against the published MANIFEST.json.
Usage: python3 -I check_evidence.py <dir-with-MANIFEST.json-and-files>
Downloaded files are named with '/' replaced by '_' relative to review-evidence/854-r1/."""
import hashlib, json, sys
from pathlib import Path
d = Path(sys.argv[1])
m = {e["file"]: e for e in json.loads((d / "MANIFEST.json").read_text())}
bad = 0
for f in sorted(d.iterdir()):
    if f.name == "MANIFEST.json":
        continue
    key = next((k for k in m if k.replace("/", "_") == f.name), None)
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    ok = key is not None and m[key]["published_sha256"] == h
    bad += not ok
    red = m[key]["path_redacted"] if key else "?"
    print(f"{'MATCH' if ok else 'MISMATCH'} {h} {key or f.name} redacted={red}")
print(f"{'OK' if not bad else 'FAIL'}: {bad} mismatch(es)")
sys.exit(1 if bad else 0)
