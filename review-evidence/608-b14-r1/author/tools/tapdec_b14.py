#!/usr/bin/env python3
"""Lane B14: summarise one inline-tap capture (read-only; nothing here touches the bench).

usage: tapdec_b14.py <capture.pcap> [<capture.pcap> ...]   (one JSON object per file on stdout)

Every frame carries the tap's 28-byte record header: little-endian words, [0] record tag (6),
[2] port (2 = switch to DUT, 3 = DUT to switch), [4] the tap's nanosecond counter (low 32 bits,
unwrapped against the pcap time, as lane B2's reader does). The Ethernet frame follows at byte 28.
Decoded per stream (port, stream_id) for AVTP stream PDUs (1722-2016):
  AAF (subtype 0x02, clause 7): byte 1 sv|version|mr|rsv|tv, byte 2 sequence_num, byte 3 tu,
  bytes 12-15 avtp_timestamp;
  CRF (subtype 0x04, clause 10): byte 1 sv|version|mr|rsv|fs|tu, byte 2 sequence_num,
  bytes 16-17 crf_data_length, 18-19 timestamp_interval, then 64-bit timestamps.
Counted: PDUs, sequence gaps (a step other than +1 modulo 256), mr toggles, tv=0 and tu=1 PDUs,
and the presentation-time step distribution (AAF: consecutive avtp_timestamp differences, mod
2^32; CRF: consecutive first-timestamp differences). Times are tap seconds from the first frame.
MSRP (ethertype 0x22EA) frames are counted only.
"""
import json
import struct
import sys
from collections import Counter


def summarise(path):
    f = open(path, "rb")
    head = f.read(24)
    nano = head[:4] == b"\x4d\x3c\xb2\xa1"
    first = None
    streams = {}
    eth = Counter()
    n = 0
    t_last = 0.0
    while True:
        h = f.read(16)
        if len(h) < 16:
            break
        sec, frac, incl, _ = struct.unpack("<4I", h)
        pkt = f.read(incl)
        if len(pkt) < incl:
            break
        n += 1
        if len(pkt) < 46:
            continue
        tag, _, port = struct.unpack("<3I", pkt[:12])
        if tag != 6:
            continue
        host = sec * 10**9 + frac * (1 if nano else 1000)
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host, lo)
        ns = lo - first[1] + round(((host - first[0]) - (lo - first[1])) / (1 << 32)) * (1 << 32)
        t = ns / 1e9
        t_last = t
        fr = pkt[28:]
        et = int.from_bytes(fr[12:14], "big")
        o, vlan = 14, None
        if et == 0x8100:
            tci = int.from_bytes(fr[14:16], "big")
            vlan = (tci >> 13, tci & 4095)
            et = int.from_bytes(fr[16:18], "big")
            o = 18
        eth[(port, hex(et), vlan is not None)] += 1
        if et != 0x22F0:
            continue
        p = fr[o:]
        if len(p) < 24 or p[0] not in (0x02, 0x04):
            continue
        sub = p[0]
        sid = p[4:12].hex()
        key = f"{port}/{sid}"
        s = streams.get(key)
        if s is None:
            s = streams[key] = dict(port=port, stream_id=sid, subtype=hex(sub), vlan=list(vlan) if vlan else None, n=0,
                                    first_t=round(t, 6), seq_gaps=[], mr_toggles=[], tv0=0, tu1=0, steps=Counter(),
                                    prev_seq=None, prev_mr=None, prev_ts=None, prev_t=None, max_gap_s=0.0)
        s["n"] += 1
        seq = p[2]
        mr = p[1] >> 3 & 1
        if sub == 0x02:
            tv, tu = p[1] & 1, p[3] & 1
            ts = int.from_bytes(p[12:16], "big")
        else:
            tv, tu = 1, p[1] & 1
            ts = int.from_bytes(p[20:28], "big") & 0xFFFFFFFF if len(p) >= 28 else None
        if s["prev_seq"] is not None and (seq - s["prev_seq"]) % 256 != 1:
            if len(s["seq_gaps"]) < 20:
                s["seq_gaps"].append(dict(t=round(t, 6), from_seq=s["prev_seq"], to_seq=seq))
            s.setdefault("seq_gap_count", 0)
            s["seq_gap_count"] += 1
        if s["prev_mr"] is not None and mr != s["prev_mr"]:
            s["mr_toggles"].append(dict(t=round(t, 6), mr=mr))
        if not tv:
            s["tv0"] += 1
        if tu:
            s["tu1"] += 1
        if ts is not None and s["prev_ts"] is not None:
            s["steps"][(ts - s["prev_ts"]) % (1 << 32)] += 1
        if s["prev_t"] is not None:
            s["max_gap_s"] = max(s["max_gap_s"], t - s["prev_t"])
        s["prev_seq"], s["prev_mr"], s["prev_ts"], s["prev_t"] = seq, mr, ts, t
        s["last_t"] = round(t, 6)
    out = []
    for s in streams.values():
        st = s.pop("steps")
        for k in ("prev_seq", "prev_mr", "prev_ts", "prev_t"):
            s.pop(k)
        s["max_gap_s"] = round(s["max_gap_s"], 6)
        s.setdefault("seq_gap_count", 0)
        common = st.most_common(1)[0][0] if st else None
        s["ts_step_mode_ns"] = common
        s["ts_step_min_max_ns"] = [min(st), max(st)] if st else None
        # steps more than 1 us off the modal step (a presentation-time discontinuity)
        odd = sorted((k, v) for k, v in st.items() if common is not None and abs(((k - common + (1 << 31)) % (1 << 32)) - (1 << 31)) > 1000)
        s["ts_steps_off_mode_gt_1us"] = [dict(step_ns=k, count=v) for k, v in odd[:20]]
        s["ts_steps_off_mode_gt_1us_total"] = sum(v for _, v in odd)
        out.append(s)
    return dict(file=path.rsplit("/", 1)[-1], frames=n, span_s=round(t_last, 6),
                ethertypes={f"port{p}/{e}/{'vlan' if v else 'plain'}": c for (p, e, v), c in sorted(eth.items())},
                streams=sorted(out, key=lambda s: (s["port"], s["stream_id"])))


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(json.dumps(summarise(a)), flush=True)
