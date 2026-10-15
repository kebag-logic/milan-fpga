#!/usr/bin/env python3
"""Reviewer probe: lane B17 burst figures per window under the page's stated rule (offline, read-only).

usage: burst_window_probe.py <author_packet_dir>

Rule as the page states it at 71d5e085: peer PDUs more than 20 us late, grouped while
successive such PDUs are less than 1 ms apart. Recomputed independently from
summary/cNN.json late_pdus and the raw cycles/cNN/{events,poll}.jsonl:
  - bursts per cycle, to the last poll and to the capture's end;
  - PDUs per burst, over each window separately (the page prints one range, 3 to 12);
  - bursts after the slip and their peak lateness, per window;
  - the slipping burst's peak (largest lateness in the slip's interval);
  - whether the first burst is inside the slip's interval, and the largest lateness before it;
  - in how many cycles a later burst to the last poll is larger than the slipping one.
Also sweeps the grouping gap to show which gaps reproduce the printed ranges.
"""
import json
import sys
from pathlib import Path

P = Path(sys.argv[1])


def jl(p):
    return [json.loads(x) for x in open(p) if x.strip()]


def group(lp, gap, thr=20.0):
    b = []
    for x in lp:
        if x["late_us"] <= thr:
            continue
        if b and x["s"] - b[-1]["last"] < gap:
            b[-1]["last"] = x["s"]; b[-1]["peak"] = max(b[-1]["peak"], x["late_us"]); b[-1]["n"] += 1
        else:
            b.append(dict(s=x["s"], last=x["s"], peak=x["late_us"], n=1))
    return b


def load():
    out = []
    for c in range(1, 11):
        cd = P / "cycles" / f"c{c:02d}"
        tb = [e for e in jl(cd / "events.jsonl") if e["kind"] == "bind"][0]["t_cmd_local"]
        pl = sorted(jl(cd / "poll.jsonl"), key=lambda r: r["n"])
        lb = [int(r["words"]["0x8d4"], 16) for r in pl]
        i = next(k for k in range(1, len(pl)) if lb[k] != lb[k - 1])
        lp = json.load(open(P / "summary" / f"c{c:02d}.json"))["tap"]["late_pdus"]
        out.append(dict(cycle=f"c{c:02d}", last=pl[-1]["t1"] - tb, lo=pl[i - 1]["t0"] - tb, hi=pl[i]["t1"] - tb, lp=lp))
    return out


def figures(cyc, gap):
    rows = []
    for k in cyc:
        b = group(k["lp"], gap)
        bl = [z for z in b if z["s"] <= k["last"]]
        ins = [z for z in b if k["lo"] <= z["s"] <= k["hi"]]
        al = [z for z in b if k["hi"] < z["s"] <= k["last"]]
        ac = [z for z in b if z["s"] > k["hi"]]
        before = [x["late_us"] for x in k["lp"] if x["s"] < k["lo"]]
        rows.append(dict(cycle=k["cycle"], per_last=len(bl), per_cap=len(b), further=len(b) - len(bl),
                         pdus_last=[min(z["n"] for z in bl), max(z["n"] for z in bl)],
                         pdus_cap=[min(z["n"] for z in b), max(z["n"] for z in b)],
                         after_last=len(al), after_cap=len(ac),
                         peak_after_last=round(max(z["peak"] for z in al), 1),
                         peak_after_cap=round(max(z["peak"] for z in ac), 1),
                         slip_peak=round(ins[0]["peak"], 1) if ins else None,
                         first_in_interval=bool(b) and bool(ins) and b[0] is ins[0],
                         max_late_before_interval=round(max(before), 1) if before else None,
                         larger_later=any(z["peak"] > ins[0]["peak"] for z in al) if ins else None))
    rng = lambda key: [min(r[key] for r in rows), max(r[key] for r in rows)]
    return dict(rows=rows, ranges=dict(
        per_last=rng("per_last"), per_cap=rng("per_cap"), further=rng("further"),
        pdus_last=[min(r["pdus_last"][0] for r in rows), max(r["pdus_last"][1] for r in rows)],
        pdus_cap=[min(r["pdus_cap"][0] for r in rows), max(r["pdus_cap"][1] for r in rows)],
        after_last=rng("after_last"), after_cap=rng("after_cap"),
        peak_after_last=rng("peak_after_last"), peak_after_cap=rng("peak_after_cap"),
        slip_peak=rng("slip_peak"), first_in_interval=sum(r["first_in_interval"] for r in rows),
        max_late_before_interval=max(r["max_late_before_interval"] or 0 for r in rows),
        larger_later=sum(bool(r["larger_later"]) for r in rows)))


PRINTED = dict(per_last=[9, 19], per_cap=[11, 24], further=[2, 7], pdus_last=[3, 12], pdus_cap=[3, 12],
               after_last=[8, 18], after_cap=[10, 23], peak_after_last=[27.1, 30.1], peak_after_cap=[27.6, 30.3],
               slip_peak=[24.6, 29.3], first_in_interval=10, larger_later=9)

cyc = load()
stated = figures(cyc, 1e-3)
cmp = {k: dict(printed=v, recomputed=stated["ranges"][k], match=stated["ranges"][k] == v) for k, v in PRINTED.items()}
cmp["max_late_before_interval_under_10us"] = dict(recomputed=stated["ranges"]["max_late_before_interval"],
                                                   match=stated["ranges"]["max_late_before_interval"] <= 10.0)
sweep = {}
for g_us in (187.5, 250, 375, 500, 750, 1000, 1500, 2000):
    r = figures(cyc, g_us * 1e-6)["ranges"]
    sweep[str(g_us)] = dict(all_burst_ranges_match=all(r[k] == PRINTED[k] for k in
                                                       ("per_last", "per_cap", "further", "pdus_last", "after_last", "after_cap")),
                            per_last=r["per_last"], per_cap=r["per_cap"], after_cap=r["after_cap"], pdus_last=r["pdus_last"])
print(json.dumps(dict(stated_rule_vs_printed=cmp, all_match=all(v["match"] for v in cmp.values()),
                      per_cycle=stated["rows"], gap_sweep_us=sweep), indent=1))
