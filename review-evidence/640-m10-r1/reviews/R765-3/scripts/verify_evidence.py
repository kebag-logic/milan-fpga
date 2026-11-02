"""Check a published evidence subtree against MANIFEST.json and its SHA256SUMS.

usage: python3 -I verify_evidence.py <evidence-root> <subdir>
"""
import hashlib, json, os, sys

root, sub = sys.argv[1], sys.argv[2]
man = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
bad = missing = ok = 0
seen = set()
for dp, _, fs in os.walk(os.path.join(root, sub)):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), root)
        seen.add(rel)
        h = hashlib.sha256(open(os.path.join(root, rel), "rb").read()).hexdigest()
        e = man.get(rel)
        if e is None:
            print("NOT-IN-MANIFEST", rel); missing += 1
        elif e["published_sha256"] != h:
            print("MISMATCH", rel); bad += 1
        else:
            ok += 1
for rel in man:
    if rel.startswith(sub + "/") and rel not in seen:
        print("MISSING-FILE", rel); missing += 1
sums = os.path.join(root, sub, "evidence", "SHA256SUMS")
sbad = sok = 0
for line in open(sums):
    h, p = line.split(None, 1)
    rel = os.path.normpath(os.path.join(sub, "evidence", p.strip()))
    e = man.get(rel)
    if e is None:
        print("SUMS-ENTRY-NOT-PUBLISHED", rel); sbad += 1
    elif e["original_sha256"] != h:
        print("SUMS-MISMATCH", rel); sbad += 1
    else:
        sok += 1
print(f"files ok={ok} mismatch={bad} missing={missing}; SHA256SUMS ok={sok} bad={sbad}")
sys.exit(1 if bad or missing or sbad else 0)
