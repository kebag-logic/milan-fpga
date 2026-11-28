"""Verify published_sha256 of every entry in an evidence MANIFEST.json against the files beside it.
usage: python3 -I verify_manifest.py <packet-dir>"""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
entries = json.loads((root / "MANIFEST.json").read_text())
listed = {e["file"] for e in entries}
bad = 0
for e in entries:
    got = hashlib.sha256((root / e["file"]).read_bytes()).hexdigest()
    ok = got == e["published_sha256"]
    bad += not ok
    print("OK " if ok else "BAD", e["file"])
extra = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json" and str(p.relative_to(root)) not in listed)
for x in extra: print("UNLISTED", x)
print(f"{len(entries)} entries, {bad} mismatches, {len(extra)} unlisted")
sys.exit(1 if bad or extra else 0)
