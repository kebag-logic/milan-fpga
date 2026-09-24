#!/usr/bin/env python3
"""Compare the A200 ACMP binding census before and after the runs.

Usage: recheck_census.py <bench-a200/bench directory>

Keys each ACMP answer by direction, entity and unique id, and prints the
state count, any non-zero connection count, and every field that differs.
"""
import json
import sys
from pathlib import Path

FIELDS = ("status", "talker", "listener", "talker_uid", "listener_uid", "dmac",
          "conn_count", "flags", "vlan", "stream_id")


def acmp(path):
    out = {}
    for ln in path.read_text().splitlines():
        r = json.loads(ln)
        if r.get("type") != "acmp":
            continue
        if r["query"] == "get_rx_state":
            key = ("rx", r["listener"], r["listener_uid"])
        else:
            key = ("tx", r["talker"], r["talker_uid"])
        out[key] = {f: r.get(f) for f in FIELDS}
    return out


def main():
    base = Path(sys.argv[1])
    a = acmp(base / "census-start.jsonl")
    b = acmp(base / "final" / "census-final.jsonl")
    print(f"ACMP states start {len(a)} end {len(b)} same set {set(a) == set(b)}")
    for side, pre in (("peer", "3cc0"), ("dut", "0200")):
        for d in ("rx", "tx"):
            print(f"  {side} {d} uids {sorted(k[2] for k in a if k[0] == d and k[1].startswith(pre))}")
    print(f"non-zero conn_count start {[k for k in a if a[k]['conn_count']]} end {[k for k in b if b[k]['conn_count']]}")
    for k in sorted(a):
        diff = {f: (a[k][f], b[k][f]) for f in FIELDS if a[k][f] != b.get(k, {}).get(f)}
        if diff:
            print(f"differs {k} {diff}")


if __name__ == "__main__":
    main()
