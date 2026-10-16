"""Lane B19 box 3: publication words and `tu` against the wire, in the same window; no bench access.

usage: corr_analyze.py <name>   reads /tmp/a624/raw/<name>, writes bench/<name>/correlation.json

Time base. Each console `milan_status` sample prints the DUT PHC (TAI_NS) read together with
CLKV_STAT, the GM and parent words, so the sample's read instant is known in DUT PHC time. On the
wire, each DUT Pdelay_Resp_Follow_Up carries t3, the DUT PHC at the response's egress, and the tap
stamps that response. A sample is placed on the tap clock through the DUT Pdelay response nearest
to it in PHC time (|dPHC| <= 3 s, so a rate error of 100 ppm moves it by at most 0.3 ms), and only
when that placement agrees with the coarse cross-host placement (lane B1's method, +/- 0.2 s),
which rejects a pairing across a PHC step. A sample with no such pairing keeps the coarse time
and is flagged. All times are seconds after the action's T0 (OUT4 off, or the software GM start),
on the tap clock moved to the build-box clock as lane B1's analyzer does.

A transition is reported as the bracket (last sample before, first sample after) on that time base;
a wire event "inside" a bracket lies between the two placed reads.
"""
from pathlib import Path
import json, re, statistics, struct, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

SWITCH, DUTC = "3cc0c6fffefe0210", "020000fffe000001"
name = sys.argv[1]
root = Path("/tmp/a624/raw") / name
out = Path(__file__).resolve().parent.parent / "bench" / name
load = lambda n: [json.loads(l) for l in (root / n).read_text().splitlines() if l.strip()]
events, console, ctrl = load("events.jsonl"), load("console.jsonl"), load("controller.jsonl")


def offset(role):
    a = [r for r in events if r["kind"] == "clock" and r["role"] == role]
    r = min(a, key=lambda x: x["t1"] - x["t0"])
    return r["remote"] - (r["t0"] + r["t1"]) / 2


co, to = offset("controller"), offset("tap")
T0 = next((e["t"] for e in events if e["kind"] == "power-command" and e["value"] == "off"), None) or \
     next(e["t"] for e in events if e["kind"] == "gm-start")
kind_on = next((e["t"] for e in events if e["kind"] == "power-command" and e["value"] == "on"), None)
raw = list(records(str(root / "tap.pcap")))
anchor = statistics.median((r["host_ns"] - r["tap_ns"]) / 1e9 for r in raw)
bb = lambda tap_ns: tap_ns / 1e9 + anchor - to          # tap time -> build-box seconds
wire = []
for r in raw:
    try:
        d = decode(r)
    except (IndexError, struct.error):
        continue
    if d.get("kind") == "CRF":
        f = r["frame"]; o = 18 if f[12:14] == b"\x81\x00" else 14
        d["avtp"]["mr"] = (f[o + 1] >> 3) & 1
    d["t"] = bb(r["tap_ns"])
    wire.append(d)
wire.sort(key=lambda d: d["tap_ns"])
k = lambda d: d.get("kind")
rel = lambda t: None if t is None else round(t - T0, 4)

# DUT PHC <-> tap pairs: t3 of each DUT Pdelay_Resp_Follow_Up against its Pdelay_Resp's tap time.
resp = {(d["ptp"]["seq"]): d for d in wire if d["port"] == 3 and k(d) == "gPTP Pdelay_Resp"}
pairs = []
for d in wire:
    if d["port"] == 3 and k(d) == "gPTP Pdelay_Resp_Follow_Up" and d["ptp"]["seq"] in resp:
        r = resp[d["ptp"]["seq"]]
        if 0 <= d["tap_ns"] - r["tap_ns"] < 1e8:
            pairs.append((d["ptp"]["body_ts"] + d["ptp"]["corr_ns"], r["tap_ns"]))
pairs.sort(key=lambda p: p[0])
phcs = [p[0] for p in pairs]
import bisect
sts = []
for r in console:
    if r["cmd"] != "milan_status":
        continue
    d = dict(re.findall(r"(\w+)=([a-zA-Z0-9_]+)", r["raw"]))
    if "TAI_NS" not in d or "SYNC" not in d:
        continue
    phc = int(d["TAI_NS"], 16)
    coarse = (r["t"] + r["end"]) / 2
    placed, how = coarse, "coarse"
    i = bisect.bisect_left(phcs, phc)
    for j in sorted({max(0, i - 1), min(len(pairs) - 1, i)}, key=lambda j: abs(phcs[j] - phc) if pairs else 0):
        if pairs and abs(phcs[j] - phc) <= 3e9:
            cand = bb(pairs[j][1] + (phc - phcs[j]))
            if abs(cand - coarse) <= .2:
                placed, how = cand, "phc"
                break
    sts.append(dict(t=placed, how=how, coarse=coarse, gm=d["GPTP_GM"], parent=d["GPTP_PARENT"], sync=d["SYNC"], asc=d["ASCAPABLE"],
                    tu=d["TU"], clkv=int(d["CLKV_STAT"], 16), pdelay=int(d["PDELAY_NS"]), gen=d["AS_PATH_GEN"], cnt=d["AS_PATH_COUNT"]))
# Samples with no PHC pairing (the link was dark) are moved by the median coarse-minus-placed offset
# of the paired ones (the error of the coarse cross-host offset, measured in this same action).
cal = statistics.median(s["coarse"] - s["t"] for s in sts if s["how"] == "phc") if any(s["how"] == "phc" for s in sts) else 0.0
for s_ in sts:
    if s_["how"] == "coarse":
        s_["t"], s_["how"] = s_["coarse"] - cal, "calibrated"
S = dict(name=name, T0=T0, samples=len(sts), placed_by_phc=sum(s["how"] == "phc" for s in sts), calibration_s=round(cal, 4),
         coarse_minus_placed_ms=[round(1e3 * min(s["coarse"] - s["t"] - cal + cal for s in sts if s["how"] == "phc"), 1),
                                 round(1e3 * statistics.median(s["coarse"] - s["t"] for s in sts if s["how"] == "phc"), 1),
                                 round(1e3 * max(s["coarse"] - s["t"] for s in sts if s["how"] == "phc"), 1)] if any(s["how"] == "phc" for s in sts) else None)


def edges(field, f=lambda v: v):
    outl, prev = [], None
    for a in sts:
        v = f(a[field])
        if prev is not None and v != prev[1]:
            outl.append(dict(to=v, last_before=rel(prev[0]["t"]), first_after=rel(a["t"]), how=[prev[0]["how"], a["how"]]))
        prev = (a, v)
    return outl


S["edges"] = dict(gm=edges("gm"), parent=edges("parent"), sync=edges("sync"), asCapable=edges("asc"), tu=edges("tu"),
                  holdover=edges("clkv", lambda v: (v >> 3) & 1), path_gen=edges("gen"), path_count=edges("cnt"))
S["pdelay_ns_range"] = [min(s["pdelay"] for s in sts), max(s["pdelay"] for s in sts)]
# Wire causes.
sw = [d for d in wire if d["port"] == 2]
after = lambda t, f: next((d for d in wire if d["t"] > t and f(d)), None)
W = {}
if kind_on:
    outage = [d for d in sw if T0 < d["t"] < kind_on]
    W["switch_last_sync"] = rel(max((d["t"] for d in outage if k(d) == "gPTP Sync"), default=None))
    W["switch_last_announce"] = rel(max((d["t"] for d in outage if k(d) == "gPTP Announce"), default=None))
    W["switch_last_pdelay_resp"] = rel(max((d["t"] for d in outage if k(d) == "gPTP Pdelay_Resp"), default=None))
    ret = [d for d in sw if d["t"] > kind_on]
    W["switch_first_frame"] = rel(ret[0]["t"]) if ret else None
    W["switch_announces_after_return"] = [(rel(d["t"]), d["ptp"]["gm_id"], d["ptp"]["gm_prio1"], d["ptp"]["tlvs"]) for d in ret if k(d) == "gPTP Announce"][:4]
    W["switch_first_sync"] = rel(next((d["t"] for d in ret if k(d) == "gPTP Sync"), None))
    # the DUT's completed Pdelay exchanges after the return (its own requests, the switch's responses)
    dq = [d for d in wire if d["port"] == 3 and d["t"] > kind_on and k(d) == "gPTP Pdelay_Req"]
    done = []
    for q in dq:
        fu = next((d for d in ret if k(d) == "gPTP Pdelay_Resp_Follow_Up" and d["ptp"]["seq"] == q["ptp"]["seq"] and 0 < d["t"] - q["t"] < .5), None)
        if fu:
            done.append(rel(fu["t"]))
    W["dut_completed_pdelay_after_return"] = done[:4]
    dm = [d for d in wire if d["port"] == 3 and d["t"] > kind_on and k(d) in ("gPTP Sync", "gPTP Announce")]
    W["dut_master_frames"] = dict(syncs=sum(k(d) == "gPTP Sync" for d in dm), announces=[(rel(d["t"]), d["ptp"]["gm_id"], d["ptp"]["gm_prio1"]) for d in dm if k(d) == "gPTP Announce"],
                                  first=rel(dm[0]["t"]) if dm else None, last=rel(dm[-1]["t"]) if dm else None)
    adp = [d for d in wire if d["port"] == 3 and k(d) == "ADP" and d["t"] > T0]
    W["dut_adp"] = [(rel(d["t"]), d["adp"]["gm_id"]) for d in adp][:6]
crf = [d for d in wire if d["port"] == 3 and k(d) == "CRF"]
tu = []
for a, b in zip(crf, crf[1:]):
    if a["avtp"]["tu"] != b["avtp"]["tu"]:
        tu.append(dict(to=b["avtp"]["tu"], last_before=rel(a["t"]), first_after=rel(b["t"])))
W["crf_tu_edges"] = tu
W["crf_mr_values"] = sorted({d["avtp"]["mr"] for d in crf})
W["crf_tu1_pdus"] = sum(d["avtp"]["tu"] for d in crf)
gaps = [(rel(a["t"]), round(b["t"] - a["t"], 4)) for a, b in zip(crf, crf[1:]) if b["t"] - a["t"] > .1]
W["crf_gaps_over_100ms"] = gaps
W["crf_first"], W["crf_last"] = (rel(crf[0]["t"]), rel(crf[-1]["t"])) if crf else (None, None)
S["wire"] = W
# Inside-bracket checks for the CRF tu edges against the CLKV tu edges.
chk = []
for e in tu:
    br = min(S["edges"]["tu"], key=lambda x: abs((x["first_after"] or 0) - e["first_after"]), default=None)
    if br:
        chk.append(dict(wire=e, csr=br, wire_inside=br["last_before"] <= e["first_after"] <= br["first_after"]))
S["crf_tu_vs_csr"] = chk
# Controller view.
for r in ctrl:
    r["lt"] = r["t"] - co
avb = [(rel(r["lt"]), r["response"]) for r in ctrl if r.get("role") == "dut" and r.get("what") == "avb"]
cv, prev = [], None
for t, r in avb:
    v = (r.get("status"), r.get("decoded", {}).get("gm"), r.get("decoded", {}).get("as_capable"))
    if v != prev:
        cv.append([t, *v]); prev = v
S["controller_dut_avb"] = cv
gmc = [(rel(r["lt"]), r["response"]["counters"].get("5")) for r in ctrl if r.get("role") == "dut" and r.get("what") == "counter-9-0"
       and r["response"].get("status") == "SUCCESS"]
cg, prev = [], None
for t, v in gmc:
    if v != prev:
        cg.append([t, v]); prev = v
S["controller_dut_gm_changed"] = cg
tucnt = [int.from_bytes(bytes.fromhex(m[1]), "little") for r in console if r["cmd"] == "mem_read 0x90000780 4"
         for m in [re.search(r"0x90000780  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})", r["raw"])] if m]
S["clkv_tucnt"] = [tucnt[0], tucnt[-1]] if tucnt else None
tu1 = [s for s in sts if s["tu"] == "1"]
S["tu1_span_s"] = round(tu1[-1]["t"] - tu1[0]["t"], 3) if tu1 else 0
out.mkdir(parents=True, exist_ok=True)
(out / "correlation.json").write_text(json.dumps(S, indent=1) + "\n")
print(json.dumps(S, indent=1))
