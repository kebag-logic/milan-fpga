#!/usr/bin/env python3
"""Cross-check the #843 round-2 author evidence tree.

Usage: check_evidence.py <author-r2 dir>

1. Every row of receipts/INDEX.md: file present, byte count and sha256 prefix.
2. Every route run (route-head/, route-dev/ x eppo/aslh/eto): LUT, FF, slice,
   RAMB36/18, DSP from <run>-utilization_place.rpt and per-corner WNS/WHS from
   <run>-timing-design-tables.txt, routing errors from <run>-route_status.rpt,
   compared with receipts/route-figures.json.
3. Floors: WNS >= +0.030 ns and WHS >= 0 ns at every corner of every run.
4. Best of three per commit = highest worst-corner WNS.
"""
import hashlib, json, os, re, sys

root = sys.argv[1]
rc = 0

def bad(msg):
    global rc
    rc = 1
    print("BAD", msg)

# 1. index
idx = open(os.path.join(root, "receipts/INDEX.md")).read()
rows = re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{16})` \|$", idx, re.M)
ok = 0
for path, size, pref in rows:
    p = os.path.join(root, path)
    if not os.path.exists(p):
        bad(f"index row missing on disk: {path}")
        continue
    b = open(p, "rb").read()
    if len(b) != int(size) or hashlib.sha256(b).hexdigest()[:16] != pref:
        if path == "receipts/INDEX.md":
            continue
        bad(f"index mismatch: {path}")
        continue
    ok += 1
print(f"index: {len(rows)} rows, {ok} match")
listed = {r[0] for r in rows}
for d, _, fs in os.walk(root):
    for f in fs:
        rel = os.path.relpath(os.path.join(d, f), root)
        if rel not in listed:
            print("unlisted on disk:", rel)

# 2. route runs
fig = json.load(open(os.path.join(root, "receipts/route-figures.json")))
RUNS = {"eppo": "ExtraPostPlacementOpt", "aslh": "AltSpreadLogic_high",
        "eto": "ExtraTimingOpt"}

def util(path):
    t = open(path).read()
    def g(label):
        m = re.search(r"^\| " + re.escape(label) + r"\s*\|\s*([0-9.]+)\s*\|", t, re.M)
        return float(m.group(1)) if m else None
    return {"LUT": g("Slice LUTs"), "FF": g("Slice Registers"),
            "SLICE": g("Slice"), "RAMB36": g("RAMB36E1"),
            "RAMB18": g("RAMB18E1"), "DSP": g("DSPs")}

def corners(path):
    t = open(path).read()
    out = {}
    for name, body in re.findall(r"^== alinx_ax7101_signoff_(\w+?)_timing\.rpt\n(.*?)(?=^== |\Z)",
                                 t, re.M | re.S):
        if name in ("all", "check"):
            continue
        nums = re.search(r"^\s+(-?[0-9.]+)\s+-?[0-9.]+\s+\d+\s+\d+\s+(-?[0-9.]+)", body, re.M)
        out[name] = [float(nums.group(1)), float(nums.group(2))]
    return out

for side, d in (("head", "route-head"), ("dev", "route-dev")):
    best = None
    for short, full in RUNS.items():
        base = os.path.join(root, "receipts", d, short)
        u = util(base + "-utilization_place.rpt")
        c = corners(base + "-timing-design-tables.txt")
        rs = open(base + "-route_status.rpt").read()
        err = int(re.search(r"nets with routing errors\.+ :\s+(\d+)", rs).group(1))
        j = fig[side][full]
        for k in ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "DSP"):
            if u[k] != j[k]:
                bad(f"{side} {full} {k}: report {u[k]} json {j[k]}")
        if set(c) != set(j["corners"]) or any(
                abs(c[k][i] - j["corners"][k][i]) > 1e-9 for k in c for i in (0, 1)):
            bad(f"{side} {full} corners: report {c} json {j['corners']}")
        wns = min(v[0] for v in c.values()); whs = min(v[1] for v in c.values())
        if err:
            bad(f"{side} {full}: {err} routing errors")
        for k, (s, h) in c.items():
            if s < 0.030 - 1e-9 or h < 0.0:
                bad(f"{side} {full} {k}: WNS {s} WHS {h} under the floor")
        print(f"{side:4} {full:22} LUT {u['LUT']:.0f} FF {u['FF']:.0f} slice {u['SLICE']:.0f} "
              f"free {15850 - u['SLICE']:.0f} RAM {u['RAMB36']:.0f}/{u['RAMB18']:.0f} DSP {u['DSP']:.0f} "
              f"WNS {wns:+.3f} WHS {whs:+.3f} errors {err}")
        if best is None or wns > best[1]:
            best = (full, wns, u, c)
    print(f"{side} best: {best[0]} WNS {best[1]:+.3f}")
    fig[side]["_best"] = best

h, dv = fig["head"]["_best"], fig["dev"]["_best"]
for k in ("LUT", "FF", "SLICE", "DSP"):
    print(f"best-vs-best {k}: {h[2][k] - dv[2][k]:+.0f}")
for grp in (("Slow_0C", "Slow_85C"), ("Fast_0C", "Fast_85C")):
    hs = min(h[3][g][0] for g in grp); ds = min(dv[3][g][0] for g in grp)
    hh = min(h[3][g][1] for g in grp); dh = min(dv[3][g][1] for g in grp)
    print(f"best-vs-best {grp[0][:4]}: WNS {ds:+.3f} -> {hs:+.3f} ({hs - ds:+.3f}); "
          f"WHS {dh:+.3f} -> {hh:+.3f} ({hh - dh:+.3f})")
print("RESULT", "PASS" if rc == 0 else "FAIL")
sys.exit(rc)
