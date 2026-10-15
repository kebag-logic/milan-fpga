#!/usr/bin/env python3
"""R635-1: recompute the B17 tap-derived figures from summary/cNN.json (the grading output; raw captures are not
published) and check the poll-derived printed figures against exact rounding of the raw poll times.
usage: python3 -I recompute_tap.py <author_dir>"""
import json, sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
A = sys.argv[1]
def jl(p): return [json.loads(x) for x in open(p) if x.startswith("{")]
def r2(x): return Decimal(repr(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
def bursts(late, th=20.0, gap=1e-3):
    out = []
    for x in late:
        if x["late_us"] <= th: continue
        if out and x["s"] - out[-1]["last"] < gap:
            out[-1]["last"] = x["s"]; out[-1]["peak"] = max(out[-1]["peak"], x["late_us"]); out[-1]["n"] += 1
        else: out.append(dict(s=x["s"], last=x["s"], peak=x["late_us"], n=1))
    return out
agg = {k: [] for k in ("delta", "ri", "rates", "first_ms", "p50ph", "p999", "nb", "bsize", "inmax", "aftermax", "nafter", "later_than_slipburst", "u2b_diff_ms", "seqgaps", "frames")}
for c in range(1, 11):
    tag = f"c{c:02d}"
    s = json.load(open(f"{A}/summary/{tag}.json"))
    ev = jl(f"{A}/cycles/{tag}/events.jsonl"); po = jl(f"{A}/cycles/{tag}/poll.jsonl")
    tb = [e for e in ev if e["kind"] == "bind-time"][0]["t_bind_local"]
    t = s["tap"]; pr = t["priming"]; late = t["late_pdus"]
    sl = s["poll"]["slips"]; assert len(sl) == 1
    lo, hi = sl[0]["s_lo"], sl[0]["s_hi"]
    b = bursts(late)
    inside = [z for z in b if lo <= z["s"] <= hi]
    # any burst overlapping the interval (first PDU before lo but later PDUs inside)
    overlap = [z for z in b if z["s"] <= hi and z["last"] >= lo]
    before10 = [z for z in late if z["s"] < lo]
    after = [z for z in b if z["s"] > hi]
    slip_burst = (inside or overlap)[0] if (inside or overlap) else None
    rates = {k: v["rate_ppm"] for k, v in t["streams"].items()}
    delta = t["delta_ppm"]
    ri = 1 / (48000 * abs(delta) * 1e-6)
    # exact recomputation of delta from unrounded? rates are rounded to 4 dp; recompute difference
    print(tag, "delta", delta, "rates", rates, "recomp", round(rates["peer-aaf"] - rates["dut-aaf"], 4), "ri %.1f" % ri,
          "cls_ri", s["classification"]["rate_interval_s"], "window", s["classification"]["bound_window_s"])
    print("   first_pdu_ms", pr["first_pdu_after_command_ms"], "ph p50", pr["phase_us_mod_pdu"]["p50"], "p999", pr["lateness_us"]["p999"],
          "max", pr["lateness_us"]["max"], "nburst", len(b), "sizes", sorted({z["n"] for z in b}))
    print("   slip [%.3f,%.3f]" % (lo, hi), "first burst", (round(b[0]["s"], 3), b[0]["peak"], b[0]["n"]) if b else None,
          "first in", bool(b) and b[0] in inside, "overlap-only", [ (round(z['s'],3),round(z['last'],3)) for z in overlap if z not in inside],
          ">10us before lo", [(z["s"], z["late_us"]) for z in before10][:5], "inmax", sl[0]["tap_lateness_max_us"],
          "pdus_in", sl[0]["tap_pdus_in_interval"])
    later = [z for z in after if slip_burst and z["peak"] > slip_burst["peak"]]
    print("   after bursts", len(after), "peak after", max((z["peak"] for z in after), default=None), "later-than-slip-burst", len(later),
          "u2b tap-host ms", round((t["unbind_to_bind_tap_s"] - t["unbind_to_bind_host_s"]) * 1e3, 3),
          "seq_gaps", {k: v["seq_gaps"] for k, v in t["streams"].items()}, "segments", {k: v["segments"] for k, v in t["streams"].items()})
    agg["delta"].append(delta); agg["ri"].append(ri); agg["rates"] += list(rates.values()); agg["first_ms"].append(pr["first_pdu_after_command_ms"])
    agg["p50ph"].append(pr["phase_us_mod_pdu"]["p50"]); agg["p999"].append(pr["lateness_us"]["p999"]); agg["nb"].append(len(b))
    agg["bsize"] += [z["n"] for z in b]; agg["inmax"].append(sl[0]["tap_lateness_max_us"]); agg["aftermax"].append(max((z["peak"] for z in after), default=None))
    agg["nafter"].append(len(after)); agg["later_than_slipburst"].append(len(later) > 0); agg["u2b_diff_ms"].append(abs(t["unbind_to_bind_tap_s"] - t["unbind_to_bind_host_s"]) * 1e3)
    # exact rounding of printed poll figures
    first = po[0]["t0"] - tb; last = sorted(po, key=lambda r: r["n"])[-1]["t1"] - tb
    print("   printed-check first %s last %s lo %s hi %s (raw %.4f %.4f %.4f %.4f)" % (r2(first), r2(last), r2(lo), r2(hi), first, last, lo, hi))
print("AGG")
for k, v in agg.items():
    v2 = [x for x in v if x is not None and not isinstance(x, bool)]
    if not v2: continue
    if k == "later_than_slipburst": print(k, sum(v), "of", len(v)); continue
    print(k, min(v2), max(v2))
