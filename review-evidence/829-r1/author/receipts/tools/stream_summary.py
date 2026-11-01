#!/usr/bin/env python3
"""Summary of the stream capture: AVTP frames by VLAN and destination with sequence gaps and rate, MSRP attribute events from each side, gPTP counts. usage: stream_summary.py <pcap> <agent.jsonl>"""
import collections, json, struct, sys
data = open(sys.argv[1], "rb").read(); o = 24
ct = collections.Counter(); first = {}; last = {}; seqs = collections.defaultdict(list); msrp = []
base = None
while o + 16 <= len(data):
    _, _, cap, ln = struct.unpack("<IIII", data[o:o+16]); r = data[o+16:o+16+cap]; o += 16 + cap
    if len(r) < 42: continue
    hi, lo = struct.unpack("<II", r[12:20]); t = (hi << 32) | lo; e = r[28:]
    if base is None: base = t
    et = struct.unpack(">H", e[12:14])[0]; p = e[14:]; vlan = None
    if et == 0x8100:
        vlan = struct.unpack(">H", e[14:16])[0]; et = struct.unpack(">H", e[16:18])[0]; p = e[18:]
    src, dst = e[6:12].hex(":"), e[:6].hex(":")
    k = (src, dst, hex(et), vlan)
    ct[k] += 1; first.setdefault(k, t); last[k] = t
    if et == 0x22f0 and len(p) > 3 and p[0] == 0x02: seqs[k].append(p[2])
    if et == 0x22ea: msrp.append(((t - base) / 1e9, src, p[:40].hex()))
for k, v in ct.most_common(14):
    span = (last[k] - first[k]) / 1e9
    gaps = 0
    if seqs.get(k):
        s = seqs[k]
        gaps = sum(1 for a, b in zip(s, s[1:]) if (a + 1) & 255 != b)
    print(k, "frames", v, f"span {span:.2f} s rate {v/span if span else 0:.1f}/s", f"seq breaks {gaps}" if k in seqs else "")
print("MSRP frames", len(msrp), "first", msrp[:2])
NAMES = ["MEDIA_LOCKED","MEDIA_UNLOCKED","STREAM_INTERRUPTED","SEQ_NUM_MISMATCH","MEDIA_RESET","TIMESTAMP_UNCERTAIN","TIMESTAMP_VALID","TIMESTAMP_NOT_VALID","UNSUPPORTED_FORMAT","LATE_TIMESTAMP","EARLY_TIMESTAMP","FRAMES_RX"]
rows = []
for l in open(sys.argv[2]):
    try: q = json.loads(l)
    except Exception: continue
    if q.get("what") == "counters-dut-5-0":
        h = q["payload"]; v = [int(h[16 + 8 * i:24 + 8 * i], 16) for i in range(12)]; rows.append((q.get("t_rx"), v))
for t, v in rows: print(round(t, 1), {n: x for n, x in zip(NAMES, v) if x})
