#!/usr/bin/env python3
"""Lane B14 item 7: every MAAP PDU on the inline tap (read-only; nothing here touches the bench).

usage: maap_b14.py <out.json> <capture.pcap> [<capture.pcap> ...]

MAAP is IEEE 1722-2016 Annex B: AVTP subtype 0xFE on ethertype 0x22F0, untagged, so the bench
brief's capture filter (ether[40:2]=0x22f0 behind the tap's 28-byte record header) keeps it.
PDU (B.2): byte 0 subtype; byte 1 sv|version|message_type (1 PROBE, 2 DEFEND, 3 ANNOUNCE);
bytes 2-3 maap_version (5 bits) | control_data_length (11 bits); bytes 4-11 stream_id;
bytes 12-17 requested_start_address; 18-19 requested_count; 20-25 conflict_start_address;
26-27 conflict_count. Each PDU is listed with the pcap time (the tap host's clock), the tap
port (3 = sent by the DUT, 2 = received by the DUT), source and destination MAC, and the fields.
Per (port, source) the ANNOUNCE intervals are summarised; every pair of claimed ranges from
different sources is checked for overlap.
"""
import json
import struct
import sys

TYPES = {1: "PROBE", 2: "DEFEND", 3: "ANNOUNCE"}


def mac(b):
    return ":".join(f"{x:02x}" for x in b)


def scan(path):
    out = []
    with open(path, "rb") as f:
        head = f.read(24)
        nano = head[:4] == b"\x4d\x3c\xb2\xa1"
        while True:
            h = f.read(16)
            if len(h) < 16:
                break
            sec, frac, incl, _ = struct.unpack("<4I", h)
            pkt = f.read(incl)
            if len(pkt) < incl or len(pkt) < 28 + 14 + 28:
                continue
            tag, _, port = struct.unpack("<3I", pkt[:12])
            if tag != 6:
                continue
            fr = pkt[28:]
            if fr[12:14] != b"\x22\xf0":
                continue
            p = fr[14:]
            if p[0] != 0xFE:
                continue
            t = sec + frac / (1e9 if nano else 1e6)
            mt = p[1] & 0x0F
            out.append(dict(t=round(t, 6), port=port, src=mac(fr[6:12]), dst=mac(fr[0:6]), type=TYPES.get(mt, mt),
                            maap_version=p[2] >> 3, cdl=int.from_bytes(p[2:4], "big") & 0x7FF,
                            req_start=mac(p[12:18]), req_count=int.from_bytes(p[18:20], "big"),
                            conflict_start=mac(p[20:26]), conflict_count=int.from_bytes(p[26:28], "big"),
                            capture=path.rsplit("/", 1)[-1]))
    return out


def addr(m):
    return int(m.replace(":", ""), 16)


def coverage(path):
    """First and last pcap time of a capture (its covered span)."""
    first = last = None
    with open(path, "rb") as f:
        head = f.read(24)
        nano = head[:4] == b"\x4d\x3c\xb2\xa1"
        while True:
            h = f.read(16)
            if len(h) < 16:
                break
            sec, frac, incl, _ = struct.unpack("<4I", h)
            f.seek(incl, 1)
            t = sec + frac / (1e9 if nano else 1e6)
            first = t if first is None else first
            last = t
    return first, last


def main():
    rows = []
    spans = []
    for a in sys.argv[2:]:
        rows += scan(a)
        s = coverage(a)
        if s[0] is not None:
            spans.append(s)
    # rotated captures overlap: the same PDU seen by two captures carries the same tap-host time
    uniq = {}
    for r in rows:
        uniq.setdefault((r["t"], r["port"], r["src"], r["type"], r["req_start"]), r)
    dups = len(rows) - len(uniq)
    rows = sorted(uniq.values(), key=lambda r: r["t"])
    spans.sort()
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + 0.5:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])

    def covered(a, b):
        return any(lo <= a and b <= hi for lo, hi in merged)
    seen = {}
    by = {}
    for r in rows:
        k = f"port{r['port']}/{r['src']}"
        by.setdefault(k, []).append(r)
        if r["type"] == "ANNOUNCE":
            seen.setdefault(r["src"], set()).add((r["req_start"], r["req_count"]))
    summary = {}
    for k, rs in by.items():
        iv = []
        for rng in sorted({(r["req_start"], r["req_count"]) for r in rs if r["type"] == "ANNOUNCE"}):
            ann = [r["t"] for r in rs if r["type"] == "ANNOUNCE" and (r["req_start"], r["req_count"]) == rng]
            # an interval counts only when the tap covered it end to end (no chunk gap inside it)
            iv += [round(b - a, 3) for a, b in zip(ann, ann[1:]) if covered(a, b)]
        summary[k] = dict(pdus=len(rs), types={t: sum(r["type"] == t for r in rs) for t in ("PROBE", "DEFEND", "ANNOUNCE")},
                          ranges=sorted({(r["req_start"], r["req_count"]) for r in rs}),
                          dsts=sorted({r["dst"] for r in rs}),
                          announce_interval_s=dict(n=len(iv), min=min(iv), max=max(iv),
                                                   mean=round(sum(iv) / len(iv), 3)) if iv else None,
                          first_t=rs[0]["t"], last_t=rs[-1]["t"])
    overlaps = []
    srcs = sorted(seen)
    for i, a in enumerate(srcs):
        for b in srcs[i + 1:]:
            for sa, ca in seen[a]:
                for sb, cb in seen[b]:
                    lo, hi = max(addr(sa), addr(sb)), min(addr(sa) + ca, addr(sb) + cb)
                    if lo < hi:
                        overlaps.append(dict(a=a, a_range=[sa, ca], b=b, b_range=[sb, cb], overlap=hi - lo))
    res = dict(captures=len(sys.argv) - 2, pdus=len(rows), duplicates_dropped=dups,
               covered_spans=len(merged), covered_s=round(sum(b - a for a, b in merged), 3),
               span_s=round(merged[-1][1] - merged[0][0], 3) if merged else None,
               by_sender=summary, overlaps=overlaps,
               non_announce=[r for r in rows if r["type"] != "ANNOUNCE"], first=rows[:4], last=rows[-4:])
    open(sys.argv[1], "w").write(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ("first", "last")}, indent=1)[:4000])


if __name__ == "__main__":
    main()
