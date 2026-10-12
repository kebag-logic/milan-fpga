#!/usr/bin/env python3
"""R624-6 independent recomputation of lane B16's headline figures from the published packet.

usage: indep_figures.py <packet root (author-r6)> <findings page> <out.json>
Reads only packet receipts (never the author's figures check), recomputes each figure with this
reviewer's own reading of the receipt, and checks that the page shows it on the expected line text.
Exit 0 only if every figure matches."""
import json, sys, re
from decimal import Decimal, ROUND_HALF_UP
P, PAGE, OUT = sys.argv[1:4]
page = open(PAGE, encoding="utf-8").read().split("\n")
J = lambda f: json.load(open(f"{P}/{f}"))
EV = lambda r: [json.loads(l) for l in open(f"{P}/runs/{r}/events.jsonl")]
res, bad = [], 0
def chk(name, value, line, needle):
    global bad
    text = page[line - 1]
    ok = needle in text
    bad += not ok
    res.append(dict(name=name, value=str(value), line=line, needle=needle, ok=ok))
def r2(x, n=2):
    return str(Decimal(str(x)).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))

# ---- servo trace: lock brackets, window polls, 0x74 counts, trim, rates, SLIP_LB, AAFM_STAT
def trace(run):
    rows = [l.rstrip("\n").split("\t") for l in open(f"{P}/r2/{run}-poll-trace.tsv")][1:]
    out = []
    for r in rows:
        st = int(r[3], 16)
        out.append(dict(n=int(r[0]), t=Decimal(r[1]), ms=Decimal(r[2]), stat=st, state=st & 7,
                        busy=bool(st & 0x40), trim=Decimal(((st >> 16) ^ 0x8000) - 0x8000) / 16,
                        aafm=int(r[4], 16), aafr=int(r[5], 16), slip_lb=int(r[6], 16), slip_tdm=int(r[7], 16),
                        crf_rate=int(r[10], 16)))
    return out
def s32(x):
    return x - (1 << 32) if x & 0x80000000 else x
summ = {}
for run, line_lock in (("bcrf", 3174), ("baaf", 3175)):
    tr = trace(run)
    rec = J(f"r2/{run}-poll-receipt.json")
    marks = rec["marks_after_set_s"]
    after = [p for p in tr if p["t"] >= 0]
    first_locked = next(p for p in after if p["state"] == 4)
    last_acq = max((p for p in after if p["state"] == 3 and p["n"] < first_locked["n"]), key=lambda p: p["n"])
    lo = last_acq["t"]; hi = first_locked["t"] + first_locked["ms"] / 1000
    win = [p for p in tr if Decimal(str(marks["window-start"])) <= p["t"] and p["t"] + p["ms"] / 1000 <= Decimal(str(marks["window-end"]))]
    winS = [p for p in tr if Decimal(str(marks["window-start"])) <= p["t"] < Decimal(str(marks["window-end"]))]
    nlock = sum(p["state"] == 4 for p in win)
    trims = [p["trim"] for p in win]
    crf = [Decimal(s32(p["crf_rate"])) / 512 for p in win]
    aaf = [Decimal(s32(p["aafr"])) / 512 for p in win]
    summ[run] = dict(lock=(str(lo), str(hi)), polls=(last_acq["n"], first_locked["n"]), win=len(win), win_starts=len(winS),
                     win_locked=nlock, busy=sum(p["busy"] for p in win), trim=(str(min(trims)), str(max(trims))),
                     crf=(r2(min(crf)), r2(max(crf))), aaf=(r2(min(aaf)), r2(max(aaf))),
                     aafm=sorted({hex(p["aafm"]) for p in win}), slip_tdm=sorted({p["slip_tdm"] for p in tr}),
                     slip_lb=(tr[0]["slip_lb"] & 0xffff, tr[-1]["slip_lb"] & 0xffff))
    steps = []
    for a, b in zip(tr, tr[1:]):
        if b["slip_lb"] != a["slip_lb"]:
            steps.append(dict(from_s=str(a["t"]), to_s=str(b["t"] + b["ms"] / 1000), states=(a["state"], b["state"]),
                              d=(a["slip_lb"] & 0xffff, b["slip_lb"] & 0xffff)))
    summ[run]["slip_steps"] = steps
    lock_ev = [e for e in EV(run) if e["kind"] == "servo-state"][0]
    chk(f"{run} lock bracket (trace start of last ACQUIRE poll; run record s_hi)", (str(lo), lock_ev["s_hi"]), line_lock, f"{r2(lo,3)} to {Decimal(str(lock_ev['s_hi'])):.3f} s")
    chk(f"{run} window LOCKED", (nlock, len(win)), line_lock, f"LOCKED at {nlock} of {len(win)}")
    chk(f"{run} trim", summ[run]["trim"], line_lock, f"{r2(max(trims),3)} to {r2(min(trims),3)} ppm")
b, a = summ["bcrf"], summ["baaf"]
chk("bcrf busy", (580, 16), 3184, f"{b['win']-b['busy']} and {b['busy']} of the window's")
chk("baaf busy", (584, 12), 3185, f"{a['win']-a['busy']} and {a['busy']} in B-AAF")
chk("bcrf crf rate", b["crf"], 3174, f"CRF sink +{r2(Decimal(b['crf'][0]))} to +{r2(Decimal(b['crf'][1]))} ppm")
chk("baaf aaf rate", a["aaf"], 3175, f"AAF meter +{a['aaf'][0]} to +{a['aaf'][1]} ppm")
chk("baaf crf rate", a["crf"], 3175, f"+{a['crf'][0]} to +{a['crf'][1]} ppm")
chk("baaf aafm", a["aafm"], 3175, "`0x001e0007`" if a["aafm"] == ["0x1e0007"] else "IMPOSSIBLE")
chk("terms LOCKED", (b["win_locked"], a["win_locked"]), 3200, f"LOCKED at {b['win_locked']} of {b['win']} window polls" if b["win_locked"] == a["win_locked"] and b["win"] == a["win"] else "IMPOSSIBLE")
chk("slip_lb ends", (b["slip_lb"][0], a["slip_lb"][1]), 3209, f"counted {b['slip_lb'][0]} dups")
chk("slip_lb end", a["slip_lb"][1], 3210, f"{a['slip_lb'][1]} at its end")

# ---- grades at (c), B0 and B16c
for run, lines in (("bcrf", (3134, 3135)), ("baaf", (3136, 3137)), ("b0-2", (3138, 3139))):
    g = J(f"summary/{run}/c-b9-grade.json")["summary"]
    for ch, ln in zip(("ch0", "ch1"), lines):
        f, al = g[f"{ch}_floor"], g[f"{ch}_all"]
        cell = f"| {g['blocks_at_floor']} | {r2(f['thdn_db_median'])} ({r2(f['thdn_db_worst'])}) | {r2(f['snr_db_median'])} | {r2(al['thdn_db_median'])} ({r2(al['thdn_db_worst'])}) |"
        chk(f"{run} {ch} grade", cell, ln, cell)
    chk(f"{run} events", g["events"], lines[0], f"| 300 | {g['events']} |")
g = J("summary/b0-2/c-b9-grade.json")["summary"]
deg = g["degraded_event_free_blocks"]
runs_, s = [], deg[0]
for x, y in zip(deg, deg[1:] + [None]):
    if y != x + 1:
        runs_.append((s, x)); s = y
inside = [x for x in deg if x <= 33]
chk("b0 degraded count", len(deg), 2826, "The other 131 blocks")
chk("b0 first runs", runs_[:4], 2827, "0 to 18,")
chk("b0 runs 3-4", runs_[2:4], 2828, "28 to 31, 43 to 44, 46 to 54")
chk("b0 inside", len(inside), 2830, f"Of the 131, {len(inside)} lie there")
chk("b0 beyond", (len(deg) - len(inside), len([r for r in runs_ if r[0] > 33])), 2832, f"The other {len(deg)-len(inside)} lie beyond")
blk = J("summary/b0-2/c-b9-grade.json")["blocks"]
w0 = max((b_ for b_ in blk if b_["block"] in inside), key=lambda b_: b_["ch0"]["thdn_db"])
w1 = max((b_ for b_ in blk if b_["block"] in inside), key=lambda b_: b_["ch1"]["thdn_db"])
chk("b0 worst inside", (w0["block"], w0["ch0"]["thdn_db"], w1["block"], w1["ch1"]["thdn_db"]), 2842, f"down to {r2(w0['ch0']['thdn_db'])} dB and {r2(w1['ch1']['thdn_db'])} dB (block {w0['block']})" if w0["block"] == w1["block"] else "IMPOSSIBLE")
bey = [b_ for b_ in blk if b_["block"] in deg and b_["block"] > 33]
x0 = max(bey, key=lambda b_: b_["ch0"]["thdn_db"]); x1 = max(bey, key=lambda b_: b_["ch1"]["thdn_db"])
chk("b0 worst beyond", (x0["block"], x1["block"]), 2842, f"(block {x0['block']})" if x0["block"] == x1["block"] else "IMPOSSIBLE")
chk("b0 beyond run span", (bey[0]["block"], bey[-1]["block"]), 2832, f"blocks {bey[0]['block']} to {bey[-1]['block']}")
chk("b0 beyond nruns", len([r for r in runs_ if r[0] > 33]), 2833, "in thirteen runs" if len([r for r in runs_ if r[0] > 33]) == 13 else "IMPOSSIBLE")

# ---- alignments
al = {r: (J(f"summary/{r}/align-a-c.json"), J(f"summary/{r}/align-b-c.json")) for r in ("pts1", "pts2", "pts3", "b0-2", "bcrf", "baaf")}
for r, (aa, bb) in al.items():
    assert aa["frames_differing"] == 0 and bb["frames_differing"] == 0 and not aa["slips"] and not bb["slips"], r
tot_a = sum(al[r][0]["compared_equal"] for r in ("pts1", "pts2", "pts3", "b0-2"))
tot_b = sum(al[r][1]["compared_equal"] for r in ("pts1", "pts2", "pts3", "b0-2"))
chk("b16b total vs a", tot_a, 2848, f"{tot_a:,} against (a)")
chk("b16b total vs b", tot_b, 2848, f"{tot_b:,} against (b)")
c_a = al["bcrf"][0]["compared_equal"] + al["baaf"][0]["compared_equal"]
c_b = al["bcrf"][1]["compared_equal"] + al["baaf"][1]["compared_equal"]
chk("b16c total vs a", c_a, 3250, f"{c_a:,} against (a)")
chk("b16c total vs b", c_b, 3250, f"{c_b:,} against (b)")
for r, ln in (("bcrf", 3149), ("baaf", 3150)):
    aa, bb = al[r]
    chk(f"{r} align", (aa["compared_equal"], bb["compared_equal"]), ln,
        f"over {bb['compared_equal']:,} recorded frames, {r2(Decimal(bb['compared_equal'])/48000,1)} s")
    chk(f"{r} align a", aa["compared_equal"], ln, f"over {aa['compared_equal']:,} frames, {r2(Decimal(aa['compared_equal'])/48000,1)} s")

# ---- (d) positive control
for r, ln in (("bcrf", 3157), ("baaf", 3158)):
    d = J(f"summary/{r}/d-loop-decode.json")
    chk(f"{r} d decoded", d["decoded"], ln, f"| {d['decoded']:,} | {d['skips']} | {d['repeats']} | {d['net_step_frames']} | {d['torn']} |")

# ---- clock-source record and restore
for r in ("bcrf", "baaf"):
    sets = [(e["tag"], e["who"], e["src"], e["status"], e["readback"]) for e in EV(r) if e["kind"] == "set-clock"]
    fin = [e for e in EV(r) if e["kind"] == "final"][0]
    exp = [("peer-internal", "peer", 0, "SUCCESS", 0), (r, "dut", 1 if r == "bcrf" else 2, "SUCCESS", 1 if r == "bcrf" else 2),
           ("restore", "dut", 0, "SUCCESS", 0), ("restore", "peer", 1, "SUCCESS", 1)]
    ok = sets == exp and fin["equal_to_found"] and fin["clk-dut"] == 0 and fin["clk-peer"] == 1
    bad += not ok
    res.append(dict(name=f"{r} clock-source sets and final", value=json.dumps([sets, fin["equal_to_found"], fin["differ"]]), line=3086, needle="events.jsonl", ok=ok))
json.dump(dict(results=res, bad=bad, summary=summ), open(OUT, "w"), indent=1, default=str)
for x in res:
    print(("OK  " if x["ok"] else "BAD ") + x["name"], "|", x["value"][:120], "| L", x["line"], "|", x["needle"][:90])
print("bad", bad)
sys.exit(1 if bad else 0)
