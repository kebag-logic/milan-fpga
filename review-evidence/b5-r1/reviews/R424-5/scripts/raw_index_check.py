#!/usr/bin/env python3
"""Check each artifact-table row's Bytes cell against RAW-ARTIFACTS.json by SHA-256.

Usage: raw_index_check.py <page.md> <RAW-ARTIFACTS.json> [<lane packet dir>]
A row whose hash is not indexed is resolved when one lane-packet file quotes
its hash and its page size together.
Prints row label, whether the hash is indexed, and whether the size agrees;
for withheld rows it prints only whether the index withholds the size too
(an integer in the index for a withheld row is a failure, value not printed).
"""
import json
import os
import re
import sys

ROW = re.compile(r"^\| (.+?) \| (withheld|[0-9]+) \| `([0-9a-f]{64})` \|$", re.M)


def main(page, index, root=None):
    files = json.load(open(index))["files"]
    by_hash = {f["sha256"]: f for f in files}
    bad = 0
    rows = ROW.findall(open(page, encoding="utf-8").read())
    for label, size, h in rows:
        f = by_hash.get(h)
        if f is None:
            both = []
            if root and size != "withheld":
                for d, _, fs in os.walk(root):
                    for n in fs:
                        t = open(os.path.join(d, n), encoding="utf-8", errors="ignore").read()
                        if h in t and re.search(r"(?<![0-9])%s(?![0-9])" % size, t):
                            both.append(os.path.relpath(os.path.join(d, n), root))
            if both:
                print(f"{label}: not a raw-index entry; hash and page size quoted together in {len(both)} lane-packet file(s), e.g. {sorted(both)[0]}")
            else:
                bad += 1
                print(f"{label}: hash NOT indexed and not quoted with its size")
            continue
        b = f.get("bytes")
        if size == "withheld":
            ok = not isinstance(b, int)
            print(f"{label}: withheld on the page; index size withheld too: {ok} ({type(b).__name__})")
        else:
            ok = b == int(size)
            print(f"{label}: page size equals index size: {ok}")
        bad += not ok
    withheld_idx = [f["path"] for f in files if not isinstance(f.get("bytes"), int)]
    print(f"rows: {len(rows)}; index entries: {len(files)}; index entries with size withheld: {len(withheld_idx)}")
    for p in withheld_idx:
        print(f"  withheld in index: {p}")
    print(f"problems: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
