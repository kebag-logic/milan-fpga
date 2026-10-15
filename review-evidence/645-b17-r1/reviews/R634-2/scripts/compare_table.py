#!/usr/bin/env python3
"""Reviewer check: the B17 slips table on the page against the reviewer recompute (offline, read-only).

usage: compare_table.py <page.md> <recompute-r2.jsonl> <author_packet_dir>
Compares cells 3 (poll coverage), 4 (SLIP_LB dups) and 5 (slip interval and counts) of every row, and the
largest-lateness cell against the grade's interval maximum rounded once to 0.1 us; prints the raw values of
c08's slip interval and c09's last poll.
"""
import json
import sys
from pathlib import Path

page = Path(sys.argv[1]).read_text().splitlines()
rec = [json.loads(x) for x in open(sys.argv[2])][:-1]
P = Path(sys.argv[3])
bad = 0
for r in rec:
    row = [x for x in page if x.startswith(f"| {r['cycle']} | 07:") and x.count("|") == 11]
    assert len(row) == 1, r["cycle"]
    cells = [c.strip() for c in row[0].strip("|").split("|")]
    want = {3: f"{r['polls']}, {r['first']} to {r['last']}", 4: f"{r['lb_first']} to {r['lb_last']}",
            5: f"{r['slip']}, +{r['dd']} dups, {r['ds']} skips", 9: f"{r['lat_in_interval']:.1f} us"}
    for i, w in want.items():
        ok = cells[i] == w
        bad += not ok
        print(("ok  " if ok else "FAIL"), r["cycle"], i, repr(cells[i]), repr(w))


def raw(c):
    ev = [json.loads(x) for x in open(P / "cycles" / c / "events.jsonl")]
    tb = [e for e in ev if e["kind"] == "bind"][0]["t_cmd_local"]
    pl = sorted((json.loads(x) for x in open(P / "cycles" / c / "poll.jsonl")), key=lambda r: r["n"])
    lb = [int(r["words"]["0x8d4"], 16) for r in pl]
    i = next(k for k in range(1, len(pl)) if lb[k] != lb[k - 1])
    return dict(slip_lo=pl[i - 1]["t0"] - tb, slip_hi=pl[i]["t1"] - tb, last=pl[-1]["t1"] - tb)


print("raw c08", json.dumps(raw("c08")))
print("raw c09", json.dumps(raw("c09")))
print("mismatches:", bad)
sys.exit(1 if bad else 0)
