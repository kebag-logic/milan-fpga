#!/usr/bin/env python3
"""Decode the MSRP MRPDUs, ACMP probes and CRF emission in the #117 Run B tap
capture (tap-runB.pcap) and test the LeaveAll-scope prediction.

Record layout (linktype 1 with a 28-byte tap prefix, little-endian):
  u32 type, u32 reclen, u32 port, u32 time_hi, u32 time_lo, u32 len, u32 caplen,
  frame; tap time in ns = time_hi * 2**32 + time_lo (checked against the
  host pcap timestamps: 101.64 s tap over 101.60 s host across the file)
Port 3 carries frames sent by the DUT (source 02:00:00:00:00:01), port 2 the
frames the switch port sends toward the DUT.
"""
import struct
import sys

PCAP = sys.argv[1] if len(sys.argv) > 1 else "tap-runB.pcap"
EV = {0: "New", 1: "JoinIn", 2: "In", 3: "JoinMt", 4: "Mt", 5: "Lv"}
DECL = {0: "Ignore", 1: "AskingFailed", 2: "Ready", 3: "ReadyFailed"}
TYPE = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
ALEN = {1: 25, 2: 34, 3: 8, 4: 4}
DUT_MAC = "02:00:00:00:00:01"


def mac(b):
    return ":".join(f"{x:02x}" for x in b)


def records(path):
    d = open(path, "rb").read()
    off = 24
    while off + 16 <= len(d):
        _ts, _tu, incl, _orig = struct.unpack("<IIII", d[off:off + 16])
        off += 16
        rec = d[off:off + incl]
        off += incl
        _typ, _rl, port, hi, lo, _ln, cap = struct.unpack("<7I", rec[:28])
        yield port, ((hi << 32) + lo) * 1e-9, rec[28:28 + cap]


def strip_vlan(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    p = 14
    tag = None
    while et == 0x8100:
        tci = struct.unpack(">H", fr[p:p + 2])[0]
        tag = (tci >> 13, tci & 0xFFF)
        et = struct.unpack(">H", fr[p + 2:p + 4])[0]
        p += 4
    return et, p, tag


def decode_msrp(pl):
    """Return (messages, problems). Each message: dict(type, alen, llen,
    vectors=[dict(la, nov, fv, events, decls)], counted)."""
    msgs, probs = [], []
    if not pl or pl[0] != 0:
        return msgs, ["ProtocolVersion != 0"]
    p = 1
    while True:
        if p + 2 > len(pl):
            probs.append("truncated before MRPDU EndMark")
            break
        if pl[p] == 0 and pl[p + 1] == 0:
            p += 2
            break
        at, al = pl[p], pl[p + 1]
        llen = struct.unpack(">H", pl[p + 2:p + 4])[0]
        p += 4
        list_start = p
        m = dict(type=at, alen=al, llen=llen, vectors=[])
        if ALEN.get(at) != al:
            probs.append(f"type {at} AttributeLength {al}")
        while True:
            vh = struct.unpack(">H", pl[p:p + 2])[0]
            if vh == 0:
                p += 2
                break
            la, nov = vh >> 13, vh & 0x1FFF
            p += 2
            fv = pl[p:p + al]
            p += al
            n3 = (nov + 2) // 3
            evs = []
            for b in pl[p:p + n3]:
                evs += [b // 36, (b // 6) % 6, b % 6]
            p += n3
            decls = []
            if at == 3:
                n4 = (nov + 3) // 4
                for b in pl[p:p + n4]:
                    decls += [(b >> 6) & 3, (b >> 4) & 3, (b >> 2) & 3, b & 3]
                p += n4
            m["vectors"].append(dict(la=la, nov=nov, fv=fv,
                                     events=evs[:nov], decls=decls[:nov]))
        m["counted"] = p - list_start
        if m["counted"] != llen:
            probs.append(f"type {at} AttributeListLength {llen} counted {m['counted']}")
        msgs.append(m)
    return msgs, probs


def fmt_msgs(msgs):
    out = []
    for m in msgs:
        for v in m["vectors"]:
            t = TYPE.get(m["type"], str(m["type"]))
            ev = ",".join(EV.get(e, "?") for e in v["events"])
            if m["type"] == 3 and v["nov"]:
                ev += "/" + ",".join(DECL[d] for d in v["decls"])
            out.append(f"{t}[LA={v['la']} n={v['nov']} fv={v['fv'].hex()}"
                       + (f" {ev}" if v["nov"] else "") + "]")
    return " ".join(out)


def main():
    t0 = None
    msrp = []       # (t, port, src, msgs, probs, raw)
    probes = []     # (t, port, msgtype, status)
    crf = []        # t of DUT CRF PDUs
    for port, t, fr in records(PCAP):
        if t0 is None:
            t0 = t
        t -= t0
        et, p, _tag = strip_vlan(fr)
        src = mac(fr[6:12])
        if et == 0x22EA:
            msgs, probs = decode_msrp(fr[p:])
            msrp.append((t, port, src, msgs, probs, fr[p:]))
        elif et == 0x22F0:
            sub = fr[p]
            if sub == 0xFC:  # ACMP (cd=1, subtype 0x7C)
                mt = fr[p + 1] & 0x0F
                status = fr[p + 2] >> 3
                probes.append((t, port, mt, status))
            elif sub == 0x04 and src == DUT_MAC:
                crf.append(t)

    print("== every MSRP MRPDU (t = tap seconds from the first record) ==")
    for t, port, src, msgs, probs, raw in msrp:
        print(f"{t:10.6f} p{port} {src} {fmt_msgs(msgs)}"
              + (f"  PROBLEMS {probs}" if probs else ""))

    def is_la(msgs):
        return any(v["la"] for m in msgs for v in m["vectors"])

    def la_types(msgs):
        return [TYPE[m["type"]] for m in msgs if any(v["la"] for v in m["vectors"])]

    def lst_decl(msgs):
        return [e for m in msgs if m["type"] == 3 for v in m["vectors"]
                for e in v["events"] if e in (0, 1, 3)]

    def dom_decl(msgs):
        return [e for m in msgs if m["type"] == 4 for v in m["vectors"]
                for e in v["events"] if e in (0, 1, 3)]

    dut_la = [(t, msgs) for t, port, src, msgs, _, _ in msrp if src == DUT_MAC and is_la(msgs)]
    sw_la = [(t, msgs) for t, port, src, msgs, _, _ in msrp if src != DUT_MAC and is_la(msgs)]
    sw = [(t, msgs) for t, port, src, msgs, _, _ in msrp if src != DUT_MAC]

    print("\n== DUT LeaveAll MRPDUs: which Messages carry LeaveAllEvent ==")
    for t, msgs in dut_la:
        print(f"{t:10.6f} LA on {la_types(msgs)} ; messages {[TYPE[m['type']] for m in msgs]}")

    print("\n== switch LeaveAll MRPDUs: message order, LA flag and NumberOfValues per vector ==")
    for t, msgs in sw_la:
        desc = [(TYPE[m["type"]], [(v["la"], v["nov"], len(v["fv"])) for v in m["vectors"]],
                 m["llen"]) for m in msgs]
        print(f"{t:10.6f} {desc}")

    print("\n== prediction part 1: switch declarations within 5 s after each DUT LeaveAll ==")
    for t, _ in dut_la:
        win = [(u, m) for u, m in sw if t < u <= t + 5.0]
        l = [(round(u - t, 4), [EV[e] for e in lst_decl(m)]) for u, m in win if lst_decl(m)]
        d = [(round(u - t, 4), [EV[e] for e in dom_decl(m)]) for u, m in win if dom_decl(m)]
        print(f"DUT LA {t:10.6f}: switch Listener declarations {l or 'NONE'}; "
              f"switch Domain declarations {d or 'NONE'}")

    print("\n== switch Listener declarations outside its own LeaveAll PDUs (periodic?) ==")
    for u, m in sw:
        if lst_decl(m) and not is_la(m):
            print(f"{u:10.6f} {[EV[e] for e in lst_decl(m)]}")

    print("\n== switch LeaveAll timing relative to the preceding DUT LeaveAll ==")
    for u, _ in sw_la:
        prev = [t for t, _ in dut_la if t < u]
        if prev:
            print(f"switch LA {u:10.6f}  - last DUT LA {prev[-1]:10.6f} = {u - prev[-1]:.6f} s")

    print("\n== DUT LeaveAll intervals ==")
    ts = [t for t, _ in dut_la]
    print([round(b - a, 6) for a, b in zip(ts, ts[1:])])

    print("\n== CRF bursts and the prediction part 2 ==")
    bursts = []
    start = crf[0]
    for a, b in zip(crf, crf[1:]):
        if b - a > 0.05:
            bursts.append((start, a))
            start = b
    bursts.append((start, crf[-1]))
    probe_cmds = [t for t, port, mt, st in probes if mt == 0]  # PROBE_TX (CONNECT_TX) command
    for s, e in bursts:
        pr = [t for t in probe_cmds if t <= e]
        dl = [t for t, _ in dut_la if t <= e]
        sl = [t for t, _ in sw_la if t <= e]
        cand = {
            "latest probe + 15 s": pr[-1] + 15.0 if pr else None,
            "latest DUT LA + 5 s": dl[-1] + 5.0 if dl else None,
            "latest switch LA + 5 s": sl[-1] + 5.0 if sl else None,
        }
        print(f"burst {s:10.6f} .. last CRF {e:10.6f} (len {e - s:.3f} s)")
        for k, v in cand.items():
            if v is not None:
                print(f"    {k:24s} = {v:10.6f}  (last CRF - this = {e - v:+.6f} s)")

    print("\n== ACMP PROBE_TX commands (msg 0) and responses (msg 1) ==")
    for t, port, mt, st in probes:
        if mt in (0, 1):
            print(f"{t:10.6f} p{port} msg={mt} status={st}")


if __name__ == "__main__":
    main()
