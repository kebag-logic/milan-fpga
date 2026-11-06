#!/usr/bin/env python3
"""Read every published measurement report through the gate's parsers and compare with the record and the prose.

usage: report_audit.py <clone> <author-r3 dir>
"""
import json, re, sys
from pathlib import Path
clone, base = Path(sys.argv[1]), Path(sys.argv[2])
sys.dont_write_bytecode = True
sys.path.insert(0, str(clone / "syn/ooc"))
import pp_resource_gate as g
from pp_baseline_rank import hierarchy
n = json.loads((clone / "syn/ooc/pp_resource_baseline.json").read_text())["endpoints"]
r3 = base / "a738c/receipts/gate"
sets = [("route-1x1", "route", r3 / "route", "route-1x1-ETO-", True), ("route EPPO", "route", r3 / "route", "route-1x1-EPPO-", False),
        ("route ASLH", "route", r3 / "route", "route-1x1-ASLH-", False), ("ooc-1x1", "ooc", r3 / "ooc", "ooc-1x1-", True),
        ("ooc-8x8", "ooc", base / "a738d/receipts/gate/ooc8", "ooc-8x8-", True)]
for name, kind, folder, prefix, recorded in sets:
    util = (folder / f"{prefix}baseline_utilization.rpt").read_text()
    got = g.utilization(util, kind)
    t = (folder / f"{prefix}timing-design-tables.txt").read_text()
    sec = re.search(r"== baseline_timing\.rpt\n(.*?)(?:\n==|\Z)", t, re.S)
    print(name, got, "| baseline_timing row:", sec.group(1).splitlines()[-1].split()[:5] if sec else "no section")
    rows = hierarchy(folder / f"{prefix}baseline_hierarchy.rpt")
    if recorded:
        rec = n[name]["record"]
        print("  mismatch vs record:", {k: (v, rec["figures"].get(k)) for k, v in got.items() if rec["figures"].get(k) != v})
        root = g.ROOTS[kind]
        order = []
        for key, c in rows.items():
            inside = key == root or key.startswith(root + "/")
            if inside and not key.endswith("/@own") and key.count("/") <= root.count("/") + 3:
                rel = key.removeprefix(root).lstrip("/") or "wrapper"
                order.append(rel)
                held = rec["scopes"].get(rel)
                if held is None or any(held[f] != c[f] for f in ("LUT", "FF", "RAMB36", "RAMB18", "DSP")):
                    print("  scope mismatch", rel)
        print("  scopes", len(order), "record", len(rec["scopes"]), "same key order as the report:", order == list(rec["scopes"]))
    if name == "route-1x1":
        hits = {k: v for k, v in rows.items() if k.endswith("KL_maap") or "maap" in k.rsplit("/", 1)[-1].lower()}
        print("  maap rows", {k: (v["LUT"], v["FF"]) for k, v in hits.items() if k.count("/") <= 3})
    print("  log rc", (folder / f"{prefix}baseline.log.rc").read_text().strip())
