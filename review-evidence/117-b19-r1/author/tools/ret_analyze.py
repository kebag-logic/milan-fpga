"""Lane B19 retention, cadence and turnaround (#117 box 1) and steady-state publication (box 3)
from one observe action; no bench access.

usage: ret_analyze.py <name>   reads /tmp/a624/raw/<name>, writes bench/<name>/retention.json
Cadence: every interval of each gPTP message stream on the DUT link, graded within 30 % of its
nominal interval (Sync 125 ms, Announce and Pdelay_Req 1 s), as the earlier #117 record did.
Turnaround: per Pdelay exchange, the tap time from the request to its response (both directions),
against the Milan 15 ms limit, and the responder's claimed t3 - t2 (the Follow_Up's
responseOriginTimestamp minus the response's requestReceiptTimestamp, corrections included).
"""
from pathlib import Path
import json, re, statistics as st, struct, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wire_summary import records, decode

SWITCH = "3cc0c6fffefe0210"
name = sys.argv[1]
root = Path("/tmp/a624/raw") / name
out = Path(__file__).resolve().parent.parent / "bench" / name
load = lambda n: [json.loads(l) for l in (root / n).read_text().splitlines() if l.strip()]
console, ctrl = load("console.jsonl"), load("controller.jsonl")
S = dict(name=name)
sts = []
for r in console:
    if r["cmd"] == "milan_status":
        d = dict(re.findall(r"(\w+)=([a-zA-Z0-9_]+)", r["raw"]))
        if "SYNC" in d:
            sts.append(d)
words = {}
for r in console:
    m = re.search(r"^(0x[0-9a-f]+)  ((?:[0-9a-f]{2} ){3}[0-9a-f]{2})", r["raw"], re.M)
    if m:
        words.setdefault(m[1], set()).add(int.from_bytes(bytes.fromhex(m[2]), "little"))
S["console"] = dict(samples=len(sts),
                    healthy=sum(d["SYNC"] == "1" and d["ASCAPABLE"] == "1" and d["TU"] == "0" and d["GPTP_GM"] == SWITCH for d in sts),
                    clkv_stat=sorted({d["CLKV_STAT"] for d in sts}), gm=sorted({d["GPTP_GM"] for d in sts}),
                    parent=sorted({d["GPTP_PARENT"] for d in sts}), path=sorted({(d["AS_PATH_COUNT"], d["AS_PATH_GEN"]) for d in sts}),
                    pdelay_ns=[min(int(d["PDELAY_NS"]) for d in sts), st.median(int(d["PDELAY_NS"]) for d in sts), max(int(d["PDELAY_NS"]) for d in sts)],
                    gptp_lat=sorted({d["GPTP_LAT"] for d in sts}),
                    words={k: sorted(hex(x) for x in v)[:6] for k, v in words.items() if k not in ("0x90000764",)},
                    crft_count_range=[min(words.get("0x90000764", {0})), max(words.get("0x90000764", {0}))])
avb = [r["response"] for r in ctrl if r.get("role") == "dut" and r.get("what") == "avb" and r["response"].get("status") == "SUCCESS"]
pavb = [r["response"] for r in ctrl if r.get("role") == "peer" and r.get("what") == "avb" and r["response"].get("status") == "SUCCESS"]
S["controller"] = dict(dut_polls=len(avb), dut_as_capable=sum(r["decoded"]["as_capable"] for r in avb),
                       dut_gm=sorted({r["decoded"]["gm"] for r in avb}), dut_flags=sorted({r["decoded"]["flags"] for r in avb}),
                       dut_pdelay_ns=[min(r["decoded"]["pdelay_ns"] for r in avb), max(r["decoded"]["pdelay_ns"] for r in avb)] if avb else None,
                       peer_polls=len(pavb), peer_as_capable=sum(r["decoded"]["as_capable"] for r in pavb),
                       peer_gm=sorted({r["decoded"]["gm"] for r in pavb}))
recs = sorted((decode(r) for r in records(str(root / "tap.pcap"))), key=lambda d: d["tap_ns"])
S["tap_records"] = len(recs)
S["tap_span_s"] = round((recs[-1]["tap_ns"] - recs[0]["tap_ns"]) / 1e9, 3)
k = lambda d: d.get("kind")
cad = {}
for label, port, kind, nominal in [("Sync, switch to DUT", 2, "gPTP Sync", 125.0), ("Follow_Up, switch to DUT", 2, "gPTP Follow_Up", 125.0),
                                   ("Announce, switch to DUT", 2, "gPTP Announce", 1000.0), ("Pdelay_Req, switch to DUT", 2, "gPTP Pdelay_Req", 1000.0),
                                   ("Pdelay_Req, DUT to switch", 3, "gPTP Pdelay_Req", 1000.0), ("Sync, DUT to switch", 3, "gPTP Sync", 125.0),
                                   ("Announce, DUT to switch", 3, "gPTP Announce", 1000.0)]:
    a = [d for d in recs if d["port"] == port and k(d) == kind]
    iv = [(b["tap_ns"] - x["tap_ns"]) / 1e6 for x, b in zip(a, a[1:])]
    cad[label] = dict(count=len(a), intervals=len(iv), log_interval=sorted({d["ptp"]["log_interval"] for d in a}),
                      src=sorted({d["ptp"]["src_port_id"] for d in a}),
                      mean=round(st.fmean(iv), 3) if iv else None, min=round(min(iv), 3) if iv else None,
                      max=round(max(iv), 3) if iv else None,
                      within_30pct=sum(abs(x - nominal) <= .3 * nominal for x in iv))
S["cadence_ms"] = cad


def exch(req_port):
    rsp = 5 - req_port
    q = {d["ptp"]["seq"]: d for d in recs if d["port"] == req_port and k(d) == "gPTP Pdelay_Req"}
    rs = {d["ptp"]["seq"]: d for d in recs if d["port"] == rsp and k(d) == "gPTP Pdelay_Resp"}
    fu = {d["ptp"]["seq"]: d for d in recs if d["port"] == rsp and k(d) == "gPTP Pdelay_Resp_Follow_Up"}
    rows = []
    for s, a in q.items():
        r, f = rs.get(s), fu.get(s)
        if r and f and 0 < r["tap_ns"] - a["tap_ns"] < 1e9:
            claimed = (f["ptp"]["body_ts"] + f["ptp"]["corr_ns"]) - (r["ptp"]["body_ts"] - r["ptp"]["corr_ns"])
            rows.append(dict(tap=r["tap_ns"] - a["tap_ns"], fu_after=f["tap_ns"] - r["tap_ns"], claimed=claimed))
    tap = [x["tap"] for x in rows]
    return dict(requests=len(q), complete=len(rows), tap_turnaround_ns=[min(tap), st.median(tap), max(tap)] if tap else None,
                resp_to_fu_ns=[min(x["fu_after"] for x in rows), max(x["fu_after"] for x in rows)] if rows else None,
                claimed_ns=[round(min(x["claimed"] for x in rows)), round(max(x["claimed"] for x in rows))] if rows else None,
                tap_minus_claimed_ns=[round(min(x["tap"] - x["claimed"] for x in rows)), round(st.median(x["tap"] - x["claimed"] for x in rows)),
                                      round(max(x["tap"] - x["claimed"] for x in rows))] if rows else None,
                over_15ms=sum(t > 15e6 for t in tap))


S["pdelay_switch_requests_dut_responds"] = exch(2)
S["pdelay_dut_requests_switch_responds"] = exch(3)
crf = [d for d in recs if d["port"] == 3 and k(d) == "CRF"]
S["dut_crf"] = dict(pdus=len(crf), tu1=sum(d["avtp"]["tu"] for d in crf), streams=sorted({d["avtp"]["stream_id"] for d in crf}),
                    vlan=sorted({str(d["vlan"]) for d in crf}),
                    max_gap_ms=round(max([(b["tap_ns"] - a["tap_ns"]) / 1e6 for a, b in zip(crf, crf[1:])] or [0]), 3))
ann = [d for d in recs if d["port"] == 2 and k(d) == "gPTP Announce"]
S["announce"] = sorted({json.dumps([d["ptp"]["gm_id"], d["ptp"]["gm_prio1"], d["ptp"]["gm_class"], d["ptp"]["steps_removed"], d["ptp"]["tlvs"]]) for d in ann})
S["dut_ptp_kinds_sent"] = sorted({k(d) for d in recs if d["port"] == 3 and str(k(d)).startswith("gPTP")})
adp = [d for d in recs if d["port"] == 3 and k(d) == "ADP"]
S["dut_adp_gm"] = sorted({d["adp"]["gm_id"] for d in adp})
out.mkdir(parents=True, exist_ok=True)
(out / "retention.json").write_text(json.dumps(S, indent=1) + "\n")
print(json.dumps(S, indent=1))
