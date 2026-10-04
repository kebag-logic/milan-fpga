#!/usr/bin/env python3
"""[R453-2] Check every figure of the PR #153 body's Vivado table and delta line
against the published report files, parsed independently of the packet's tools.

Usage: vivado_table_check.py VIVADO_DIR PR_BODY.md
"""
import re, sys
from pathlib import Path

V, body = Path(sys.argv[1]), Path(sys.argv[2]).read_text()
ROWS = {  # PR body table label -> run directory
    "Shipping route at the merge, `main` `5c71928a`": "r1b-main-5c71928a-route-1x1",
    "Shipping route at the merge, head `6e950fea`": "r1b-head-6e950fea-route-1x1",
    "Shipping route, round 1 base `f4167536`": "r1-base-f4167536-route-1x1",
    "Shipping route, round 1 head `3ab2e4da`": "r1-head-3ab2e4da-route-1x1",
    "Standalone 1x1, base": "r1-base-f4167536-ooc-1x1",
    "Standalone 1x1, head": "r1-head-3ab2e4da-ooc-1x1",
    "Standalone 8x8, base": "r1-base-f4167536-ooc-8x8",
    "Standalone 8x8, head": "r1-head-3ab2e4da-ooc-8x8",
}
fails = 0


def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    fails += not ok


def table(text, first_col):
    """Rows of the report table whose first cell is first_col: list of cell lists."""
    out = []
    for line in text.splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 3 and c[1].rstrip("*").strip() == first_col:
            out.append(c)
    return out


def num(s):
    return int(float(s.replace(",", "")))


def figures(run):
    u = (V / run / "baseline_utilization.rpt").read_text()
    f = {"LUT": num(table(u, "Slice LUTs")[0][2]), "FF": num(table(u, "Slice Registers")[0][2]),
         "RAMB36": num(table(u, "RAMB36/FIFO")[0][2]), "RAMB18": num(table(u, "RAMB18")[0][2]),
         "DSP": num(table(u, "DSPs")[0][2])}
    s = table(u, "Slice")
    f["Slice"] = num(s[0][2]) if s else None
    m = re.search(r"^\|\s*CARRY4\s*\|\s*(\d+)", u, re.M)
    f["CARRY4"] = int(m.group(1))
    t = (V / run / "timing-extract.txt").read_text()
    m = re.search(r"-------\s+-------.*\n\s+(-?[0-9.]+)\s+\S+\s+\S+\s+\S+\s+(-?[0-9.]+)", t)
    f["WNS"], f["WHS"] = float(m.group(1)), float(m.group(2))
    h = (V / run / "baseline_hierarchy.rpt").read_text()
    hdr = None
    for line in h.splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 5 and c[1] == "Instance":
            hdr = c
        elif hdr and len(c) == len(hdr) and c[1] == "u_notify":
            d = dict(zip(hdr, c))
            f["notify"] = (int(d["Total LUTs"]), int(d["LUTRAMs"]), int(d["FFs"]))
            break
    return f


F = {r: figures(r) for r in ROWS.values()}
for label, run in ROWS.items():
    m = re.search(r"^\| " + re.escape(label) + r" \|(.*)\|\s*$", body, re.M)
    if not m:
        check(False, f"row {label} present")
        continue
    c = [x.strip() for x in m.group(1).split("|")]
    f = F[run]
    lut, ff, sl, br, dsp, wns, nt = c
    check(num(lut) == f["LUT"], f"{run} LUT {lut} == {f['LUT']}")
    check(num(ff) == f["FF"], f"{run} FF {ff} == {f['FF']}")
    check((sl == "" and f["Slice"] is None) or (sl != "" and num(sl) == f["Slice"]) or (sl == "" and "ooc" in run),
          f"{run} Slice '{sl}' vs {f['Slice']}")
    b36, b18 = [num(x) for x in br.split("/")]
    check((b36, b18) == (f["RAMB36"], f["RAMB18"]), f"{run} RAMB36/18 {br} == {f['RAMB36']}/{f['RAMB18']}")
    check(num(dsp) == f["DSP"], f"{run} DSP {dsp} == {f['DSP']}")
    w = re.findall(r"[-+][0-9.]+", wns)
    check(float(w[0]) == f["WNS"] and (len(w) < 2 or float(w[1]) == f["WHS"]),
          f"{run} WNS/WHS {wns} == {f['WNS']:+.3f}/{f['WHS']:+.3f}")
    m2 = re.match(r"([0-9,]+) \(([0-9]+)\) / ([0-9,]+)", nt)
    check((num(m2.group(1)), int(m2.group(2)), num(m2.group(3))) == f["notify"], f"{run} u_notify {nt} == {f['notify']}")


def d(h, b, k):
    return F[h][k] - F[b][k]


H, M = "r1b-head-6e950fea-route-1x1", "r1b-main-5c71928a-route-1x1"
Hh, Bb = "r1-head-3ab2e4da-route-1x1", "r1-base-f4167536-route-1x1"
quoted = [
    ("merge LUT", d(H, M, "LUT"), -763), ("merge FF", d(H, M, "FF"), -2031), ("merge Slice", d(H, M, "Slice"), -6),
    ("merge CARRY4", d(H, M, "CARRY4"), -150), ("merge WNS x1000", round(1000 * d(H, M, "WNS")), 195),
    ("r1 LUT", d(Hh, Bb, "LUT"), -650), ("r1 FF", d(Hh, Bb, "FF"), -1950), ("r1 Slice", d(Hh, Bb, "Slice"), -15),
    ("r1 CARRY4", d(Hh, Bb, "CARRY4"), -147), ("r1 WNS x1000", round(1000 * d(Hh, Bb, "WNS")), 27),
    ("1x1 LUT", d("r1-head-3ab2e4da-ooc-1x1", "r1-base-f4167536-ooc-1x1", "LUT"), -894),
    ("1x1 FF", d("r1-head-3ab2e4da-ooc-1x1", "r1-base-f4167536-ooc-1x1", "FF"), -2042),
    ("8x8 LUT", d("r1-head-3ab2e4da-ooc-8x8", "r1-base-f4167536-ooc-8x8", "LUT"), -925),
    ("8x8 FF", d("r1-head-3ab2e4da-ooc-8x8", "r1-base-f4167536-ooc-8x8", "FF"), -2175),
    ("u_notify merge LUT", F[H]["notify"][0] - F[M]["notify"][0], -927),
    ("u_notify merge FF", F[H]["notify"][2] - F[M]["notify"][2], -2012),
    ("image move vs r1 head LUT", F[H]["LUT"] - F[Hh]["LUT"], 581),
]
for name, got, exp in quoted:
    check(got == exp, f"delta {name}: {got:+} (quoted {exp:+})")
print(f"RESULT {'PASS' if fails == 0 else 'FAIL'} ({fails} failing)")
sys.exit(1 if fails else 0)
