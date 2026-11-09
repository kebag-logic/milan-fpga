#!/usr/bin/env python3
"""Verify every file of a published evidence directory against its MANIFEST.json.
Usage: verify_evidence_manifest.py <evidence-dir> [prefix]
Exit 0 iff every listed file exists with its published_sha256 and no unlisted
file is present (under the prefix, when one is given)."""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); prefix = sys.argv[2] if len(sys.argv) > 2 else ""
rows = json.loads((root / "MANIFEST.json").read_text())
listed = {r["file"]: r for r in rows}
bad = 0; checked = 0
for name, r in listed.items():
    if not name.startswith(prefix):
        continue
    p = root / name
    if not p.is_file():
        print("MISSING", name); bad += 1; continue
    h = hashlib.sha256(p.read_bytes()).hexdigest(); checked += 1
    if h != r["published_sha256"]:
        print("MISMATCH", name); bad += 1
on_disk = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"MANIFEST.json"}
extra = sorted(n for n in on_disk - set(listed) if n.startswith(prefix))
for n in extra:
    print("UNLISTED", n); bad += 1
red = sum(1 for n, r in listed.items() if n.startswith(prefix) and r.get("path_redacted"))
print(f"checked {checked} files under '{prefix or '*'}', {bad} problems, {red} path-redacted")
sys.exit(1 if bad else 0)
