#!/usr/bin/env python3
"""Independent before/after census comparison.

Usage: census_cmp.py <start.jsonl> <end.jsonl>
ACMP GET_RX_STATE / GET_TX_STATE entries are keyed by (listener or talker,
unique id); AEM responses by (command, target, request). Payload octets 2..3
of READ_DESCRIPTOR responses (reserved) are masked. Prints only-in-one-side
keys, differing keys, and the bound/unbound summary.
"""
import json, sys
from collections import OrderedDict


def load(p):
    out = OrderedDict()
    starts = []
    for line in open(p):
        j = json.loads(line)
        if j.get("type") == "start":
            starts.append(j.get("argv"))
            continue
        if j.get("type") == "acmp":
            k = ("acmp", j["query"], j["listener"] if "rx" in j["query"] else j["talker"],
                 j["listener_uid"] if "rx" in j["query"] else j["talker_uid"])
            v = {x: j[x] for x in ("status", "stream_id", "talker", "listener", "talker_uid", "conn_count", "flags", "dmac", "vlan")}
            out[k] = v
        elif j.get("type") == "aem":
            p_ = j.get("payload", "")
            if j["cmd"] == "READ_DESCRIPTOR" and len(p_) >= 8:
                p_ = p_[:4] + "xxxx" + p_[8:]
            if j["cmd"] == "GET_COUNTERS":
                continue
            out[("aem", j["cmd"], j["target"], j.get("req"))] = (j["status"], p_)
        elif j.get("type") == "adp":
            out[("adp", j.get("entity_id"))] = {k: v for k, v in j.items() if k not in ("t", "available_index")}
    return out, starts


a, sa = load(sys.argv[1])
b, sb = load(sys.argv[2])
print("keys start", len(a), "end", len(b))
for k in a:
    if k not in b:
        print("ONLY-START", k)
for k in b:
    if k not in a:
        print("ONLY-END", k)
diff = [k for k in a if k in b and a[k] != b[k]]
for k in diff:
    print("DIFF", k, "\n   start", str(a[k])[:300], "\n   end  ", str(b[k])[:300])
acmp = [k for k in a if k[0] == "acmp"]
bound = [k for k in acmp if a[k]["conn_count"] or a[k]["talker"] != "0000000000000000" and k[1] == "get_rx_state"]
print("acmp states", len(acmp), "bound at start", bound,
      "bound at end", [k for k in b if k[0] == "acmp" and b[k]["conn_count"]])
print("RESULT", "IDENTICAL" if not diff and set(a) == set(b) else "DIFFERENT")
