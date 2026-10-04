#!/usr/bin/env python3
"""[R453-2] Independent re-derivation of the #232 lane's Vivado figures.

Usage: vivado_check.py VIVADO_DIR [PUBLISHED_MANIFEST_JSON]

VIVADO_DIR is review-evidence/pp232-r1/author-r2/evidence-r2/vivado of the
public evidence branch. This script does not import or reuse the packet's own
tools; it parses the reports with its own code and prints PASS/FAIL per check.

Checks:
  * every whole report's sha256 equals its raw record in sources.tsv
    (redacted files are checked against MANIFEST.json's original_sha256);
  * every log-extract's baseline.log record equals the README run table;
  * route head - main: LUT, FF, logic/memory LUT, slices, CARRY4;
  * u_notify / u_resp / u_d3 hierarchy rows;
  * WNS/WHS of the head route and each signoff corner;
  * Synth 8-7186 line count in each log extract (actual diagnostic lines);
  * index RAM mapping rows and census RAM cell counts.
"""
import hashlib, json, re, sys
from pathlib import Path

V = Path(sys.argv[1])
MAN = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
orig = {e["file"].split("evidence-r2/vivado/")[-1]: e["original_sha256"]
        for e in MAN if "evidence-r2/vivado/" in e["file"]}
fails = 0


def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails += 1


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def util(run, label):
    t = (V / run / "baseline_utilization.rpt").read_text()
    for line in t.splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 3 and c[1].rstrip("*").strip() == label:
            return int(float(c[2]))
    raise KeyError(label)


def hrow(run, inst):
    t = (V / run / "baseline_hierarchy.rpt").read_text()
    hdr = None
    for line in t.splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) > 5 and c[1] == "Instance":
            hdr = c
        if hdr and len(c) == len(hdr) and c[1] == inst:
            d = dict(zip(hdr, c))
            return int(d["Total LUTs"]), int(d["LUTRAMs"]), int(d["FFs"])
    raise KeyError(inst)


runs = sorted(p.name for p in V.iterdir() if (p / "sources.tsv").exists())
readme = (V / "README.md").read_text()
for r in runs:
    src = {}
    for line in (V / r / "sources.tsv").read_text().splitlines()[1:]:
        n, b, h = line.split("\t")
        src[n] = (int(b), h)
    for f in sorted((V / r).iterdir()):
        if f.name in src:
            exp = src[f.name][1]
            got = orig.get(f"{r}/{f.name}", sha(f))
            how = "original (path-redacted in publication)" if f"{r}/{f.name}" in orig else "published"
            check(got == exp, f"{r}/{f.name} {how} sha256 == sources.tsv raw record")
    lb, lh = src["baseline.log"]
    m = re.search(r"\|\s*`" + re.escape(r) + r"`\s*\|.*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|", readme)
    check(m and int(m.group(1)) == lb and m.group(2) == lh, f"{r} baseline.log record == README run table ({lb} B, {lh[:16]})")
    le = (V / r / "log-extract.txt").read_text()
    n7186 = sum(1 for l in le.splitlines() if re.match(r"^baseline\.log:\d+: (WARNING|INFO|CRITICAL WARNING): \[Synth 8-7186\]", l))
    hdr = int(re.search(r"^## Synth 8-7186: (\d+)", le, re.M).group(1))
    print(f"INFO {r}: Synth 8-7186 diagnostic lines counted = {n7186}, header says {hdr}")
    check(n7186 == hdr, f"{r} Synth 8-7186 count consistent")
    if "head" in r:
        check(n7186 == 0, f"{r} zero Synth 8-7186")

H, M = "r1b-head-6e950fea-route-1x1", "r1b-main-5c71928a-route-1x1"
for lab, exp in (("Slice LUTs", -763), ("Slice Registers", -2031), ("LUT as Logic", -1625),
                 ("LUT as Memory", 862), ("Slice", -6), ("CARRY4", -150)):
    try:
        d = util(H, lab) - util(M, lab)
    except KeyError:
        # CARRY4 is in the primitives table
        def prim(run, p):
            t = (V / run / "baseline_utilization.rpt").read_text()
            return int(re.search(r"^\|\s*" + p + r"\s*\|\s*(\d+)", t, re.M).group(1))
        d = prim(H, lab) - prim(M, lab)
    check(d == exp, f"route head-main {lab}: {d:+} (quoted {exp:+})")
print("INFO route LUT head/main", util(H, "Slice LUTs"), util(M, "Slice LUTs"),
      "FF", util(H, "Slice Registers"), util(M, "Slice Registers"))
for inst, exp in (("u_notify", (-927, None, -2012)), ("u_resp", (0, None, 0)), ("u_d3", (34, None, 0))):
    h, m = hrow(H, inst), hrow(M, inst)
    print(f"INFO {inst} head {h} main {m}")
    check(h[0] - m[0] == exp[0] and h[2] - m[2] == exp[2], f"{inst} delta LUT {h[0]-m[0]:+} FF {h[2]-m[2]:+}")
check(hrow(H, "u_notify")[1] == 960, "u_notify LUTRAM 960 at head")
for r in runs:
    check(hrow(r, "u_resp")[2] == 260, f"{r} u_resp 260 FF")

te = (V / H / "timing-extract.txt").read_text()
blocks = re.split(r"^##\s+", te, flags=re.M)
seen = {}
for b in blocks:
    name = b.split("\n", 1)[0].strip()
    m = re.search(r"-------\s+-------.*\n\s+(-?[0-9.]+)\s+\S+\s+\S+\s+\S+\s+(-?[0-9.]+)", b)
    if m and "Design Timing Summary" in b:
        seen[name] = (float(m.group(1)), float(m.group(2)))
for k, v in seen.items():
    print(f"INFO {H} {k}: WNS {v[0]:+.3f} WHS {v[1]:+.3f}")
first = next(iter(seen.values()))
check(first == (0.274, 0.023), "head baseline_timing WNS +0.274 / WHS +0.023")
mt = (V / M / "timing-extract.txt").read_text()
m = re.search(r"-------\s+-------.*\n\s+(-?[0-9.]+)\s+\S+\s+\S+\s+\S+\s+(-?[0-9.]+)", mt)
check((float(m.group(1)), float(m.group(2))) == (0.079, 0.014), "main baseline_timing WNS +0.079 / WHS +0.014")
corners = {k: v for k, v in seen.items() if "signoff_" in k}
check(len(corners) == 4 and all(v[0] > 0 and v[1] > 0 for v in corners.values()), "four signoff corners, all positive")
for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C"):
    t = (V / H / f"alinx_ax7101_signoff_{c}_negative.rpt").read_text()
    check("No timing paths found" in t, f"{c} negative-slack report empty")
rs = (V / H / "alinx_ax7101_route_status.rpt").read_text()
check(re.search(r"nets with routing errors\.*\s*:\s*0\b", rs) is not None, "head route: 0 nets with routing errors")

le = (V / H / "log-extract.txt").read_text()
ix64 = len(re.findall(r"g_ix_chunk\[\d+\]\.mem_r_reg\s*\|[^|]*\|\s*64 x 1\s*\|\s*RAM64M x 1", le))
ix16 = len(re.findall(r"g_ix_chunk\[18\]\.mem_r_reg\s*\|[^|]*\|\s*16 x 1\s*\|\s*RAM16X1D x 1", le))
rows = re.search(r"rows_r_reg\s*\|[^|]*\|\s*16 x 128\s*\|\s*RAM32M x 64", le)
check(ix64 == 288 and ix16 == 16 and rows is not None, f"mapping report: index 64x1 rows {ix64}, 16x1 rows {ix16}, rows_r RAM32M x 64")
cen = {}
for line in (V / H / "census.tsv").read_text().splitlines()[1:]:
    s, p, n = line.split("\t")
    cen[(s, p)] = int(n)
check((cen.get(("u_notify", "RAM32M")), cen.get(("u_notify", "RAM64X1D")), cen.get(("u_notify", "RAM32X1D"))) == (88, 288, 16),
      "census u_notify RAM32M 88, RAM64X1D 288, RAM32X1D 16")
check(88 * 4 + 288 * 2 + 16 * 2 == 960, "88x4 + 288x2 + 16x2 = 960 LUTRAM")
print(f"RESULT {'PASS' if fails == 0 else 'FAIL'} ({fails} failing)")
sys.exit(1 if fails else 0)
