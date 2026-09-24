#!/usr/bin/env python3
"""Summarize the controller-host logs of the soak (issue 387, A249). Offline.

watch.jsonl (avdecc_ro.py watch): per entity, GET_AVB_INFO status counts, as_capable, GM,
flags, propagation delay statistics, GET_AS_PATH values, response times, and ADP GM ids.
counters.jsonl (a231_counters_poll.py): per descriptor, status counts, counters_valid, first
and last value of every counter, and every change with the controller-host time.

usage: a249_ctrl_summary.py --watch watch.jsonl --counters counters.jsonl
"""
import json
import statistics as st
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%H:%M:%S.%f")[:-3] + "Z"


def load(p):
    out = []
    for line in open(p):
        if line.startswith("{"):
            out.append(json.loads(line))
    return out


def watch(p):
    recs = load(p)
    print(f"== watch {p}: {len(recs)} records")
    by = defaultdict(list)
    adp = Counter()
    for r in recs:
        if r.get("type") in ("avb_info", "as_path"):
            by[(r["target"], r["type"])].append(r)
        elif r.get("type") == "adp":
            adp[(r["entity_id"], r["gptp_gm"])] += 1
    for (tgt, kind), rows in sorted(by.items()):
        stc = Counter(r["status"] for r in rows)
        ok = [r for r in rows if r["status"] == "SUCCESS"]
        print(f"  {tgt} {kind}: status {dict(stc)}; first {iso(rows[0]['t'])} last {iso(rows[-1]['t'])}")
        if kind == "avb_info" and ok:
            vals = Counter(json.dumps({k: v for k, v in r["decoded"].items() if k != "pdelay_ns"},
                                      sort_keys=True) for r in ok)
            for v, n in vals.items():
                print(f"     x{n} {v}")
            pd = [r["decoded"]["pdelay_ns"] for r in ok]
            print(f"     pdelay_ns n={len(pd)} median={st.median(pd)} min={min(pd)} max={max(pd)}")
        if kind == "as_path" and ok:
            vals = Counter(json.dumps(r["decoded"], sort_keys=True) for r in ok)
            for v, n in vals.items():
                print(f"     x{n} {v}")
        rt = [r["rtt_ms"] for r in ok]
        if rt:
            print(f"     response ms median={st.median(rt):.3f} max={max(rt):.3f}")
    print(f"  ADP (entity, gptp_gm) seen: {dict(adp)}")


def counters(p):
    recs = load(p)
    rows = [r for r in recs if r.get("type") == "counters"]
    done = [r for r in recs if r.get("type") == "done"]
    print(f"== counters {p}: {len(rows)} answers, done {done}")
    by = defaultdict(list)
    for r in rows:
        by[(r["target"], r["req_type"], r["req_index"])].append(r)
    for key, rs in sorted(by.items()):
        stc = Counter(r["status"] for r in rs)
        ok = [r for r in rs if r["status"] == "SUCCESS"]
        print(f"  {key[0]} type {key[1]:#06x} index {key[2]}: status {dict(stc)}; "
              f"first {iso(rs[0]['t'])} last {iso(rs[-1]['t'])}")
        if not ok:
            continue
        valid = Counter(r["decoded"]["counters_valid"] for r in ok)
        unclaimed = sum(1 for r in ok if r["decoded"]["nonzero_unclaimed"])
        print(f"     counters_valid {dict(valid)}; answers with a non-zero unclaimed quadlet: {unclaimed}")
        names = list(ok[0]["decoded"]["counters"].keys())
        for n in names:
            seq = [(r["t"], r["decoded"]["counters"].get(n)) for r in ok]
            ch = [(iso(a[0]), a[1], iso(b[0]), b[1]) for a, b in zip(seq, seq[1:]) if a[1] != b[1]]
            print(f"     {n:20s} first {seq[0][1]} last {seq[-1][1]} changes {len(ch)} {ch[:6]}")


def main():
    a = sys.argv[1:]
    if "--watch" in a:
        watch(a[a.index("--watch") + 1])
    if "--counters" in a:
        counters(a[a.index("--counters") + 1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
