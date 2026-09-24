#!/usr/bin/env python3
"""R273-7: compare this round's case receipts with round four's, per case,
on the verdict AND on the refusal reason (the pin). Reasons are compared
after replacing line numbers ("line N"/":N") so a pure line shift is not
reported as a pin change; any other text difference is.
usage: compare_pins.py <prev-receipts-dir> <this-receipts-dir> <stem>..."""
import json, re, sys
from pathlib import Path
prev, cur = Path(sys.argv[1]), Path(sys.argv[2])
norm = lambda s: re.sub(r"(/tmp|<tmp>)/milan-[a-z]+-[a-z0-9_]+", "<tmp>", re.sub(r"\b(line|lines) \d+|:\d+\b|\b\d+ to \d+\b", "#", s or ""))
total = vchg = pchg = 0
for stem in sys.argv[3:]:
    for mode in ("sdk", "absent"):
        now = {r["label"]: r for r in json.loads((cur / f"{stem}-head-{mode}.json").read_text())["results"]}
        was = {r["label"]: r for r in json.loads((prev / f"{stem}-head-{mode}.json").read_text())["results"]}
        assert now.keys() == was.keys(), (stem, mode)
        tally = {}
        for label, r in now.items():
            p = was[label]; total += 1
            tally[r["verdict"]] = tally.get(r["verdict"], 0) + 1
            if p["verdict"] != r["verdict"]:
                vchg += 1; print(f"VERDICT {stem} {mode} {label}: {p['verdict']} -> {r['verdict']}")
            elif norm(p.get("reason")) != norm(r.get("reason")):
                pchg += 1; print(f"PIN {stem} {mode} {label}:\n  was {p.get('reason','')[:300]}\n  now {r.get('reason','')[:300]}")
        print(f"{stem} {mode}: {len(now)} cases {tally}")
print(f"TOTAL {total} cases, {vchg} verdict changes, {pchg} pin changes")
