#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent reviewer decoder for the issue 117 inline-tap captures.

Written from the capture bytes, not from the bench tools. Reads a classic
little-endian pcap whose records carry a 28-octet tap envelope in front of the
Ethernet frame:

  word0  record type (6 = tapped frame)
  word1  padded record length
  word2  tap port: 2 = frame the switch sent, 3 = frame the DUT sent
  word3  constant high word (not used)
  word4  nanoseconds, wrapping every 2**32 ns
  word5  frame length, word6 frame length again

The 32-bit nanosecond word is unwrapped against the pcap host time: the
number of wraps between two records is the one that makes the tap delta
closest to the host delta. Records without a valid envelope are counted and
excluded.

Usage: r264_wire.py <cmd> <pcap> [...]
  events <pcap>       one line per decoded gPTP/AVTP/ADP/MSRP frame (TSV)
  step2  <pcap> ...   cadence and Pdelay statistics per capture and summed
  crf    <pcap>       CRF PDU census (count, tu, sequence continuity)
"""
import json
import struct
import sys
from statistics import mean, median

WRAP = 1 << 32


def records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    if magic != 0xA1B2C3D4:
        raise SystemExit(f"{path}: unsupported pcap magic {magic:#x}")
    linktype = struct.unpack("<I", raw[20:24])[0]
    if linktype != 1:
        raise SystemExit(f"{path}: linktype {linktype}")
    off = 24
    while off + 16 <= len(raw):
        sec, usec, incl, orig = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        data = raw[off:off + incl]
        off += incl
        yield sec + usec * 1e-6, data


def tapped(path):
    """Yield (tap_ns, host_s, port, frame); also returns count of excluded."""
    out = []
    excluded = 0
    last_host = None
    last_w = None
    acc = None
    for host, data in records(path):
        if len(data) < 28:
            excluded += 1
            continue
        w = struct.unpack("<7I", data[:28])
        flen = w[5]
        if w[0] != 6 or w[2] not in (2, 3) or w[5] != w[6] or 28 + flen != len(data):
            excluded += 1
            continue
        ns = w[4]
        if acc is None:
            acc = ns
        else:
            mod = (ns - last_w) % WRAP
            host_delta_ns = (host - last_host) * 1e9
            k = round((host_delta_ns - mod) / WRAP)
            if k < 0:
                k = 0
            acc += mod + k * WRAP
        last_w, last_host = ns, host
        out.append((acc, host, w[2], data[28:]))
    return out, excluded


def ts10(b):
    sec = int.from_bytes(b[:6], "big")
    ns = int.from_bytes(b[6:10], "big")
    return sec, ns


def decode(frame):
    """Return (kind, fields) for the frames this review needs."""
    et = int.from_bytes(frame[12:14], "big")
    p = 14
    vlan = None
    if et == 0x8100:
        tci = int.from_bytes(frame[14:16], "big")
        vlan = (tci >> 13, tci & 0xFFF)
        et = int.from_bytes(frame[16:18], "big")
        p = 18
    src = frame[6:12].hex()
    body = frame[p:]
    if et == 0x88F7 and len(body) >= 34:
        mt = body[0] & 0x0F
        dom = body[4]
        corr = int.from_bytes(body[8:16], "big", signed=True)
        spid = body[20:28].hex() + ":" + body[28:30].hex()
        seq = int.from_bytes(body[30:32], "big")
        lmi = struct.unpack("b", body[33:34])[0]
        f = dict(mt=mt, dom=dom, corr=corr, spid=spid, seq=seq, lmi=lmi, src=src)
        if mt in (0x3, 0xA):
            f["ts"] = ts10(body[34:44])
            f["req"] = body[44:52].hex() + ":" + body[52:54].hex()
        if mt == 0xB:
            f["prio1"] = body[47]
            f["cls"] = body[48]
            f["acc"] = body[49]
            f["var"] = int.from_bytes(body[50:52], "big")
            f["prio2"] = body[52]
            f["gm"] = body[53:61].hex()
            f["steps"] = int.from_bytes(body[61:63], "big")
            f["tsrc"] = body[63]
            tl = body[64:]
            path = []
            while len(tl) >= 4:
                t = int.from_bytes(tl[:2], "big")
                n = int.from_bytes(tl[2:4], "big")
                if t == 0x0008:
                    path = [tl[4 + 8 * i:12 + 8 * i].hex() for i in range(n // 8)]
                tl = tl[4 + n:]
            f["path"] = path
        return "ptp", f
    if et == 0x22F0 and len(body) >= 4:
        sub = body[0]
        if sub == 0x04:  # CRF
            return "crf", dict(tu=body[1] & 0x01, sv=body[1] >> 7, seq=body[2],
                               sid=body[4:12].hex(), vlan=vlan, src=src)
        if sub == 0xFA:  # ADP
            return "adp", dict(msg=body[1] & 0x0F, eid=body[4:12].hex(),
                               avail=int.from_bytes(body[36:40], "big") if len(body) >= 48 else None,
                               gm=body[40:48].hex() if len(body) >= 48 else None,
                               dom=body[48] if len(body) >= 49 else None)
        if sub == 0xFB:
            return "aecp", dict(msg=body[1] & 0x0F)
        if sub == 0xFC:
            return "acmp", dict(msg=body[1] & 0x0F)
        return "avtp", dict(sub=sub, vlan=vlan)
    if et == 0x22EA:
        return "msrp", dict(len=len(body))
    return "other", dict(et=et)


def ptp_events(path):
    recs, excluded = tapped(path)
    ev = []
    for tns, host, port, fr in recs:
        kind, f = decode(fr)
        ev.append((tns, host, port, kind, f))
    return ev, excluded, len(recs)


MT = {0: "Sync", 2: "PdelayReq", 3: "PdelayResp", 8: "FollowUp", 0xA: "PdelayRespFU",
      0xB: "Announce", 0xC: "Signaling"}


def intervals(ts):
    return [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]


def step2(path):
    ev, excluded, n = ptp_events(path)
    r = dict(file=path, records=n, excluded=excluded)
    sel = lambda port, mt: [e for e in ev if e[3] == "ptp" and e[2] == port and e[4]["mt"] == mt]
    for name, port, mt in (("sync_sw", 2, 0), ("ann_sw", 2, 0xB), ("preq_sw", 2, 2), ("preq_dut", 3, 2),
                           ("sync_dut", 3, 0), ("ann_dut", 3, 0xB)):
        s = sel(port, mt)
        iv = intervals([e[0] for e in s])
        r[name] = dict(count=len(s), n_iv=len(iv),
                       mean=round(mean(iv), 3) if iv else None,
                       min=round(min(iv), 3) if iv else None,
                       max=round(max(iv), 3) if iv else None,
                       out30=sum(1 for x in iv if abs(x - (125 if mt == 0 else 1000)) > 0.3 * (125 if mt == 0 else 1000)),
                       lmi=sorted({e[4]["lmi"] for e in s}),
                       spid=sorted({e[4]["spid"] for e in s}))
    # Pdelay exchanges: requester port rq, responder port rs
    for name, rq, rs in (("x_sw_req", 2, 3), ("x_dut_req", 3, 2)):
        reqs = sel(rq, 2)
        resp = {e[4]["seq"]: e for e in sel(rs, 3)}
        fu = {e[4]["seq"]: e for e in sel(rs, 0xA)}
        done = 0
        turn, r2f, claimed, diff = [], [], [], []
        for q in reqs:
            s = q[4]["seq"]
            if s in resp and s in fu and resp[s][0] > q[0]:
                done += 1
                t_turn = resp[s][0] - q[0]
                turn.append(t_turn)
                r2f.append(fu[s][0] - resp[s][0])
                t2 = resp[s][4]["ts"]
                t3 = fu[s][4]["ts"]
                # claimed turnaround t3 - t2 including correction fields (ns * 2^16)
                c = (t3[0] - t2[0]) * 1e9 + (t3[1] - t2[1]) + (fu[s][4]["corr"] - resp[s][4]["corr"]) / 65536.0
                claimed.append(c)
                diff.append(t_turn - c)
        r[name] = dict(requests=len(reqs), complete=done,
                       turn_ns=[round(min(turn)), round(max(turn)), round(median(turn))] if turn else None,
                       turn_over_2ms=[round(x / 1e6, 3) for x in turn if x > 2e6],
                       r2f_ns=[round(min(r2f)), round(max(r2f))] if r2f else None,
                       claimed_ns=[round(min(claimed)), round(max(claimed))] if claimed else None,
                       diff_ns=[round(min(diff)), round(max(diff)), round(median(diff))] if diff else None)
    anns = sel(2, 0xB)
    r["ann_fields"] = sorted({json.dumps({k: a[4][k] for k in ("prio1", "cls", "acc", "var", "prio2", "gm", "steps", "tsrc", "dom")}
                                         | {"path": a[4]["path"]}) for a in anns})
    r["ptp_domains"] = sorted({e[4]["dom"] for e in ev if e[3] == "ptp"})
    r["dut_ptp_mt"] = sorted({MT.get(e[4]["mt"], e[4]["mt"]) for e in ev if e[3] == "ptp" and e[2] == 3})
    r["dut_adp_gm"] = sorted({e[4]["gm"] for e in ev if e[3] == "adp" and e[2] == 3})
    return r


def crf(path):
    ev, excluded, n = ptp_events(path)
    c = [e for e in ev if e[3] == "crf" and e[2] == 3]
    seqs = [e[4]["seq"] for e in c]
    gaps = sum(1 for a, b in zip(seqs, seqs[1:]) if (b - a) % 256 != 1)
    return dict(file=path, crf_dut=len(c), tu1=sum(e[4]["tu"] for e in c),
                seq_gaps=gaps, vlans=sorted({str(e[4]["vlan"]) for e in c}),
                sids=sorted({e[4]["sid"] for e in c}),
                first_host=c[0][1] if c else None, last_host=c[-1][1] if c else None,
                crf_switch_side=sum(1 for e in ev if e[3] == "crf" and e[2] == 2))


def main(argv):
    cmd = argv[1]
    if cmd == "step2":
        allr = [step2(p) for p in argv[2:]]
        print(json.dumps(allr, indent=1))
    elif cmd == "crf":
        print(json.dumps(crf(argv[2]), indent=1))
    elif cmd == "events":
        ev, excluded, n = ptp_events(argv[2])
        for tns, host, port, kind, f in ev:
            print(f"{tns}\t{host:.6f}\t{port}\t{kind}\t{json.dumps(f, sort_keys=True)}")
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
