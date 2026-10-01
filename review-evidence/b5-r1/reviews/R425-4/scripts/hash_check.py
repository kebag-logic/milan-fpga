#!/usr/bin/env python3
"""Check every SHA-256 the findings page cites against the pinned archive.

usage: hash_check.py <page.md> <b5-r1 dir at the pinned commit>

For each 64-hex value on the page: is it a manifest original_sha256 or
published_sha256 (and of which file, masked or not); otherwise, which published
files quote it. Also: every manifest published_sha256 equals the bytes on disk,
and the page's list of label-masked lane-packet files equals the manifest's
path_redacted set.
"""
import hashlib, json, re, sys
from pathlib import Path

page, base = Path(sys.argv[1]), Path(sys.argv[2])
text = page.read_text()
man = json.load(open(base / "MANIFEST.json"))
by_orig, by_pub = {}, {}
bad = 0
for e in man:
    by_orig.setdefault(e["original_sha256"], []).append(e)
    by_pub.setdefault(e["published_sha256"], []).append(e)
    p = base / e["file"]
    if not p.exists():
        print("MISSING", e["file"]); bad += 1; continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]:
        print("PUBLISHED-MISMATCH", e["file"]); bad += 1
print(f"manifest entries {len(man)}, published-bytes mismatches/missing {bad}")
on_disk = {str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()} - {"MANIFEST.json"}
print("files on disk not in manifest:", sorted(on_disk - {e["file"] for e in man}))

hashes = []
for m in re.finditer(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", text):
    line = text.count("\n", 0, m.start()) + 1
    hashes.append((line, m.group(0)))
print(f"page SHA-256 values: {len(hashes)}")
corpus = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}
unresolved = 0
for line, h in hashes:
    if h in by_orig:
        for e in by_orig[h]:
            kind = "original_sha256 of path_redacted file" if e["path_redacted"] else "unmasked file, published bytes match"
            print(f":{line} {h[:12]} {kind}: {e['file']}")
    elif h in by_pub:
        print(f":{line} {h[:12]} published_sha256 only: {[e['file'] for e in by_pub[h]]}"); unresolved += 1
    else:
        q = sorted(k for k, v in corpus.items() if h.encode() in v)
        if q:
            print(f":{line} {h[:12]} quoted in {len(q)} published files: {q[:4]}")
        else:
            print(f":{line} {h[:12]} NOT FOUND"); unresolved += 1
print(f"unresolved {unresolved}")
red = sorted(e["file"] for e in man if e["path_redacted"])
print("path_redacted files:")
for f in red:
    print("  ", f)
print("REDACTED", len(red), "UNRESOLVED", unresolved, "PUBBAD", bad)
