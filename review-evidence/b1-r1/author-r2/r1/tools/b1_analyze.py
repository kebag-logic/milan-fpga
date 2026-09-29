"""Analyze one lane-B1 action from its raw records; no bench access.

Derived from the PR #600 analyzer (analyze.py in this directory). Adds the
firmware-published link state (MAC_STATUS, link_status, LINKG_STAT), the AVB
interface link counters, and for the software-grandmaster kind the PHC
steps, holdover, `tu`, `mr`, MEDIA_RESET and servo trajectories.

usage: b1_analyze.py <name>
Writes bench/<name>/analysis.json and bench/<name>/raw-artifacts.json.
"""
from pathlib import Path
import hashlib, json, re, statistics, struct, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

SWITCH = "3cc0c6fffefe0210"
HOST_GM = "<controller-host-eui64>"
DUT_SID = "0200000000010001"
PEER_SID = "3cc0c60102034000"
name = sys.argv[1]
root = Path("/tmp/b1-a438/raw") / name
packet = Path(__file__).resolve().parent.parent / "bench" / name


def load(n):
    p = root / n
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


events = load("events.jsonl")
console = load("console.jsonl")
ctrl = load("controller.jsonl")


def offset(role, tag=None):
    a = [r for r in events if r["kind"] == "clock" and r["role"] == role and (tag is None or r["tag"] == tag)]
    r = min(a, key=lambda x: x["t1"] - x["t0"])
    return r["remote"] - (r["t0"] + r["t1"]) / 2, (r["t1"] - r["t0"]) / 2


co, ce = offset("controller")
to, te = offset("tap")
for r in ctrl:
    r["local_t"] = r["t"] - co
kind_off = next((r["t"] for r in events if r["kind"] == "power-command" and r["value"] == "off"), None)
kind_on = next((r["t"] for r in events if r["kind"] == "power-command" and r["value"] == "on"), None)
gm_start = next((r["t"] for r in events if r["kind"] == "gm-start"), None)
gm_end = next((r["t"] for r in events if r["kind"] == "gm-end"), None)
T0 = kind_off or gm_start or (console[0]["t"] if console else 0)


def rel(t):
    return None if t is None else round(t - T0, 3)


sts, words = [], {}
for r in console:
    if r["cmd"] == "milan_status":
        d = {k: v for k, v in re.findall(r"(\w+)=([a-zA-Z0-9_]+)", r["raw"])}
        if "TAI_NS" in d and "SYNC" in d:
            d["t"], d["end"] = r["t"], r["end"]
            sts.append(d)
    else:
        m = re.search(r"^(0x[0-9a-f]+)  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})", r["raw"], re.M)
        if m:
            words.setdefault(m[1], []).append((r["t"], int.from_bytes(bytes.fromhex(m[2]), "little")))


def changes(rows, f=lambda v: v):
    out, prev = [], object()
    for t, v in rows:
        v = f(v)
        if v != prev:
            out.append([rel(t), v])
            prev = v
    return out


W = lambda a: words.get(a, [])
S = dict(name=name, T0=T0, T0_is="OUT4 off command" if kind_off else ("software GM start" if gm_start else "first console sample"),
         clock_offset_s=dict(controller=co, tap=to), clock_half_rtt_s=dict(controller=ce, tap=te),
         console_samples=len(sts),
         max_console_gap_s=max([b["t"] - a["t"] for a, b in zip(sts, sts[1:])] or [0]),
         reset_epochs=sorted({v for _, v in W("0x90000720")}),
         mac_status=changes(W("0x90000110"), hex), link_status_csr=changes(W("0xf000181c"), hex),
         linkg_stat=changes(W("0x90000774"), hex),
         clkv_tucnt_first_last=[W("0x90000780")[0][1], W("0x90000780")[-1][1]] if W("0x90000780") else None,
         servo=changes(W("0x900008f8"), lambda v: dict(state=v & 7, locked_mmcm=(v >> 5) & 1, discards=(v >> 10) & 63,
                                                        trim_ppm=round(struct.unpack("<h", struct.pack("<H", v >> 16))[0] / 16, 2))),
         crf_ctrl=changes(W("0x90000750"), hex),
         crft_count_first_last=[W("0x90000764")[0][1], W("0x90000764")[-1][1]] if W("0x90000764") else None,
         gm=changes([(r["t"], r["GPTP_GM"]) for r in sts]),
         health=changes([(r["t"], "sync%s asc%s tu%s" % (r["SYNC"], r["ASCAPABLE"], r["TU"])) for r in sts]),
         holdover=changes([(r["t"], (int(r["CLKV_STAT"], 16) >> 3) & 1) for r in sts]),
         events=[dict(kind=e["kind"], t=rel(e["t"]), **{k: e[k] for k in ("value", "rc") if k in e}) for e in events
                 if e["kind"] in ("power-command", "power-result", "gm-start", "gm-end", "gm-prep-offset")])
if kind_off:
    S.update(off=kind_off, on=kind_on, off_hold_s=kind_on - kind_off)

# PHC discontinuities: the change of (PHC - wall) between two console samples.
steps = []
for a, b in zip(sts, sts[1:]):
    delta = (int(b["TAI_NS"], 16) - int(a["TAI_NS"], 16)) / 1e9 - (b["t"] - a["t"])
    if abs(delta) > 0.0005:  # console jitter measured at +/-0.11 ms
        steps.append(dict(bracket=[rel(a["t"]), rel(b["end"])], phc_minus_wall_delta_s=round(delta, 6)))
S["phc_discontinuities"] = steps

# The firmware-published link state.
mac = W("0x90000110")
down = next((i for i, (t, v) in enumerate(mac) if t > T0 and not v & 1), None)
if down is not None:
    S["mac_link_down"] = dict(first_down=rel(mac[down][0]), last_up_before=rel(mac[down - 1][0]) if down else None)
    up = next((i for i in range(down, len(mac)) if mac[i][1] & 1), None)
    if up is not None:
        S["mac_link_up"] = dict(first_up=rel(mac[up][0]), last_down_before=rel(mac[up - 1][0]), value=hex(mac[up][1]))
S["mac_status_values"] = sorted({hex(v) for _, v in mac})

# Controller view.
S["carrier"] = changes([(r["local_t"], r["value"]) for r in ctrl if r.get("type") == "carrier"])
S["counter_endpoints"], S["counter_transitions"] = {}, {}
for role, what in [("dut", "counter-9-0"), ("dut", "counter-5-1"), ("dut", "counter-6-1"), ("dut", "counter-36-0"),
                   ("peer", "counter-9-0"), ("peer", "counter-5-8"), ("peer", "counter-6-2"), ("peer", "counter-36-0")]:
    a = [r for r in ctrl if r.get("role") == role and r.get("what") == what and r["response"].get("status") == "SUCCESS"]
    if a:
        first, last = a[0]["response"]["counters"], a[-1]["response"]["counters"]
        S["counter_endpoints"][role + ":" + what] = dict(first=first, last=last,
                                                        delta={k: last[k] - v for k, v in first.items()}, polls=len(a))
        keep = [k for k in first if int(k) < 11]
        S["counter_transitions"][role + ":" + what] = changes(
            [(r["local_t"], {k: r["response"]["counters"][k] for k in keep}) for r in a])
S["link_counters"] = {k: dict(LINK_UP=v["first"]["0"], LINK_DOWN=v["first"]["1"], end_LINK_UP=v["last"]["0"],
                              end_LINK_DOWN=v["last"]["1"], GM_CHANGED=[v["first"].get("5"), v["last"].get("5")])
                      for k, v in S["counter_endpoints"].items() if k.endswith("counter-9-0")}
states = [r for r in ctrl if r.get("what", "").startswith("state-") and r["response"].get("status") == 0]
S["bindings"] = dict(polls=len(states), all_connected=all(r["response"].get("conn_count") == 1 for r in states),
                     conn_counts=sorted({r["response"].get("conn_count") for r in states}))
S["peer_available_index"] = [x[1] for x in changes([(r["local_t"], r["available_index"]) for r in ctrl
                                                     if r.get("type") == "adp" and r.get("entity_id") == "3cc0c60102030000"])][::max(1, 1)]
S["peer_available_index"] = [S["peer_available_index"][0], S["peer_available_index"][-1]] if S["peer_available_index"] else None
S["dut_avb_gm"] = changes([(r["local_t"], r["response"].get("decoded", {}).get("gm")) for r in ctrl
                           if r.get("role") == "dut" and r.get("what") == "avb" and r["response"].get("status") == "SUCCESS"])

# Wire, from the inline tap.
raw = list(records(str(root / "tap.pcap"))) if (root / "tap.pcap").exists() else []
anchors = [(r["host_ns"] - r["tap_ns"]) / 1e9 for r in raw]
anchor = statistics.median(anchors) if anchors else 0
wire = []
for r in raw:
    try:
        d = decode(r)
    except (IndexError, struct.error):
        continue
    d["t"] = r["tap_ns"] / 1e9 + anchor - to
    if d.get("kind") == "CRF":
        f = r["frame"]
        o = 18 if f[12:14] == b"\x81\x00" else 14
        p = f[o:]
        d["avtp"]["mr"] = (p[1] >> 3) & 1
        d["avtp"]["valid"] = (len(p) >= 28 and p[0] == 4 and p[1] & 0xF0 == 0x80 and p[3] == 1
                              and int.from_bytes(p[12:16], "big") == 48000 and p[16:20] == bytes.fromhex("00080060")
                              and d["vlan"] == (3, 2) and p[4:12].hex() == (DUT_SID if r["port"] == 3 else PEER_SID))
        d["avtp"]["ts0"] = int.from_bytes(p[20:28], "big") if len(p) >= 28 else None
    wire.append(d)
wire.sort(key=lambda d: d["t"])
S["tap_records"] = len(wire)
S["tap_anchor_spread_s"] = [min(anchors) - anchor, max(anchors) - anchor] if anchors else None
S["wire"] = {}
for role, port in [("dut", 3), ("peer", 2)]:
    a = [r for r in wire if r.get("kind") == "CRF" and r["port"] == port]
    S["wire"][role] = dict(pdus=len(a), valid_pdus=sum(bool(r["avtp"]["valid"]) for r in a),
                           tu_counts={str(i): sum(r["avtp"]["tu"] == i for r in a) for i in (0, 1)},
                           mr=changes([(r["t"], r["avtp"]["mr"]) for r in a]),
                           tu=changes([(r["t"], r["avtp"]["tu"]) for r in a]),
                           max_gap_s=round(max([b["t"] - x["t"] for x, b in zip(a, a[1:])] or [0]), 4),
                           first=rel(a[0]["t"]) if a else None, last=rel(a[-1]["t"]) if a else None)
ann = [r for r in wire if r.get("kind") == "gPTP Announce" and r["port"] == 2]
S["announce_gm"] = changes([(r["t"], (r["ptp"]["gm_id"], r["ptp"]["gm_prio1"], r["ptp"]["steps_removed"])) for r in ann])

if kind_off:
    sw = [r for r in wire if r["port"] == 2]
    S["last_far_frame_before_on"] = rel(max((r["t"] for r in sw if kind_off < r["t"] < kind_on), default=None) or None)
    S["far_frames_during_off_after_5s"] = sum(1 for r in sw if kind_off + 5 < r["t"] < kind_on)
    post = [r for r in wire if r["t"] > kind_on]
    S["first_wire_return"] = rel(post[0]["t"]) if post else None
    gm = [r for r in wire if r["t"] > kind_on and r["port"] == 2 and r.get("kind") in ("gPTP Announce", "gPTP Sync")]
    first = gm[0]["t"] if gm else None
    S["first_gm"], S["first_gm_kind"] = rel(first), (gm[0]["kind"] if gm else None)
    healthy = [r for r in sts if r["t"] > kind_on and r["SYNC"] == "1" and r["ASCAPABLE"] == "1" and r["TU"] == "0"
               and r["GPTP_GM"] == SWITCH]
    S["gptp_recovered_at"] = rel(healthy[0]["end"]) if healthy else None
    S["gptp_recovery_s"] = round(healthy[0]["end"] - first, 3) if healthy and first else None
    # the start of the final continuously healthy run
    tail = None
    for r in reversed([r for r in sts if r["t"] > kind_on]):
        if r["SYNC"] == "1" and r["ASCAPABLE"] == "1" and r["TU"] == "0" and r["GPTP_GM"] == SWITCH:
            tail = r
        else:
            break
    S["gptp_steady_from"] = rel(tail["end"]) if tail else None
    for role, port in [("dut", 3), ("peer", 2)]:
        a = [r for r in wire if r["t"] > kind_on and r.get("kind") == "CRF" and r["port"] == port and r["avtp"]["valid"]]
        w = S["wire"][role]
        w["first_valid_after_on"] = rel(a[0]["t"]) if a else None
        w["post_pdus"], w["post_tu1"] = len(a), sum(r["avtp"]["tu"] for r in a)
        w["first_valid_after_wire_return_s"] = round(a[0]["t"] - post[0]["t"], 3) if a and post else None
        w["post_max_gap_s"] = round(max([b["t"] - x["t"] for x, b in zip(a, a[1:])] or [0]), 4)
        w["post_last"] = rel(a[-1]["t"]) if a else None
    S["media_locked_at"] = {}
    for role, what in [("dut", "counter-5-1"), ("peer", "counter-5-8")]:
        a = [r for r in ctrl if r.get("role") == role and r.get("what") == what and r["local_t"] > kind_on
             and r["response"].get("status") == "SUCCESS"
             and r["response"]["counters"]["0"] == r["response"]["counters"]["1"] + 1]
        S["media_locked_at"][role] = rel(a[0]["local_t"]) if a else None
    servo = [t for t, v in W("0x900008f8") if t > kind_on and v & 7 == 4]
    S["servo_locked_at"] = rel(servo[0]) if servo else None
if gm_start:
    S["gm_start"], S["gm_end"] = gm_start, gm_end
    S["gm_hold_s"] = round(gm_end - gm_start, 3) if gm_end else None
    host_ann = [r for r in ann if r["ptp"]["gm_id"] == HOST_GM]
    S["host_gm_first_announce"] = rel(host_ann[0]["t"]) if host_ann else None
    S["host_gm_last_announce"] = rel(host_ann[-1]["t"]) if host_ann else None
    back = [r for r in ann if r["ptp"]["gm_id"] == SWITCH and host_ann and r["t"] > host_ann[-1]["t"]]
    S["switch_gm_first_announce_after"] = rel(back[0]["t"]) if back else None
    # Time on the wire: the far end's Sync/Follow_Up precise origin timestamps against the tap clock.
    fu = [r for r in wire if r.get("kind") == "gPTP Follow_Up" and r["port"] == 2]
    sy = {r["ptp"]["seq"]: r for r in wire if r.get("kind") == "gPTP Sync" and r["port"] == 2}
    gm_minus_tap = []
    for r in fu:
        s = sy.get(r["ptp"]["seq"])
        if s and abs(s["t"] - r["t"]) < 0.1:
            gm_minus_tap.append((s["t"], (r["ptp"]["body_ts"] + r["ptp"]["corr_ns"]) / 1e9 - s["t"]))
    jumps = []
    for (ta, a), (tb, b) in zip(gm_minus_tap, gm_minus_tap[1:]):
        if abs((b - a)) > 50e-6:
            jumps.append(dict(between=[rel(ta), rel(tb)], delta_s=round(b - a, 6)))
    S["far_time_jumps"] = jumps
    # DUT PHC on the wire: its Pdelay_Resp requestReceiptTimestamp (t2) against the tap time of the request.
    req = {r["ptp"]["seq"]: r for r in wire if r.get("kind") == "gPTP Pdelay_Req" and r["port"] == 2}
    dut_minus_tap = []
    for r in wire:
        if r.get("kind") == "gPTP Pdelay_Resp" and r["port"] == 3:
            q = req.get(r["ptp"]["seq"])
            if q and 0 < r["t"] - q["t"] < 0.1:
                dut_minus_tap.append((q["t"], r["ptp"]["body_ts"] / 1e9 - q["t"]))
    djumps = []
    for (ta, a), (tb, b) in zip(dut_minus_tap, dut_minus_tap[1:]):
        if abs(b - a) > 50e-6:
            djumps.append(dict(between=[rel(ta), rel(tb)], delta_s=round(b - a, 6)))
    S["dut_phc_wire_jumps"] = djumps
    S["dut_pdelay_pairs"] = len(dut_minus_tap)
    S["far_sync_pairs"] = len(gm_minus_tap)
    # Per-step reaction windows: from each PHC discontinuity.
    per = []
    for st in steps:
        t_step = st["bracket"][1] + T0
        after = [r for r in sts if r["t"] >= st["bracket"][0] + T0]
        tu1 = [r for r in after if r["TU"] == "1"]
        tu_clear = next((r for r in after if r["t"] > t_step and r["TU"] == "0"
                         and all(x["TU"] == "0" for x in sts if x["t"] >= r["t"] and x["t"] < r["t"] + 2)), None)
        hold = [r for r in after if (int(r["CLKV_STAT"], 16) >> 3) & 1 and r["t"] < t_step + 5]
        crf = {}
        for role, port in [("dut", 3), ("peer", 2)]:
            a = [r for r in wire if r.get("kind") == "CRF" and r["port"] == port and t_step - 5 < r["t"] < t_step + 20]
            crf[role] = dict(pdus=len(a), tu1=sum(r["avtp"]["tu"] for r in a),
                             tu1_span=[rel(min((r["t"] for r in a if r["avtp"]["tu"]), default=None) or None),
                                       rel(max((r["t"] for r in a if r["avtp"]["tu"]), default=None) or None)],
                             mr=changes([(r["t"], r["avtp"]["mr"]) for r in a]),
                             max_gap_s=round(max([b["t"] - x["t"] for x, b in zip(a, a[1:])] or [0]), 4))
        per.append(dict(step=st, tu_first_set=rel(tu1[0]["t"]) if tu1 else None,
                        tu_steady_clear=rel(tu_clear["end"]) if tu_clear else None,
                        holdover_samples=len(hold), crf=crf))
    S["per_step"] = per

packet.mkdir(parents=True, exist_ok=True)
(packet / "analysis.json").write_text(json.dumps(S, indent=1) + "\n")
manifest = [dict(path=str(f), size=f.stat().st_size, sha256=hashlib.sha256(f.read_bytes()).hexdigest())
            for f in sorted(root.iterdir()) if f.is_file()]
(packet / "raw-artifacts.json").write_text(json.dumps(manifest, indent=1) + "\n")
print(json.dumps(S, indent=1)[:200000])
