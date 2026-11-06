"""Check every author-r3/ file of the published evidence against MANIFEST.json.
usage: python3 -I verify_evidence_manifest.py <pp212-r1 dir>"""
import hashlib, json, os, sys
root = sys.argv[1]
d = json.load(open(os.path.join(root, "MANIFEST.json")))
r3 = [e for e in d if e["file"].startswith("author-r3/")]
ok = bad = miss = 0
for e in r3:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        miss += 1; print("MISSING", e["file"]); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() == e["published_sha256"]:
        ok += 1
    else:
        bad += 1; print("BAD", e["file"])
listed = {e["file"] for e in r3}
unl = [os.path.relpath(os.path.join(r, f), root) for r, _, fs in os.walk(os.path.join(root, "author-r3")) for f in fs]
unl = [u for u in unl if u not in listed]
red = sum(1 for e in r3 if e["path_redacted"])
diff = sum(1 for e in r3 if e["original_sha256"] != e["published_sha256"])
print(f"author-r3 entries {len(r3)}: match {ok}, mismatch {bad}, missing {miss}, unlisted files {len(unl)}; "
      f"path-redacted {red}; original != published digest {diff}")
