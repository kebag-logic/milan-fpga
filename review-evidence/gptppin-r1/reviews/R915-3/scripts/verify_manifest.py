"""Verify a published evidence MANIFEST.json: every entry's published_sha256 matches its file."""
import hashlib, json, sys, pathlib
root = pathlib.Path(sys.argv[1]); prefix = sys.argv[2] if len(sys.argv) > 2 else ""
entries = json.loads((root / "MANIFEST.json").read_text())
ok = bad = 0; listed = set()
for e in entries:
    if not e["file"].startswith(prefix): continue
    listed.add(e["file"])
    h = hashlib.sha256((root / e["file"]).read_bytes()).hexdigest()
    if h == e["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", e["file"])
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and str(p.relative_to(root)).startswith(prefix)}
unlisted = sorted(present - listed)
for u in unlisted: print("UNLISTED", u)
print(f"prefix={prefix!r} entries={ok+bad} ok={ok} mismatch={bad} unlisted={len(unlisted)}")
sys.exit(1 if bad else 0)
