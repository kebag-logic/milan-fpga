#!/usr/bin/env python3
"""Raw-capture identity chain: packet index, per-action records and page rows.

Usage: raw_index_check.py <packet author dir> <repo clone>

Checks that RAW-ARTIFACTS.json lists 112 captures whose sizes sum to its
total_bytes, that every per-action raw-artifacts.json agrees with it, and that
the capture-hash tables on the two findings pages carry exactly the same
(identifier, bytes, sha256) rows. The raw captures themselves stay outside
the public packet, so their bytes are not re-hashed here.
"""
import json
import re
import sys
from pathlib import Path


def main():
    pkt, repo = Path(sys.argv[1]), Path(sys.argv[2])
    idx = json.load(open(pkt / "RAW-ARTIFACTS.json"))
    rows = {(f["path"], f["size"], f["sha256"]) for f in idx["files"]}
    total = sum(f["size"] for f in idx["files"])
    print("location:", idx["location"])
    print("index files", len(idx["files"]), "total_bytes", idx["total_bytes"], "sum", total)
    per = set()
    for p in sorted(pkt.glob("*/*/raw-artifacts.json")):
        per |= {(f["path"], f["size"], f["sha256"]) for f in json.load(open(p))}
    print("per-action entries", len(per), "agree with index", per == rows)
    page = set()
    pat = re.compile(r"^\| `([a-z0-9-]+/tap\.pcap)` \| (\d+) \| `([0-9a-f]{64})` \|$")
    for name in ("606_FIRST_BIND_MEASUREMENT.md", "608_75_WITHDRAWAL_AND_RESTART.md"):
        for line in (repo / "docs/findings" / name).read_text().splitlines():
            m = pat.match(line)
            if m:
                page.add((m.group(1), int(m.group(2)), m.group(3)))
    print("page rows", len(page), "page == index", page == rows)
    print("only in index", sorted(rows - page)[:5], "only in page", sorted(page - rows)[:5])
    ok = len(rows) == 112 and total == idx["total_bytes"] and per == rows and page == rows
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
