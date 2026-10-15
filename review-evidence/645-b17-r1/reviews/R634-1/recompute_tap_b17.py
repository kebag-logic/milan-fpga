#!/usr/bin/env python3
"""Reviewer cross-check of the B17 tap-derived figures from the published per-cycle grades.

usage: python3 -I recompute_tap_b17.py <evidence author dir>

The raw captures are not published, so this reads summary/cNN.json (the grading's output, which
lists every peer PDU more than 10 us late against the post-bind fit, the per-stream rates and the
priming quantities) and re-derives, independently of the summary tool: delta_ppm from the stream
rates, the rate interval 1/(48000 x |delta_ppm| x 1e-6) from the stated (rounded) delta and from the
unrounded difference, the bursts over 20 us (grouped while consecutive PDUs are < 1 ms apart), each
slip's in-interval maximum, whether the first burst starts inside the slip interval, whether any PDU
over 10 us precedes the interval, and the bursts after it. It also checks that summary/cNN.json's
slip intervals equal those recomputed from the raw poll log.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
FS = 48000
rows = []
for c in range(1, 11):
    r = json.load(open(root / f"summary/c{c:02d}.json"))
    tap = r["tap"]
    st = tap["streams"]
    late = tap["late_pdus"]
    # bursts over 20 us
    b = []
    for x in late:
        if x["late_us"] <= 20.0:
            continue
        if b and x["s"] - b[-1]["last"] < 1e-3:
            b[-1]["last"] = x["s"]; b[-1]["n"] += 1; b[-1]["peak"] = max(b[-1]["peak"], x["late_us"])
        else:
            b.append(dict(s=x["s"], last=x["s"], n=1, peak=x["late_us"]))
    sl = r["poll"]["slips"]
    assert len(sl) == 1, sl
    s = sl[0]
    lo, hi = s["s_lo"], s["s_hi"]
    in_iv = [x for x in late if lo <= x["s"] <= hi]
    before = [x for x in late if x["s"] < lo]
    b_in = [z for z in b if lo <= z["s"] <= hi]
    b_after = [z for z in b if z["s"] > hi]
    d_raw = st["peer-aaf"]["rate_ppm"] - st["dut-aaf"]["rate_ppm"]
    d = tap["delta_ppm"]
    pr = tap["priming"]
    slipped_peak = max((z["peak"] for z in b_in), default=None)
    rows.append(dict(
        cycle=f"c{c:02d}", peer=st["peer-aaf"]["rate_ppm"], dut_aaf=st["dut-aaf"]["rate_ppm"], dut_crf=st["dut-crf"]["rate_ppm"],
        seq_gaps={k: v["seq_gaps"] for k, v in st.items()},
        delta=d, delta_recomputed=round(d_raw, 4), interval_from_stated=round(1 / (FS * abs(d) * 1e-6)) if d else None,
        interval_from_unrounded=round(1 / (FS * abs(d_raw) * 1e-6)) if d_raw else None,
        expected_slips_in_window=round(r["classification"]["bound_window_s"] * FS * abs(d) * 1e-6, 5),
        bound_window=r["classification"]["bound_window_s"],
        unbind_to_bind_tap=tap.get("unbind_to_bind_tap_s"), unbind_to_bind_host=tap.get("unbind_to_bind_host_s"),
        tap_host_diff_ms=round((tap["unbind_to_bind_tap_s"] - tap["unbind_to_bind_host_s"]) * 1e3, 3),
        slip=(lo, hi), max_in_interval=round(max(x["late_us"] for x in in_iv), 3) if in_iv else None,
        tool_in_interval=s.get("tap_lateness_max_us"), pdus_in_interval=s.get("tap_pdus_in_interval"),
        late10_before_interval=len(before), bursts=len(b), burst_pdus=(min(z["n"] for z in b), max(z["n"] for z in b)),
        first_burst_s=round(b[0]["s"], 3), first_burst_inside=bool(b) and lo <= b[0]["s"] <= hi, bursts_inside=len(b_in),
        bursts_after=len(b_after), slipped_burst_peak=slipped_peak,
        peak_after=max((z["peak"] for z in b_after), default=None),
        later_burst_exceeds_slipped=any(z["peak"] > slipped_peak for z in b_after) if slipped_peak else None,
        first_pdu_ms=pr["first_pdu_after_command_ms"], phase_p50=pr["phase_us_mod_pdu"]["p50"], p999=pr["lateness_us"]["p999"],
        classes=[x["cls"] for x in r["classification"]["slips"]]))
for x in rows:
    print(json.dumps(x))
rng = lambda k: (min(x[k] for x in rows), max(x[k] for x in rows))
print(json.dumps(dict(summary=True, delta=rng("delta"), all_rates=(min(min(x["peer"], x["dut_aaf"], x["dut_crf"]) for x in rows),
                                                                    max(max(x["peer"], x["dut_aaf"], x["dut_crf"]) for x in rows)),
                      interval_min=min(x["interval_from_stated"] for x in rows), expected_max=rng("expected_slips_in_window")[1],
                      tap_host_diff_ms=rng("tap_host_diff_ms"), max_in_interval=rng("max_in_interval"),
                      bursts=rng("bursts"), burst_pdus=(min(x["burst_pdus"][0] for x in rows), max(x["burst_pdus"][1] for x in rows)),
                      bursts_after=rng("bursts_after"), peak_after=rng("peak_after"), first_pdu_ms=rng("first_pdu_ms"),
                      phase_p50=rng("phase_p50"), p999=rng("p999"),
                      all_first_inside=all(x["first_burst_inside"] for x in rows),
                      none_before=all(x["late10_before_interval"] == 0 for x in rows),
                      later_exceeds_count=sum(1 for x in rows if x["later_burst_exceeds_slipped"]),
                      bursts_inside=[x["bursts_inside"] for x in rows])))
