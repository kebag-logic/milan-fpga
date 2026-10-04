#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Summarize R463-3's runs: probe verdicts against probes.py's expectations, campaign
arm counts, and suite tallies. Usage: python3 summarize.py OUT [RECEIPTS]"""

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import probes  # noqa: E402

out = Path(sys.argv[1])
dest = Path(sys.argv[2]) if len(sys.argv) > 2 else out
expect = {p[0]: (p[3], p[4]) for p in probes.PROBES}
rows = []
for f in sorted((out / "probes").glob("*/result.json")):
    r = json.loads(f.read_text())
    exp, why = expect.get(r["probe"], (r["expect"], r["why"]))
    tally = [ln for ln in r["lines"] if ln.startswith("AQ: ") and "checks" in ln
             or re.match(r"^\d+ checks: ", ln)]
    fails = [ln for ln in r["lines"] if ln.startswith("FAIL")]
    rows.append({"probe": r["probe"], "expect": exp, "verdict": r["verdict"], "rc": r["rc"],
                 "why": why, "tally": tally[-1:], "failing": fails})
camp = {}
for name in ("acmp-camp",):
    res = out / name / "results.json"
    if res.exists():
        recs = []
        for x in json.loads(res.read_text()):
            log = (out / name / f"{x['mutant']}.log").read_text(errors="replace")
            t = re.findall(r"^((?:ACMP|AQ): \d+ checks, \d+ failures|\d+ checks: \d+ PASS, \d+ FAIL)$",
                           log, re.M)
            recs.append({"mutant": x["mutant"], "verdict": x["verdict"],
                         "failing_checks": len(x.get("failing_checks", [])), "tally": t[-1:]})
        camp[name] = recs
summary = {"probes": rows, "campaigns": camp}
(dest / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
for r in rows:
    print(f"{r['probe']:32s} expect {r['expect']:6s} got {r['verdict']:6s} {r['tally']}")
for name, recs in camp.items():
    k = sum(1 for x in recs if x["verdict"] in ("KILLED",))
    g = sum(1 for x in recs if x["mutant"].startswith("golden") and x["verdict"] == "PASS")
    print(f"{name}: {k} KILLED, {g} goldens PASS, {len(recs)} records")
