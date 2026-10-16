"""Lane B19 first reach (#117 box 1): analyze the one OUT0 cold cycle; no bench access.

Inputs: /tmp/a624/raw/firstreach/{events,console-boot,controller}.jsonl and tap.pcap.
All times are seconds after the OUT0 "on" command on the build-box clock. The tap is
placed on that clock as lane B1's analyzer does (median host-minus-tap anchor, then
the measured capture-host offset); the controller host's records by its measured offset.
"Link-up" is bracketed by the wire: the first frame on the DUT link in either direction
after the on command. The DUT end's asCapable comes from the controller's GET_AVB_INFO
polls (one round a second) and the wire; the switch end's from its first Sync and
Announce to the DUT, which an 802.1AS port sends only while asCapable.

usage: fr_analyze.py [<raw_dir>]   writes analysis.json beside this packet's firstreach/
"""
from pathlib import Path
import json, re, statistics, struct, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

SWITCH = "3cc0c6fffefe0210"
DUT_CLOCK = "020000fffe000001"
root = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/a624/raw/firstreach")
out = Path(__file__).resolve().parent.parent / "firstreach"
load = lambda n: [json.loads(l) for l in (root / n).read_text().splitlines() if l.strip()]
events, ctrl, boot = load("events.jsonl"), load("controller.jsonl"), load("console-boot.jsonl")


def offset(role):
    a = [r for r in events if r["kind"] == "clock" and r["role"] == role]
    r = min(a, key=lambda x: x["t1"] - x["t0"])
    return r["remote"] - (r["t0"] + r["t1"]) / 2, (r["t1"] - r["t0"]) / 2


co, ce = offset("controller")
to, te = offset("tap")
off = next(e["t"] for e in events if e["kind"] == "power-command" and e["value"] == "off")
on = next(e["t"] for e in events if e["kind"] == "power-command" and e["value"] == "on")
rel = lambda t: None if t is None else round(t - on, 3)
S = dict(T0="OUT0 on command (build-box clock)", off_s=rel(off), on_result_s=rel(next(e["t"] for e in events if e["kind"] == "power-result" and e["value"] == "on")),
         clock_offset_s=dict(controller=co, tap=to), clock_half_rtt_s=dict(controller=ce, tap=te))

# Console across the boot: the first byte, the identity lines and the prompt.
txt, marks = "", {}
for b in boot:
    txt += b["data"]
    for key, pat in [("first_byte", ""), ("bios_crc", "BIOS CRC passed"), ("csr_id", "CSR ID="), ("aem", "AEM 7512 B"),
                     ("nvm", "Milan NVM:"), ("fabric", "fabric entity enabled"), ("prompt", "Console")]:
        if key not in marks and pat in txt:
            marks[key] = rel(b["t"])
S["boot"] = marks
S["boot_lines"] = [l.strip() for l in txt.replace("\r", "").split("\n") if l.startswith(("Milan", " BIOS CRC", " LiteX git"))]

# Controller (AECP) view of the DUT and the peer.
for r in ctrl:
    r["lt"] = r["t"] - co
avb = [(r["lt"], r["response"]) for r in ctrl if r.get("role") == "dut" and r.get("what") == "avb"]
S["dut_avb_info"] = []
prev = object()
for t, r in avb:
    v = (r["status"], r.get("decoded", {}).get("as_capable"), r.get("decoded", {}).get("gm"))
    if v != prev and t > off - 1:
        S["dut_avb_info"].append([rel(t), *v])
        prev = v
after = [(t, r) for t, r in avb if t > on]
first_ok = next(((t, r) for t, r in after if r["status"] == "SUCCESS"), None)
first_asc = next(((t, r) for t, r in after if r["status"] == "SUCCESS" and r["decoded"]["as_capable"] == 1), None)
last_not = max((t for t, r in after if first_asc and t < first_asc[0]), default=None)
S["dut_first_aecp_answer"] = rel(first_ok[0]) if first_ok else None
S["dut_asCapable_aecp"] = dict(first_set_poll=rel(first_asc[0]) if first_asc else None, last_poll_before=rel(last_not),
                               pdelay_ns=first_asc[1]["decoded"]["pdelay_ns"] if first_asc else None,
                               gm=first_asc[1]["decoded"]["gm"] if first_asc else None)
gm_sw = next(((t, r) for t, r in after if r["status"] == "SUCCESS" and r["decoded"]["gm"] == SWITCH), None)
S["dut_gm_switch_aecp"] = rel(gm_sw[0]) if gm_sw else None
cnt = {}
for role, what in [("dut", "counter-9-0"), ("dut", "counter-5-0"), ("dut", "counter-6-0"), ("dut", "counter-6-1"), ("dut", "counter-36-0"),
                   ("peer", "counter-9-0"), ("peer", "counter-5-0"), ("peer", "counter-5-8"), ("peer", "counter-6-0"), ("peer", "counter-36-0")]:
    a = [(r["lt"], r["response"]["counters"]) for r in ctrl if r.get("role") == role and r.get("what") == what
         and r["response"].get("status") == "SUCCESS"]
    if a:
        ch, pv = [], None
        for t, c in a:
            k = {x: c[x] for x in c if int(x) < 11 and int(x) != 6}
            if k != pv:
                ch.append([rel(t), k]); pv = k
        cnt[role + ":" + what] = dict(first=a[0][1], last=a[-1][1], changes=ch)
S["counters"] = cnt
st = [(r["lt"], r["role"], r["what"], r["response"].get("status"), r["response"].get("conn_count"))
      for r in ctrl if str(r.get("what", "")).startswith("state-")]
S["acmp_states"] = {f"{role}:{what}": sorted({(s, c) for _, rr, w, s, c in st if rr == role and w == what}, key=str)
                    for role, what in sorted({(x[1], x[2]) for x in st})}

# Wire.
raw = list(records(str(root / "tap.pcap")))
anchor = statistics.median((r["host_ns"] - r["tap_ns"]) / 1e9 for r in raw)
wire = []
for r in raw:
    try:
        d = decode(r)
    except (IndexError, struct.error):
        continue
    d["t"] = r["tap_ns"] / 1e9 + anchor - to
    wire.append(d)
wire.sort(key=lambda d: d["t"])
outage = [d for d in wire if off < d["t"] < on]
S["last_frame_after_off_command"] = {("switch" if p == 2 else "dut"): rel(max((d["t"] for d in outage if d["port"] == p), default=None)) for p in (2, 3)}
last = max((d["t"] for d in outage), default=off)
S["frames_between_last_and_on"] = sum(1 for d in outage if d["t"] > last)
post = [d for d in wire if d["t"] > on]
first = lambda f: next((d for d in post if f(d)), None)
fr = dict(any=first(lambda d: True), switch=first(lambda d: d["port"] == 2), dut=first(lambda d: d["port"] == 3))
S["link_up_bracket"] = {k: (rel(v["t"]), v["port"], v["kind"]) if v else None for k, v in fr.items()}
k = lambda d: d.get("kind")
S["first_after_on"] = {}
for name, port, kind in [("switch Pdelay_Req", 2, "gPTP Pdelay_Req"), ("DUT Pdelay_Resp", 3, "gPTP Pdelay_Resp"),
                         ("DUT Pdelay_Req", 3, "gPTP Pdelay_Req"), ("switch Pdelay_Resp", 2, "gPTP Pdelay_Resp"),
                         ("switch Sync", 2, "gPTP Sync"), ("switch Follow_Up", 2, "gPTP Follow_Up"),
                         ("switch Announce", 2, "gPTP Announce"), ("DUT Sync", 3, "gPTP Sync"), ("DUT Announce", 3, "gPTP Announce"),
                         ("DUT ADP", 3, "ADP"), ("DUT MSRP", 3, "MSRP"), ("DUT CRF", 3, "CRF"), ("DUT MVRP", 3, "MVRP"),
                         ("switch MSRP", 2, "MSRP"), ("peer ACMP", 2, "ACMP"), ("DUT ACMP", 3, "ACMP")]:
    d = first(lambda d: d["port"] == port and k(d) == kind)
    S["first_after_on"][name] = rel(d["t"]) if d else None


def exchanges(req_port):
    """Pdelay exchanges started by the req_port side after the on command: (t_req, t_resp, t_fu, turnaround_ns)."""
    rsp_port = 5 - req_port
    reqs = [d for d in post if d["port"] == req_port and k(d) == "gPTP Pdelay_Req"]
    out = []
    for q in reqs:
        rs = next((d for d in post if d["port"] == rsp_port and k(d) == "gPTP Pdelay_Resp" and d["ptp"]["seq"] == q["ptp"]["seq"]
                   and 0 < d["t"] - q["t"] < .5), None)
        fu = next((d for d in post if d["port"] == rsp_port and k(d) == "gPTP Pdelay_Resp_Follow_Up" and d["ptp"]["seq"] == q["ptp"]["seq"]
                   and rs and 0 <= d["t"] - rs["t"] < .5), None)
        out.append(dict(req=rel(q["t"]), seq=q["ptp"]["seq"], resp=rel(rs["t"]) if rs else None, fu=rel(fu["t"]) if fu else None,
                        turnaround_ns=round((rs["tap_ns"] - q["tap_ns"])) if rs else None))
    return out


S["pdelay_switch_requests"] = exchanges(2)[:8]
S["pdelay_dut_requests"] = exchanges(3)[:8]
ann = [d for d in post if d["port"] == 2 and k(d) == "gPTP Announce"]
S["switch_announces"] = [(rel(d["t"]), d["ptp"]["gm_id"], d["ptp"]["gm_prio1"]) for d in ann[:4]]
dann = [d for d in post if d["port"] == 3 and k(d) == "gPTP Announce"]
S["dut_announces"] = [(rel(d["t"]), d["ptp"]["gm_id"], d["ptp"]["gm_prio1"]) for d in dann[:6]]
dsy = [d for d in post if d["port"] == 3 and k(d) == "gPTP Sync"]
S["dut_syncs"] = dict(count=len(dsy), first=rel(dsy[0]["t"]) if dsy else None, last=rel(dsy[-1]["t"]) if dsy else None)
crf = [d for d in post if d["port"] == 3 and k(d) == "CRF"]
S["dut_crf"] = dict(count=len(crf), first=rel(crf[0]["t"]) if crf else None,
                    first_tu0=rel(next((d["t"] for d in crf if d["avtp"]["tu"] == 0), None)),
                    tu1=sum(d["avtp"]["tu"] for d in crf), last_tu1=rel(max((d["t"] for d in crf if d["avtp"]["tu"]), default=None)))
adp = [d for d in post if d["port"] == 3 and k(d) == "ADP"]
S["dut_adp"] = [(rel(d["t"]), d["adp"]["gm_id"], d["adp"]["avail_index"]) for d in adp[:6]]
# DUT PHC minus grandmaster time, from the DUT's Pdelay_Resp t2 (its PHC at the switch's request) and the
# switch's Sync/Follow_Up precise origin plus correction, both against the tap clock (lane B1's method).
fu = [d for d in post if d["port"] == 2 and k(d) == "gPTP Follow_Up"]
sy = {d["ptp"]["seq"]: d for d in post if d["port"] == 2 and k(d) == "gPTP Sync"}
gm_tap = [(sy[d["ptp"]["seq"]]["tap_ns"], (d["ptp"]["body_ts"] + d["ptp"]["corr_ns"]) - sy[d["ptp"]["seq"]]["tap_ns"])
          for d in fu if d["ptp"]["seq"] in sy and 0 <= d["tap_ns"] - sy[d["ptp"]["seq"]]["tap_ns"] < 1e8]
reqs = {d["ptp"]["seq"]: d for d in post if d["port"] == 2 and k(d) == "gPTP Pdelay_Req"}
dut_tap = [(reqs[d["ptp"]["seq"]]["tap_ns"], d["ptp"]["body_ts"] - reqs[d["ptp"]["seq"]]["tap_ns"], d["t"])
           for d in post if d["port"] == 3 and k(d) == "gPTP Pdelay_Resp" and d["ptp"]["seq"] in reqs]
S["dut_minus_gm"] = []
for tq, x, t in dut_tap[:12]:
    g = min(gm_tap, key=lambda r: abs(r[0] - tq)) if gm_tap else None
    S["dut_minus_gm"].append([rel(t), None if g is None else round((x - g[1]) / 1e3, 3)])
S["dut_minus_gm_unit"] = "us; the switch's Sync nearest in tap time, so a few tens of ns of path delay and tap transit remain"
S["tap_records"] = len(wire)
out.mkdir(exist_ok=True)
(out / "analysis.json").write_text(json.dumps(S, indent=1) + "\n")
print(json.dumps(S, indent=1))
