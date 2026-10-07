#!/usr/bin/env python3
"""Trace the #163 final-head timing figures to the published measurement record.

Usage: verify_measurement.py EVIDENCE_DIR   (review-evidence/pp163-r1 of the evidence branch)
Checks, from published files only:
  * every rc file of measurement-m3final is 0;
  * the gate record (record-m3final.stdout) carries inputs_sha256, WNS and WHS, and the OOC design;
  * the gate run (gate-m3final.stdout) passed against that directory;
  * the cone run (cone-m3final.stdout) opened that directory's checkpoint and its counts equal
    the cone block of evidence/measurement-m3final.json;
  * the cone histogram sums to the pair count, its deepest bin is max_levels and no bin is above 20;
  * the per-group summary (evidence/cone-summary-m3final-all.txt) accounts for every pair and
    its deepest group equals max_levels;
  * the setup slack in measurement-m3final.json equals the record's WNS;
  * the published MANIFEST.json digest of each file read equals its sha256.
Prints JSON; exit 0 only if every check holds.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ev = Path(sys.argv[1])
m = ev / "author-r3/measurement-m3final"
checks = {}
rcs = {p.name: p.read_text().strip() for p in sorted(m.glob("*.rc"))}
checks["all_rc_zero"] = (rcs, all(v == "0" for v in rcs.values()) and len(rcs) == 6)
rec = json.loads((m / "record-m3final.stdout").read_text())
checks["record"] = ({"design": rec["identity"]["design"], "flow": rec["identity"]["flow"],
                     "clock": rec["identity"]["standalone_clock_ns"], "inputs_sha256": rec["inputs_sha256"],
                     "WNS_ns": rec["figures"]["WNS_ns"], "WHS_ns": rec["figures"]["WHS_ns"]},
                    rec["identity"]["design"] == "KL_pp_shadow" and rec["figures"]["WNS_ns"] == 3.337
                    and rec["inputs_sha256"] == "24ba6a244a83a0b764e6de5131a9c94752135f01ecab5afad83258c7b4767be1"
                    and rec["identity"]["standalone_clock_ns"] == ["20.000"])
gate = (m / "gate-m3final.stdout").read_text()
checks["gate"] = (re.findall(r"endpoint .*|RESULT: \w+", gate),
                  "RESULT: PASS" in gate and "meas/ooc-m3final" in gate)
cone_out = (m / "cone-m3final.stdout").read_text()
meas = json.loads((ev / "author-r3/evidence/measurement-m3final.json").read_text())
cone = meas["cone"]
head = re.search(r"arbiter cells (\d+) endpoint pins (\d+) startpoints (\d+)", cone_out)
written = re.search(r"cone paths written: (\d+)", cone_out)
dcp = re.search(r"open_checkpoint (\S+)", cone_out.split("Command:")[1])
checks["cone_stdout_vs_json"] = ({"stdout": [head.groups(), written.group(1), dcp.group(1)],
                                  "json": [cone["sequential_cells"], cone["queried_endpoint_pins"],
                                           cone["queried_startpoints"], cone["pairs"]]},
                                 [int(x) for x in head.groups()] == [cone["sequential_cells"],
                                                                     cone["queried_endpoint_pins"],
                                                                     cone["queried_startpoints"]]
                                 and int(written.group(1)) == cone["pairs"]
                                 and dcp.group(1).endswith("meas/ooc-m3final/baseline_synth.dcp"))
hist = {int(k): v for k, v in cone["histogram"].items()}
checks["histogram"] = ({"sum": sum(hist.values()), "max_bin": max(hist), "above_20_bins": sum(v for k, v in hist.items() if k > 20),
                        "max_levels": cone["max_levels"], "above_20": cone["above_20"]},
                       sum(hist.values()) == cone["pairs"] and max(hist) == cone["max_levels"] == 16
                       and cone["above_20"] == 0 and all(k <= 20 for k in hist))
summary = (ev / "author-r3/evidence/cone-summary-m3final-all.txt").read_text()
total = sum(int(x) for x in re.findall(r"-> \S+: (\d+) paths", summary))
deep = max(int(x) for x in re.findall(r"max (\d+) levels", summary))
first = re.match(r"paths (\d+)\s+max levels (\d+)", summary)
checks["summary"] = ({"group_paths_total": total, "deepest_group": deep, "header": first.groups()},
                     total == cone["pairs"] and deep == 16 and first.groups() == (str(cone["pairs"]), "16"))
checks["setup_slack"] = (meas["timing"]["setup"], meas["timing"]["setup"]["worst_slack_ns"] == rec["figures"]["WNS_ns"]
                         and meas["timing"]["setup"]["failing_endpoints"] == 0)
manifest = {row["file"]: row for row in json.loads((ev / "MANIFEST.json").read_text())}
read = [p for p in m.rglob("*") if p.is_file()] + [ev / "author-r3/evidence/measurement-m3final.json",
                                                    ev / "author-r3/evidence/cone-summary-m3final-all.txt"]
bad = []
for p in read:
    rel = str(p.relative_to(ev))
    row = manifest.get(rel)
    if row is None or row["published_sha256"] != hashlib.sha256(p.read_bytes()).hexdigest():
        bad.append(rel)
checks["manifest"] = ({"files": len(read), "unlisted_or_mismatched": bad}, not bad)
ok = all(v[1] for v in checks.values())
print(json.dumps({k: {"value": v[0], "ok": v[1]} for k, v in checks.items()} | {"all_ok": ok}, indent=1))
sys.exit(0 if ok else 1)
