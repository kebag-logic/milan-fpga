"""Offline replay of one lane-B2 action capture; writes analysis.json, msrp.tsv, acmp.tsv.

Independent of the live runner: it re-reads the raw tap capture, unwraps the
tap clock (wire_summary.records), decodes every MSRPDU strictly, and derives
every time below on that one tap clock.

usage: b2_analyze.py <bind|cycles>/<name>
"""
import collections, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records

if sys.flags.optimize:
    raise SystemExit("refused: assertions are part of this analysis; do not run with -O")
packet = Path(__file__).resolve().parent.parent
rel = sys.argv[1]
dest = packet / rel
name = dest.name
result = json.loads((dest / "result.json").read_text())
mode = result["mode"]
SID = "0200000000010001"
DUT_EID, DUT_MAC = "020000fffe000001", "020000000001"
PDU_PERIOD_NS = 2_000_000          # CRF: 500 PDU/s
SETTLE_NS = 500_000_000            # #75 stop-assertion settling allowance
LEAVETIME_NS = 7_500_000_000       # processor T-MRP-LEAVE upper bound (4.5-7.5 s)
EV = ["New", "JoinIn", "In", "JoinMt", "Mt", "Lv"]
DECL = ("New", "JoinIn", "JoinMt")
TYPES = {1: "TalkerAdvertise", 2: "TalkerFailed", 3: "Listener", 4: "Domain"}
ALEN = {1: 25, 2: 34, 3: 8, 4: 4}

raw = list(records("/tmp/b2-a440/raw/" + name + "/tap.pcap"))
t0 = raw[0]["tap_ns"]
events, acmp, crf, pdus, malformed = [], [], [], [], []


def msrp(p, ns, sender, pdu_index):
    if not (p and p[0] == 0):
        raise ValueError("MSRP version")
    o = 1
    out = []
    while o + 2 <= len(p) and p[o:o + 2] != bytes(2):
        if o + 4 > len(p):
            raise ValueError("message header")
        typ, alen = p[o:o + 2]
        length = int.from_bytes(p[o + 2:o + 4], "big")
        o += 4
        end = o + length
        if typ not in TYPES or alen != ALEN[typ] or end > len(p):
            raise ValueError("message shape")
        while o + 2 <= end and p[o:o + 2] != bytes(2):
            h = int.from_bytes(p[o:o + 2], "big")
            o += 2
            n, la = h & 8191, h >> 13
            if la not in (0, 1) or o + alen > end:
                raise ValueError("vector header")
            fv = p[o:o + alen]
            o += alen
            ne, nf = (n + 2) // 3, ((n + 3) // 4 if typ == 3 else 0)
            if o + ne + nf > end:
                raise ValueError("packed events length")
            ep, fp = p[o:o + ne], p[o + ne:o + ne + nf]
            o += ne + nf
            if la:
                out.append(dict(ns=ns, sender=sender, type=TYPES[typ], event="LeaveAll", sid=None, listener=None, pdu=pdu_index))
            for k in range(n):
                if ep[k // 3] >= 216:
                    raise ValueError("three-packed event")
                ev = (ep[k // 3] // (36, 6, 1)[k % 3]) % 6
                sid = (fv[:6] + ((int.from_bytes(fv[6:8], "big") + k) & 65535).to_bytes(2, "big")).hex() if typ in (1, 2, 3) else None
                lv = (fp[k // 4] // (64, 16, 4, 1)[k % 4]) % 4 if typ == 3 else None
                out.append(dict(ns=ns, sender=sender, type=TYPES[typ], event=EV[ev], sid=sid, listener=lv, pdu=pdu_index))
        if not (o + 2 == end and p[o:o + 2] == bytes(2)):
            raise ValueError("attribute endmark")
        o = end
    if not (o + 2 <= len(p) and p[o:o + 2] == bytes(2)):
        raise ValueError("PDU endmark")
    return out


for rec in raw:
    fr = rec["frame"]
    ns = rec["tap_ns"] - t0
    et = int.from_bytes(fr[12:14], "big")
    off, vlan = 14, None
    if et == 0x8100:
        tci = int.from_bytes(fr[14:16], "big")
        vlan = (tci >> 13, tci & 4095)
        et = int.from_bytes(fr[16:18], "big")
        off = 18
    p = fr[off:]
    sender = "DUT" if rec["port"] == 3 else "bridge"
    if et == 0x22EA:
        idx = len(pdus)
        try:
            evs = msrp(p, ns, sender, idx)
        except (ValueError, IndexError) as e:
            malformed.append(dict(ns=ns, error=str(e)))
            evs = []
        pdus.append(dict(ns=ns, sender=sender, source=fr[6:12].hex(), leaveall=any(e["event"] == "LeaveAll" for e in evs),
                         summary=sorted({(e["type"], e["event"]) for e in evs})))
        events.extend(evs)
    if et == 0x22F0 and len(p) >= 12:
        if p[0] == 0xFC and len(p) >= 56:
            acmp.append(dict(ns=ns, sender=sender, mt=p[1] & 15, status=p[2] >> 3, sid=p[4:12].hex(),
                             controller=p[12:20].hex(), talker=p[20:28].hex(), listener=p[28:36].hex(),
                             tuid=int.from_bytes(p[36:38], "big"), luid=int.from_bytes(p[38:40], "big"),
                             dmac=p[40:46].hex(), seq=int.from_bytes(p[48:50], "big")))
        if p[0] == 4:
            valid = (len(p) >= 28 and p[1] & 0xF0 == 0x80 and p[3] == 1 and int.from_bytes(p[12:16], "big") == 48000
                     and p[16:20] == bytes.fromhex("00080060") and vlan == (3, 2))
            crf.append(dict(ns=ns, sid=p[4:12].hex(), valid=valid, port=rec["port"], seq=p[2],
                            timestamp=int.from_bytes(p[20:28], "big"), dmac=fr[:6].hex(), src=fr[6:12].hex(),
                            flags=p[1] & 0x0F))

for i, e in enumerate(events):
    e["i"] = i
target = [r for r in crf if r["valid"] and r["sid"] == SID and r["port"] == 3]
foreign_target = [r for r in crf if r["sid"] == SID and not (r["valid"] and r["port"] == 3)]
a = dict(name=name, mode=mode, records=len(raw), msrp_pdus=len(pdus), msrp_events=len(events),
         msrp_malformed=malformed, target_valid_pdus=len(target), target_invalid_or_misdirected=len(foreign_target),
         capture_span_s=(raw[-1]["tap_ns"] - t0) / 1e9,
         reversals=sum(b["tap_ns"] < x["tap_ns"] for x, b in zip(raw, raw[1:])),
         anchor_spread_s=(max(r["host_ns"] - r["tap_ns"] for r in raw) - min(r["host_ns"] - r["tap_ns"] for r in raw)) / 1e9)


def s(ns):
    return None if ns is None else round(ns / 1e9, 9)


def txn(action, mt):
    rows = [json.loads(x) for x in (dest / (action + ".jsonl")).read_text().splitlines()]
    return next(r for r in rows if r.get("kind") == "transaction" and r["mt"] == mt)


def wire_of(tx, mt_resp):
    cmd = next(r for r in acmp if r["mt"] == mt_resp - 1 and r["seq"] == tx["seq"] and r["controller"] == tx["response"]["controller"])
    rsp = next(r for r in acmp if r["mt"] == mt_resp and r["seq"] == tx["seq"] and r["controller"] == tx["response"]["controller"] and r["status"] == 0)
    return cmd, rsp


def counters(which):
    rows = [json.loads(x) for x in (dest / ("snapshot-" + which + ".jsonl")).read_text().splitlines()]
    r = next(x["response"] for x in rows if x.get("role") == "dut" and x.get("what") == "counter-6-1")
    return r["counters"]


def console_word(which, addr):
    import re
    t = (dest / ("console-" + which + ".txt")).read_text()
    m = re.search(r"^" + addr + r"  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})", t, re.M)
    return int.from_bytes(bytes.fromhex(m[1]), "little") if m else None


def order(e):
    return (e["ns"], e["i"])


cb, ca = counters("before"), counters("after")
a["dut_out1_start_stop_before"] = [cb.get("0"), cb.get("1")]
a["dut_out1_start_stop_after"] = [ca.get("0"), ca.get("1")]
a["dut_out1_start_stop_delta"] = [ca.get("0") - cb.get("0"), ca.get("1") - cb.get("1")]
a["crft_count_before_after"] = [console_word("before", "0x90000764"), console_word("after", "0x90000764")]
a["rst_epoch_before_after"] = [console_word("before", "0x90000720"), console_word("after", "0x90000720")]
a["pp_diag_before_after"] = [console_word("before", "0x90000930"), console_word("after", "0x90000930")]

if mode in ("bind", "observe"):
    cut = None
    if mode == "bind":
        tx = txn("bind", 6)
        cmd, ack = wire_of(tx, 7)
        cut = cmd["ns"]
    pre_end = cut if cut is not None else raw[-1]["tap_ns"] - t0
    pre = [e for e in events if e["ns"] < pre_end]
    a["pre_window_s"] = s(pre_end)
    a["pre_dut_leaveall_pdus"] = len({e["pdu"] for e in pre if e["sender"] == "DUT" and e["event"] == "LeaveAll"})
    a["pre_dut_target_ta_events"] = dict(collections.Counter(e["event"] for e in pre if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID))
    a["pre_dut_target_ta_declarations"] = sum(e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] in DECL for e in pre)
    a["pre_dut_ta_declarations_any_stream"] = sum(e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["event"] in DECL for e in pre)
    a["pre_bridge_target_listener_declarations"] = sum(e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] in DECL for e in pre)
    a["pre_target_pdus"] = sum(r["ns"] < pre_end for r in target)
    a["fresh"] = (a["pre_dut_target_ta_declarations"] == 0 and a["pre_dut_leaveall_pdus"] >= 1
                  and a["pre_bridge_target_listener_declarations"] == 0 and a["pre_target_pdus"] == 0 and a["pre_window_s"] >= 15.9)
if mode == "bind":
    R = ack["ns"]
    a["connect_command_s"], a["response_s"] = s(cmd["ns"]), s(R)
    probes = [r for r in acmp if r["mt"] in (0, 1) and r["talker"] == DUT_EID and r["tuid"] == 1 and r["ns"] >= cmd["ns"]]
    a["probe_exchanges"] = [dict(after_response_s=s(r["ns"] - R), mt=r["mt"], sender=r["sender"], status=r["status"], seq=r["seq"]) for r in probes]
    first_probe_resp = next((r for r in probes if r["mt"] == 1 and r["sender"] == "DUT"), None)
    a["first_probe_response_status"] = first_probe_resp["status"] if first_probe_resp else None
    a["first_probe_response_after_response_s"] = s(first_probe_resp["ns"] - R) if first_probe_resp else None
    post = [e for e in events if e["ns"] >= cmd["ns"]]
    ta = next((e for e in post if e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] in DECL), None)
    a["first_dut_ta"] = dict(after_response_s=s(ta["ns"] - R), event=ta["event"]) if ta else None
    bpdu = next((p for p in pdus if p["sender"] == "bridge" and p["ns"] >= R), None)
    a["first_bridge_mrpdu"] = dict(after_response_s=s(bpdu["ns"] - R), leaveall=bpdu["leaveall"], content=bpdu["summary"]) if bpdu else None
    bpdu_cmd = next((p for p in pdus if p["sender"] == "bridge" and p["ns"] >= cmd["ns"]), None)
    a["first_bridge_mrpdu_after_command_s"] = s(bpdu_cmd["ns"] - R) if bpdu_cmd else None
    rd = next((e for e in post if e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] in DECL and e["listener"] == 2), None)
    a["first_bridge_ready"] = dict(after_response_s=s(rd["ns"] - R), event=rd["event"]) if rd else None
    la_before_ready = [p for p in pdus if p["sender"] == "bridge" and p["leaveall"] and R <= p["ns"] <= (rd["ns"] if rd else R)]
    a["bridge_leaveall_between_response_and_ready"] = len(la_before_ready)
    first = next((r for r in target if r["ns"] >= R), None)
    a["first_valid_pdu_s"] = s(first["ns"]) if first else None
    a["latency_s"] = s(first["ns"] - R) if first else None
    assert a["latency_s"] == result["latency_s"] or first is None, "independent timing mismatch"
    if first:
        nxt = target[target.index(first) + 1] if target.index(first) + 1 < len(target) else None
        a["first_pair_progresses"] = bool(nxt and nxt["seq"] == (first["seq"] + 1) % 256 and nxt["timestamp"] > first["timestamp"])
        a["first_pdu_src_ok"] = first["src"] == DUT_MAC
        st = [json.loads(x) for x in (dest / "snapshot-after.jsonl").read_text().splitlines()]
        peer8 = next(x["response"] for x in st if x.get("role") == "peer" and x.get("what") == "state-5-8")
        a["settled_listener_state"] = dict(conn_count=peer8.get("conn_count"), sid=peer8.get("stream_id"), dmac=peer8.get("dmac"))
        a["first_pdu_dmac_ok"] = first["dmac"] == peer8.get("dmac") and peer8.get("stream_id") == SID
        a["ready_to_first_pdu_s"] = s(first["ns"] - rd["ns"]) if rd else None
    a["result"] = "PASS" if (a.get("fresh") and first and a["latency_s"] < 1 and a.get("first_pair_progresses")
                             and a.get("first_pdu_dmac_ok") and a.get("first_pdu_src_ok")) else ("NOT_FRESH" if not a.get("fresh") else "FAIL")
if mode == "unbind":
    tx = txn("unbind", 8)
    cmd, dr = wire_of(tx, 9)
    D = dr["ns"]
    a["disconnect_response_s"] = s(D)
    lv = next((e for e in events if e["ns"] >= D and e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] == "Lv"), None)
    a["bridge_listener_lv_after_response_s"] = s(lv["ns"] - D) if lv else None
    last = max((r["ns"] for r in target), default=None)
    a["last_valid_pdu_after_response_s"] = s(last - D) if last is not None else None
    a["pdus_after_lv_plus_period"] = sum(r["ns"] > lv["ns"] + PDU_PERIOD_NS for r in target) if lv else None
    ta_lv = next((e for e in events if e["ns"] >= D and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] == "Lv"), None)
    a["dut_ta_lv_after_response_s"] = s(ta_lv["ns"] - D) if ta_lv else None
    a["dut_ta_declarations_after_lv"] = sum(e["ns"] > ta_lv["ns"] and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] in DECL for e in events) if ta_lv else None
    a["settle_after_ta_lv_s"] = s(raw[-1]["tap_ns"] - t0 - ta_lv["ns"]) if ta_lv else None
    a["result"] = "SETTLED" if ta_lv and a["dut_ta_declarations_after_lv"] == 0 and a["pdus_after_lv_plus_period"] == 0 else "FAIL"
if mode == "cycle":
    txd, txc = txn("cycle", 8), txn("cycle", 6)
    dcmd, dr = wire_of(txd, 9)
    ccmd, ack = wire_of(txc, 7)
    D, C, R = dr["ns"], ccmd["ns"], ack["ns"]
    a.update(disconnect_response_s=s(D), connect_command_s=s(C), response_s=s(R), hold_s=s(C - D))
    hold = [r for r in target if D <= r["ns"] < R]
    a["hold_pdus"] = len(hold)
    a["settled_pdus"] = sum(D + SETTLE_NS <= r["ns"] < R for r in target)
    a["last_half_second_pdus"] = sum(C - SETTLE_NS < r["ns"] < C for r in target)
    a["stopped"] = a["settled_pdus"] == 0
    lv = next((e for e in events if D <= e["ns"] < R and e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] == "Lv"), None)
    a["bridge_lv_after_disconnect_s"] = s(lv["ns"] - D) if lv else None
    if lv:
        before = [r for r in target if r["ns"] < R]
        last_stop = max((r["ns"] for r in before if r["ns"] <= lv["ns"] + PDU_PERIOD_NS), default=None)
        after_period = [r for r in before if r["ns"] > lv["ns"] + PDU_PERIOD_NS]
        a["pdus_after_lv_plus_period"] = len(after_period)
        last_before_R = max((r["ns"] for r in before), default=None)
        a["last_pdu_after_lv_s"] = s(last_before_R - lv["ns"]) if last_before_R is not None else None
        a["last_pdu_after_disconnect_s"] = s(last_before_R - D) if last_before_R is not None else None
        # Registrar state at the withdrawal: the last Listener-type LeaveAll (own or received)
        # before the Lv, and whether a bridge Listener declaration for the stream re-registered
        # it (LV -> IN) between that LeaveAll and the Lv, in capture order.
        ordered = sorted(events, key=order)
        li = next(k for k, e in enumerate(ordered) if e["i"] == lv["i"])
        la = next((e for e in reversed(ordered[:li]) if e["event"] == "LeaveAll" and e["type"] == "Listener"), None)
        lai = next(k for k, e in enumerate(ordered) if la and e["i"] == la["i"]) if la else None
        # Without a LeaveAll in the capture, IN must be shown by a bridge declaration of the
        # stream (rJoinIn/rJoinMt/rNew leave or put the registrar IN) seen before the Lv.
        reg = [e for e in ordered[(lai + 1 if la else 0):li] if e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] in DECL]
        a["last_listener_leaveall_before_lv"] = dict(sender=la["sender"], before_lv_s=s(lv["ns"] - la["ns"])) if la else None
        a["reregistered_after_leaveall"] = bool(reg) if la else None
        a["bridge_declarations_before_lv"] = len(reg)
        a["last_bridge_declaration_before_lv_s"] = s(lv["ns"] - reg[-1]["ns"]) if reg else None
        own = [e for e in events if e["sender"] == "DUT" and e["event"] == "LeaveAll" and e["type"] == "Listener"]
        near = min(own, key=lambda e: abs(e["ns"] - lv["ns"]), default=None)
        a["nearest_own_leaveall_minus_lv_s"] = s(near["ns"] - lv["ns"]) if near else None
        # The own sLA edge precedes its LeaveAll frame by the applicant walk (microseconds):
        # a frame less than 1 ms after the Lv means the registrar may already have been LV.
        own_just_after = near is not None and 0 <= near["ns"] - lv["ns"] < 1_000_000
        if (la and not reg and lv["ns"] - la["ns"] < LEAVETIME_NS) or own_just_after:
            a["registrar_at_lv"] = "LV"
        elif reg:
            a["registrar_at_lv"] = "IN"
        else:
            a["registrar_at_lv"] = "UNDETERMINED"
        if a["registrar_at_lv"] in ("IN", "UNDETERMINED"):
            a["stop_608"] = "PASS" if a["pdus_after_lv_plus_period"] == 0 else "FAIL"
        else:
            a["stop_608"] = "LV-WINDOW: stop not graded at one PDU (documented LV + rLv)"
    else:
        a["stop_608"] = "NO-LV"
    a["dut_ta_declarations_in_hold"] = sum(D <= e["ns"] < C and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] in DECL for e in events)
    a["dut_ta_lv_in_hold"] = sum(D <= e["ns"] < C and e["sender"] == "DUT" and e["type"] == "TalkerAdvertise" and e["sid"] == SID and e["event"] == "Lv" for e in events)
    first = next((r for r in target if r["ns"] >= R), None)
    a["restart_s"] = s(first["ns"] - R) if first else None
    assert a["restart_s"] == result["latency_s"] or first is None, "independent timing mismatch"
    if first:
        nxt = target[target.index(first) + 1] if target.index(first) + 1 < len(target) else None
        a["first_pair_progresses"] = bool(nxt and nxt["seq"] == (first["seq"] + 1) % 256 and nxt["timestamp"] > first["timestamp"])
    redecl = next((e for e in events if e["ns"] >= R and e["sender"] == "bridge" and e["type"] == "Listener" and e["sid"] == SID and e["event"] in DECL and e["listener"] == 2), None)
    a["bridge_ready_after_response_s"] = s(redecl["ns"] - R) if redecl else None
    a["demonstrated_restart"] = bool(a["stopped"] and first and a["restart_s"] >= 0)
    a["restart_75"] = ("PASS" if a["restart_s"] < 1 else "FAIL") if a["demonstrated_restart"] else "NOT RESTART"
    a["counted_stop_start"] = a["dut_out1_start_stop_delta"] == [1, 1] if a["stopped"] else a["dut_out1_start_stop_delta"] == [0, 0]
for window, (lo, hi) in {"whole": (0, raw[-1]["tap_ns"] - t0)}.items():
    a["msrp_pdus_by_sender"] = dict(collections.Counter(p["sender"] for p in pdus if lo <= p["ns"] <= hi))
    a["leaveall_pdus_by_sender"] = dict(collections.Counter(p["sender"] for p in pdus if p["leaveall"]))
with (dest / "msrp.tsv").open("w") as f:
    f.write("t_s\tsender\ttype\tevent\tstream_id\tlistener\n")
    for e in events:
        f.write(f"{e['ns'] / 1e9:.9f}\t{e['sender']}\t{e['type']}\t{e['event']}\t{e['sid']}\t{e['listener']}\n")
with (dest / "acmp.tsv").open("w") as f:
    f.write("t_s\tsender\tmt\tstatus\tseq\ttalker\ttuid\tlistener\tluid\n")
    for r in acmp:
        f.write(f"{r['ns'] / 1e9:.9f}\t{r['sender']}\t{r['mt']}\t{r['status']}\t{r['seq']}\t{r['talker']}\t{r['tuid']}\t{r['listener']}\t{r['luid']}\n")
(dest / "analysis.json").write_text(json.dumps(a, indent=2) + "\n")
if malformed:
    raise SystemExit("malformed MSRP: " + json.dumps(malformed[:3]))
print(name, mode, a.get("result") or a.get("restart_75"), a.get("latency_s") or a.get("restart_s"), a.get("stop_608", ""))
