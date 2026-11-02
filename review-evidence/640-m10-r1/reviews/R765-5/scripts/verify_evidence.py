"""Check checked-out evidence files against MANIFEST.json and SHA256SUMS.

Usage: python3 -I verify_evidence.py <evidence-root> <subdir-prefix> [<subdir-prefix> ...]
"""
import hashlib, json, os, sys

root = sys.argv[1]
prefixes = sys.argv[2:]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
idx = {e["file"]: e for e in man}
ok = bad = unlisted = 0
for dp, _, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), root)
        if rel == "MANIFEST.json" or not any(rel.startswith(p) for p in prefixes):
            continue
        h = hashlib.sha256(open(os.path.join(dp, f), "rb").read()).hexdigest()
        e = idx.get(rel)
        if e is None:
            unlisted += 1
            print("UNLISTED", rel)
        elif e["published_sha256"] == h:
            ok += 1
        else:
            bad += 1
            print("MISMATCH", rel)
listed = [k for k in idx if any(k.startswith(p) for p in prefixes)]
print(f"manifest entries under prefixes: {len(listed)}; on disk ok={ok} mismatch={bad} unlisted={unlisted}")
for p in prefixes:
    sums = os.path.join(root, p, "evidence", "SHA256SUMS")
    if not os.path.exists(sums):
        continue
    n = m = red = 0
    for line in open(sums):
        line = line.rstrip("\n")
        if not line:
            continue
        digest, name = line.split(None, 1)
        name = name.lstrip("*")
        rel = os.path.join(p, "evidence", name)
        n += 1
        e = idx.get(os.path.normpath(rel))
        if e is None:
            print("SUMS-NOT-IN-MANIFEST", rel); m += 1
        elif digest == e["published_sha256"]:
            pass
        elif digest == e["original_sha256"] and e.get("path_redacted"):
            red += 1
        else:
            print("SUMS-MISMATCH", rel); m += 1
    print(f"{p}: SHA256SUMS lines={n} unexplained={m} redacted-original-match={red}")
