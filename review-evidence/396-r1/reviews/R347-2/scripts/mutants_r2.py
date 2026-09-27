#!/usr/bin/env python3
"""R347-2 disposable mutation probe of the round-2 release code.

Usage: python3 -B mutants_r2.py <extracted-tree>

Same harness as round-1 mutants.py: each mutant edits
tb/tools/torture_campaign.py inside an extracted tree, runs --self-test and
the plan behave feature, reports KILLED (either gate fails) or SURVIVED, and
restores the original bytes.  The reviewed clone is never touched.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("R01 eligibility ignores topology_explicit",
     "    return (settings.topology_explicit\n            and \"stream_binding\"",
     "    return (True\n            and \"stream_binding\""),
    ("R02 eligibility ignores the stream-binding inventory",
     "            and \"stream_binding\" in settings.persisted_items\n",
     "            and True\n"),
    ("R03 interval ceiling made exclusive",
     "settings.soak_interval_s <= RELEASE_MAX_SOAK_INTERVAL_S)",
     "settings.soak_interval_s < RELEASE_MAX_SOAK_INTERVAL_S)"),
    ("R04 power repeats skip the common prerequisites",
     "        args[\"release_eligible\"] &= _release_profile_eligible(settings)\n        args[\"topology_explicit\"] = settings.topology_explicit\n        steps.append(",
     "        args[\"topology_explicit\"] = settings.topology_explicit\n        steps.append("),
    ("R05 boot observation drops the margin",
     "boot_observation_s=settings.restore_bound_s + settings.boot_margin_s,",
     "boot_observation_s=settings.restore_bound_s,"),
    ("R06 restore bound made exclusive",
     "restore_limit_exclusive=False,", "restore_limit_exclusive=True,"),
    ("R07 ADP limit made inclusive",
     "adp_limit_exclusive=True,", "adp_limit_exclusive=False,"),
    ("R08 CLI --restore-bound-s not threaded",
     "        release = replace(release, restore_bound_s=a.restore_bound_s,\n",
     "        release = replace(release,\n"),
    ("R09 CLI --boot-margin-s not threaded",
     "                          boot_margin_s=a.boot_margin_s,\n",
     ""),
    ("R10 topology check reads the DUT spec only",
     "    for spec in (dut_spec, peer_spec):\n        keys =",
     "    for spec in (dut_spec,):\n        keys ="),
    ("R11 topology check does not require CRF keys",
     "{\"entity\", \"mac\", \"crf_in\", \"crf_out\"} <= keys",
     "{\"entity\", \"mac\"} <= keys"),
    ("R12 topology check does not require listener shape",
     "                or not {\"listeners\", \"listener_index_set\"} & keys):",
     "                or False):"),
    ("R13 CRF overlap check covers talkers only",
     "        if (device.crf_out in device.talker_indices(False)\n                or device.crf_in in device.listener_indices(False)):",
     "        if (device.crf_out in device.talker_indices(False)):"),
    ("R14 CRF overlap check removed",
     "            raise ValueError(\"release AAF indices must not include a CRF index\")",
     "            pass"),
    ("R15 boot oracle ignores restarts",
     "\"PASS\" if boot_passes == 1 and restarts == 0 else \"FAIL\"",
     "\"PASS\" if boot_passes == 1 else \"FAIL\""),
    ("R16 boot oracle ignores capture completeness",
     "    if (capture_complete is not True or type(boot_passes)",
     "    if (False or type(boot_passes)"),
    ("R17 boot oracle accepts zero passes",
     "\"PASS\" if boot_passes == 1 and restarts == 0 else \"FAIL\"",
     "\"PASS\" if boot_passes <= 1 and restarts == 0 else \"FAIL\""),
    ("R18 restore_bound_s positive-integer validation dropped",
     "\"idle_cycles\", \"commit_cycles\", \"restore_bound_s\", \"boot_margin_s\"):",
     "\"idle_cycles\", \"commit_cycles\"):"),
    ("R19 topology_explicit type check dropped",
     "        if type(self.topology_explicit) is not bool:\n            raise ValueError(\"topology_explicit must be a boolean\")\n",
     ""),
    ("R20 power.single-boot assertion dropped from POWER_ASSERTS",
     "    AssertSpec(\"power.single-boot\", RELEASE_CLAUSE +",
     "    AssertSpec(\"power.single-boot-x\", RELEASE_CLAUSE +"),
    ("R21 restore bound marked not provisional",
     "restore_bound_provisional=True,", "restore_bound_provisional=False,"),
    ("R22 soak eligibility ignores duration (common prerequisites only)",
     "                release_eligible=(settings.soak_duration_s\n                                  >= ReleaseSettings.soak_duration_s),",
     "                release_eligible=True,"),
]


def run(tree: Path, *cmd: str) -> int:
    return subprocess.run(cmd, cwd=tree, stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL, timeout=600).returncode


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    target = tree / "tb/tools/torture_campaign.py"
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    print(f"target sha256 {digest}")
    gates = ((sys.executable, "-B", str(target), "--self-test"),
             (sys.executable, "-B", "-m", "behave",
              "tests/features/torture_campaign_plan.feature", "-f", "progress"))
    base = tuple(run(tree, *g) for g in gates)
    print(f"baseline self-test rc={base[0]} behave rc={base[1]}")
    if base != (0, 0):
        return 2
    text = original.decode()
    survivors = 0
    try:
        for name, old, new in MUTANTS:
            count = text.count(old)
            if count != 1:
                print(f"UNAPPLIED ({count} matches)  {name}")
                survivors += 1
                continue
            target.write_text(text.replace(old, new))
            st, bh = (run(tree, *g) for g in gates)
            verdict = "KILLED  " if (st or bh) else "SURVIVED"
            survivors += verdict == "SURVIVED"
            print(f"{verdict} self-test rc={st} behave rc={bh}  {name}")
            target.write_bytes(original)
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    print(f"restored target sha256 {digest}; survivors {survivors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
