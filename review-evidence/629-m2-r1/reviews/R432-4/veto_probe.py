#!/usr/bin/env python3
"""Reviewer probe: plant veto variants through gmstep_mutants.run_control.

Uses the campaign's own planting, build and verdict code against a copy of the
tree (argument 1, the milan_dp directory of that copy). Each probe reports
caught or SURVIVED; nothing in the copy's tracked files is written.
  P1 round 4's published form (appended to the request's last line)
  P2 round 4b's form (inside the selected-CRF group), the shipped control
  P3 a veto over both followed-AAF terms on a re-base cycle (no named check
     claims this; it asks whether any check grades AAF + PHC-step coincidence)
"""
import sys
import tempfile
from pathlib import Path

dp = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(dp))
import gmstep_mutants as gm  # noqa: E402

CHECK = "coincident: a PHC step does not suppress the CRF restart"
probes = [
    ("P1 round-4 form: veto appended to the request's last line",
     gm.RESTART_TRIGGER, gm.RESTART_TRIGGER[:-1] + " & ~media_rebase_p_w;", CHECK),
    ("P2 round-4b form: veto inside the selected-CRF group",
     gm.CRF_RESTART_TERMS, gm.CRF_RESTART_TERMS[:-1] + " & ~media_rebase_p_w)", CHECK),
    ("P3 veto over both followed-AAF terms on a re-base cycle",
     gm.RESTART_TRIGGER,
     "       | ((aafm_disrupt_p_w | aafm_mr_toggle_p_w) & ~media_rebase_p_w);", "coincident"),
]
results = []
with tempfile.TemporaryDirectory(prefix="r432-veto-") as td:
    for tag, (name, anchor, rep, check) in enumerate(probes):
        c = gm.Control(name, "datapath", anchor, rep, check, False)
        print(f"==== {name}", flush=True)
        caught = gm.run_control(c, Path(td), 100 + tag)
        results.append((name, caught))
        sys.stdout.flush()
print()
for name, caught in results:
    print(f"{'caught' if caught else 'SURVIVED'}: {name}")
expected = [False, True, False]
ok = [c for _, c in results] == expected
print("as expected (P1 survives, P2 caught, P3 survives)" if ok else "NOT as expected")
raise SystemExit(0 if ok else 1)
