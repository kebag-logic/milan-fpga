#!/usr/bin/env python3
"""Resolve every SHA-256 on the page against the pinned archive manifest.

Usage: hash_check.py <page.md> <manifest.json> <archive b5-r1 dir>
Each 64-hex value is classified as a manifest original_sha256 (and of which
file), a manifest published_sha256, or quoted inside published packet files.
Prints labels and file paths only; exits 1 on any unresolved value.
"""
import json
import os
import re
import sys


def main(page, manifest, root):
    text = open(page, encoding="utf-8").read()
    values = list(dict.fromkeys(re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", text)))
    entries = json.load(open(manifest))
    files = []
    for top in ("author", "author-r2", "author-r3"):
        for d, _, fs in os.walk(os.path.join(root, top)):
            files += [os.path.join(d, f) for f in fs]
    problems = 0
    print(f"page SHA-256 values: {len(values)}")
    for v in values:
        orig = [e for e in entries if e["original_sha256"] == v]
        pub = [e for e in entries if e["published_sha256"] == v]
        line = text[: text.index(v)].count("\n") + 1
        if orig or pub:
            e = (orig or pub)[0]
            kind = "original" if orig else "published"
            same = e["original_sha256"] == e["published_sha256"]
            print(f":{line} {v[:8]} manifest {kind}_sha256 of {e['file']} "
                  f"(path_redacted={e['path_redacted']}, published==original: {same})")
            continue
        hits = []
        for f in files:
            try:
                if v in open(f, encoding="utf-8", errors="ignore").read():
                    hits.append(os.path.relpath(f, root))
            except OSError:
                pass
        if hits:
            print(f":{line} {v[:8]} quoted in {len(hits)} published file(s), e.g. {sorted(hits)[0]}")
        else:
            problems += 1
            print(f":{line} {v[:8]} UNRESOLVED")
    print(f"problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
