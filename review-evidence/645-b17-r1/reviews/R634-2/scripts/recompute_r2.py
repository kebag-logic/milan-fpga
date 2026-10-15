#!/usr/bin/env python3
"""Reviewer recompute of lane B17's round-2 printed figures (offline, read-only).

usage: recompute_r2.py <author_packet_dir>

Independent of the lane's summary tool. Reads only:
  cycles/cNN/poll.jsonl     raw counter log (t0/t1 host seconds, CSR words)
  cycles/cNN/events.jsonl   bind and unbind command instants
  summary/cNN.json          the grade, used ONLY for tap data (late_pdus, first PDU, frames, interval lateness)
  restore/dut-{start,end}.txt  SLIP_LB baselines (0x900008d4, little endian)
Every poll figure is computed unrounded and rounded once at print time.
Bursts: peer PDUs with late_us > 20, grouped while consecutive late PDUs are < 1 ms apart.
Windows after a slip: bursts whose first PDU is after the slip interval's end and no later than
  last_poll = end of the cycle's last poll, hold = 32 s after the bind, capture = no end.
Prints one JSON line per cycle and a final ranges line.
"""
import json
import re
import sys
from pathlib import Path

P = Path(sys.argv[1])


def jl(p):
    return [json.loads(x) for x in open(p) if x.strip()]


def base(p):
    m = re.search(r"^0x900008d4\s+((?:[0-9a-f]{2} ){4})", Path(p).read_text(), re.M)
    return int.from_bytes(bytes.fromhex(m.group(1).replace(" ", "")), "little") & 0xFFFF


def wd(r, k):
    return int(r["words"][k], 16)


out = []
for c in range(1, 11):
    cd = P / "cycles" / f"c{c:02d}"
    ev = jl(cd / "events.jsonl")
    tb = [e for e in ev if e["kind"] == "bind"][0]["t_cmd_local"]
    tu = [e for e in ev if e["kind"] == "unbind"][0]["t_cmd_local"]
    bt = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
    assert bt == tb
    hold = [e for e in ev if e["kind"] == "start"][0]["hold_s"]
    pl = sorted(jl(cd / "poll.jsonl"), key=lambda r: r["n"])
    g = json.load(open(P / "summary" / f"c{c:02d}.json"))
    tap = g["tap"]
    rel = lambda t: t - tb
    first, last = rel(pl[0]["t0"]), rel(pl[-1]["t1"])
    lb = [wd(r, "0x8d4") for r in pl]
    slips = []
    for i in range(1, len(pl)):
        if lb[i] != lb[i - 1]:
            slips.append(dict(lo=rel(pl[i - 1]["t0"]), hi=rel(pl[i]["t1"]),
                              dd=(lb[i] & 0xFFFF) - (lb[i - 1] & 0xFFFF), ds=(lb[i] >> 16) - (lb[i - 1] >> 16)))
    tdm = {wd(r, "0x8d8") for r in pl}
    rs = [wd(r, "0x8dc") for r in pl]
    post = [i for i, r in enumerate(pl) if rel(r["t1"]) > 0]
    ipf = next(i for i in post if not (rs[i] >> 8) & 1)
    icv = next(i for i in post if (rs[i] >> 9) & 1)
    fpdu = tap["priming"]["first_pdu_after_command_ms"] / 1e3
    durs = [(r["t1"] - r["t0"], r) for r in pl]
    longp = [dict(from_unbind=r["t0"] - tu, from_bind=rel(r["t0"]), took=d) for d, r in durs if d > 0.2]
    others = max(d for d, r in durs if d <= 0.2)
    # bursts
    b = []
    for x in tap["late_pdus"]:
        if x["late_us"] <= 20.0:
            continue
        if b and x["s"] - b[-1]["last"] < 1e-3:
            b[-1]["last"] = x["s"]; b[-1]["peak"] = max(b[-1]["peak"], x["late_us"]); b[-1]["n"] += 1
            b[-1]["gaps"].append(x["s"] - b[-1]["prev"]); b[-1]["prev"] = x["s"]
        else:
            b.append(dict(s=x["s"], last=x["s"], prev=x["s"], peak=x["late_us"], n=1, gaps=[]))
    assert len(slips) == 1
    s = slips[0]
    inside = [z for z in b if s["lo"] <= z["s"] <= s["hi"]]
    before10 = [x for x in tap["late_pdus"] if x["s"] < s["lo"]]
    win = dict(last_poll=last, hold=hold, capture=float("inf"))
    aft = {}
    for k, e in win.items():
        a = [z for z in b if s["hi"] < z["s"] <= e]
        aft[k] = dict(n=len(a), peak=max(z["peak"] for z in a),
                      larger=any(z["peak"] > inside[0]["peak"] for z in a))
    per = {k: len([z for z in b if z["s"] <= e]) for k, e in win.items()}
    burst_pdus = {k: [min(z["n"] for z in b if z["s"] <= e), max(z["n"] for z in b if z["s"] <= e)] for k, e in win.items()}
    maxgap_us = max((gg for z in b for gg in z["gaps"]), default=0) * 1e6
    lp_in = max(x["late_us"] for x in tap["late_pdus"] if s["lo"] <= x["s"] <= s["hi"])
    out.append(dict(
        cycle=f"c{c:02d}", polls=len(pl), first=f"{first:+.2f}", last=f"{last:+.2f}", last_raw=last,
        lb_first=lb[0] & 0xFFFF, lb_last=lb[-1] & 0xFFFF, slip=f"{s['lo']:.2f} to {s['hi']:.2f}", dd=s["dd"], ds=s["ds"],
        width=s["hi"] - s["lo"], polls_left=last - s["hi"], tdm_values=sorted(tdm),
        prefill_by=rel(pl[ipf]["t1"]), prefill_after=max(rel(pl[ipf - 1]["t0"]), fpdu), pf_first_post=ipf == post[0],
        prev_poll_read_prefill1=bool((rs[ipf - 1] >> 8) & 1), first_pdu=fpdu, conv_by=rel(pl[icv]["t1"]), conv_lag=icv - ipf,
        fill=[min(rs[i] & 0xFF for i in range(ipf, len(pl))), max(rs[i] & 0xFF for i in range(ipf, len(pl)))],
        held=all(not (rs[i] >> 8) & 1 for i in range(ipf, len(pl))) and all((rs[i] >> 9) & 1 for i in range(icv, len(pl))),
        rails=sorted({x >> 16 for x in rs}), long_polls=longp, other_max=others,
        long2_in_interval=[s["lo"] <= lp["from_bind"] < s["hi"] for lp in longp],
        bursts_per=per, burst_pdus=burst_pdus, max_gap_in_burst_us=maxgap_us, inside=len(inside),
        first_burst_inside=bool(inside) and b[0] is inside[0], slip_burst_peak=inside[0]["peak"], lat_in_interval=lp_in,
        grade_lat_in=g["poll"]["slips"][0]["tap_lateness_max_us"],
        max_before_interval=max((x["late_us"] for x in before10), default=None), after=aft,
        frames=tap["frames"]))

for r in out:
    print(json.dumps(r))
bl0, bl1 = base(P / "restore/dut-start.txt"), base(P / "restore/dut-end.txt")
cont = [out[0]["lb_first"] == bl0] + [out[i]["lb_first"] == out[i - 1]["lb_last"] for i in range(1, 10)] + [out[-1]["lb_last"] == bl1]
rng = lambda f: (min(f(r) for r in out), max(f(r) for r in out))
print(json.dumps(dict(
    baseline_start=bl0, baseline_end=bl1, continuity_all=all(cont), continuity=cont,
    polls_left=[f"{x:.1f}" for x in rng(lambda r: r["polls_left"])], width=[f"{x:.2f}" for x in rng(lambda r: r["width"])],
    last_poll=[f"{x:+.2f}" for x in rng(lambda r: r["last_raw"])],
    prefill_by=[f"{x:.2f}" for x in rng(lambda r: r["prefill_by"])],
    pf_first_post=[r["cycle"] for r in out if r["pf_first_post"]],
    conv_next=[r["cycle"] for r in out if r["conv_lag"] == 1], conv_lags=sorted({r["conv_lag"] for r in out}),
    conv_by_next=[f"{x:.2f}" for x in rng(lambda r: r["conv_by"] if r["conv_lag"] == 1 else r["prefill_by"]) ],
    conv_by_next_only=[f"{min(r['conv_by'] for r in out if r['conv_lag']==1):.2f}", f"{max(r['conv_by'] for r in out if r['conv_lag']==1):.2f}"],
    fill=[min(r["fill"][0] for r in out), max(r["fill"][1] for r in out)], held=all(r["held"] for r in out),
    first_pdu_ms=[f"{x*1e3:.1f}" for x in rng(lambda r: r["first_pdu"])],
    long_count=sorted({len(r["long_polls"]) for r in out}),
    long_took=[f"{min(lp['took'] for r in out for lp in r['long_polls']):.2f}", f"{max(lp['took'] for r in out for lp in r['long_polls']):.2f}"],
    other_max=f"{max(r['other_max'] for r in out):.2f}",
    long_unbind=[f"{min(r['long_polls'][0]['from_unbind'] for r in out):.2f}", f"{max(r['long_polls'][0]['from_unbind'] for r in out):.2f}"],
    long_bind=[f"{min(r['long_polls'][1]['from_bind'] for r in out):.2f}", f"{max(r['long_polls'][1]['from_bind'] for r in out):.2f}"],
    long2_inside=[r["cycle"] for r in out if r["long2_in_interval"][1]],
    per_cycle={k: rng(lambda r, k=k: r["bursts_per"][k]) for k in ("last_poll", "hold", "capture")},
    after_n={k: rng(lambda r, k=k: r["after"][k]["n"]) for k in ("last_poll", "hold", "capture")},
    after_peak={k: [f"{x:.1f}" for x in rng(lambda r, k=k: r["after"][k]["peak"])] for k in ("last_poll", "hold", "capture")},
    after_larger={k: sum(r["after"][k]["larger"] for r in out) for k in ("last_poll", "hold", "capture")},
    further_to_capture=rng(lambda r: r["after"]["capture"]["n"] - r["after"]["last_poll"]["n"]),
    burst_pdus={k: [min(r["burst_pdus"][k][0] for r in out), max(r["burst_pdus"][k][1] for r in out)] for k in ("last_poll", "capture")},
    max_gap_in_burst_us=round(max(r["max_gap_in_burst_us"] for r in out), 1),
    inside_counts=sorted({r["inside"] for r in out}), first_burst_inside_all=all(r["first_burst_inside"] for r in out),
    lat_in=[f"{x:.1f}" for x in rng(lambda r: r["lat_in_interval"])], lat_in_matches_grade=all(abs(r["lat_in_interval"] - r["grade_lat_in"]) < 1e-9 for r in out),
    none_over10_before=all(r["max_before_interval"] is None for r in out),
    frames=sorted(r["frames"] for r in out))))
