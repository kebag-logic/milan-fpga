#!/usr/bin/env python3
"""Re-derive the steady-state console, controller and census claims (Step 2
asCapable retention, Step 4 publication table, Step 5 probe parity).

Usage: steady.py <bench-a200 dir>
"""
import json, os, statistics as st, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condec

b = sys.argv[1]
files = [("identity", "identity/console-identity.txt"), ("A", "bench/runA/console.txt"),
         ("B", "bench/runB/console.txt"), ("final", "bench/final/console-final.txt")]
allstat = []
for name, rel in files:
    recs = condec.parse(os.path.join(b, rel))
    ms = [r for r in recs if r["cmd"] == "milan_status"]
    good = [r for r in ms if r["fields"].get("SYNC") == "1" and r["fields"].get("ASCAPABLE") == "1"
            and r["fields"].get("TU") == "0"]
    allstat += [(name, r) for r in ms]
    print(f"== {name}: milan_status {len(ms)} all-good {len(good)}")
    for k in ("GPTP_GM", "GPTP_PARENT", "AS_PATH_COUNT", "AS_PATH_GEN", "CLKV_STAT", "GPTP_LAT", "VERSION"):
        print(f"   {k}: {dict(Counter(r['fields'].get(k) for r in ms))}")
    pd = [int(r["fields"]["PDELAY_NS"]) for r in ms]
    print(f"   PDELAY_NS min {min(pd)} max {max(pd)} median {st.median(pd)}")
    words = Counter()
    for r in recs:
        if "addr" in r:
            words[(hex(r["addr"]), r["word"] if r["word"] is None else hex(r["word"]))] += 1
    for (a, w), n in sorted(words.items()):
        print(f"   mem {a} = {w} x{n}")
    crcs = [(r["cmd"], r["crc"]) for r in recs if "crc" in r]
    if crcs:
        print("   crc:", crcs)
    if name == "B":
        cc = [(r["iso"], r["word"]) for r in recs if r.get("addr") == 0x9000066C]
        ct = [(r["iso"], r["word"]) for r in recs if r.get("addr") == 0x90000750]
        c64 = [(r["iso"], r["word"]) for r in recs if r.get("addr") == 0x90000764]
        print("   0x66c first/last:", cc[0], cc[-1], "distinct", sorted({hex(w) for _, w in cc}))
        print("   0x750 distinct:", sorted({hex(w) for _, w in ct}), "first", ct[0], "last", ct[-1])
        print("   0x764 distinct:", sorted({hex(w) for _, w in c64}))
        tu = [r for r in ms if int(r["fields"]["CLKV_STAT"], 16) & 1]
        print("   samples with CLKV_STAT[0]=1:", len(tu))
allpd = [int(r["fields"]["PDELAY_NS"]) for n, r in allstat if n in ("A", "B", "final")]
print(f"== steady PDELAY_NS (A,B,final) min {min(allpd)} max {max(allpd)} median {st.median(allpd)}; n {len(allpd)}")
print(f"== all milan_status samples {len(allstat)}; all-good "
      f"{sum(1 for n, r in allstat if r['fields'].get('SYNC') == '1' and r['fields'].get('ASCAPABLE') == '1' and r['fields'].get('TU') == '0')}")

# controller poll Run A
polls = [json.loads(l) for l in open(os.path.join(b, "bench/runA/pw1-watch.jsonl"))]
ai = [p for p in polls if p.get("cmd") == "GET_AVB_INFO" and p.get("target") == "020000fffe000001"]
ap = [p for p in polls if p.get("cmd") == "GET_AS_PATH" and p.get("target") == "020000fffe000001"]


def avb(p):
    # GET_AVB_INFO response payload (IEEE 1722.1 7.4.40): desc_type(2) desc_index(2)
    # gptp_grandmaster_id(8) propagation_delay(4) gptp_domain_number(1) flags(1) msrp_mappings_count(2) ...
    x = bytes.fromhex(p["payload"])
    return x[4:12].hex(), int.from_bytes(x[12:16], "big"), x[16], x[17]


dec = [avb(p) for p in ai]
print(f"== Run A controller: GET_AVB_INFO DUT polls {len(ai)} statuses {Counter(p['status'] for p in ai)}")
print(f"   gm {Counter(d[0] for d in dec)} domain {Counter(d[2] for d in dec)} flags {Counter(hex(d[3]) for d in dec)}")
pdl = [d[1] for d in dec]
print(f"   propagation_delay min {min(pdl)} max {max(pdl)} median {st.median(pdl)}")
print(f"   AS_CAPABLE (flags bit0) set in {sum(1 for d in dec if d[3] & 1)}/{len(dec)}")
paths = Counter()
for p in ap:
    x = bytes.fromhex(p["payload"])
    n = int.from_bytes(x[2:4], "big")
    paths[(n, tuple(x[4 + 8 * i:12 + 8 * i].hex() for i in range(n)))] += 1
print(f"   GET_AS_PATH DUT polls {len(ap)}: {dict(paths)}")
