#!/usr/bin/env python3
"""Compare the committed SoC extract, the page and the memory-map SVG with the published export.
Usage: soc_crosscheck.py <repo-root> <export-dir>"""
import json, re, sys
root, exp = sys.argv[1], sys.argv[2]
soc = json.load(open(f"{root}/scripts/register_map_soc.json"))
aem = json.load(open(f"{exp}/aem_desc.json"))
rows = [l.split(",") for l in open(f"{exp}/csr.csv").read().splitlines() if l and not l.startswith("#")]
regions = {r[1]: (int(r[2], 16), int(r[3])) for r in rows if r[0] == "memory_region"}
banks = {r[1]: int(r[2], 16) for r in rows if r[0] == "csr_base"}
regs = {r[1]: (int(r[2], 16), int(r[3]), r[4]) for r in rows if r[0] == "csr_register"}
consts = {r[1]: r[2] for r in rows if r[0] == "constant"}
bad = 0
def check(name, a, b):
    global bad
    if a != b:
        bad += 1
        print("DIFF", name, a, b)
check("regions", regions, {r["name"]: (r["origin"], r["size"]) for r in soc["memory_regions"]})
check("banks", banks, {r["name"]: r["origin"] for r in soc["csr_banks"]})
check("regs", regs, {r["name"]: (r["address"], r["words"], r["mode"]) for r in soc["csr_registers"]})
for k, v in soc["constants"].items():
    check("const " + k, str(v), consts.get(k))
for k, v in soc["pp_windows"].items():
    check("window " + k, v, aem[k])
print("extract vs export: regions", len(regions), "banks", len(banks), "registers", len(regs), "constants", len(soc["constants"]), "differences", bad)
page = open(f"{root}/docs/reference/REGISTER_MAP.md", encoding="utf-8").read()
svg = open(f"{root}/docs/diagrams/memory_map.svg", encoding="utf-8").read()
drawio = open(f"{root}/docs/diagrams/memory_map.drawio", encoding="utf-8").read()
miss = 0
for name, (o, s) in regions.items():
    span = f"0x{o:08X} - 0x{o + s - 1:08X}"
    row = f"| `{name}` | `0x{o:08X}` | `0x{o + s - 1:08X}` | {s:,}"
    for tag, ok in (("page", row in page), ("svg", span in svg), ("drawio", span in drawio)):
        if not ok:
            miss += 1
            print("MISSING", tag, name, span)
names = sorted(banks, key=banks.get)
step = min(b - a for a, b in zip(sorted(banks.values()), sorted(banks.values())[1:]))
for name in names:
    o = banks[name]
    row = f"| `{name}` | `0x{o:08X}` | `0x{o + step - 1:08X}` |"
    label = f"LiteX CSR bank {name}"
    for tag, ok in (("page", row in page), ("svg", label in svg and f"0x{o:08X} - 0x{o + step - 1:08X}" in svg), ("drawio", label in drawio)):
        if not ok:
            miss += 1
            print("MISSING", tag, name)
pg = re.findall(r"^\| `(0x[0-9A-F]{8})` \| `(\w+)` \| (\d+) \| (\w+) \|", page, re.M)
for addr, name, words, mode in pg:
    a, w, m = regs[name]
    if int(addr, 16) != a or int(words) != w or mode != m.upper():
        miss += 1
        print("PAGE-REG DIFF", name, addr, words, mode, regs[name])
print("page/svg/drawio cross-check: regions", len(regions), "banks", len(banks), "page CSR rows", len(pg), "missing or different", miss)
print("phy_crg", [k for k in regs if "phy_crg" in k], "link_status", [k for k in regs if "link_status" in k])
