#!/usr/bin/env python3
# verify_evidence.py ROOT PREFIX: check every MANIFEST.json entry under PREFIX against the
# downloaded file's sha256 (published_sha256), and list downloaded files under PREFIX that
# the manifest does not carry
import hashlib, json, os, sys

root, prefix = sys.argv[1], sys.argv[2]
man = json.load(open(os.path.join(root, "MANIFEST.json")))
listed = {e["file"]: e for e in man if e["file"].startswith(prefix)}
ok = bad = missing = 0
for f, e in sorted(listed.items()):
    p = os.path.join(root, f)
    if not os.path.isfile(p):
        print("MISSING", f); missing += 1; continue
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if h == e["published_sha256"]:
        ok += 1
    else:
        print("MISMATCH", f); bad += 1
    if e.get("path_redacted") or e["original_sha256"] != e["published_sha256"]:
        print("REDACTED", f)
on_disk = set()
for d, _, fs in os.walk(os.path.join(root, prefix)):
    for x in fs:
        on_disk.add(os.path.relpath(os.path.join(d, x), root))
extra = sorted(on_disk - set(listed))
for x in extra:
    print("UNLISTED", x)
print(f"prefix {prefix}: {len(listed)} listed, {ok} match, {bad} mismatch, {missing} missing, {len(extra)} unlisted")
sys.exit(1 if bad or missing or extra else 0)
