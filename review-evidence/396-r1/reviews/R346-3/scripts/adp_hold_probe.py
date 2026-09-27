#!/usr/bin/env python3
"""R346-3 probe: evaluate the ADP rule the planner EMITS (not a copy of it) under varied
power-off holds, and check the hold is recorded but never enters the window arithmetic.

Usage: python3 -B adp_hold_probe.py <repo-root>
Reads the plan through the head's own CLI; evaluates `adp_deadline`/`adp_elapsed` strings with
a restricted namespace that ALSO defines hold/pre-cut variables, so a formula that referenced
them would change verdict with the hold.  Exit 0 only if every expectation holds.
"""
from __future__ import annotations

import json
import subprocess
import sys

root = sys.argv[1]
DUT = "entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=16,crf_in=16"
PEER = "entity=8899aabbccddeeff,mac=8899aabbccdd,talkers=2,listeners=2,crf_out=16,crf_in=16"
fails = 0


def plan(hold: int | None) -> list[dict]:
    argv = [sys.executable, "-B", "tb/tools/torture_campaign.py", "--plan", "--areas", "soak,power",
            "--json", "--dut", DUT, "--peer", PEER]
    if hold is not None:
        argv += ["--power-off-hold-s", str(hold)]
    out = subprocess.run(argv, cwd=root, capture_output=True, text=True, check=True, timeout=600)
    return json.loads(out.stdout)


def expect(label: str, got, want) -> None:
    global fails
    ok = got == want
    fails += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: got={got!r} want={want!r}")


def verdict(args: dict, boot_s: float, hold_s: float, precut_age_s: float) -> str:
    t0 = 1000.0
    ns = {"pre_cut_valid_time": 10, "t0_host_s": t0,
          "first_post_cut_available_host_s": t0 + boot_s,
          # decoys: a formula that charged these would move with them
          "power_off_hold_s": hold_s, "power_off_host_s": t0 - hold_s,
          "pre_cut_last_available_host_s": t0 - hold_s - precut_age_s}
    deadline = eval(args["adp_deadline"], {"__builtins__": {}}, ns)  # noqa: S307 - probe only
    elapsed = eval(args["adp_elapsed"], {"__builtins__": {}}, ns)  # noqa: S307
    ok = 0 <= elapsed < deadline if args["adp_limit_exclusive"] else 0 <= elapsed <= deadline
    return "PASS" if ok else "FAIL"


for hold in (None, 1, 8, 60, 3600):
    steps = plan(hold)
    power = [s for s in steps if s["sid"].startswith("power.")]
    expect(f"hold={hold} two power repeats", len(power), 2)
    for s in power:
        a = s["args"]
        expect(f"hold={hold} {s['sid']} recorded hold", a["power_off_hold_s"], 8 if hold is None else hold)
        expect(f"hold={hold} {s['sid']} hold not in window", a["power_off_hold_in_adp_window"], False)
        expect(f"hold={hold} {s['sid']} adp_start", a["adp_start"], "T0")
        expect(f"hold={hold} {s['sid']} required valid_time", a["adp_required_valid_time"], 10)
        expect(f"hold={hold} {s['sid']} eligible (hold is provenance only)", a["release_eligible"], True)
        for boot, want in ((5.0, "PASS"), (19.99, "PASS"), (20.0, "FAIL"), (25.0, "FAIL"), (-0.1, "FAIL")):
            for age in (0.0, 4.9):
                expect(f"hold={hold} {s['sid']} boot={boot} precut_age={age}",
                       verdict(a, boot, 8 if hold is None else hold, age), want)

# The superseded round-2 formula, for contrast: it leaves boot only 20 - hold - advert age, so at
# the repository's 8 s hold a boot of 7.2 s fails with a 4.9 s-old advert (8 + 4.9 + 7.2 > 20) and
# 13 s fails with a fresh one -- boots the corrected T0 rule passes.  Decision item 3 removed this.
old = {"adp_deadline": "pre_cut_last_available_host_s + 2 * pre_cut_valid_time - t0_host_s",
       "adp_elapsed": "first_post_cut_available_host_s - t0_host_s", "adp_limit_exclusive": True}
expect("contrast: superseded formula, hold=8, age=4.9, boot=7.2", verdict(old, 7.2, 8, 4.9), "FAIL")
expect("contrast: superseded formula, hold=8, age=0, boot=13", verdict(old, 13.0, 8, 0.0), "FAIL")
print(f"{'PASS' if not fails else 'FAIL'}: {fails} unexpected result(s)")
sys.exit(1 if fails else 0)
