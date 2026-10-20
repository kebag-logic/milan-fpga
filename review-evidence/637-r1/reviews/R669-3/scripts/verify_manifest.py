"""Hash each downloaded evidence file against the published MANIFEST.json.
Usage: python3 -I verify_manifest.py <evidence-dir>  (dir holds MANIFEST.json and files by manifest path)"""
import hashlib, json, os, sys
root = sys.argv[1]
entries = {e["file"]: e for e in json.load(open(os.path.join(root, "MANIFEST.json")))}
ok = bad = 0
for dp, _d, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), root)
        if rel == "MANIFEST.json":
            continue
        e = entries.get(rel)
        h = hashlib.sha256(open(os.path.join(dp, f), "rb").read()).hexdigest()
        good = e is not None and h == e["published_sha256"]
        ok += good; bad += not good
        print(("OK  " if good else "BAD ") + rel + ("" if e else " (not in manifest)")
              + (" redacted" if e and e.get("path_redacted") else ""))
print(f"ok {ok} bad {bad}")
sys.exit(1 if bad else 0)
