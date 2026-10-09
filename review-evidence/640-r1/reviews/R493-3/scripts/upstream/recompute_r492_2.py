#!/usr/bin/env python3
"""Independent recomputation of the Mark II plan's Round 1c/1d figures from
the committed resource-gate record, plus the lever ranges the plan states.
Every derived figure is then searched for, formatted as the pages print it,
on the page(s) that state it. Usage: recompute_r492_2.py <repo>  (run -I)"""
import json, sys, math
from pathlib import Path
repo = Path(sys.argv[1])
rec = json.loads((repo / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
route, o1 = rec["route-1x1"]["record"], rec["ooc-1x1"]["record"]
plan = (repo / "docs/design/MARK_II_AREA_PLAN.md").read_text()
budget = (repo / "docs/design/AREA_BUDGET.md").read_text()
ok = bad = 0
def f(n):
    s = f"{abs(n):,}" if float(n).is_integer() else f"{abs(n):,}".rstrip("0")
    return ("-" if n < 0 else "") + s
def check(label, value, expect=None, pages=("plan", "budget"), text=None):
    global ok, bad
    if expect is not None and value != expect:
        bad += 1; print(f"MISMATCH {label}: computed {value}, expected {expect}"); return
    t = text if text is not None else f(value)
    where = [p for p in pages if t in (plan if p == "plan" else budget)]
    if len(where) == len(pages):
        ok += 1; print(f"ok   {label}: {t} on {','.join(where)}")
    else:
        bad += 1; print(f"MISS {label}: {t!r} not on {[p for p in pages if p not in where]}")
L = lambda s, k="LUT": o1["scopes"][s][k]
fig = route["figures"]
base = fig["LUT"]; check("route LUT", base, 50267)
tiles = fig["RAMB36"] + fig["RAMB18"] / 2; check("route tiles", tiles, 87.5)
check("route RAMB36/RAMB18", (fig["RAMB36"], fig["RAMB18"]), (74, 27), text="| 74 | 27 | 87.5 | 87.5 |")
# Split basis from ooc-1x1 scopes
basis = {
 "ADP": L("u_pp/u_adp"), "listener": L("u_pp/u_listener") + L("u_pp/u_lsn_admit"),
 "talker": L("u_pp/u_talker"), "originator": L("u_pp/u_originator"),
 "binding": L("u_pp/u_nvm_shadow"), "SRP": L("u_pp/u_srp"), "AECP": L("u_pp/u_aecp"),
 "notify": L("u_pp/u_notify"), "nvmport": L("u_pp/u_nvm_port") + L("u_pp/u_nvm_arb"),
 "nvm": L("u_nvm")}
print("basis", basis)
sub = sum(basis.values()); check("disjoint wrapper subtotal", sub, 17678, pages=("plan",))
check("unowned wrapper residual", L("wrapper") - sub, 5501, pages=("plan",))
gross = sub + 429; check("gross reference", gross, 18107, pages=("plan",))
c, lo, hi = gross - 3102 - 1000, gross - 3102 - 2000 - 1500, gross - 3102 - 500 + 1500
check("split central raw", c, 14005, pages=("plan",)); check("split cons raw", lo, 11505, pages=("plan",)); check("split opt raw", hi, 16005, pages=("plan",))
S = (11500, 14000, 16000)
# Lever ranges as the plan states them (lo, central, hi)
lev = {"M2": (100, 200, 400), "M5": (400, 600, 1000), "M6": (400, 600, 900), "M7": (300, 500, 700)}
named = 823 + 873; check("M8a named cells", named, 1696, pages=("plan",))
m8a = tuple(math.floor((named * share - debit) / 100) * 100 for share, debit in ((0.5, 400), (0.75, 250), (1.0, 100)))
check("M8a rounded cases", m8a, (400, 1000, 1500), text="| 1,000 | 33,367 |", pages=("plan","budget"))
for share, debit, raw in ((0.5, 400, 448), (0.75, 250, 1022), (1.0, 100, 1596)):
    check(f"M8a raw {share}", int(named * share - debit), raw, pages=("plan",))
lev["M8a"] = m8a; lev["M8b"] = (1300, 1700, 2200)
order = ["M2", "M5", "M6", "M7", "M8a", "M8b"]
for idx, name in ((0, "cons"), (1, "central"), (2, "opt")):
    i = {"cons": 0, "central": 1, "opt": 2}[name]
    img = base - S[i]; rows = [img]
    for k in order:
        img -= lev[k][i]; rows.append(img)
    print(name, "cumulative", rows)
cons_rows = [base - 11500]; cen_rows = [base - 14000]; opt_rows = [base - 16000]
for k in order:
    cons_rows.append(cons_rows[-1] - lev[k][0]); cen_rows.append(cen_rows[-1] - lev[k][1]); opt_rows.append(opt_rows[-1] - lev[k][2])
names = ["F0-F5, complete qualified flip / L2", "M2", "M5", "M6", "M7", "M8a", "M8b, conditional"]
sav = [14000] + [lev[k][1] for k in order]
for n, s_, a, b, c_ in zip(names, sav, cen_rows, cons_rows, opt_rows):
    check(f"cumulative row {n}", None, text=f"| {n} | {f(s_)} | {f(a)} | {f(b)} | {f(c_)} |", pages=("plan",))
full = (cons_rows[-1], cen_rows[-1], opt_rows[-1]); check("full split", full, (35867, 31667, 27567), text="31,667")
check("full split head 38040 central %", round((38040 - cen_rows[-1]) / 38040 * 100, 2), 16.75, pages=("plan",), text="16.75 percent")
check("full split head 38040 cons %", round((38040 - cons_rows[-1]) / 38040 * 100, 2), 5.71, pages=("plan",), text="5.71 percent")
check("without M8b cons", cons_rows[-1] + 1300, 37167)
ml = tuple(sum(lev[k][i] for k in order) for i in range(3)); check("M-lane totals", ml, (2900, 4600, 6700), text="4,600")
m310 = (1500 + 900, 2600 + 1200, 3600 + 1500); check("M3/M10 totals", m310, (2400, 3800, 5100), text="3,800")
nos = tuple(base - ml[i] - m310[i] for i in range(3)); check("no split incl", nos, (44967, 41867, 38467), text="41,867")
check("no split before M3/M10", base - ml[1], 45667)
ret = basis["AECP"] + basis["notify"] + basis["originator"] + basis["nvmport"] + basis["nvm"]
check("partial retained", ret, 10095, pages=("plan",))
prem = sub - ret + 429; check("partial removal basis", prem, 8012)
pc = (prem - 3102 - 2000 - 1500, prem - 3102 - 1000, prem - 3102 - 500 + 1500); check("partial split saving", pc, (1410, 3910, 5910), text="3,910")
par = tuple(base - pc[i] - ml[i] - m310[i] for i in range(3)); check("partial images", par, (43557, 37957, 32557), text="37,957")
check("partial central without M8b", par[1] + 1700, 39657)
for label, imgs in (("Full split", full), ("No split, including M3/M10", nos), ("Partial, F5 unqualified", par)):
    for case, v in zip(("Conservative", "Central", "Optimistic"), imgs):
        h1, h2 = 38040 - v, 37659 - v
        sg = lambda h: ("+" if h >= 0 else "-") + f"{abs(h):,}"
        check(f"scenario {label} {case}", None, text=f"| {label} | {case} | {f(v)} | {sg(h1)} | {sg(h2)} |")
# M3 basis
m3 = 0.6 * L("u_pp/u_notify") + 0.7 * (L("u_pp/u_aecp/u_d3") + L("u_pp/u_aecp/u_dyn")) \
     + 0.5 * (L("u_pp/u_aecp") - sum(L(f"u_pp/u_aecp/{c}") for c in ("u_d3", "u_dyn", "u_store", "u_ucpu", "u_resp"))) \
     + 0.4 * L("u_pp/u_dispatch/u_aecp_q")
print(f"M3 displaced {m3:.1f}; own logic {L('u_pp/u_aecp') - sum(L(f'u_pp/u_aecp/{c}') for c in ('u_d3','u_dyn','u_store','u_ucpu','u_resp'))}; aecp_q {L('u_pp/u_dispatch/u_aecp_q')}")
check("M3 displaced ~3,380", round(m3, -1), 3380, pages=("plan",), text="3,380")
check("M3 net near 2,600", round(m3 - 1000 + 200, -2), 2600, pages=("plan",), text="2,600")
# Memory ledger
sc = route["scopes"]
aecp_t = sc["u_pp/u_aecp"]["RAMB36"] + sc["u_pp/u_aecp"]["RAMB18"] / 2
srp_t = sc["u_pp/u_srp"]["RAMB36"] + sc["u_pp/u_srp"]["RAMB18"] / 2
wr_t = sc["wrapper"]["RAMB36"] + sc["wrapper"]["RAMB18"] / 2
rel = ["u_pp/g_rx_pool[0].u_rx_slots", "u_pp/g_rx_pool[1].u_rx_slots", "u_pp/g_rx_pool[2].u_rx_slots",
       "u_pp/g_rx_pool[4].u_rx_slots", "u_pp/g_rx_pool[5].u_rx_slots", "u_pp/u_mrp_strip", "u_pp/u_tx_slots",
       "u_pp/u_timer", "u_pp/u_trace", "u_pp/u_rx_validator", "ctl_fifo"]
r36 = sum(sc[s]["RAMB36"] for s in rel); r18 = sum(sc[s]["RAMB18"] for s in rel)
check("credited removals AECP+SRP", aecp_t + srp_t, 6.5, text="| -6 | -1 | -6.5 | 81 |")
check("release scopes RAMB36/RAMB18", (r36, r18), (10, 2), pages=("plan",), text="| Total | 10 | 2 | 11 |")
part = sc["wrapper"]["RAMB36"] - sc["u_pp/u_aecp"]["RAMB36"] - sc["u_pp/u_srp"]["RAMB36"] - r36, \
       sc["wrapper"]["RAMB18"] - sc["u_pp/u_aecp"]["RAMB18"] - sc["u_pp/u_srp"]["RAMB18"] - r18
check("wrapper partition complete (residual RAMB36,RAMB18)", part, (0, 0), text="")
mbx = 1 + 10 / 2; bios = 18 + 1 / 2
led = tiles - (aecp_t + srp_t) + mbx - bios + 50 + 2
check("ledger total", led, 120.5, text="`87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5`")
check("after conditional release", led - (r36 + r18 / 2), 109.5, text="109.5")
check("headroom before release", 121.5 - led, 1.0, text="")
check("no-reuse totals", (led + bios, led - 11 + bios), (139.0, 128.0), text="139 and 128")
check("56-tile conditional", led - 11 + 6, 115.5, text="115.5")
check("partial 50-tile hold", led + aecp_t, 126.5, text="126.5")
check("reserve and ceiling", (round(135 * 0.1, 1), 135 - 13.5), (13.5, 121.5), text="121.5")
check("preflight section sum", 56948 + 3458 + 0 + 78744 + 8192, 147342, pages=("plan",), text="147,342")
check("preflight alignment", 147360 - 147342, 18, pages=("plan",), text="adds 18")
check("224 KiB at 4 KiB", math.ceil(224 * 1024 / 4096), 56, text="56 tiles")
print(f"info: 50 tiles x 4,096 B = {50*4096:,} B usable at 32-bit width; x 4,608 B raw = {50*4608:,} B; 224 KB = {224*1000:,} B / 224 KiB = {224*1024:,} B")
print(f"info: largest preflight 147,360 B needs {math.ceil(147360/4096)} tiles at 4 KiB; shipping 94,688 B needs {math.ceil(94688/4096)}")
print(f"RESULT ok={ok} bad={bad}")
sys.exit(1 if bad else 0)
