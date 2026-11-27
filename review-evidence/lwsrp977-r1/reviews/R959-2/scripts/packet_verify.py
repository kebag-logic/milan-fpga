#!/usr/bin/env python3
"""packet_verify.py <packet-root>: check every author-r2 file against the
publication MANIFEST.json (published_sha256), and the author's own
receipts/INDEX.md sha256 list against the manifest's original_sha256 (the
published copies of path-redacted files differ from the originals by design)."""
import hashlib, json, os, re, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
entries = {e["file"]: e for e in m if e["file"].startswith("author-r2/")}
on_disk = []
for d, _, fs in os.walk(os.path.join(root, "author-r2")):
    on_disk += [os.path.relpath(os.path.join(d, f), root) for f in fs]
ok = bad = 0
for f in sorted(on_disk):
    e = entries.get(f)
    h = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    if e is None:
        print(f"UNLISTED {f}"); bad += 1
    elif h == e["published_sha256"]:
        ok += 1
    else:
        print(f"PUBLISHED-MISMATCH {f}"); bad += 1
print(f"manifest: {len(entries)} author-r2 entries; files {len(on_disk)}; published hash ok {ok}; problems {bad}; "
      f"path-redacted {sum(e['path_redacted'] for e in entries.values())}")
idx = {}
for line in open(os.path.join(root, "author-r2/receipts/INDEX.md")):
    mm = re.match(r"^([0-9a-f]{64})  \./(.*)$", line.strip())
    if mm:
        idx["author-r2/receipts/" + mm.group(2)] = mm.group(1)
orig = pub = neither = 0
for f, h in sorted(idx.items()):
    e = entries.get(f)
    if e and h == e["original_sha256"]:
        orig += 1
    elif e and h == e["published_sha256"]:
        pub += 1
    else:
        neither += 1
        print(f"INDEX-MISMATCH {f}: index {h} manifest original {e and e['original_sha256']} published {e and e['published_sha256']}")
print(f"INDEX.md: {len(idx)} entries; equal to manifest original {orig}; equal to published only {pub}; matching neither {neither}")
sys.exit(1 if bad or neither else 0)
