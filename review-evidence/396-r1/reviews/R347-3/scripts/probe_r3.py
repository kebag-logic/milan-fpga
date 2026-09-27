#!/usr/bin/env python3
"""R347-3 probe of the round-3 release contract.

Usage: python3 -B probe_r3.py <extracted-tree>

Imports tb/tools/torture_campaign.py from the extracted tree (never the
reviewed clone) and prints:
  1. the emitted ADP expressions evaluated for several power-off holds and
     pre-cut advertisement ages (the round-2 F3 case);
  2. release_eligible for restore bounds 29/30/31/3600 via the API and CLI;
  3. topology_explicit for CLI specs missing only CRF keys, only the
     listener shape, or spelling entity as entity_id, on each role;
  4. stale round-2 strings remaining in the release text.
"""
from __future__ import annotations

import contextlib
import io
import json
import re
import sys
from pathlib import Path
from unittest.mock import patch

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "tb/tools"))
import torture_campaign as tp  # noqa: E402

DUT = "entity=0011223344556677,mac=001122334455,talkers=2,listeners=2,crf_out=16,crf_in=16"
PEER = "entity=8899aabbccddeeff,mac=8899aabbccdd,talkers=2,listeners=2,crf_out=16,crf_in=16"


def cli(*extra: str, dut: str = DUT, peer: str = PEER) -> tuple[int, list]:
    argv = ["torture_campaign.py", "--plan", "--areas", "soak,power", "--json",
            "--dut", dut, "--peer", peer, *extra]
    out, err = io.StringIO(), io.StringIO()
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(out), \
            contextlib.redirect_stderr(err):
        try:
            rc = tp.main()
        except SystemExit as exc:
            rc = exc.code
    return rc, (json.loads(out.getvalue()) if rc == 0 else [err.getvalue().strip()])


def evaluate(expr: str, env: dict) -> float:
    if not re.fullmatch(r"[\w\s\*\+\-]+", expr):
        raise ValueError(expr)
    return eval(expr, {"__builtins__": {}}, dict(env))  # noqa: S307 - vetted arithmetic


print("== 1. ADP window from the emitted plan expressions")
for hold in (8, 13, 60):
    idle = tp.build_plan(["power"], release=tp.ReleaseSettings(power_off_hold_s=hold))[0].args
    print(f"  power_off_hold_s={idle['power_off_hold_s']} in_window={idle['power_off_hold_in_adp_window']}"
          f" start={idle['adp_start']} required_valid_time={idle['adp_required_valid_time']}"
          f" deadline='{idle['adp_deadline']}' elapsed='{idle['adp_elapsed']}'"
          f" exclusive={idle['adp_limit_exclusive']}")
    for age in (0.0, 4.9):
        for boot in (12.0, 19.9, 20.0):
            t0 = 1000.0
            env = {"pre_cut_valid_time": 10,
                   "pre_cut_last_available_host_s": t0 - hold - age,
                   "t0_host_s": t0, "first_post_cut_available_host_s": t0 + boot,
                   "power_off_hold_s": hold}
            deadline = evaluate(idle["adp_deadline"], env)
            elapsed = evaluate(idle["adp_elapsed"], env)
            ok = 0 <= elapsed < deadline if idle["adp_limit_exclusive"] else 0 <= elapsed <= deadline
            print(f"    pre-cut ad age {age:4.1f} s, boot-to-first-ad {boot:4.1f} s:"
                  f" deadline {deadline:4.1f} s, elapsed {elapsed:4.1f} s -> {'PASS' if ok else 'FAIL'}")

print("== 2. release_eligible [soak, power.idle, power.journal_commit]")
for bound in (29, 30, 31, 3600):
    api = [s.args["release_eligible"] for s in tp.build_plan(
        ["soak", "power"], release=tp.ReleaseSettings(topology_explicit=True, restore_bound_s=bound))]
    rc, steps = cli("--restore-bound-s", str(bound))
    print(f"  restore_bound_s={bound}: API {api}; CLI rc {rc} {[s['args']['release_eligible'] for s in steps]}")
for hold in (1, 8, 600):
    api = [s.args["release_eligible"] for s in tp.build_plan(
        ["soak", "power"], release=tp.ReleaseSettings(topology_explicit=True, power_off_hold_s=hold))]
    print(f"  power_off_hold_s={hold} (recorded only): API {api}")
rc, steps = cli()
print(f"  CLI default --power-off-hold-s: {[s['args'].get('power_off_hold_s') for s in steps]}")

print("== 3. topology_explicit from CLI specs")


def drop(spec: str, keys: set[str]) -> str:
    return ",".join(p for p in spec.split(",") if p.split("=", 1)[0] not in keys)


for role in ("dut", "peer"):
    for label, keys in (("CRF keys", {"crf_in", "crf_out"}), ("listener shape", {"listeners"}),
                        ("crf_in only", {"crf_in"}), ("talker shape", {"talkers"})):
        specs = {"dut": DUT, "peer": PEER}
        specs[role] = drop(specs[role], keys)
        rc, steps = cli(dut=specs["dut"], peer=specs["peer"])
        print(f"  {role} missing {label}: rc {rc}; topology_explicit "
              f"{[s['args']['topology_explicit'] for s in steps] if rc == 0 else steps}; "
              f"release_eligible {[s['args']['release_eligible'] for s in steps] if rc == 0 else '-'}")
rc, steps = cli(dut=DUT.replace("entity=", "entity_id="))
print(f"  dut spells entity_id: rc {rc}; topology_explicit "
      f"{[s['args']['topology_explicit'] for s in steps] if rc == 0 else steps}")

print("== 4. stale round-2 release strings")
stale = ("applicable holdover", "pre_cut_last_available_host_s +", "already expired",
         "never replace the pre-cut origin", "comment-5854930205", "GM-change `tu` lasts",
         "lasts 0.25 s per B.1.1", "through boot_observation_s\"")
for rel in ("REQUIREMENTS.md", "docs/testing/TESTING.md", "tb/tools/torture_campaign.py",
            "tests/features/torture_campaign_plan.feature", "tests/steps/torture_release_steps.py"):
    text = (tree / rel).read_text(encoding="utf-8")
    hits = [(s, text[:text.index(s)].count("\n") + 1) for s in stale if s in text]
    print(f"  {rel}: {hits if hits else 'none'}")
