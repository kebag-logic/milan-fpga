#!/usr/bin/env python3
"""Independent stale-evidence probe on the motivating top, KL_pp_shadow.

usage (cwd = checkout root, PYTHONDONTWRITEBYTECODE=1): pp_shadow_probe.py <work-dir>

Uses the shipping run.sh and real tools. Generator output is altered only via
the same private python3 wrapper the shipping ROM controls use (ucode.hex
replaced after a successful real generator run); no source changes.
  cold     --cache H              real ROMs, stores
  warm     --cache H              must hit with the cold count
  changed  --cache H  (ucode.hex changed) must MISS and equal the uncached count
  uncached no cache   (ucode.hex changed) the live reference
Prints a JSON summary; exit 0 only when every expectation holds.
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "syn/yosys")
import rom_cache_selftest as r  # noqa: E402

work = Path(sys.argv[1])
p = r.Probe(work, tops=("KL_pp_shadow",))
head = work / "head"
change = ("ucode.hex", "changed")
cold = p.run("cold", ["--cache", str(head)])
with ThreadPoolExecutor(max_workers=3) as pool:
    fw = pool.submit(p.run, "warm", ["--cache", str(head)])
    fc = pool.submit(p.run, "changed", ["--cache", str(head)], change)
    fu = pool.submit(p.run, "uncached", [], change)
    warm, changed, uncached = fw.result(), fc.result(), fu.result()
look = lambda rec, op: r.cache_inputs(rec, op).get("KL_pp_shadow", {})
summary = {name: dict(exit=rec["exit"], seconds=rec["seconds"], cells=rec["cells"], hits=rec["hits"],
                      rom_sha256=look(rec, "lookup").get("rom_sha256"),
                      rom_images=[e for e in rec["events"] if "image" in e])
           for name, rec in (("cold", cold), ("warm", warm), ("changed", changed), ("uncached", uncached))}
diff_fields = sorted(k for k in look(cold, "lookup") if look(cold, "lookup")[k] != look(changed, "lookup").get(k))
checks = {
    "all_exit_0": all(x["exit"] == 0 for x in (cold, warm, changed, uncached)),
    "cold_live": not cold["hits"] and "KL_pp_shadow" in cold["cells"],
    "cold_lookup_equals_store": look(cold, "lookup") == look(cold, "store"),
    "warm_hit_same_cells": warm["hits"] == ["KL_pp_shadow"] and warm["cells"] == cold["cells"],
    "changed_missed": not changed["hits"],
    "changed_equals_uncached": changed["cells"] == uncached["cells"],
    "changed_lookup_equals_store": look(changed, "lookup") == look(changed, "store"),
    "only_rom_digest_differs": diff_fields == ["rom_sha256"],
}
summary["changed_vs_cold_differing_identity_fields"] = diff_fields
summary["cells_differ_changed_vs_cold"] = changed["cells"] != cold["cells"]
summary["checks"] = checks
print(json.dumps(summary, indent=1))
sys.exit(0 if all(checks.values()) else 1)
