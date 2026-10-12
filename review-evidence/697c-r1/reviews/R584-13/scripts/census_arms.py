#!/usr/bin/env python3
"""Run ctrl_pin's proof census, the unplanted proof under its audit hook, and
every census/hook arm (census_arms) against the given checkout, the way
pin_controls judges them; print one line per arm and a tally.
usage: python3 -I census_arms.py <superproject-root>"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_pin  # noqa: E402

findings = ctrl_pin.proof_census()
print(f"proof census findings: {len(findings)}")
for f in findings:
    print("  ", f)
arms = [("the pin proof as the checkout holds it, under its audit hook", lambda: None, ctrl_pin.unplanted, ""),
        *ctrl_pin.census_arms()]
bad = 0
for what, spoil, check, needle in arms:
    spoil()
    accepted, detail = check()
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] {what}: {detail[:220]}", flush=True)
    bad += not ok
print(f"TALLY: {len(arms)} arms, {bad} misbehaved, census findings {len(findings)}")
sys.exit(1 if bad or findings else 0)
