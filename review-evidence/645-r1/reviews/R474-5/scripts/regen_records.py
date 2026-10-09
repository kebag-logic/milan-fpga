#!/usr/bin/env python3
"""Regenerate the three resource-gate records from the published round-2f receipts.

Usage: python3 -I regen_records.py <clone> <receipts-dir> <out-json>

Uses the gate's own parsers from <clone>/syn/ooc/pp_resource_gate.py on the
retained reports.  Every field the receipts carry in full is regenerated and
compared with (a) the published `record` output and (b) the record committed in
<clone>/syn/ooc/pp_resource_baseline.json.  Fields the receipts carry only as
an excerpt (per-scope CARRY4 from the 8 MB cell census, inputs_sha256 over the
generated LiteX top) are reported as NOT REGENERATED, with what was cross-checked.
"""
import importlib.util, json, re, sys
from pathlib import Path

clone, rec, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(clone / "syn/ooc"))
spec = importlib.util.spec_from_file_location("gate", clone / "syn/ooc/pp_resource_gate.py")
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)

ENDPOINTS = {"route-1x1": ("route-1x1", "route", "baseline_timing.rpt.excerpt.txt"),
             "ooc-1x1": ("ooc-1x1", "ooc", "baseline_timing.rpt"),
             "ooc-8x8": ("ooc-8x8", "ooc", "baseline_timing.rpt")}
committed = json.loads((clone / "syn/ooc/pp_resource_baseline.json").read_text())
result, fails = {}, 0


for name, (sub, kind, timing_name) in ENDPOINTS.items():
    d = rec / sub
    script = (d / gate.SCRIPTS[kind]).read_text()
    report = (d / "baseline_utilization.rpt").read_text()
    figures = gate.utilization(report, kind)
    figures.update(gate.timing((d / timing_name).read_text()))
    carry_row = re.findall(r"^\| CARRY4\s+\|\s+(\d+) \|", report, re.M)
    figures["CARRY4"] = int(carry_row[0]) if len(carry_row) == 1 else None
    ident = gate.identity(d, script, report)
    rows = gate.hierarchy(d / "baseline_hierarchy.rpt")
    root = gate.ROOTS[kind]
    scopes = {}
    for key, counts in rows.items():
        inside = key == root or key.startswith(root + "/")
        if inside and not key.endswith("/@own") and key.count("/") <= root.count("/") + 3:
            rel = key.removeprefix(root).lstrip("/") or "wrapper"
            scopes[rel] = {f: counts[f] for f in ("LUT", "FF", "RAMB36", "RAMB18", "DSP")}
    unrouted = gate.routing(d, kind) if kind == "route" else None
    published = json.loads((rec / "commands" / f"record-{name}.log").read_text())
    entry = committed["endpoints"][name]
    crec = entry["record"]
    checks = {}
    checks["figures == published"] = figures == published["figures"]
    checks["figures == committed"] = figures == crec["figures"]
    checks["identity == published"] = ident == published["identity"]
    checks["identity == committed"] = ident == crec["identity"]
    strip = lambda s: {k: {f: v[f] for f in ("LUT", "FF", "RAMB36", "RAMB18", "DSP")} for k, v in s.items()}
    checks["scopes(LUT/FF/RAMB/DSP) == published"] = scopes == strip(published["scopes"])
    checks["scopes(LUT/FF/RAMB/DSP) == committed"] = scopes == strip(crec["scopes"])
    checks["published record == committed record"] = published == crec
    checks["inputs_sha256 published == committed"] = published["inputs_sha256"] == crec["inputs_sha256"]
    checks["wrapper CARRY4 == total (ooc only)"] = (kind != "ooc") or crec["scopes"]["wrapper"]["CARRY4"] == figures["CARRY4"]
    if kind == "route":
        checks["route status complete"] = unrouted == []
    status, lines = 0, []
    result[name] = {"kind": kind, "regenerated_figures": figures, "identity": ident,
                    "scope_count": len(scopes), "checks": checks,
                    "not_regenerated": ["per-scope CARRY4 (cell census retained as excerpt only)",
                                        "inputs_sha256 (generated LiteX top retained as size and hash only)"]}
    fails += sum(1 for v in checks.values() if not v)
    for k, v in checks.items():
        print(f"{name}: {'OK  ' if v else 'FAIL'} {k}")
    print(f"{name}: figures {figures}")
out.write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
print("RESULT:", "PASS" if fails == 0 else f"FAIL ({fails})")
sys.exit(1 if fails else 0)
