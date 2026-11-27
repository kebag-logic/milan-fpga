#!/usr/bin/env python3
"""packet_verify_r3.py <packet-root>: check every author-r3 file against the
publication MANIFEST.json (published_sha256), and the author-r3
receipts/INDEX.md table (| path | sha256 |, relative to author-r3/) against
the manifest's original_sha256 and published_sha256."""
import hashlib, json, os, re, sys
root = sys.argv[1]
m = json.load(open(os.path.join(root, "MANIFEST.json")))
entries = {e["file"]: e for e in m if e["file"].startswith("author-r3/")}
on_disk = []
for d, _, fs in os.walk(os.path.join(root, "author-r3")):
    on_disk += [os.path.relpath(os.path.join(d, f), root) for f in fs]
ok = bad = 0
hashes = {}
for f in sorted(on_disk):
    h = hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest()
    hashes[f] = h
    e = entries.get(f)
    if e is None:
        print(f"UNLISTED {f}"); bad += 1
    elif h == e["published_sha256"]:
        ok += 1
    else:
        print(f"PUBLISHED-MISMATCH {f}"); bad += 1
missing = [f for f in entries if f not in hashes]
for f in missing:
    print(f"MANIFEST-ONLY {f}"); bad += 1
print(f"manifest: {len(entries)} author-r3 entries; files {len(on_disk)}; published hash ok {ok}; problems {bad}; "
      f"path-redacted {sum(e['path_redacted'] for e in entries.values())}")
idx = {}
for line in open(os.path.join(root, "author-r3/receipts/INDEX.md")):
    mm = re.match(r"^\|\s*([^|]+?)\s*\|\s*([0-9a-f]{64})\s*\|$", line.strip())
    if mm:
        idx["author-r3/" + mm.group(1)] = mm.group(2)
orig = pub = neither = 0
for f, h in sorted(idx.items()):
    e = entries.get(f)
    if e and h == e["original_sha256"]:
        orig += 1
    elif e and h == e["published_sha256"]:
        pub += 1
    else:
        neither += 1
        print(f"INDEX-MISMATCH {f}: index {h} manifest {e and (e['original_sha256'], e['published_sha256'])}")
notidx = [f for f in on_disk if f not in idx and f != "author-r3/receipts/INDEX.md"]
for f in notidx:
    print(f"NOT-IN-INDEX {f}")
print(f"INDEX.md: {len(idx)} entries; equal to manifest original {orig}; equal to published only {pub}; matching neither {neither}; delivered files not indexed {len(notidx)}")
sys.exit(1 if bad or neither else 0)
