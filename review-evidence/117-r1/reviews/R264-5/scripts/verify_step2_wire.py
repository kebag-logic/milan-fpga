#!/usr/bin/env python3
"""Independent re-derivation of the Step 2 wire statistics from the pinned tap captures.

Usage: verify_step2_wire.py <a200-packet-dir>

Own decoder (does not import the packet's tools). Tap record = 28-octet
envelope (tag 6, port 3 = DUT sent, port 2 = switch sent, tap ns modulo 2^32
at [16:20]) + Ethernet frame. The tap time is unwrapped against the pcap host
time. Prints, per run and summed: host (non-envelope) record count; Sync,
Announce, Pdelay_Req interval counts, min/mean/max and logMessageInterval;
the Pdelay exchange completeness and tap request-to-response times in both
directions; the DUT's own Sync/Announce count; the CRF PDU count, tu bits and
sequence continuity in Run B; Announce grandmaster fields.
"""
import os
import statistics as st
import struct
import sys

WRAP = 1 << 32


def records(path):
    raw = open(path, "rb").read()
    magic = struct.unpack("<I", raw[:4])[0]
    nano = magic == 0xA1B23C4D
    off, first, host = 24, None, 0
    out = []
    while off + 16 <= len(raw):
        s, f, incl, _ = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        hns = s * 10**9 + (f if nano else f * 1000)
        if len(pkt) >= 42 and struct.unpack("<I", pkt[:4])[0] == 6 and struct.unpack("<I", pkt[8:12])[0] in (2, 3):
            lo = struct.unpack("<I", pkt[16:20])[0]
            if first is None:
                first = (hns, lo)
            k = round(((hns - first[0]) - (lo - first[1])) / WRAP)
            out.append((lo - first[1] + k * WRAP, struct.unpack("<I", pkt[8:12])[0], pkt[28:]))
        else:
            host += 1
    return out, host


def l2(fr):
    et, off = struct.unpack(">H", fr[12:14])[0], 14
    while et == 0x8100:
        et, off = struct.unpack(">H", fr[off + 2:off + 4])[0], off + 4
    return et, fr[off:]


def stats(v):
    return f"n={len(v)} min={min(v):.1f} mean={st.mean(v):.2f} max={max(v):.1f}" if v else "n=0"


def run(path):
    recs, host = records(path)
    msgs = {}
    crf = []
    for t, port, fr in recs:
        et, p = l2(fr)
        if et == 0x88F7 and len(p) >= 34:
            mt = p[0] & 0x0F
            msgs.setdefault((port, mt), []).append((t, p))
        elif et == 0x22F0 and p and p[0] == 0x04:
            crf.append((t, port, p))
    res = {"host": host}
    for (port, mt), lst in msgs.items():
        ts = [t for t, _ in lst]
        iv = [(b - a) / 1e6 for a, b in zip(ts, ts[1:])]
        lmi = sorted({struct.unpack(">b", p[33:34])[0] for _, p in lst})
        res[(port, mt)] = (len(lst), iv, lmi, lst)
    return res, crf


def pdelay(res, req_port):
    resp_port = 5 - req_port
    reqs = res.get((req_port, 2), (0, [], [], []))[3]
    resps = {(p[30:32], p[44:54]): t for t, p in res.get((resp_port, 3), (0, [], [], []))[3]}
    fups = {(p[30:32], p[44:54]): t for t, p in res.get((resp_port, 0xA), (0, [], [], []))[3]}
    turn, fu, complete = [], [], 0
    for t, p in reqs:
        key = (p[30:32], p[20:30])
        if key in resps and key in fups:
            complete += 1
            turn.append(resps[key] - t)
            fu.append(fups[key] - resps[key])
    return len(reqs), complete, turn, fu


def main():
    pk = sys.argv[1]
    names = {"A": "bench/runA/tap-runA.pcap", "B": "bench/runB/tap-runB.pcap", "C": "bench/runC/tap-runC.pcap", "final": "bench/final/tap-final.pcap"}
    tot = {}
    for r, rel in names.items():
        res, crf = run(os.path.join(pk, rel))
        print(f"== run {r}: host records {res['host']}")
        for key, label in (((2, 0), "Sync switch->DUT"), ((2, 0xB), "Announce switch->DUT"), ((2, 2), "Pdelay_Req switch->DUT"), ((3, 2), "Pdelay_Req DUT->switch"), ((3, 0), "Sync DUT->switch"), ((3, 0xB), "Announce DUT->switch")):
            n, iv, lmi, _ = res.get(key, (0, [], [], []))
            print(f"  {label}: msgs {n} intervals {stats(iv)} ms logMessageInterval {lmi}")
            tot.setdefault(label, []).extend(iv)
            if label.startswith("Sync switch"):
                tot.setdefault("sync-within-30pct", []).append(all(87.5 <= x <= 162.5 for x in iv))
            if label.startswith(("Announce", "Pdelay_Req")) and n:
                tot.setdefault(label + "-30pct", []).append(all(700 <= x <= 1300 for x in iv))
        for rp, lab in ((2, "switch req, DUT resp"), (3, "DUT req, switch resp")):
            n, c, turn, fu = pdelay(res, rp)
            ts = sorted(turn)
            print(f"  Pdelay {lab}: {c}/{n} complete; req->resp ns min {ts[0] if ts else '-'} max {ts[-1] if ts else '-'}; top3 {ts[-3:]}; resp->fup ns min {min(fu) if fu else '-'} max {max(fu) if fu else '-'}")
            tot.setdefault(lab + " n", []).append((c, n))
            tot.setdefault(lab + " turn", []).extend(turn)
        anns = res.get((2, 0xB), (0, [], [], []))[3]
        gm = {(p[47], p[48], p[49], struct.unpack('>H', p[50:52])[0], p[52], p[53:61].hex(), struct.unpack('>H', p[61:63])[0], p[63]) for _, p in anns}
        print(f"  Announce (prio1, class, accuracy, oslv, prio2, gm, stepsRemoved, timeSource): {sorted(gm)}")
        if crf:
            seqs = [p[2] for _, _, p in crf]
            gaps = sum(1 for a, b in zip(seqs, seqs[1:]) if (a + 1) & 0xFF != b)
            tu = sum(p[1] & 1 for _, _, p in crf)
            print(f"  CRF PDUs {len(crf)} ports {sorted({pt for _, pt, _ in crf})} tu=1 count {tu} seq gaps {gaps} first {crf[0][0]/1e9:.3f}s last {crf[-1][0]/1e9:.3f}s (tap clock)")
    print("== summed over runs A, B, C, final")
    for k, v in tot.items():
        if not v:
            print(f"  {k}: none")
        elif k.endswith(" n"):
            print(f"  {k}: {sum(c for c, _ in v)}/{sum(n for _, n in v)}")
        elif k.endswith("turn"):
            print(f"  {k}: count {len(v)} min {min(v)} max {max(v)}")
        elif isinstance(v[0], bool):
            print(f"  {k}: {all(v)}")
        else:
            print(f"  {k}: intervals {stats(v)} ms")


if __name__ == "__main__":
    main()
