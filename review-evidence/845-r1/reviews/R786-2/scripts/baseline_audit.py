#!/usr/bin/env python3
"""Audit the thirteenth record against the twelfth and the published gate reports.

usage: baseline_audit.py <clone> <author-r3 a738d receipts dir> <old-rev> <new-rev>
"""
import json, re, subprocess, sys
from pathlib import Path
clone, receipts, old, new = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(clone / "syn/ooc"))
sys.dont_write_bytecode = True
import pp_resource_gate as g
from pp_baseline_rank import hierarchy

def show(rev):
    return subprocess.run(["git", "-C", str(clone), "show", f"{rev}:syn/ooc/pp_resource_baseline.json"],
                          check=True, capture_output=True, text=True).stdout
ot, nt = show(old), show(new)
o, n = json.loads(ot), json.loads(nt)

print("== byte form: gate writer form equals file")
src = (clone / "syn/ooc/pp_resource_gate.py").read_text()
m = re.search(r"text = (json\.dumps\(.*)", src)
print("writer:", m.group(1) if m else "not found")
print("file equals the writer form:", json.dumps(n, indent=1) + "\n" == nt)

print("== non-record fields")
for k in n:
    if k != "endpoints" and n[k] != o[k]:
        print("FILE FIELD CHANGED", k)
print("endpoints", list(o["endpoints"]), list(n["endpoints"]))
for name, ne in n["endpoints"].items():
    oe = o["endpoints"][name]
    for k in sorted(set(ne) | set(oe)):
        if k != "record" and ne.get(k) != oe.get(k):
            print(f"{name}: {k} changed")
            if k == "measured":
                print("  old:", oe.get(k)); print("  new:", ne.get(k))
    orr, nr = oe["record"], ne["record"]
    idn = {k: (orr["identity"][k], nr["identity"][k]) for k in nr["identity"] if orr["identity"][k] != nr["identity"][k]}
    for k, (a, b) in idn.items():
        if isinstance(a, list):
            print(f"{name}: identity.{k} lines changed:", [x for x in a if x not in b], "->", [x for x in b if x not in a])
        else:
            print(f"{name}: identity.{k}: {a} -> {b}")
    print(f"{name}: inputs {orr['inputs_sha256'][:16]} -> {nr['inputs_sha256']}")
    print(f"{name}: figures", {k: (orr['figures'][k], nr['figures'][k], round(nr['figures'][k] - orr['figures'][k], 3)) for k in nr['figures']})
    print(f"{name}: scope keys added {sorted(set(nr['scopes']) - set(orr['scopes']))} removed {sorted(set(orr['scopes']) - set(nr['scopes']))}")

print("== records reproduced from published reports through the gate's own parsers")
sets = {"route-1x1": ("route", receipts / "gate/route-selected", "route-1x1-ETO-"),
        "ooc-8x8": ("ooc", receipts / "gate/ooc8", "ooc-8x8-")}
for name, (kind, folder, prefix) in sets.items():
    rec = n["endpoints"][name]["record"]
    util = (folder / f"{prefix}baseline_utilization.rpt").read_text()
    got = g.utilization(util, kind)
    bad = {k: (v, rec["figures"].get(k)) for k, v in got.items() if rec["figures"].get(k) != v}
    print(name, "utilization figures", len(got), "mismatch", bad)
    print(name, "report identity", g.header(util, "Tool Version"), "|", g.header(util, "Device"), "|", g.header(util, "Design"), "|", g.header(util, "Design State"), "| record", rec["identity"]["tool"], rec["identity"]["device"], rec["identity"]["design"], rec["identity"]["state"])
    rows = hierarchy(folder / f"{prefix}baseline_hierarchy.rpt")
    root = g.ROOTS[kind]
    mism = total = 0
    seen = set()
    for key, counts in rows.items():
        inside = key == root or key.startswith(root + "/")
        if inside and not key.endswith("/@own") and key.count("/") <= root.count("/") + 3:
            rel = key.removeprefix(root).lstrip("/") or "wrapper"
            seen.add(rel)
            total += 1
            held = rec["scopes"].get(rel)
            if held is None or any(held[f] != counts[f] for f in ("LUT", "FF", "RAMB36", "RAMB18", "DSP")):
                mism += 1
                print("  scope mismatch", rel, held, counts)
    print(name, "scopes from report", total, "mismatch", mism, "record scopes not in report", sorted(set(rec["scopes"]) - seen)[:5])
    if kind == "route":
        for wanted in ("alinx_ax7101/milan_datapath", "alinx_ax7101/milan_datapath/pp_shadow"):
            print("  ", wanted, {f: rows[wanted][f] for f in ("LUT", "FF")} if wanted in rows else "absent")
