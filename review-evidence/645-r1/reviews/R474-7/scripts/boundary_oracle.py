#!/usr/bin/env python3
"""Reviewer-planted boundary cases for follow_ring/trace_table.py.

    python3 -I -B boundary_oracle.py <source-tree> <out-dir> [--random N] [--seed S]

An independent integer oracle: every decimal is scaled to an integer number
of 1e-30 s units, so bin membership is pure integer arithmetic. It checks
slips/skips/recentres per bin, PDU attribution (render_fill), the number of
rows, the servo snapshot (last window with t <= bin end) and event_trace.
Planted cases: exact edges k*step from a decimal origin across many bins
(float accumulation would drift), +/-1e-9 and +/-1e-30 neighbours, the
default -2..60 s window edges, a short final bin, exponent-form CLI values,
and simultaneous dup/skip/recentre. Exit 0 only when every case agrees.
"""
import argparse
import csv
import json
import random
import subprocess
import sys
from decimal import Decimal, localcontext
from pathlib import Path

SCALE = 30


def units(s: str) -> int:
    with localcontext() as ctx:
        ctx.prec = 200
        d = Decimal(s).scaleb(SCALE)
    i = int(d)
    if Decimal(i) != d:
        raise ValueError(f"{s} needs more than {SCALE} decimals")
    return i


def fmt(u: int) -> str:
    sign = "-" if u < 0 else ""
    u = abs(u)
    w, f = divmod(u, 10 ** SCALE)
    return f"{sign}{w}.{f:0{SCALE}d}".rstrip("0").rstrip(".") if f else f"{sign}{w}"


def oracle(origin, frm, to, step, events, pdus, servo, end_u):
    lo, hi, st = origin + frm, origin + to, step
    n = max(1, -(-(hi - lo) // st))
    bins = [{"slips": 0, "skips": 0, "recentres": 0, "fill": "-"} for _ in range(n)]
    for kind, t in events:
        if lo <= t < hi:
            b = bins[(t - lo) // st]
            if kind == "recentre":
                b["recentres"] += 1
            else:
                b["slips"] += 1
                b["skips"] += kind == "skip"
    for t, fill in pdus:
        if lo <= t < hi:
            b = bins[(t - lo) // st]
            b.setdefault("fills", []).append(fill)
    for b in bins:
        fs = b.pop("fills", None)
        if fs:
            b["fill"] = f"{min(fs)}..{max(fs)}"
    for i, b in enumerate(bins):
        te = min(hi, lo + (i + 1) * st)
        prior = [e for (ts, e) in servo if ts <= te]
        b["e_ns"] = str(prior[-1]) if prior else "0"
        if end_u is None:
            b["trace"] = "unavailable"
        else:
            b["trace"] = "complete" if lo + i * st >= 0 and te <= end_u else "partial"
    return bins


def run(src, work, name, origin, frm, to, step, events, pdus, servo, end, cli=None,
        default_window=False):
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    log = f"info: t={origin} s  CLOCK_SOURCE <- 1\n" if default_window else ""
    log += "".join(f"RING-EVENT: {k} {t}\n" for k, t in events)
    if end is not None:
        log += f"RING-EVENTS: complete through {end} s\n"
    (d / "run.log").write_text(log)
    (d / "pdu.csv").write_text("arrive_s,ring_margin_ticks,render_fill,render_delay_ticks\n" +
                               "".join(f"{t},5.3,{f},8.5\n" for t, f in pdus))
    (d / "servo.csv").write_text("t_s,state,pi_run,ew_ns,trim_ppm,meter_valid\n" +
                                 "".join(f"{t},4,1,{e},0.0,1\n" for t, e in servo))
    argv = [sys.executable, "-I", "-B", str(src / "tb/verilator/follow_ring/trace_table.py"),
            str(d / "run.log"), str(d / "pdu.csv"), str(d / "servo.csv"), "--csv", str(d / "table.csv")]
    c = cli or {}
    if not default_window:
        argv += ["--origin-s", c.get("origin", origin), "--from-s", c.get("from", frm),
                 "--to-s", c.get("to", to), "--step-s", c.get("step", step)]
    r = subprocess.run(argv, capture_output=True, text=True)
    (d / "table.txt").write_text(r.stdout + r.stderr + f"rc={r.returncode}\n")
    if r.returncode != 0:
        return {"case": name, "pass": False, "why": "cli rc", "stderr": r.stderr[-400:]}
    rows = list(csv.DictReader((d / "table.csv").open()))
    fw = "-2" if default_window else frm
    tw = "60" if default_window else to
    exp = oracle(units(origin), units(fw), units(tw), units(step),
                 [(k, units(t)) for k, t in events], [(units(t), f) for t, f in pdus],
                 [(units(t), e) for t, e in servo], None if end is None else units(end))
    got = [{"slips": int(r["slips"]), "skips": int(r["skips"]), "recentres": int(r["recentres"]),
            "fill": r["render_fill"], "e_ns": r["e_ns"], "trace": r["event_trace"]} for r in rows]
    ok = got == exp
    out = {"case": name, "pass": ok, "rows": len(rows), "expected_rows": len(exp), "argv": argv[4:]}
    if not ok:
        diff = [(i, g, e) for i, (g, e) in enumerate(zip(got, exp)) if g != e][:5]
        out["first_diffs"] = diff
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--random", type=int, default=60)
    ap.add_argument("--seed", type=int, default=4747)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    res = []
    one = 10 ** SCALE
    # 1: exact edges across 997 bins from a decimal origin, decimal step 0.1
    o, f, t, s = "0.3", "0", "99.7", "0.1"
    lo, st = units(o) + units(f), units(s)
    ks = [1, 2, 3, 7, 10, 29, 333, 500, 996]
    ev = []
    for k in ks:
        e = lo + k * st
        ev += [("dup", fmt(e)), ("skip", fmt(e - 10 ** (SCALE - 9))), ("recentre", fmt(e + 1))]
    pd = [(fmt(lo + k * st), k % 90 + 1) for k in ks]
    res.append(run(a.source, a.out, "many-bins-edges", o, f, t, s, ev, pd,
                   [(fmt(lo + 3 * st), 11), (fmt(lo + 3 * st + 1), 12)], "200"))
    # 2: default window -2..60 s about the first set; both window edges
    o = "12.345678"
    lo, hi = units(o) - 2 * one, units(o) + 60 * one
    ev = [("dup", fmt(lo)), ("skip", fmt(hi)), ("recentre", fmt(hi - 1)), ("dup", fmt(lo - 1))]
    res.append(run(a.source, a.out, "default-window-edges", o, None, None, "0.5", ev,
                   [(fmt(lo), 7), (fmt(hi), 8)], [], "100", default_window=True))
    # 3: short final bin, step does not divide the range; events at the exact end
    o, f, t, s = "1.1", "-0.05", "0.33", "0.07"
    lo, hi = units(o) + units(f), units(o) + units(t)
    ev = [("dup", fmt(hi)), ("skip", fmt(hi - 1)), ("recentre", fmt(lo + 5 * units(s)))]
    res.append(run(a.source, a.out, "short-final-bin", o, f, t, s, ev,
                   [(fmt(hi - 1), 3), (fmt(hi), 4)], [(fmt(hi), 9)], "5"))
    # 4: exponent-form CLI values equal to plain decimals
    res.append(run(a.source, a.out, "exponent-cli", "0.1", "0", "0.4", "0.1",
                   [("dup", "0.3"), ("skip", "0.29999999999"), ("recentre", "0.5")],
                   [("0.3", 5)], [], "1",
                   cli={"origin": "1e-1", "from": "0E+3", "to": "4e-1", "step": "1.0e-1"}))
    # 5: simultaneous events at one instant, and a bin that starts before t=0
    res.append(run(a.source, a.out, "simultaneous-and-negative-start", "0.2", "-0.4", "0.4", "0.2",
                   [("dup", "0.2"), ("skip", "0.2"), ("recentre", "0.2"), ("dup", "0")],
                   [("0.2", 2)], [("0.4", 1)], "0.5"))
    # 6: no completion record: unavailable on every row, counts still read
    res.append(run(a.source, a.out, "no-completion-record", "0", "0", "1", "0.25",
                   [("dup", "0.5")], [], [], None))
    # random: decimal origin/from/to/step to 9 places; events at edges and neighbours
    rng = random.Random(a.seed)
    for i in range(a.random):
        o = fmt(rng.randrange(0, 50 * 10 ** 9) * 10 ** (SCALE - 9))
        f = fmt(rng.randrange(-3 * 10 ** 9, 10 ** 9) * 10 ** (SCALE - 9))
        st = rng.randrange(1, 10 ** 9) * 10 ** (SCALE - 9)
        nb = rng.randrange(1, 40)
        span = nb * st - rng.randrange(0, st)
        t = fmt(units(f) + span)
        lo = units(o) + units(f)
        ev, pd, sv = [], [], []
        for _ in range(12):
            k = rng.randrange(0, nb + 1)
            d = rng.choice([0, 0, 1, -1, 10 ** (SCALE - 9), -(10 ** (SCALE - 9))])
            e = lo + k * st + d
            ev.append((rng.choice(["dup", "skip", "recentre"]), fmt(max(e, 0))))
            pd.append((fmt(max(e, 0)), rng.randrange(0, 20)))
            sv.append((fmt(max(e, 0)), rng.randrange(-99, 99)))
        sv.sort(key=lambda x: units(x[0]))
        end = fmt(lo + rng.randrange(0, nb + 1) * st) if rng.random() < 0.5 else fmt(lo + nb * st + one)
        res.append(run(a.source, a.out, f"random-{i:03d}", o, f, t, fmt(st), ev, pd, sv,
                       end if units(end) >= 0 else "0"))
    (a.out / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    bad = [r for r in res if not r["pass"]]
    for r in bad:
        print(json.dumps(r))
    print(f"boundary oracle: {len(res) - len(bad)}/{len(res)} cases agree")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
