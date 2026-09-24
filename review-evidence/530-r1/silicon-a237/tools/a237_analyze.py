#!/usr/bin/env python3
"""Issue 530 silicon rerun analysis (A237, offline, read-only).

Reads the tap capture of the DUT link (wire_summary.records: tap port 3 = frames
the DUT sent, tap port 2 = frames the bench switch sent), and optionally the
controller-host GET_COUNTERS log, the bind-window log and the console transcript.
Everything is placed on the tap hardware clock. Controller-host and capture-server
times are NTP; they map onto the tap clock through a straight line fitted to the
per-5 s minima of (pcap host time - tap time). Console times are build-box times
and take --console-offset-s (capture server minus build box) first.

Reports:
  - ACMP traffic for the CRF pair (bind, probes and their status, unbind);
  - CRF and AAF emission from the DUT: bursts (a gap over 10 ms ends one), sequence
    continuity, tu, VLAN, interval statistics;
  - a full MSRP decode (every vector, every value, LeaveAll flags, NumberOfValues 0
    vectors), per port: the LeaveAll MRPDUs and their spacing, the DUT's Talker
    declarations for the CRF stream and the switch's Listener declarations for it;
  - the #530 acceptance quantities;
  - Stream Output 1 counters and the console CSRs against the same timeline.

usage: a237_analyze.py <tap.pcap> [--counters f] [--bind f] [--console f]
                       [--console-offset-s x] [--json out.json]
"""
import argparse
import json
import re
import statistics as st
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_summary as ws  # noqa: E402

DUT_SID = "0200000000010001"
DUT_EID = "020000fffe000001"
PEER_EID = "3cc0c60102030000"
EV = ["New", "JoinIn", "In", "JoinMt", "Mt", "Lv"]
LD = ["Ignore", "AskingFailed", "Ready", "ReadyFailed"]
ATTR = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
ACMPN = {0: "CONNECT_TX_COMMAND(probe)", 1: "CONNECT_TX_RESPONSE", 2: "DISCONNECT_TX_COMMAND",
         3: "DISCONNECT_TX_RESPONSE", 4: "GET_TX_STATE_COMMAND", 5: "GET_TX_STATE_RESPONSE",
         6: "CONNECT_RX_COMMAND(bind)", 7: "CONNECT_RX_RESPONSE", 8: "DISCONNECT_RX_COMMAND(unbind)",
         9: "DISCONNECT_RX_RESPONSE", 10: "GET_RX_STATE_COMMAND", 11: "GET_RX_STATE_RESPONSE"}
ACMP_STATUS = {0: "SUCCESS", 3: "TALKER_DEST_MAC_FAIL"}


def msrp_decode(frame):
    """Every vector of one MSRPDU: attr, leaveall, nv, first stream id (or raw), events, decls."""
    p = frame[14:]
    out = []
    i = 1
    while i + 4 <= len(p):
        at, al = p[i], p[i + 1]
        if at == 0:
            break
        ll = struct.unpack(">H", p[i + 2:i + 4])[0]
        body = p[i + 4:i + 4 + ll]
        j = 0
        while j + 2 <= len(body):
            vh = struct.unpack(">H", body[j:j + 2])[0]
            if vh == 0:
                break
            nv, la = vh & 0x1FFF, vh >> 13
            fv = body[j + 2:j + 2 + al]
            j += 2 + al
            nb = (nv + 2) // 3
            ev = []
            for b in body[j:j + nb]:
                ev += [EV[b // 36] if b // 36 < 6 else "?", EV[(b // 6) % 6], EV[b % 6]]
            j += nb
            ev = ev[:nv]
            ld = []
            if at == 3:
                n4 = (nv + 3) // 4
                for b in body[j:j + n4]:
                    ld += [LD[(b >> 6) & 3], LD[(b >> 4) & 3], LD[(b >> 2) & 3], LD[b & 3]]
                j += n4
                ld = ld[:nv]
            first = fv[:8].hex() if at in (1, 2, 3) else fv.hex()
            out.append(dict(attr=ATTR.get(at, str(at)), la=la, nv=nv, first=first, ev=ev, ld=ld))
        i += 4 + ll
    return out


def sid_values(v):
    """Stream ids covered by a stream-typed vector (FirstValue + i)."""
    base = int(v["first"], 16)
    return [(f"{base + k:016x}", v["ev"][k], v["ld"][k] if v["ld"] else None) for k in range(v["nv"])]


def stats(xs):
    if not xs:
        return "n=0"
    return (f"n={len(xs)} min={min(xs):.3f} median={st.median(xs):.3f} "
            f"mean={st.mean(xs):.3f} max={max(xs):.3f}")


def fit_host(recs):
    """tap_ns -> capture-host ns: least squares through per-5 s minima of host - tap."""
    bins = {}
    for r in recs:
        k = r["tap_ns"] // 5_000_000_000
        d = r["host_ns"] - r["tap_ns"]
        if k not in bins or d < bins[k][1]:
            bins[k] = (r["tap_ns"], d)
    pts = sorted(bins.values())
    n = len(pts)
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    b = sum((x - mx) * (y - my) for x, y in pts) / sxx if sxx else 0.0
    a = my - b * mx
    resid = [y - (a + b * x) for x, y in pts]
    return (lambda t: t + a + b * t), dict(points=n, slope_ppm=b * 1e6,
                                           resid_ms_min=min(resid) / 1e6, resid_ms_max=max(resid) / 1e6)


def load_jsonl(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line.startswith("{"):
            out.append(json.loads(line))
    return out


def console_samples(path):
    """Yield (t_buildbox_s, cmd, text) from a console_poll transcript."""
    hdr = re.compile(r"^### (\S+)Z cmd='([^']*)' elapsed=")
    cur = None
    buf = []
    import datetime as dt
    for line in open(path, errors="replace"):
        m = hdr.match(line)
        if m:
            if cur:
                yield cur[0], cur[1], "".join(buf)
            t = dt.datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").replace(
                tzinfo=dt.timezone.utc).timestamp()
            cur, buf = (t, m.group(2)), []
        else:
            buf.append(line)
    if cur:
        yield cur[0], cur[1], "".join(buf)


def memword(text):
    m = re.search(r"^0x[0-9a-f]{8}\s+([0-9a-f]{2}) ([0-9a-f]{2}) ([0-9a-f]{2}) ([0-9a-f]{2})", text, re.M)
    if not m:
        return None
    return int("".join(reversed(m.groups())), 16)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pcap")
    ap.add_argument("--counters")
    ap.add_argument("--bind")
    ap.add_argument("--console")
    ap.add_argument("--console-offset-s", type=float, default=0.0)
    ap.add_argument("--json")
    a = ap.parse_args()

    recs = list(ws.records(a.pcap))
    recs.sort(key=lambda r: r["tap_ns"])
    host_of, fit = fit_host(recs)
    t0 = recs[0]["tap_ns"]
    T = lambda ns: (ns - t0) / 1e9  # noqa: E731  seconds on the tap clock from the first record
    H = lambda ns: host_of(ns) / 1e9  # noqa: E731  capture-server NTP seconds
    res = dict(pcap=a.pcap, records=len(recs), host_records_excluded=ws.HOST_RECORDS[0],
               fit=fit, t0_host=H(t0))
    print(f"tap records {len(recs)}, host-generated excluded {ws.HOST_RECORDS[0]}")
    print(f"clock fit: {fit}")
    print(f"t=0 is tap record 1 = capture-server {H(t0):.6f}")

    acmp, crf, aaf, msrp = [], [], [], []
    for r in recs:
        d = ws.decode(r)
        k = d.get("kind")
        if k == "ACMP":
            p = r["frame"][14:]
            if len(p) >= 54:
                acmp.append(dict(t=T(r["tap_ns"]), h=H(r["tap_ns"]), port=r["port"], msg=p[1] & 0xF,
                                 status=p[2] >> 3, sid=p[4:12].hex(), talker=p[20:28].hex(),
                                 listener=p[28:36].hex(), tuid=struct.unpack(">H", p[36:38])[0],
                                 luid=struct.unpack(">H", p[38:40])[0], dmac=p[40:46].hex(":"),
                                 cc=struct.unpack(">H", p[46:48])[0], seq=struct.unpack(">H", p[48:50])[0]))
        elif k == "CRF" and r["port"] == 3:
            crf.append((r["tap_ns"], d))
        elif k == "AAF" and r["port"] == 3:
            aaf.append((r["tap_ns"], d))
        elif k == "MSRP":
            msrp.append(dict(t=T(r["tap_ns"]), h=H(r["tap_ns"]), port=r["port"], vec=msrp_decode(r["frame"])))

    # ---- ACMP for the pair
    print("\n== ACMP for DUT talker uid 1 / peer listener uid 8 (tap s, capture-server UTC s)")
    pair = [x for x in acmp if x["talker"] == DUT_EID and x["tuid"] == 1 and x["msg"] in (0, 1, 2, 3, 6, 7, 8, 9)]
    for x in pair:
        print(f"{x['t']:10.6f} {x['h']:.6f} p{x['port']} {ACMPN[x['msg']]} status={x['status']}"
              f"({ACMP_STATUS.get(x['status'], '?')}) dmac={x['dmac']} cc={x['cc']}")
    bind = next((x for x in pair if x["msg"] == 6), None)
    unbind = next((x for x in pair if x["msg"] == 8), None)
    probes = [x for x in pair if x["msg"] == 1]
    res["acmp_pair"] = pair

    # ---- CRF emission
    print("\n== CRF PDUs from the DUT")
    bursts = []
    for ns, d in crf:
        if not bursts or ns - bursts[-1]["last_ns"] > 10e6:
            bursts.append(dict(first_ns=ns, last_ns=ns, n=0, seq0=d["avtp"]["seq"], seq_gaps=0,
                               prev_seq=None, max_gap_ns=0, tu=set(), vlan=set(), dst=set(), sid=set()))
        b = bursts[-1]
        if b["n"]:
            b["max_gap_ns"] = max(b["max_gap_ns"], ns - b["last_ns"])
            if d["avtp"]["seq"] != (b["prev_seq"] + 1) & 0xFF:
                b["seq_gaps"] += 1
        b["prev_seq"] = d["avtp"]["seq"]
        b["last_ns"] = ns
        b["n"] += 1
        b["tu"].add(d["avtp"]["tu"])
        b["vlan"].add(d["vlan"])
        b["dst"].add(d["dst"])
        b["sid"].add(d["avtp"]["stream_id"])
    for i, b in enumerate(bursts):
        dur = (b["last_ns"] - b["first_ns"]) / 1e9
        print(f"burst {i + 1}: {T(b['first_ns']):.6f} .. {T(b['last_ns']):.6f} tap s "
              f"(UTC {H(b['first_ns']):.6f} .. {H(b['last_ns']):.6f}), {dur:.3f} s, {b['n']} PDUs, "
              f"{b['n'] / dur if dur else 0:.2f} PDU/s, max interval {b['max_gap_ns'] / 1e6:.3f} ms, "
              f"seq discontinuities {b['seq_gaps']}, tu {sorted(b['tu'])}, vlan(pcp,vid) {sorted(b['vlan'])}, "
              f"dst {sorted(b['dst'])}, stream {sorted(b['sid'])}")
    ivals = [(crf[k][0] - crf[k - 1][0]) / 1e6 for k in range(1, len(crf))]
    print(f"all CRF PDUs {len(crf)}; intervals ms {stats(ivals)}")
    print(f"AAF PDUs from the DUT: {len(aaf)}")
    res["crf_bursts"] = [dict(first_t=T(b["first_ns"]), last_t=T(b["last_ns"]), first_h=H(b["first_ns"]),
                              last_h=H(b["last_ns"]), n=b["n"], max_interval_ms=b["max_gap_ns"] / 1e6,
                              seq_gaps=b["seq_gaps"], tu=sorted(b["tu"]), vlan=[list(v) for v in b["vlan"] if v])
                         for b in bursts]
    res["crf_total"] = len(crf)
    res["aaf_total"] = len(aaf)

    # ---- MSRP
    la_pdus = {2: [], 3: []}
    dut_talker, sw_listener, other = [], [], []
    for m in msrp:
        flagged = sorted({v["attr"] for v in m["vec"] if v["la"]})
        if flagged:
            la_pdus[m["port"]].append(dict(t=m["t"], h=m["h"], types=flagged,
                                           nv0=sorted({v["attr"] for v in m["vec"] if v["la"] and v["nv"] == 0}),
                                           all_types=sorted({v["attr"] for v in m["vec"]})))
        for v in m["vec"]:
            if v["attr"] in ("TalkerAdvertise", "TalkerFailed", "Listener"):
                for sid, ev, ld in sid_values(v):
                    if sid != DUT_SID:
                        continue
                    e = dict(t=m["t"], h=m["h"], port=m["port"], attr=v["attr"], ev=ev, ld=ld, la=v["la"])
                    if m["port"] == 3 and v["attr"] in ("TalkerAdvertise", "TalkerFailed"):
                        dut_talker.append(e)
                    elif m["port"] == 2 and v["attr"] == "Listener":
                        sw_listener.append(e)
                    else:
                        other.append(e)
    print(f"\n== MSRP: {len(msrp)} MRPDUs ({sum(1 for m in msrp if m['port'] == 3)} from the DUT, "
          f"{sum(1 for m in msrp if m['port'] == 2)} from the switch)")
    for port, name in ((2, "switch -> DUT"), (3, "DUT -> switch")):
        L = la_pdus[port]
        sp = [L[k]["t"] - L[k - 1]["t"] for k in range(1, len(L))]
        kinds = {}
        for x in L:
            key = (tuple(x["types"]), tuple(x["nv0"]))
            kinds[key] = kinds.get(key, 0) + 1
        print(f"LeaveAll MRPDUs {name}: {len(L)}; spacing s {stats(sp)}")
        for key, n in kinds.items():
            print(f"   flagged types {list(key[0])}, of which NumberOfValues-0 vectors {list(key[1])}: {n}")
    res["leaveall"] = {str(k): v for k, v in la_pdus.items()}

    def counts(evs):
        c = {}
        for e in evs:
            k = f"{e['attr']} {'LA ' if e['la'] else ''}{e['ev']}{'/' + e['ld'] if e['ld'] else ''}"
            c[k] = c.get(k, 0) + 1
        return c

    print(f"DUT Talker declarations for {DUT_SID}: {counts(dut_talker)}")
    print(f"switch Listener declarations for {DUT_SID}: {counts(sw_listener)}")
    if other:
        print(f"other declarations for {DUT_SID}: {counts(other)}")
    ta_first = next((e for e in dut_talker if e["attr"] == "TalkerAdvertise"), None)
    ta_lv = [e for e in dut_talker if e["attr"] == "TalkerAdvertise" and e["ev"] == "Lv"]
    tf = [e for e in dut_talker if e["attr"] == "TalkerFailed"]
    lr_first = next((e for e in sw_listener if e["ld"] in ("Ready", "ReadyFailed") and e["ev"] != "Lv"), None)
    l_first = sw_listener[0] if sw_listener else None
    l_lv = [e for e in sw_listener if e["ev"] == "Lv"]
    print("DUT TalkerAdvertise Lv:", [round(e["t"], 6) for e in ta_lv])
    print("DUT TalkerFailed:", [(round(e["t"], 6), e["ev"]) for e in tf])
    print("switch Listener Lv:", [(round(e["t"], 6), e["ld"]) for e in l_lv])
    print("first DUT TalkerAdvertise:", ta_first and (round(ta_first["t"], 6), ta_first["ev"]))
    print("first switch Listener (any):", l_first and (round(l_first["t"], 6), l_first["ev"], l_first["ld"]))
    print("first switch Listener Ready/ReadyFailed:", lr_first and (round(lr_first["t"], 6), lr_first["ev"], lr_first["ld"]))

    # switch Listener re-declaration after each DUT LeaveAll, and DUT TA after each switch LeaveAll
    def next_after(evs, t, attr=None):
        for e in evs:
            if e["t"] > t and (attr is None or e["attr"] == attr) and e["ev"] != "Lv":
                return e
        return None
    rd_l = []
    for x in la_pdus[3]:
        e = next_after(sw_listener, x["t"])
        rd_l.append(None if e is None else e["t"] - x["t"])
    rd_t = []
    for x in la_pdus[2]:
        e = next_after(dut_talker, x["t"], "TalkerAdvertise")
        rd_t.append(None if e is None else e["t"] - x["t"])

    # ---- acceptance
    print("\n== #530 acceptance quantities (tap clock)")
    acc = {}
    if bind and unbind:
        tb, tu_ = bind["t"], unbind["t"]
        acc["bind_t"], acc["unbind_t"], acc["bound_s"] = tb, tu_, tu_ - tb
        acc["bind_h"], acc["unbind_h"] = bind["h"], unbind["h"]
        print(f"bound window: CONNECT_RX {tb:.6f} .. DISCONNECT_RX {tu_:.6f} = {tu_ - tb:.3f} s "
              f"(UTC {bind['h']:.3f} .. {unbind['h']:.3f})")
        inb = lambda t: tb <= t <= tu_  # noqa: E731
        acc["dut_ta_lv_bound"] = [e["t"] for e in ta_lv if inb(e["t"])]
        acc["dut_tf_bound"] = [e["t"] for e in tf if inb(e["t"])]
        acc["sw_listener_lv_bound"] = [e["t"] for e in l_lv if inb(e["t"])]
        la_sw = [x["t"] for x in la_pdus[2] if inb(x["t"])]
        la_dut = [x["t"] for x in la_pdus[3] if inb(x["t"])]
        acc["leaveall_switch_bound"] = len(la_sw)
        acc["leaveall_dut_bound"] = len(la_dut)
        acc["leaveall_switch_spacing"] = stats([la_sw[k] - la_sw[k - 1] for k in range(1, len(la_sw))])
        acc["leaveall_dut_spacing"] = stats([la_dut[k] - la_dut[k - 1] for k in range(1, len(la_dut))])
        rl = [d for x, d in zip(la_pdus[3], rd_l) if inb(x["t"])]
        rt = [d for x, d in zip(la_pdus[2], rd_t) if inb(x["t"])]
        acc["switch_listener_redeclare_after_dut_leaveall_s"] = stats([d for d in rl if d is not None])
        acc["switch_listener_redeclare_missing"] = sum(1 for d in rl if d is None)
        acc["dut_ta_redeclare_after_switch_leaveall_s"] = stats([d for d in rt if d is not None])
        acc["dut_ta_redeclare_missing"] = sum(1 for d in rt if d is None)
        bb = [b for b in res["crf_bursts"] if b["last_t"] >= tb and b["first_t"] <= tu_ + 60]
        acc["bursts_overlapping_bound_window"] = len(bb)
        if bb:
            acc["first_pdu_t"], acc["last_pdu_t"] = bb[0]["first_t"], bb[-1]["last_t"]
            acc["stream_s"] = bb[-1]["last_t"] - bb[0]["first_t"]
            acc["first_pdu_after_bind_s"] = bb[0]["first_t"] - tb
            acc["last_pdu_after_unbind_s"] = bb[-1]["last_t"] - tu_
            acc["max_interval_ms"] = max(b["max_interval_ms"] for b in bb)
            acc["seq_gaps"] = sum(b["seq_gaps"] for b in bb)
        if lr_first and bb:
            acc["first_listener_ready_t"] = lr_first["t"]
            acc["first_listener_ready_h"] = lr_first["h"]
            acc["first_pdu_h"] = bb[0]["first_h"]
            acc["first_pdu_minus_first_ready_ms"] = (bb[0]["first_t"] - lr_first["t"]) * 1e3
        pre = [e for e in sw_listener if e["t"] < (bb[0]["first_t"] if bb else 1e18)]
        acc["switch_listener_before_first_pdu"] = counts(pre)
        acc["probe_responses"] = [(round(x["t"], 6), ACMP_STATUS.get(x["status"], x["status"])) for x in probes]
        after_unbind_l = [e for e in sw_listener if e["t"] >= tu_]
        acc["switch_listener_after_unbind"] = [(round(e["t"] - tu_, 6), e["ev"], e["ld"]) for e in after_unbind_l[:6]]
        ta_after = [e for e in dut_talker if e["t"] >= tu_ and e["attr"] == "TalkerAdvertise" and e["ev"] == "Lv"]
        acc["dut_ta_lv_after_unbind_s"] = [round(e["t"] - tu_, 6) for e in ta_after]
        last_probe = max((x["t"] for x in probes if x["t"] <= tu_), default=None)
        if last_probe is not None:
            acc["last_probe_response_t"] = last_probe
            acc["dut_ta_lv_after_last_probe_s"] = [round(e["t"] - last_probe, 6) for e in ta_after]
        for k, v in acc.items():
            print(f"  {k}: {v}")
    res["acceptance"] = acc

    # ---- counters
    if a.counters:
        print("\n== GET_COUNTERS (controller-host NTP time; tap s via the capture-server fit)")
        rows = [d for d in load_jsonl(a.counters) if d.get("type") == "counters"]
        so1 = [d for d in rows if d["target"] == DUT_EID and d["req_type"] == 6 and d["req_index"] == 1]
        so0 = [d for d in rows if d["target"] == DUT_EID and d["req_type"] == 6 and d["req_index"] == 0]
        si8 = [d for d in rows if d["target"] == PEER_EID and d["req_type"] == 5 and d["req_index"] == 8]
        bad = [d for d in rows if d.get("status") != "SUCCESS"]
        print(f"reads: SO1 {len(so1)}, SO0 {len(so0)}, peer SI8 {len(si8)}, not SUCCESS {len(bad)}")
        h0 = H(t0)
        prev = None
        changes = []
        for d in so1:
            c = d.get("decoded", {}).get("counters", {})
            k = (c.get("STREAM_START"), c.get("STREAM_STOP"), c.get("MEDIA_RESET"), c.get("TIMESTAMP_UNCERTAIN"))
            if k != prev:
                changes.append((round(d["t"] - h0, 3), round(d["t"], 3), c))
                prev = k
        print("SO1 STREAM_START/STOP/MEDIA_RESET/TIMESTAMP_UNCERTAIN changes (t tap-approx s, UTC, counters):")
        for x in changes:
            print("  ", x)
        ft = [(round(d["t"] - h0, 3), d["decoded"]["counters"]["FRAMES_TX"]) for d in so1 if "decoded" in d]
        res["so1_changes"] = changes
        res["so1_frames_tx"] = ft
        so0c = {json.dumps(d.get("decoded", {}).get("counters", {}), sort_keys=True) for d in so0}
        print(f"SO0 (AAF) distinct counter blocks: {so0c}")
        # FRAMES_TX increments: time of each change
        inc = []
        for k in range(1, len(ft)):
            if ft[k][1] != ft[k - 1][1]:
                inc.append((ft[k][0], ft[k - 1][1], ft[k][1]))
        steps = {}
        for _, a0, a1 in inc:
            steps[a1 - a0] = steps.get(a1 - a0, 0) + 1
        print(f"FRAMES_TX changes {len(inc)}; step sizes {steps}; first {inc[:3]}; last {inc[-3:]}")
        print(f"FRAMES_TX final {ft[-1] if ft else None}")
        pc = [(round(d["t"] - h0, 3), d["decoded"]["counters"]) for d in si8 if "decoded" in d]
        if pc:
            keys = ["MEDIA_LOCKED", "MEDIA_UNLOCKED", "STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                    "TIMESTAMP_UNCERTAIN", "UNSUPPORTED_FORMAT", "LATE_TIMESTAMP", "EARLY_TIMESTAMP"]
            prevk = None
            print("peer SI8 changes (excluding FRAMES_RX / TIMESTAMP_VALID):")
            for t, c in pc:
                kk = tuple(c.get(x) for x in keys)
                if kk != prevk:
                    print("  ", t, {x: c.get(x) for x in keys}, "FRAMES_RX", c.get("FRAMES_RX"))
                    prevk = kk
            print("peer SI8 last:", pc[-1])
            res["peer_si8_last"] = pc[-1]

    if a.bind:
        print("\n== bind window log")
        for d in load_jsonl(a.bind):
            if d["type"] in ("start", "bind", "unbind", "refused", "interrupted", "done"):
                print("  ", d["type"], round(d["t"] - H(t0), 3), {k: v for k, v in d.items() if k in ("response", "attempt", "reason", "argv")})
        st_rows = [d for d in load_jsonl(a.bind) if d["type"] == "state"]
        kinds = {}
        for d in st_rows:
            k = (d["tag"].split("+")[0].split("-")[0], d["peer_rx"].get("status"), d["peer_rx"].get("conn_count"),
                 d["peer_rx"].get("talker"), d["dut_tx"].get("conn_count"), d["dut_tx"].get("dmac"))
            kinds[k] = kinds.get(k, 0) + 1
        for k, v in kinds.items():
            print("   state", k, v)

    if a.console:
        print("\n== console (build-box time + offset -> capture-server time)")
        h0 = H(t0)
        series = {}
        status = {}
        for t, cmd, text in console_samples(a.console):
            tt = t + a.console_offset_s - h0
            if cmd.startswith("mem_read"):
                v = memword(text)
                series.setdefault(cmd.split()[1], []).append((tt, v))
            elif cmd == "milan_status":
                m = re.search(r"GPTP_GM=(\S+).*SYNC=(\d) ASCAPABLE=(\d) TU=(\d)", text, re.S)
                k = m.groups() if m else ("?",)
                status[k] = status.get(k, 0) + 1
        print("milan_status (GM, SYNC, ASCAPABLE, TU):", status)
        names = {"0x90000750": "CRFT_CTRL", "0x90000764": "CRFT_COUNT", "0x90000694": "LWSRP_STATUS",
                 "0x9000066c": "ACMP_TALKER", "0x90000780": "CLKV_TUCNT", "0x900007e8": "GPTP_DROPW",
                 "0x900007ec": "GPTP_DROPE"}
        res["console"] = {}
        for addr, ser in series.items():
            nm = names.get(addr, addr)
            if nm == "CRFT_COUNT":
                print(f"{nm}: samples {len(ser)}, first {ser[0][1]:#x} at {ser[0][0]:.3f}, last {ser[-1][1]} "
                      f"({ser[-1][1]:#x}) at {ser[-1][0]:.3f}")
                fz = next((ser[k][0] for k in range(len(ser)) if all(s[1] == ser[-1][1] for s in ser[k:])), None)
                print(f"   frozen at its final value from {fz:.3f}")
                res["console"][nm] = dict(first=ser[0][1], last=ser[-1][1], frozen_from=fz)
                continue
            edges = []
            prev = object()
            for tt, v in ser:
                if v != prev:
                    edges.append((round(tt, 3), None if v is None else f"{v:#x}"))
                    prev = v
            print(f"{nm}: samples {len(ser)}, edges {len(edges) - 1}: {edges[:12]}{' ...' if len(edges) > 12 else ''}")
            res["console"][nm] = edges
    if a.json:
        with open(a.json, "w") as f:
            json.dump(res, f, indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
