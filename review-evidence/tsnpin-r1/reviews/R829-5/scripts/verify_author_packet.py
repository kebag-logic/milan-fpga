"""Check the author-r4 part of review-evidence/tsnpin-r1/MANIFEST.json against an extracted copy of the archive.
Usage: python3 -I verify_author_packet.py <extracted review-evidence/tsnpin-r1 dir> [prefix]"""
import hashlib, json, os, sys
root = sys.argv[1]; prefix = sys.argv[2] if len(sys.argv) > 2 else "author-r4/"
entries = [e for e in json.load(open(os.path.join(root, "MANIFEST.json"))) if e["file"].startswith(prefix)]
bad, missing = [], []
for e in entries:
    p = os.path.join(root, e["file"])
    if not os.path.exists(p):
        missing.append(e["file"]); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != e["published_sha256"]:
        bad.append(e["file"])
on_disk = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(os.path.join(root, prefix)) for f in fs}
unlisted = sorted(on_disk - {e["file"] for e in entries})
print(f"{prefix}: {len(entries)} listed, {len(missing)} missing, {len(bad)} hash mismatches, {len(unlisted)} unlisted, "
      f"{sum(e['path_redacted'] for e in entries)} marked path_redacted")
for x in missing + bad + unlisted:
    print("  ", x)
