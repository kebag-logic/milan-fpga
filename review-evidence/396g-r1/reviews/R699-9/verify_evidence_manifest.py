"""Usage: python3 -I verify_evidence_manifest.py <evidence root containing MANIFEST.json> [prefix]
Checks published_sha256 of every listed file (optionally only those under prefix) and lists unlisted files."""
import hashlib, json, os, sys
root = sys.argv[1]; pre = sys.argv[2] if len(sys.argv) > 2 else ""
m = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in m}
bad = ok = 0
for f, e in sorted(listed.items()):
    if not f.startswith(pre): continue
    p = os.path.join(root, f)
    h = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else "MISSING"
    if h == e["published_sha256"]: ok += 1
    else: bad += 1; print("MISMATCH", f, h)
unlisted = [os.path.relpath(os.path.join(d, n), root) for d, _, ns in os.walk(root) for n in ns]
unlisted = [u for u in unlisted if u.startswith(pre) and u not in listed and u != "MANIFEST.json"]
print(f"prefix={pre!r} listed_ok={ok} mismatched={bad} unlisted={len(unlisted)}")
for u in unlisted[:10]: print("UNLISTED", u)
