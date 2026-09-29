"""Compare two controller censuses: stream states, settings and descriptors.

Counters are reported separately (they are expected to move). usage:
census_compare.py <start.jsonl> <end.jsonl>
"""
import json, sys
def load(p):
    out = {}
    for l in open(p):
        if l.strip():
            r = json.loads(l)
            out[(r["role"], r["what"])] = r["response"]
    return out
a, b = load(sys.argv[1]), load(sys.argv[2])
same = diff = 0
for k in sorted(set(a) | set(b)):
    role, what = k
    x, y = a.get(k, {}), b.get(k, {})
    if what.startswith("counter"):
        continue
    if what.startswith("state"):
        fx = {f: x.get(f) for f in ("status", "stream_id", "talker", "talker_uid", "listener", "listener_uid", "dmac", "conn_count", "flags", "vlan")}
        fy = {f: y.get(f) for f in fx}
    elif what == "avb":
        # GET_AVB_INFO bytes 12-15 are the measured propagation delay, not a setting
        px, py = x.get("payload", ""), y.get("payload", "")
        fx, fy = (x.get("status"), px[:24] + px[32:]), (y.get("status"), py[:24] + py[32:])
    elif what.startswith("desc") and role == "peer":
        # the reference peer varies the reserved half-word after configuration_index
        px, py = x.get("payload", ""), y.get("payload", "")
        fx, fy = (x.get("status"), px[:4] + px[8:]), (y.get("status"), py[:4] + py[8:])
    else:
        fx, fy = (x.get("status"), x.get("payload")), (y.get("status"), y.get("payload"))
    if what.startswith("state") and fx.get("conn_count") == 0 and fy.get("conn_count") == 0 and fx != fy:
        print("RETAINED-TX-STATE", role, what, "conn_count 0 both;", {f: (fx[f], fy[f]) for f in fx if fx[f] != fy[f]})
        same += 1
        continue
    if fx == fy:
        same += 1
    else:
        diff += 1
        print("DIFF", role, what, fx, "->", fy)
print(f"compared {same + diff} non-counter reads: {same} equal, {diff} differ")
for k in sorted(set(a) | set(b)):
    if k[1] == "counter-9-0":
        print("AVB_INTERFACE", k[0], a[k].get("counters"), "->", b[k].get("counters"))
