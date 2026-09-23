#!/usr/bin/env python3
"""Detail probes on the step 3 captures and consoles.

Usage: probe_details.py <bench-a202 dir>
(1) records bracketing the dark window per cycle (port, kind, time);
(2) CLKV_STAT holdover samples around the loss edge (contiguity);
(3) host-only (no tap envelope) record counts and their ethertypes for
    every tap capture in the packet; kernel-drop lines of every tcpdump log.
"""
import glob, os, struct, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import condec, step3, tapdec

base = sys.argv[1]
for n in range(1, 7):
    cdir = os.path.join(base, "bench", f"cycle{n}")
    off, _ = step3.offsets(cdir)
    ps = step3.powerstrip(cdir)
    t0 = ps["T_OFF_CMD"] - off["ps"](ps["T_OFF_CMD"])
    recs, st_, resid, nb = step3.tap_timeline(os.path.join(cdir, f"tap-c{n}.pcap"))
    for r in recs:
        r["t"] = r["srv"] - off["server"](r["srv"]) - t0
    g = max(range(len(recs) - 1), key=lambda i: recs[i + 1]["t"] - recs[i]["t"])
    before = recs[max(0, g - 3):g + 1]
    last3 = [r for r in recs if r["port"] == 3 and r["t"] < recs[g + 1]["t"]][-1]
    print(f"cycle {n}: last records before dark: {[(round(r['t'], 3), r['port'], r['kind'], r.get('mt')) for r in before]}")
    print(f"          first after dark: {[(round(r['t'], 3), r['port'], r['kind'], r.get('mt')) for r in recs[g + 1:g + 4]]}")
    con = condec.parse(os.path.join(cdir, "console.txt"))
    S = [(r["t"] - t0, int(r["fields"]["CLKV_STAT"], 16)) for r in con if r["cmd"] == "milan_status" and r.get("ok")]
    win = [(round(t, 2), hex(c)) for t, c in S if 0.8 < t < 1.9]
    print(f"          CLKV_STAT 0.8..1.9 s: {win}")
print("host-only records and ethertypes per capture:")
for p in sorted(glob.glob(os.path.join(base, "..", "bench-a*", "bench", "**", "*.pcap"), recursive=True)):
    ho = Counter()
    for host_ns, pkt, lt in tapdec.pcap_records(p):
        if len(pkt) >= 42 and struct.unpack("<I", pkt[:4])[0] == 6 and struct.unpack("<I", pkt[8:12])[0] in (2, 3):
            continue
        et = struct.unpack(">H", pkt[12:14])[0] if len(pkt) >= 14 else None
        ho[hex(et) if et is not None else None] += 1
    print(f"  {os.path.relpath(p, os.path.join(base, '..'))}: {sum(ho.values())} {dict(ho)}")
print("tcpdump drop lines:")
for p in sorted(glob.glob(os.path.join(base, "..", "bench-a*", "bench", "**", "tcpdump*.log"), recursive=True)):
    d = [l.strip() for l in open(p) if "dropped" in l]
    print(f"  {os.path.relpath(p, os.path.join(base, '..'))}: {d}")
