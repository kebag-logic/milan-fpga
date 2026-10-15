#!/usr/bin/env python3
"""Lane B17: the lane's per-cycle table, the bind-priming figures and the summary (offline, read-only).

usage: summ_b17.py <packet_dir>
Reads cycles/cNN/events.jsonl, the raw counter logs cycles/cNN/poll.jsonl, summary/cNN.json (ana_b17.py),
summary/peer-gap.json (peer_gap_b17.py) and restore/dut-{start,end}.txt. Writes summary/cycles.json,
summary/table.md, summary/priming.md, summary/figures.json and summary/counter-logs.sha256.

Round 2 rules:
  * Every poll figure (poll coverage, slip intervals, what is left of the polls after a slip, the RENDER_STAT
    brackets, the long polls) is computed here from the raw counter log and the bind's instant, unrounded, and
    rounded once when printed. The grade's 3-decimal poll figures are only cross-checked (within 0.0005 s).
    A time of day (the bind's UTC instant) is a clock reading and is truncated to the millisecond, not rounded.
  * A printed figure whose only source is a value the grade already rounded (the tap figures) is printed from
    that value only when no rounding tie makes the result depend on the discarded digits; an ambiguous one
    stops the tool. Every such figure is listed in figures.json under "rounding".
  * Late bursts: the peer PDUs later than 20 us against the post-bind fit (ana_b17.py's late_pdus), grouped
    into one burst while successive qualifying PDUs are less than 1 ms apart; a burst's time is its first PDU's, its peak
    its largest lateness. Every after-slip figure is given per window, each named: "last_poll" (bursts that
    start no later than the end of the cycle's last poll), "hold" (no later than the 32 s hold after the bind)
    and "capture" (to the end of the 50 s capture, about 41.9 s after the bind). The counter is read only to
    the last poll; that bursts after it slipped nothing rests on the cumulative counter, checked here: each
    cycle's first SLIP_LB read equals the previous cycle's last, c01's first equals the start baseline and
    c10's last equals the end baseline.
  * RENDER_STAT is read once inside each poll, so its prefill exit is a bracket, not an instant: after the
    later of the start of the last poll that read prefill 1 and the first peer PDU after the bind (tap), and
    no later than the end of the first poll that read prefill 0. Convergence is "by" the end of the first poll
    that read converged 1, which is that poll or a later one.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

P = Path(sys.argv[1])
BURST_US, BURST_GAP_S, LONG_POLL_S, FS = 20.0, 1e-3, 0.2, 48_000
ROUNDING = []


def jl(path):
    return [json.loads(x) for x in open(path) if x.startswith("{")]


def r1(v, dp, sign=False):
    """A raw value rounded once."""
    return f"{v:+.{dp}f}" if sign else f"{v:.{dp}f}"


def once(v, src_dp, dp, what, sign=False):
    """A value the grade rounded to src_dp decimals, printed at dp < src_dp decimals: exact unless it sits on a tie."""
    d = Decimal(repr(v)).quantize(Decimal(1).scaleb(-src_dp))
    q = Decimal(1).scaleb(-dp)
    tie = abs(d) % q == q / 2
    ROUNDING.append(dict(figure=what, grade_value=str(d), grade_decimals=src_dp, printed_decimals=dp, tie=tie))
    if tie:
        sys.exit(f"rounding tie: {what} = {d} cannot be printed at {dp} decimals from the grade")
    out = d.quantize(q, rounding=ROUND_HALF_EVEN)
    return f"{out:+}" if sign and out >= 0 else f"{out}"


def baseline(path):
    m = re.search(r"^0x900008d4\s+((?:[0-9a-f]{2} ){4})", Path(path).read_text(), re.M)
    v = int.from_bytes(bytes.fromhex(m.group(1).replace(" ", "")), "little")
    return dict(dups=v & 0xFFFF, skips=v >> 16)


def bursts(late):
    out = []
    for x in late:
        if x["late_us"] <= BURST_US:
            continue
        if out and x["s"] - out[-1]["last_s"] < BURST_GAP_S:
            out[-1]["last_s"] = x["s"]
            out[-1]["peak_us"] = max(out[-1]["peak_us"], x["late_us"])
            out[-1]["pdus"] += 1
        else:
            out.append(dict(s=x["s"], last_s=x["s"], peak_us=x["late_us"], pdus=1))
    return out


def word(row, off):
    return int(row["words"][off], 16)


gap = json.load(open(P / "summary" / "peer-gap.json"))
rows, logs = [], []
for cdir in sorted((P / "cycles").glob("c[0-9][0-9]")):
    c = cdir.name
    ev = jl(cdir / "events.jsonl")
    k = {e["kind"]: e for e in ev}
    r = json.load(open(P / "summary" / f"{c}.json"))
    po, tap, cl = r["poll"], r["tap"], r["classification"]
    raw = (cdir / "poll.jsonl").read_bytes()
    logs.append(f"{hashlib.sha256(raw).hexdigest()}  cycles/{c}/poll.jsonl")
    polls = sorted(jl(cdir / "poll.jsonl"), key=lambda x: x["n"])
    assert [x["n"] for x in polls] == list(range(len(polls))) and all(len(x["words"]) == 8 for x in polls), c
    t_bind = k["bind-time"]["t_bind_local"]
    t_unbind = [e for e in ev if e["kind"] == "unbind"][0]["t_cmd_local"]
    hold_s = k["start"]["hold_s"]
    rel = lambda t: t - t_bind
    first_s, last_s = rel(polls[0]["t0"]), rel(polls[-1]["t1"])
    assert abs(first_s - po["first_poll_s"]) <= 5e-4 and abs(last_s - po["last_poll_s"]) <= 5e-4, c

    # SLIP_LB changes, from the raw log
    slips = []
    for a, b in zip(polls, polls[1:]):
        dd = (word(b, "0x8d4") & 0xFFFF) - (word(a, "0x8d4") & 0xFFFF)
        ds = (word(b, "0x8d4") >> 16) - (word(a, "0x8d4") >> 16)
        if dd or ds:
            slips.append(dict(s_lo=rel(a["t0"]), s_hi=rel(b["t1"]), dups=dd, skips=ds))
    assert len(slips) == len(po["slips"]) and all(
        abs(x["s_lo"] - y["s_lo"]) <= 5e-4 and abs(x["s_hi"] - y["s_hi"]) <= 5e-4 and x["dups"] == y["dups"] and x["skips"] == y["skips"]
        for x, y in zip(slips, po["slips"])), c
    slip_tdm_static = len({word(x, "0x8d8") for x in polls}) == 1

    # RENDER_STAT brackets, from the raw log (a poll is after the bind when it ends after it, as ana_b17.py reads it)
    first_pdu_s = tap["priming"]["first_pdu_after_command_ms"] / 1e3
    post = [i for i, x in enumerate(polls) if rel(x["t1"]) > 0]
    rs = lambda i: word(polls[i], "0x8dc")
    i_pf = next(i for i in post if not rs(i) >> 8 & 1)
    assert rs(i_pf - 1) >> 8 & 1, c
    i_cv = next(i for i in post if rs(i) >> 9 & 1)
    held = all(not rs(i) >> 8 & 1 for i in range(i_pf, len(polls))) and all(rs(i) >> 9 & 1 for i in range(i_cv, len(polls)))
    render = dict(prefill_exit_after_s=max(rel(polls[i_pf - 1]["t0"]), first_pdu_s), prefill_exit_by_s=rel(polls[i_pf]["t1"]),
                  prefill_exit_first_post_poll=i_pf == post[0], lower_bound_is_first_pdu=first_pdu_s > rel(polls[i_pf - 1]["t0"]),
                  converged_by_s=rel(polls[i_cv]["t1"]), converged_polls_after_exit=i_cv - i_pf, held_to_last_poll=held,
                  fill_from_exit=[min(rs(i) & 0xFF for i in range(i_pf, len(polls))), max(rs(i) & 0xFF for i in range(i_pf, len(polls)))],
                  rails=sorted({rs(i) >> 16 for i in range(len(polls))}))

    # polls that took longer than LONG_POLL_S, from the raw log
    long_polls = [dict(n=x["n"], start_from_unbind_s=x["t0"] - t_unbind, start_from_bind_s=rel(x["t0"]), took_s=x["t1"] - x["t0"])
                  for x in polls if x["t1"] - x["t0"] > LONG_POLL_S]

    b = bursts(tap.get("late_pdus") or [])
    windows = dict(last_poll=last_s, hold=hold_s, capture=float("inf"))
    sl_out = []
    for x, y in zip(slips, cl["slips"]):
        inside = [z for z in b if x["s_lo"] <= z["s"] <= x["s_hi"]]
        before = [z for z in tap["late_pdus"] if z["s"] < x["s_lo"]]
        lat_in = po["slips"][len(sl_out)]["tap_lateness_max_us"]
        after = {}
        for wn, end in windows.items():
            a = [z for z in b if x["s_hi"] < z["s"] <= end]
            after[wn] = dict(bursts=len(a), peak_us=max((z["peak_us"] for z in a), default=None),
                             larger_than_slipping=any(z["peak_us"] > inside[0]["peak_us"] for z in a) if inside else None)
        sl_out.append(dict(s_lo=x["s_lo"], s_hi=x["s_hi"], width_s=x["s_hi"] - x["s_lo"], polls_left_s=last_s - x["s_hi"],
                           dups=x["dups"], skips=x["skips"], cls=y["cls"], basis=y["basis"], lateness_max_in_interval_us=lat_in,
                           first_burst_in_interval=bool(b) and b[0] in inside, slipping_burst_peak_us=inside[0]["peak_us"] if inside else None,
                           lateness_max_before_interval_us=max((z["late_us"] for z in before), default=None), after=after,
                           long_poll_in_interval=any(x["s_lo"] <= lp["start_from_bind_s"] < x["s_hi"] for lp in long_polls)))
    cap = k["capture-end"]
    pr = tap["priming"]
    rows.append(dict(
        cycle=c, tool_sha256=k["start"]["tool_sha256"], poller_sha256=k["start"]["poller_sha256"], t_bind_local=t_bind,
        # a time of day is a clock reading: truncated, as a clock shows it, not rounded
        bind_utc=datetime.fromtimestamp(t_bind, timezone.utc).strftime("%H:%M:%S.%f")[:-3],
        unbind_to_bind_s=t_bind - t_unbind, unbind_to_bind_tap_s=tap["unbind_to_bind_tap_s"],
        unbind_status=r["unbind_status"], bind_status=r["bind_status"],
        format_check=[dict(talker_fmt=f["talker_fmt"], listener_fmt=f["listener_fmt"], set=f["set"]) for f in r["format_check"]],
        states=r["states"], polls=len(polls), first_poll_s=first_s, last_poll_s=last_s, hold_s=hold_s,
        poll_spacing_s=[min(y["t0"] - x["t0"] for x, y in zip(polls, polls[1:])), max(y["t0"] - x["t0"] for x, y in zip(polls, polls[1:]))],
        slip_lb_first=dict(dups=word(polls[0], "0x8d4") & 0xFFFF, skips=word(polls[0], "0x8d4") >> 16),
        slip_lb_last=dict(dups=word(polls[-1], "0x8d4") & 0xFFFF, skips=word(polls[-1], "0x8d4") >> 16), slip_tdm_static=slip_tdm_static,
        servo_states=sorted({word(x, "0x8f8") & 7 for x in polls}), aafm_stat_values=sorted({x["words"]["0x8e0"] for x in polls}),
        settle_boundary="undefined: no poll read LOCKED (MCSRV_STAT state IDLE throughout)" if po["servo_states"] == [0] else "check",
        render=render, long_polls=long_polls, slips=sl_out, rates_ppm={n: v["rate_ppm"] for n, v in tap["streams"].items()},
        seq_gaps={n: v["seq_gaps"] for n, v in tap["streams"].items()}, delta_ppm=tap["delta_ppm"],
        rate_interval_s=1 / (FS * abs(tap["delta_ppm"]) * 1e-6), bound_window_s=cl["bound_window_s"], rate_slips_expected=cl["rate_slips_expected"],
        first_pdu_after_bind_ms=pr["first_pdu_after_command_ms"], phase_us_mod_pdu=pr["phase_us_mod_pdu"], lateness_us=pr["lateness_us"],
        late_bursts={wn: len([z for z in b if z["s"] <= end]) for wn, end in windows.items()},
        late_burst_pdus=[min((z["pdus"] for z in b), default=None), max((z["pdus"] for z in b), default=None)],
        late_burst_times_s=[z["s"] for z in b], peer_gap=gap[c],
        capture=dict(file=cap["file"], bytes=cap["bytes"], sha256=cap["sha256"], summary=cap["summary"], removed_from_tap=cap["removed_from_tap"]),
        ended_bound_as_found=k["cycle-check"]["bound_as_found"], clk_dut_end=k["cycle-check"]["clk_dut_end"]))

# the cumulative counter: no slip between the last poll of one cycle and the first of the next, or after c10
start_bl, end_bl = baseline(P / "restore" / "dut-start.txt"), baseline(P / "restore" / "dut-end.txt")
chain = [start_bl] + [x for r in rows for x in (r["slip_lb_first"], r["slip_lb_last"])] + [end_bl]
continuity = dict(start_baseline=start_bl, end_baseline=end_bl,
                  joins_equal=[chain[i] == chain[i + 1] for i in range(0, len(chain), 2)])
assert all(continuity["joins_equal"]), continuity

(P / "summary" / "counter-logs.sha256").write_text("\n".join(logs) + "\n")
digest = hashlib.sha256((P / "summary" / "counter-logs.sha256").read_bytes()).hexdigest()
S = [s for r in rows for s in r["slips"]]
mn = lambda xs: min(xs)
mx = lambda xs: max(xs)

# ---------------------------------------------------------------------------------------------- printed
md = ["| Cycle | Bind, UTC | Settle boundary | Polls, s from the bind | `SLIP_LB` dups | Slip: s from the bind, count | Before or after | Class | delta_ppm, rate interval | Largest lateness in the slip's interval |",
      "|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    for s in r["slips"] or [None]:
        md.append("| {c} | {b} | Undefined (servo IDLE) | {n}, {f} to {l} | {a} to {e} | {sl} | {ba} | {cl} | {d}, {ri} s | {lt} |".format(
            c=r["cycle"], b=r["bind_utc"], n=r["polls"], f=r1(r["first_poll_s"], 2, True), l=r1(r["last_poll_s"], 2, True),
            a=r["slip_lb_first"]["dups"], e=r["slip_lb_last"]["dups"],
            sl=f"{r1(s['s_lo'], 2)} to {r1(s['s_hi'], 2)}, +{s['dups']} dups, {s['skips']} skips" if s else "none",
            ba="No boundary" if s else "-", cl=f"({s['cls']})" if s else "-", d=f"{r['delta_ppm']:+.4f}", ri=f"{r['rate_interval_s']:,.0f}",
            lt=once(s["lateness_max_in_interval_us"], 3, 1, f"{r['cycle']} lateness in interval") + " us" if s else "-"))
(P / "summary" / "table.md").write_text("\n".join(md) + "\n")


def rng(vals, dp, what, src_dp=None, sign=False, unit=""):
    lo, hi = min(vals), max(vals)
    f = (lambda v, t: once(v, src_dp, dp, f"{what} {t}", sign)) if src_dp is not None else (lambda v, t: r1(v, dp, sign))
    return f"{f(lo, 'min')} to {f(hi, 'max')}{unit}"


def irng(vals):
    return f"{min(vals)} to {max(vals)}"


rates = [v for r in rows for v in r["rates_ppm"].values()]
d_abs = max(abs(r["delta_ppm"]) for r in rows)
fig = dict(
    slip_after_bind_s=f"{r1(mn([s['s_lo'] for s in S]), 2)} to {r1(mx([s['s_hi'] for s in S]), 2)}",
    slip_interval_width_s=rng([s["width_s"] for s in S], 2, "width"),
    polls_left_after_slip_s=rng([s["polls_left_s"] for s in S], 1, "left"),
    last_poll_min_s=r1(mn([r["last_poll_s"] for r in rows]), 2),
    last_poll_s=rng([r["last_poll_s"] for r in rows], 2, "last poll", sign=True),
    prefill_exit_by_s=rng([r["render"]["prefill_exit_by_s"] for r in rows], 2, "prefill by"),
    prefill_exit_first_post_poll=[r["cycle"] for r in rows if r["render"]["prefill_exit_first_post_poll"]],
    prefill_exit_brackets={r["cycle"]: f"({r1(r['render']['prefill_exit_after_s'], 3)}, {r1(r['render']['prefill_exit_by_s'], 3)}]" for r in rows},
    converged_by_s=rng([r["render"]["converged_by_s"] for r in rows], 2, "converged by"),
    converged_one_poll_later=[r["cycle"] for r in rows if r["render"]["converged_polls_after_exit"] == 1],
    converged_later_by_s=rng([r["render"]["converged_by_s"] for r in rows if r["render"]["converged_polls_after_exit"] == 1], 2, "converged later by"),
    converged_max_polls_after_exit=max(r["render"]["converged_polls_after_exit"] for r in rows),
    render_held_to_last_poll=all(r["render"]["held_to_last_poll"] for r in rows),
    fill_from_exit=f"{min(r['render']['fill_from_exit'][0] for r in rows)} to {max(r['render']['fill_from_exit'][1] for r in rows)}",
    first_pdu_ms=rng([r["first_pdu_after_bind_ms"] for r in rows], 1, "first PDU", 3),
    phase_median_us=rng([r["phase_us_mod_pdu"]["p50"] for r in rows], 3, "phase p50"),
    lateness_p999_us=rng([r["lateness_us"]["p999"] for r in rows], 1, "lateness p99.9", 3),
    burst_pdus=irng([x for r in rows for x in r["late_burst_pdus"]]),
    bursts_per_cycle={wn: irng([r["late_bursts"][wn] for r in rows]) for wn in ("last_poll", "hold", "capture")},
    lateness_in_interval_us=rng([s["lateness_max_in_interval_us"] for s in S], 1, "in interval", 3),
    bursts_after_slip={wn: irng([s["after"][wn]["bursts"] for s in S]) for wn in ("last_poll", "hold", "capture")},
    peak_after_slip_us={wn: rng([s["after"][wn]["peak_us"] for s in S], 1, f"after {wn}", 3) for wn in ("last_poll", "hold", "capture")},
    later_larger={wn: sum(1 for s in S if s["after"][wn]["larger_than_slipping"]) for wn in ("last_poll", "hold", "capture")},
    first_burst_in_interval=sum(1 for s in S if s["first_burst_in_interval"]),
    none_over_10us_before=sum(1 for s in S if s["lateness_max_before_interval_us"] is None),
    rates_vs_gptp_ppm=rng(rates, 2, "rates", 4, sign=True),
    delta_ppm=f"{min(r['delta_ppm'] for r in rows):+.4f} to {max(r['delta_ppm'] for r in rows):+.4f}",
    rate_interval_min_s=f"{min(r['rate_interval_s'] for r in rows):,.0f}",
    rate_interval_min_at_resolution_s=f"{1 / (FS * (d_abs + 1e-4) * 1e-6):,.0f}",
    rate_slips_expected_max=once(max(r["rate_slips_expected"] for r in rows), 4, 3, "expected slips max"),
    bound_window_s=rng([r["bound_window_s"] for r in rows], 1, "bound window", 3),
    unbind_to_bind_tap_vs_host_ms_max=r1(max(abs(r["unbind_to_bind_tap_s"] - r["unbind_to_bind_s"]) for r in rows) * 1e3, 1),
    long_polls=dict(per_cycle=irng([len(r["long_polls"]) for r in rows]),
                    after_unbind_s=rng([lp["start_from_unbind_s"] for r in rows for lp in r["long_polls"] if lp["start_from_bind_s"] < 0], 2, "long after unbind"),
                    after_bind_s=rng([lp["start_from_bind_s"] for r in rows for lp in r["long_polls"] if lp["start_from_bind_s"] > 0], 2, "long after bind"),
                    took_s=rng([lp["took_s"] for r in rows for lp in r["long_polls"]], 2, "long took"),
                    others_took_max_s=r1(max(x["t1"] - x["t0"] for cdir in sorted((P / "cycles").glob("c[0-9][0-9]"))
                                             for x in jl(cdir / "poll.jsonl") if x["t1"] - x["t0"] <= LONG_POLL_S), 2),
                    slip_intervals_containing_one=[r["cycle"] for r in rows for s in r["slips"] if s["long_poll_in_interval"]]),
    peer_stream_after_unbind_s={r["cycle"]: r1(r["peer_gap"]["peer_last_before_bind_s"] - r["peer_gap"]["unbind_s"], 2) for r in rows},
    peer_stream_last_before_bind_s={r["cycle"]: r1(r["peer_gap"]["peer_last_before_bind_s"], 2) for r in rows},
)
(P / "summary" / "figures.json").write_text(json.dumps(dict(figures=fig, rounding=ROUNDING), indent=1) + "\n")

pm = ["| Quantity | Window | Range over the ten cycles |", "|---|---|---|",
      f"| First peer PDU on the DUT's link after the bind's command | The bind | {fig['first_pdu_ms']} ms |",
      f"| Arrival phase against the DUT's own transmit grid, median, modulo one PDU | The whole post-bind stream | {fig['phase_median_us']} us |",
      f"| Arrival lateness against a line fitted to the arrivals, 99.9th percentile | The whole post-bind stream | {fig['lateness_p999_us']} us |",
      f"| Bursts of PDUs over 20 us late per cycle, grouped while less than 1 ms apart, {fig['burst_pdus']} such PDUs each | To the last poll | {fig['bursts_per_cycle']['last_poll']} |",
      f"| The same | To the capture's end, about 41.9 s after the bind | {fig['bursts_per_cycle']['capture']} |",
      f"| Largest lateness in the slip's interval | The slip's interval | {fig['lateness_in_interval_us']} us |",
      f"| Bursts after the slip | To the last poll | {fig['bursts_after_slip']['last_poll']} |",
      f"| Largest lateness after the slip | To the last poll | {fig['peak_after_slip_us']['last_poll']} us |",
      f"| Bursts after the slip | To the capture's end | {fig['bursts_after_slip']['capture']} |",
      f"| Largest lateness after the slip | To the capture's end | {fig['peak_after_slip_us']['capture']} us |"]
(P / "summary" / "priming.md").write_text("\n".join(pm) + "\n")

lane = dict(cycles=len(rows), slips=len(S), classes={x: sum(1 for s in S if s["cls"] == x) for x in ("a", "b", "c")},
            slip_lb=[rows[0]["slip_lb_first"], rows[-1]["slip_lb_last"]], counter_continuity=continuity,
            windows=dict(last_poll="bursts starting no later than the end of the cycle's last poll", hold="no later than the 32 s hold",
                         capture="to the end of the capture, about 41.9 s after the bind"),
            delta_resolution_ppm=1e-4, counter_logs_manifest_sha256=digest, poller_sha256=sorted({r["poller_sha256"] for r in rows}),
            tool_sha256=sorted({r["tool_sha256"] for r in rows}), rounding_ties=sum(1 for x in ROUNDING if x["tie"]))
(P / "summary" / "cycles.json").write_text(json.dumps(dict(lane=lane, cycles=rows), indent=1) + "\n")
print(json.dumps(dict(lane=lane, figures=fig), indent=1))
