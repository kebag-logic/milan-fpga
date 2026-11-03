"""Check fetched author receipts against the published evidence MANIFEST.json.
Usage: python3 -I verify_author_receipts.py MANIFEST.json PREFIX FILE..."""
import hashlib, json, os, sys
manifest = {entry["file"]: entry for entry in json.load(open(sys.argv[1]))}
for path in sys.argv[3:]:
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
    entry = manifest.get(sys.argv[2] + os.path.basename(path))
    state = "MISSING" if entry is None else ("OK" if entry["published_sha256"] == digest else "MISMATCH")
    print(os.path.basename(path), digest, state)
