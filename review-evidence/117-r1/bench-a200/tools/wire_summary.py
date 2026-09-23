#!/usr/bin/env python3
"""Decode a ProfiShark 1G+ tap capture (issue 117, A200).

Record layout, as captured by tcpdump on the tap interface (LINKTYPE_ETHERNET
with a 28-byte tap envelope in front of the frame):
  [0:4]   tag (6)      [4:8]  envelope length word
  [8:12]  tap port: 3 = frames the DUT sent, 2 = frames the far end sent
  [12:16] a second word the tap supplies (not used)
  [16:20] tap hardware time, nanoseconds modulo 2^32
  [20:28] captured/wire lengths
  [28:]   the Ethernet frame without FCS
The nanosecond word is unwrapped against the pcap host timestamp, which is
coarse (USB batching) but never wrong by 2 s, so every record gets a
monotonic tap time in ns. Intervals below come from that tap time.

usage: wire_summary.py <pcap> [--json out.json] [--events out.tsv]
"""
import json
import statistics as st
import struct
import sys
from collections import defaultdict

PTP_NAMES = {0x0: "Sync", 0x2: "Pdelay_Req", 0x3: "Pdelay_Resp", 0x8: "Follow_Up",
             0xA: "Pdelay_Resp_Follow_Up", 0xB: "Announce", 0xC: "Signaling"}
PORT_NAMES = {3: "DUT->far", 2: "far->DUT"}
WRAP = 1 << 32
HOST_RECORDS = [0]


def records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    if magic not in (0xA1B2C3D4, 0xA1B23C4D):
        raise SystemExit(f"not a little-endian pcap: {magic:#x}")
    nano = magic == 0xA1B23C4D
    off = 24
    first = None
    while off + 16 <= len(raw):
        ts_s, ts_f, incl, _orig = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        host_ns = ts_s * 10**9 + (ts_f if nano else ts_f * 1000)
        if len(pkt) < 28 + 14:
            continue
        tag, _envlen, port = struct.unpack("<III", pkt[:12])
        if tag != 6 or port not in (2, 3):
            # No tap envelope: a frame the capture host itself sent or received
            # on the tap interface, not a tapped frame.
            HOST_RECORDS[0] += 1
            continue
        tap_lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host_ns, tap_lo)
        k = round(((host_ns - first[0]) - (tap_lo - first[1])) / WRAP)
        tap_ns = tap_lo - first[1] + k * WRAP
        yield dict(host_ns=host_ns, tap_ns=tap_ns, port=port, frame=pkt[28:])


def ts10(b):
    return int.from_bytes(b[0:6], "big") * 10**9 + int.from_bytes(b[6:10], "big")


def decode(rec):
    fr = rec["frame"]
    d = dict(dst=fr[0:6].hex(":"), src=fr[6:12].hex(":"), port=rec["port"],
             tap_ns=rec["tap_ns"], host_ns=rec["host_ns"])
    et = struct.unpack(">H", fr[12:14])[0]
    p = fr[14:]
    vlan = None
    if et == 0x8100:
        tci = struct.unpack(">H", fr[14:16])[0]
        vlan = (tci >> 13, tci & 0xFFF)
        et = struct.unpack(">H", fr[16:18])[0]
        p = fr[18:]
    d["ethertype"] = et
    d["vlan"] = vlan
    if et == 0x88F7 and len(p) >= 34:
        mt = p[0] & 0xF
        d["kind"] = "gPTP " + PTP_NAMES.get(mt, f"type{mt}")
        d["ptp"] = dict(mt=mt, domain=p[4], flags=p[6:8].hex(),
                        corr_ns=int.from_bytes(p[8:16], "big", signed=True) / 65536.0,
                        src_port_id=p[20:30].hex(), seq=struct.unpack(">H", p[30:32])[0],
                        log_interval=struct.unpack("b", p[33:34])[0])
        if mt == 0xB and len(p) >= 64:
            a = d["ptp"]
            a["gm_prio1"] = p[47]
            a["gm_class"] = p[48]
            a["gm_accuracy"] = p[49]
            a["gm_variance"] = struct.unpack(">H", p[50:52])[0]
            a["gm_prio2"] = p[52]
            a["gm_id"] = p[53:61].hex()
            a["steps_removed"] = struct.unpack(">H", p[61:63])[0]
            a["time_source"] = p[63]
            tlvs = []
            o = 64
            msg_len = min(struct.unpack(">H", p[2:4])[0], len(p))
            a["message_length"] = msg_len
            while o + 4 <= msg_len:
                t, n = struct.unpack(">HH", p[o:o + 4])
                body = p[o + 4:o + 4 + n]
                if t == 0x0008:
                    tlvs.append(("PathTrace", [body[i:i + 8].hex() for i in range(0, len(body), 8)]))
                else:
                    tlvs.append((f"tlv{t:#06x}", body.hex()))
                o += 4 + n
                if n == 0:
                    break
            a["tlvs"] = tlvs
        if mt in (0x0, 0x8, 0x2, 0x3, 0xA):
            d["ptp"]["body_ts"] = ts10(p[34:44])
        if mt in (0x3, 0xA):
            d["ptp"]["req_port_id"] = p[44:54].hex()
        if mt == 0x8 and len(p) >= 76:
            # Follow_Up information TLV (802.1AS 11.4.4.3)
            d["ptp"]["csro"] = struct.unpack(">i", p[54:58])[0]
            d["ptp"]["gm_time_base"] = struct.unpack(">H", p[58:60])[0]
        if mt == 0xC and len(p) >= 54:
            d["ptp"]["signal_tlv"] = p[44:].hex()
    elif et == 0x22F0 and len(p) >= 12:
        sub = p[0]
        if sub == 0xFA:
            d["kind"] = "ADP"
            d["adp"] = dict(msg=p[1] & 0xF, entity_id=p[4:12].hex(), model_id=p[12:20].hex(),
                            avail_index=struct.unpack(">I", p[36:40])[0],
                            gm_id=p[40:48].hex(), gm_domain=p[48],
                            cfg=struct.unpack(">H", p[52:54])[0],
                            interface_index=struct.unpack(">H", p[56:58])[0])
        elif sub == 0xFB:
            d["kind"] = "AECP"
        elif sub == 0xFC:
            d["kind"] = "ACMP"
            d["acmp"] = dict(msg=p[1] & 0xF, status=p[2] >> 3)
        elif sub == 0xFE:
            d["kind"] = "MAAP"
        elif sub == 0x02:
            d["kind"] = "AAF"
            d["avtp"] = dict(stream_id=p[4:12].hex(), seq=p[2], tv=p[1] & 1, tu=p[3] & 1,
                             ts=struct.unpack(">I", p[12:16])[0])
        elif sub == 0x04:
            d["kind"] = "CRF"
            d["avtp"] = dict(stream_id=p[4:12].hex(), seq=p[2], tu=p[1] & 1, fs=(p[1] >> 1) & 1,
                             crf_type=p[3])
        else:
            d["kind"] = f"AVTP sub {sub:#04x}"
    elif et == 0x22EA:
        d["kind"] = "MSRP"
    elif et == 0x88F5:
        d["kind"] = "MVRP"
    elif et == 0x88CC:
        d["kind"] = "LLDP"
    else:
        d["kind"] = f"ethertype {et:#06x}"
    return d


def intervals_ms(ts):
    return [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]


def fmt_stats(v):
    if not v:
        return "n/a"
    return (f"n={len(v)} median={st.median(v):.3f} min={min(v):.3f} max={max(v):.3f} "
            f"mean={st.fmean(v):.3f}")


def main():
    args = sys.argv[1:]
    path = args[0]
    js = args[args.index("--json") + 1] if "--json" in args else None
    ev = args[args.index("--events") + 1] if "--events" in args else None
    recs = sorted((decode(r) for r in records(path)), key=lambda d: d["tap_ns"])
    if not recs:
        print("no records")
        return 1
    t0 = recs[0]["tap_ns"]
    span = (recs[-1]["tap_ns"] - t0) / 1e9
    print(f"file: {path}")
    print(f"tapped records: {len(recs)}  host-generated records excluded: {HOST_RECORDS[0]}  "
          f"tap span: {span:.3f} s  ports: {sorted({r['port'] for r in recs})}")
    groups = defaultdict(list)
    for r in recs:
        groups[(r["port"], r["src"], r["kind"])].append(r)
    print("\n== per (tap port, source, kind): count, interval statistics (ms)")
    for key in sorted(groups):
        rows = groups[key]
        port, src, kind = key
        print(f"  port {port} ({PORT_NAMES.get(port, '?')}) {src} {kind:26s} "
              f"{fmt_stats(intervals_ms([r['tap_ns'] for r in rows]))}")
        if kind.startswith("gPTP"):
            li = sorted({r["ptp"]["log_interval"] for r in rows})
            dom = sorted({r["ptp"]["domain"] for r in rows})
            sp = sorted({r["ptp"]["src_port_id"] for r in rows})
            print(f"      logMessageInterval {li} domain {dom} sourcePortIdentity {sp}")
        if kind == "gPTP Announce":
            ann = sorted({(r["ptp"]["gm_id"], r["ptp"]["gm_prio1"], r["ptp"]["gm_class"],
                           r["ptp"]["gm_accuracy"], r["ptp"]["gm_variance"], r["ptp"]["gm_prio2"],
                           r["ptp"]["steps_removed"], r["ptp"]["time_source"],
                           json.dumps(r["ptp"]["tlvs"])) for r in rows})
            for a in ann:
                print(f"      GM {a[0]} prio1 {a[1]} class {a[2]} accuracy {a[3]:#04x} "
                      f"variance {a[4]:#06x} prio2 {a[5]} stepsRemoved {a[6]} timeSource {a[7]:#04x} tlvs {a[8]}")
        if kind == "gPTP Follow_Up":
            tb = sorted({r["ptp"].get("gm_time_base") for r in rows})
            print(f"      gmTimeBaseIndicator {tb}")
        if kind == "gPTP Signaling":
            print(f"      TLV bodies {sorted({r['ptp']['signal_tlv'] for r in rows})}")
        if kind == "ADP":
            ids = sorted({(r["adp"]["entity_id"], r["adp"]["model_id"], r["adp"]["gm_id"],
                           r["adp"]["gm_domain"], r["adp"]["interface_index"]) for r in rows})
            for i in ids:
                print(f"      entity {i[0]} model {i[1]} gptp_gm {i[2]} domain {i[3]} interface {i[4]}")
        if kind in ("AAF", "CRF"):
            sids = defaultdict(lambda: [0, 0])
            for r in rows:
                sids[r["avtp"]["stream_id"]][r["avtp"]["tu"]] += 1
            for s, (tu0, tu1) in sorted(sids.items()):
                print(f"      stream {s} tu=0 x{tu0} tu=1 x{tu1} vlan {rows[0]['vlan']}")
    if js:
        with open(js, "w") as f:
            json.dump([{k: v for k, v in r.items()} for r in recs], f, default=str)
    if ev:
        with open(ev, "w") as f:
            f.write("t_s\tport\tsrc\tkind\tdetail\n")
            for r in recs:
                det = ""
                if "ptp" in r:
                    q = r["ptp"]
                    det = f"seq={q['seq']} li={q['log_interval']} spid={q['src_port_id']}"
                    if "gm_id" in q:
                        det += f" gm={q['gm_id']} p1={q['gm_prio1']} sr={q['steps_removed']}"
                elif "adp" in r:
                    det = f"eid={r['adp']['entity_id']} gm={r['adp']['gm_id']}"
                elif "avtp" in r:
                    det = f"sid={r['avtp']['stream_id']} tu={r['avtp']['tu']}"
                f.write(f"{(r['tap_ns'] - t0) / 1e9:.9f}\t{r['port']}\t{r['src']}\t{r['kind']}\t{det}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
