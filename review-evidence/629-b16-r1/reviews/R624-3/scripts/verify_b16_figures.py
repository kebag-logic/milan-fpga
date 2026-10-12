#!/usr/bin/env python3
"""Reviewer-side recomputation of lane B16's headline figures from the author's packet, independent of the
author's figures check: it reads the per-block and per-poll records, not the author's summary fields where a
per-record source exists, and prints each recomputed figure beside the text the findings page shows.

usage: verify_b16_figures.py <author packet root> <findings.md> <out.json>

Offline and read-only. Exit 0 when every comparison holds, 1 otherwise.
"""
import json
import statistics
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT, PAGE, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
page = PAGE.read_text(encoding="utf-8")
results = []


def J(rel):
    return json.loads((ROOT / rel).read_text())


def r2(x, nd=2):
    return str(Decimal(str(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def check(name, got, want, on_page=None):
    ok = str(got) == str(want)
    present = None if on_page is None else (on_page in page)
    results.append(dict(name=name, recomputed=str(got), shown=str(want), equal=ok, page_text=on_page,
                        page_has_text=present))
    return ok and present is not False


def runs(idx):
    out, s = [], None
    for i, b in enumerate(idx):
        if s is None:
            s = b
        if i + 1 == len(idx) or idx[i + 1] != b + 1:
            out.append((s, b))
            s = None
    return out


# ---- B0 (b0-2) and the B16c cases at (c), from the per-block records
def floor_blocks(g):
    """Event-free blocks within 3 dB of each channel's all-block median THD+N, on both channels."""
    blocks = g["blocks"]
    med = {ch: statistics.median(b[ch]["thdn_db"] for b in blocks) for ch in ("ch0", "ch1")}
    return [b for b in blocks if b["events"] == 0 and all(b[ch]["thdn_db"] <= med[ch] + 3 for ch in ("ch0", "ch1"))]


for run, nfloor in (("b0-2", 169), ("bcrf", 300), ("baaf", 300)):
    g = J(f"summary/{run}/c-b9-grade.json")
    fl = floor_blocks(g)
    check(f"{run} (c) blocks", len(g["blocks"]), 300)
    check(f"{run} (c) blocks at floor (own rule)", len(fl), nfloor)
    check(f"{run} (c) events", sum(b["events"] for b in g["blocks"]) + len(g["events"]), 0)
    for ch, tone in (("ch0", "997"), ("ch1", "9973")):
        fm = r2(statistics.median(b[ch]["thdn_db"] for b in fl))
        fw = r2(max(b[ch]["thdn_db"] for b in fl))
        am = r2(statistics.median(b[ch]["thdn_db"] for b in g["blocks"]))
        aw = r2(max(b[ch]["thdn_db"] for b in g["blocks"]))
        results.append(dict(name=f"{run} {tone} floor median/worst, all median/worst", recomputed=[fm, fw, am, aw]))
    if run == "b0-2":
        deg = [b["block"] for b in g["blocks"] if b not in fl]
        rr = runs(deg)
        check("b0-2 degraded count", len(deg), 131)
        check("b0-2 degraded runs", rr[:4], [(0, 18), (28, 31), (43, 44), (46, 54)])
        check("b0-2 later runs after 46-54", len(rr) - 4, 11, "and eleven later runs")
        ov = J("summary/b0-2/align-a-c.json")["compared_equal"]
        whole = ov // 48000  # blocks wholly inside the overlap: 0 .. whole-1
        inside = [b for b in deg if b < whole]
        beyond = [b for b in deg if b >= whole]
        check("b0-2 overlap frames (a)", ov, 1637452)
        check("b0-2 whole blocks inside", whole - 1, 33, "hold whole blocks\n0 to 33")
        check("b0-2 degraded inside", len(inside), 23)
        check("b0-2 degraded beyond", len(beyond), 108)
        check("b0-2 beyond runs", len(runs(beyond)), 13, "in thirteen runs")
        check("b0-2 beyond span", (min(beyond), max(beyond)), (43, 251))
        for ch, want in (("ch0", "-100.61"), ("ch1", "-80.63")):
            wb = max((b for b in g["blocks"] if b["block"] in inside), key=lambda b: b[ch]["thdn_db"])
            check(f"b0-2 worst inside {ch}", (wb["block"], r2(wb[ch]["thdn_db"])), (7, want))
        for ch, want in (("ch0", "-100.47"), ("ch1", "-80.48")):
            wb = max((b for b in g["blocks"] if b["block"] in beyond), key=lambda b: b[ch]["thdn_db"])
            check(f"b0-2 worst beyond {ch}", (wb["block"], r2(wb[ch]["thdn_db"])), (224, want))

# ---- (d), the positive control: blocks wholly inside the playback at the loop's floor
for run, want in (("pts2", (13, 11)), ("b0-2", (303, 303)), ("bcrf", (303, 303)), ("baaf", (303, 303))):
    d = J(f"summary/{run}/d-extcap-pair.json")
    for row in d["rows"]:
        k = "tone_997" if "tone_997" in row else "tone_9973"
        pb = row[k]["per_block"]
        first = next(i for i, b in enumerate(pb) if b["thdn_db"] > -300)  # the block holding the start
        inside = pb[first + 1:]
        floor = row[k]["median"]["thdn_db"]
        at = sum(1 for b in inside if abs(b["thdn_db"] - floor) <= 3)
        check(f"{run} (d) pair_channel {row['pair_channel']} pre-blocks/start/inside/at-floor",
              (first, len(inside), at), (2,) + want)

# pts2 taps of the DUT's talker: 23 blocks, 15 wholly inside, all at floor
for t in ("dut", "peer"):
    d = J(f"summary/pts2/ctl-dut-talker-{t}-tap.json")
    for c in d["channels"]:
        for k in ("tone_997", "tone_9973"):
            if not isinstance(c.get(k), dict):
                continue
            pb = c[k]["per_block"]
            silent = [i for i, b in enumerate(pb) if b["thdn_db"] <= -300]
            fl = c[k]["median"]["thdn_db"]
            at = [i for i, b in enumerate(pb) if abs(b["thdn_db"] - fl) <= 3]
            results.append(dict(name=f"pts2 tap {t} ch{c['channel']} {k}", blocks=len(pb), silent=silent, at_floor=at))

# ---- B16c (a) attribution (R625-2-F1)
for run, want in (("bcrf", ("-123.98", "-123.97")), ("baaf", ("-123.98", "-123.98"))):
    d = J(f"summary/{run}/a-peer-tap.json")
    got, worst = [], []
    for c in d["channels"][:2]:
        k = "tone_997" if c["channel"] == 0 else "tone_9973"
        got.append(r2(c[k]["median"]["thdn_db"]))
        worst.append(r2(max(b["thdn_db"] for b in c[k]["per_block"])))
    check(f"{run} (a) medians 997/9973", tuple(got), want)
    check(f"{run} (a) worst blocks", tuple(worst), ("-123.93", "-123.93"))
check("R625-2-F1 text", True, True,
      "At (a), medians are -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is -123.93 dB.")

# The B16c poll figures are recomputed by verify_polls.py.
Path(OUT).write_text(json.dumps(results, indent=1, default=str))
bad = [r for r in results if r.get("equal") is False or r.get("page_has_text") is False]
for r in results:
    print(json.dumps(r, default=str)[:400])
print("BAD", len(bad))
sys.exit(1 if bad else 0)
