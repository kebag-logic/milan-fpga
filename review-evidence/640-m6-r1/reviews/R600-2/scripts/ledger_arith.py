#!/usr/bin/env python3
"""Recompute the Mark II ledger figures in the composed tree from their rows.

usage: python3 -I ledger_arith.py <checkout>

Reads docs/design/MARK_II_AREA_PLAN.md, docs/design/AREA_BUDGET.md and
syn/ooc/pp_resource_baseline.json as data only. Prints one line per check and
exits 1 if any check fails.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PLAN = (ROOT / "docs/design/MARK_II_AREA_PLAN.md").read_text()
BUDGET = (ROOT / "docs/design/AREA_BUDGET.md").read_text()
RECORD = json.loads((ROOT / "syn/ooc/pp_resource_baseline.json").read_text())
fails = 0


def check(name, ok, detail=""):
    global fails
    fails += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


def num(s):
    s = s.strip().strip("*").replace(",", "").replace("+", "")
    return float(s)


def table_after(text, heading_regex, first_col_regex):
    """Rows (as cell lists) of the first table after a heading match."""
    m = re.search(heading_regex, text, re.M)
    assert m, heading_regex
    rows = []
    started = False
    for line in text[m.end():].splitlines():
        if line.startswith("|"):
            started = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if re.match(first_col_regex, cells[0]):
                rows.append(cells)
        elif started:
            break
    return rows


def section(text, heading):
    m = re.search(rf"^### {re.escape(heading)}\n", text, re.M)
    assert m, heading
    end = re.search(r"^##+ ", text[m.end():], re.M)
    return text[m.end(): m.end() + (end.start() if end else len(text))]


# 1. Intermediate measurements: base row equals the route-1x1 record; delta rows recomputed.
rec = None
for key, val in RECORD.items():
    if isinstance(val, dict) and "route-1x1" in val:
        rec = val["route-1x1"]
if rec is None:
    rec = RECORD.get("endpoints", {}).get("route-1x1")
print("route-1x1 record keys:", sorted(rec.keys()) if isinstance(rec, dict) else rec)

for lane, rowname in (("M2", "M2 route"), ("M6", "M6 route")):
    sec = section(PLAN, f"{lane} intermediate measurement")
    rows = {r[0].split(" at ")[0].strip(): r for r in table_after(sec, r"^\| Measurement", r"^(Base|M\d|Routed|Post)")}
    base, cand, delta = rows["Base route"], rows[rowname], rows["Routed delta"]
    for i, col in ((1, "LUT"), (2, "FF"), (3, "Slices")):
        d = num(cand[i]) - num(base[i])
        check(f"{lane} routed delta {col}", d == num(delta[i]), f"{cand[i]} - {base[i]} = {d:+.0f}, row says {delta[i]}")
    b36, b18 = (num(x) for x in base[4].split("/"))
    c36, c18 = (num(x) for x in cand[4].split("/"))
    check(f"{lane} RAMB delta", delta[4].replace(" ", "") == f"{int(c36 - b36)}/{int(c18 - b18)}", f"row says {delta[4]}")
    bw, bh = (num(x) for x in base[5].split("/"))
    cw, ch = (num(x) for x in cand[5].split("/"))
    dw, dh = (num(x) for x in delta[5].split("/"))
    check(f"{lane} WNS/WHS delta", round(cw - bw, 3) == dw and round(ch - bh, 3) == dh, f"{cw - bw:+.3f}/{ch - bh:+.3f} vs {delta[5]}")
    check(f"{lane} base row = plan's other lane base row", base[1:] == table_after(section(PLAN, "M2 intermediate measurement"), r"^\| Measurement", r"^Base")[0][1:])
    check(f"{lane} base row LUT = route-1x1 headline 50,267 in AREA_BUDGET", "| `route-1x1` | 50,267 | 54,413 | 74 / 27 |" in BUDGET)
    fig = rec["record"]["figures"]
    check(f"{lane} base row = gate record figures",
          (num(base[1]), num(base[2]), num(base[3]), b36 + b18 / 2) == (fig["LUT"], fig["FF"], fig["SLICE"], fig["BRAM_TILE"]),
          f"record LUT {fig['LUT']} FF {fig['FF']} SLICE {fig['SLICE']} tiles {fig['BRAM_TILE']}")

# M6 per-block credits sum to the stated reproducible saving.
sec = section(PLAN, "M6 intermediate measurement")
blocks = table_after(sec, r"^\| Block", r"^(Listener|Channel|Talker|Render)")
changed = [r for r in blocks if "RTL unchanged" not in r[0]]


def drop(cell):
    a, b = (num(x) for x in cell.split("->"))
    return a - b


routed = sum(drop(r[1]) for r in changed)
synth = sum(drop(r[2]) for r in changed)
ff = sum(drop(r[3]) for r in changed)
check("M6 credited routed saving = 468", routed == 468, f"{routed:.0f}")
check("M6 credited post-synthesis saving = 418", synth == 418, f"{synth:.0f}")
check("M6 credited FF saving = 839 (REVIEW READY)", ff == 839, f"{ff:.0f}")
check("M6 text states 418 post-synthesis, 468 routed", "The reproducible saving is 418 LUTs post-synthesis, 468 routed." in sec)
check("AREA_BUDGET M6 note agrees", "M6 has measured its lane: 418 LUTs post-synthesis, 468 routed in its blocks, no block-RAM growth." in BUDGET)
sec2 = section(PLAN, "M2 intermediate measurement")
m2rows = {r[0]: r for r in table_after(sec2, r"^\| Measurement", r"^(Routed|Post)")}
check("M2 reproducible 34 = post-synthesis delta row", num(m2rows["Post-synthesis delta, same runs"][1]) == -34 and "The reproducible saving is 34 LUTs" in sec2)
check("M2 routed 128 = routed delta row", num(m2rows["Routed delta"][1]) == -128)
check("AREA_BUDGET M2 note agrees", "M2 has measured its lane: 34 LUTs post-synthesis, 128 routed, no block-RAM growth." in BUDGET)

# 2. Disjointness: M2 credits SoC crossings only, M6 credits two hdl/ieee1722 blocks only.
check("M2 section credits no M6 block", not re.search(r"monitor|channel-map|chan_map", sec2, re.I))
check("M6 section credits no M2 array", not re.search(r"MAC crossing|CSR (W|R|FIFO)|RAMB18s", sec, re.I))
check("L9 states no M2 overlap", "No M2 table credit overlaps these arrays." in PLAN)

# 3. Cumulative default-image table: each row = previous - saving (central).
rows = table_after(PLAN, r"^### Cumulative default-image estimates", r"^\d")
prev = None
for r in rows:
    if r[1] == "Recorded baseline":
        prev = [num(x) for x in r[3:6]]
        check("cumulative baseline = 50,267", prev == [50267] * 3)
        continue
    if r[2].startswith("No assumed"):
        continue
    cur = [num(x) for x in r[3:6]]
    s = num(r[2])
    check(f"cumulative central row {r[0]} {r[1]}", cur[0] == prev[0] - s, f"{prev[0]:.0f}-{s:.0f}={prev[0]-s:.0f} vs {cur[0]:.0f}")
    prev = cur
check("cumulative M2 row keeps planning 200", any(r[1] == "M2" and r[2] == "200" for r in rows))
check("cumulative M6 row keeps planning 600", any(r[1] == "M6" and r[2] == "600" for r in rows))
check("central headroom 38,040-31,667=6,373", 38040 - 31667 == 6373 and "Central headroom below 38,040 is 6,373 LUTs." in PLAN)
check("conservative headroom 38,040-35,867=2,173", 38040 - 35867 == 2173 and "The conservative estimate leaves 2,173" in PLAN)

# 4. AREA_BUDGET lane table: image after = previous - saving.
rows = table_after(BUDGET, r"^\| Lane \| Estimated saving", r"^(F0|M\d)")
img = 50267
for r in rows:
    if not re.match(r"^[\d,]+$", r[1]):
        continue
    img -= num(r[1])
    check(f"AREA_BUDGET lane row {r[0]}", img == num(r[2]), f"{img:.0f} vs {r[2]}")

# 5. Block-RAM ledger in both documents: running tile totals.
for name, text in (("plan", PLAN), ("budget", BUDGET)):
    rows = table_after(text, r"^\| Item \| RAMB36 delta", r"^(Recorded|L2|Measured|M8a|Total|M2|Conditional)")
    tiles = None
    for r in rows:
        t = num(r[1]) + num(r[2]) / 2
        check(f"{name} BRAM row tile delta {r[0][:30]}", t == num(r[3]), f"{t} vs {r[3]}")
        tiles = t if tiles is None else tiles + t
        check(f"{name} BRAM running total {r[0][:30]}", tiles == num(r[4]), f"{tiles} vs {r[4]}")
    check(f"{name} M2 +2 allowance row retained", any(r[0] == "M2 maximum additional allocation" for r in rows))

print(f"{fails} failure(s)")
sys.exit(1 if fails else 0)
