#!/usr/bin/env python3
"""Compare two census.sh outputs (issue 117, A202).

Prints each ACMP state and each AEM read side by side. AEM payloads are
compared whole, except READ_DESCRIPTOR, whose reserved half-word after
configuration_index (the peer fills it with varying values) is masked as A200
did, and the counter,
AVB_INFO, AS_PATH and ADP records, which are expected to move and are
printed for the record rather than compared.

usage: census_compare.py <start.jsonl> <end.jsonl>
"""
import json
import sys

MOVING = {"GET_COUNTERS", "GET_AVB_INFO", "GET_AS_PATH"}


def load(p):
    acmp, aem, adp = {}, {}, {}
    for line in open(p):
        if not line.startswith("{"):
            continue
        r = json.loads(line)
        if r["type"] == "acmp":
            ent = r["talker"] if r["query"] == "get_tx_state" else r["listener"]
            uid = r["talker_uid"] if r["query"] == "get_tx_state" else r["listener_uid"]
            key = (r["query"], ent, uid)
            acmp[key] = (r["status"], r["talker"] if r["query"] == "get_rx_state" else "-", r["conn_count"])
        elif r["type"] == "aem":
            key = (r["target"], r["cmd"], r["req"])
            pl = r.get("payload", "")
            if r["cmd"] == "READ_DESCRIPTOR":
                pl = pl[:4] + "xxxx" + pl[8:]
            aem[key] = (r["status"], pl, r.get("decoded"))
        elif r["type"] == "adp":
            adp[(r["entity_id"], r["interface_index"])] = (r["gptp_gm"], r["available_index"])
    return acmp, aem, adp


def main():
    a0, e0, d0 = load(sys.argv[1])
    a1, e1, d1 = load(sys.argv[2])
    same = 0
    for k in sorted(set(a0) | set(a1)):
        ok = a0.get(k) == a1.get(k)
        same += ok
        print(f"ACMP {k}: start {a0.get(k)} end {a1.get(k)} {'SAME' if ok else 'DIFFERENT'}")
    print(f"ACMP states identical: {same} of {len(set(a0) | set(a1))}")
    fixed = moving = 0
    for k in sorted(set(e0) | set(e1)):
        s0, s1 = e0.get(k), e1.get(k)
        if k[1] in MOVING:
            moving += 1
            print(f"AEM {k}: start {s0[2] if s0 and s0[2] else (s0[1][:80] if s0 else None)} "
                  f"end {s1[2] if s1 and s1[2] else (s1[1][:80] if s1 else None)} (moving, recorded)")
            continue
        ok = s0 is not None and s1 is not None and s0[:2] == s1[:2]
        fixed += ok
        print(f"AEM {k}: {'SAME' if ok else 'DIFFERENT'} {'' if ok else (s0, s1)}")
    print(f"AEM settings reads identical: {fixed} of {len(set(e0) | set(e1)) - moving}")
    for k in sorted(set(d0) | set(d1)):
        print(f"ADP {k}: start {d0.get(k)} end {d1.get(k)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
