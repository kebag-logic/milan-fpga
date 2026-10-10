#!/usr/bin/env python3
"""Compare the 08:23 final reads with the 05:17-05:20 as-found reads, row by row.

As found: item2/setup/events.jsonl (kind as-found, 05:17:01) for formats, clock
sources, DUT listener states, the peer's STREAM_INPUT 0 and the DUT maps, and
restore/asfound-rx.jsonl (05:18:32) for the peer's STREAM_INPUT 8.
Final: the raw snapshot-final.jsonl (08:23:49; formats and clock sources) and
restore/final-*.jsonl (08:23:47-48; listener states and DUT map payloads).

usage: final_vs_asfound.py <packet-author-dir> <snapshot-final.jsonl>
"""
import json
import sys

A, SNAP = sys.argv[1], sys.argv[2]


def jl(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line.startswith("{"):
            out.append(json.loads(line))
    return out


af = next(d for d in jl(f"{A}/item2/setup/events.jsonl") if d["kind"] == "as-found")
asfound = {k: v for k, v in af.items() if k not in ("t", "mono_raw_ns", "kind")}
# The setup record holds listener states as connection counts; the 05:18 GET_RX_STATE
# reads give the peer's two bound inputs in full.
for uid in (0, 8):
    rx = next(d for d in jl(f"{A}/restore/asfound-rx.jsonl")
              if d.get("type") == "acmp" and d.get("listener_uid") == uid)
    full = dict(conn_count=rx["conn_count"],
                talker="dut" if rx["talker"] == "020000fffe000001" else rx["talker"],
                talker_uid=rx["talker_uid"], flags=rx["flags"])
    if uid == 0:
        assert full["conn_count"] == asfound["rx-peer-0"]
    asfound[f"rx-peer-{uid}"] = full

snap = jl(SNAP)
names = {("peer", 5, 0): "fmt-peer-in-0", ("dut", 5, 0): "fmt-dut-in-0", ("dut", 5, 1): "fmt-dut-in-1",
         ("dut", 6, 0): "fmt-dut-out-0", ("dut", 6, 1): "fmt-dut-out-1", ("peer", 6, 0): "fmt-peer-out-0",
         ("peer", 6, 2): "fmt-peer-out-2"}
final = {}
for d in snap:
    if d.get("category") == "format":
        k = names.get((d["role"], d["descriptor_type"], d["descriptor_index"]))
        if k:
            final[k] = d["value"]
    if d.get("category") == "clock":
        final[f"clk-{d['role']}"] = d["value"]
for f, key in (("final-maps", "rx-peer-0"), ("final-peer-in8", "rx-peer-8"),
               ("final-dut-in0", "rx-dut-0"), ("final-dut-in1", "rx-dut-1")):
    final[key] = next(d for d in jl(f"{A}/restore/{f}.jsonl") if d.get("kind") == "after")["rx"]
for d in jl(f"{A}/restore/final-maps.jsonl"):
    if d.get("kind") == "audio-map":
        final[f"map-dut-{d['descriptor_type']}-0"] = d["mappings"]

n = eq = 0
for k, v in asfound.items():
    want = v[1] if k.startswith("map-") else v
    got = final.get(k)
    if isinstance(want, int) and isinstance(got, dict):
        got = got["conn_count"]
    ok = want == got
    n += 1
    eq += ok
    print(f"{k:18s} {'EQUAL' if ok else 'DIFFER'} as-found={json.dumps(want)[:70]} final={json.dumps(got)[:70]}")
print(f"rows {n} equal {eq}")
