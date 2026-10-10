#!/usr/bin/env python3
"""Tie the round 2 raw inputs to the archived raw index.

list:  hash each raw file and print its row of raw-inputs.tsv: SHA-256, bytes,
       the raw-index file and line that holds the same digest and size, the
       path as that index publishes it, and the copy under inputs/ if any.
check: re-read every row against the archived raw index (same line, same path,
       digest and size) and re-hash every copy under inputs/. Exits 1 on any
       difference. Needs only the archived packet and this folder.

usage: inputs_vs_index.py list  <raw-index-dir> <inputs-dir> <raw-file>...
       inputs_vs_index.py check <raw-inputs.tsv> <raw-index-dir> <inputs-dir>
"""
import hashlib
import json
import os
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def index(ri):
    out = {}
    for name in sorted(os.listdir(ri)):
        if name.endswith(".jsonl"):
            for n, line in enumerate(open(os.path.join(ri, name)), 1):
                d = json.loads(line)
                out.setdefault(d["sha256"], []).append((name, n, d["path"], d["bytes"]))
    return out


def main():
    mode = sys.argv[1]
    if mode == "list":
        ri, inp, files = sys.argv[2], sys.argv[3], sys.argv[4:]
        idx = index(ri)
        print("sha256\tbytes\tindex\tline\tpublished_path\tcopy")
        bad = 0
        for p in files:
            s, b = sha(p), os.path.getsize(p)
            tail = "/".join(p.split("/")[-3:])
            hits = [h for h in idx.get(s, []) if h[3] == b and h[2].endswith(tail)]
            if len(hits) != 1:
                print(f"NOT-IN-INDEX\t{s}\t{b}\t{tail}")
                bad += 1
                continue
            name, n, pub, _ = hits[0]
            copy = os.path.basename(p) if os.path.exists(os.path.join(inp, os.path.basename(p))) else "-"
            print(f"{s}\t{b}\t{name}\t{n}\t{pub}\t{copy}")
        sys.exit(1 if bad else 0)
    if mode == "check":
        tsv, ri, inp = sys.argv[2], sys.argv[3], sys.argv[4]
        rows = [r.rstrip("\n").split("\t") for r in open(tsv)][1:]
        lines = {}
        bad = 0
        for s, b, name, n, pub, copy in rows:
            if name not in lines:
                lines[name] = open(os.path.join(ri, name)).read().splitlines()
            d = json.loads(lines[name][int(n) - 1])
            ok = d["sha256"] == s and str(d["bytes"]) == b and d["path"] == pub
            if copy != "-":
                ok = ok and sha(os.path.join(inp, copy)) == s and str(os.path.getsize(os.path.join(inp, copy))) == b
            bad += not ok
            if not ok:
                print("MISMATCH", name, n, pub)
        print(f"rows {len(rows)}; equal to the archived raw index {len(rows) - bad}; "
              f"copies under inputs/ re-hashed {sum(r[5] != '-' for r in rows)}")
        sys.exit(1 if bad else 0)
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
