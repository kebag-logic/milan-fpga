# verify_manifest.py <evidence-root>: check every downloaded file against MANIFEST.json published_sha256
import hashlib, json, os, sys
root = sys.argv[1]
d = json.load(open(os.path.join(root, "MANIFEST.json")))
ok = bad = absent = 0
for e in d:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        absent += 1
        continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == e["published_sha256"]:
        ok += 1
    else:
        bad += 1
        print("MISMATCH", e["file"])
print(f"verified={ok} mismatched={bad} not-downloaded={absent} entries={len(d)}")
sys.exit(1 if bad else 0)
