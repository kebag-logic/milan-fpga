#!/usr/bin/env python3
"""R347-1 disposable mutation probe for the #396 release planner.

Usage: python3 -B mutants.py <extracted-tree>

<extracted-tree> is `git archive <head>` of the reviewed commit.  Each mutant
edits tb/tools/torture_campaign.py inside that tree, runs the planner
--self-test and the plan behave feature, records whether either gate failed
(KILLED) or both passed (SURVIVED), and restores the original bytes.  The
reviewed clone is never touched.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    # --- audit (area_covers_every_index / _release_coverage) ---
    ("A1 audit checks only the first repeat group of an area",
     "        for step in steps:\n            defects = _release_coverage(step, dut, peer)",
     "        for step in steps[:1]:\n            defects = _release_coverage(step, dut, peer)"),
    ("A2 per-repeat observation audit checks the DUT only",
     '    for role, device in (("dut", dut), ("peer", peer)):\n        for kind, descriptor, indices in (',
     '    for role, device in (("dut", dut),):\n        for kind, descriptor, indices in ('),
    ("A3 direction audit checks the return direction only",
     '    for direction, talker, listener in (("outbound", dut, peer),\n                                        ("return", peer, dut)):',
     '    for direction, talker, listener in (("return", peer, dut),):'),
    ("A4 direction audit checks the outbound direction only (control)",
     '    for direction, talker, listener in (("outbound", dut, peer),\n                                        ("return", peer, dut)):',
     '    for direction, talker, listener in (("outbound", dut, peer),):'),
    ("A5 CRF binding audit skipped for the outbound direction",
     "        if (talker.crf_out is None or listener.crf_in is None\n                or not any(",
     '        if direction == "return" and (talker.crf_out is None or listener.crf_in is None\n                or not any('),
    ("A6 per-repeat observation audit checks listeners only",
     '                ("talker", "stream_output", device.talker_indices()),\n                ("listener", "stream_input", device.listener_indices())):\n            seen = {t.get("index") for t in targets',
     '                ("listener", "stream_input", device.listener_indices()),):\n            seen = {t.get("index") for t in targets'),
    ("A7 power phase-mix audit removed",
     '        if area == "power" and {s.args.get("phase") for s in steps} != {',
     '        if False and {s.args.get("phase") for s in steps} != {'),
    # --- planner parameter threading ---
    ("P1 soak interval hardcoded to 60 s",
     "                interval_s=settings.soak_interval_s,",
     "                interval_s=60,"),
    ("P2 power total_cycles hardcoded to 200",
     "        args.update(cycles=count, total_cycles=settings.power_cycles,",
     "        args.update(cycles=count, total_cycles=200,"),
    ("P3 power release_eligible ignores the idle/commit minimums",
     "\n                                      and settings.idle_cycles >= ReleaseSettings.idle_cycles\n                                      and settings.commit_cycles >= ReleaseSettings.commit_cycles),",
     "),"),
    ("P4 soak release_eligible always true",
     "                release_eligible=(settings.soak_duration_s\n                                  >= ReleaseSettings.soak_duration_s),",
     "                release_eligible=True,"),
    ("P5 soak duration hardcoded",
     "    args.update(duration_s=settings.soak_duration_s,",
     "    args.update(duration_s=604800,"),
    ("P6 persisted items hardcoded",
     "                    persisted_items=list(settings.persisted_items),",
     '                    persisted_items=["stream_binding"],'),
    ("P7 idle/commit sum check removed",
     "        if self.idle_cycles + self.commit_cycles != self.power_cycles:",
     "        if False:"),
    ("P8 rebind bound made inclusive",
     "rebind_limit_exclusive=True,", "rebind_limit_exclusive=False,"),
    ("P9 soak endpoint sample dropped",
     "sample_at_start=True, sample_at_end=True,",
     "sample_at_start=True, sample_at_end=False,"),
    # --- planner topology coverage ---
    ("T1 outbound CRF pair dropped",
     "        pairs.append(_multi_pair(Endpoint(talker, talker.crf_out),",
     "        if talker is not dut: pairs.append(_multi_pair(Endpoint(talker, talker.crf_out),"),
    ("T2 peer CRF sink counter target dropped",
     "                           for index in indices)",
     "                           for index in indices if not (device is peer and index == device.crf_in))"),
    ("T3 return AAF pairs dropped",
     "        for index, sink in enumerate(inputs):",
     "        for index, sink in enumerate(inputs if talker is dut else []):"),
    ("T4 AAF bound into the CRF sink",
     "        inputs = listener.listener_indices(include_crf=False)\n        if not outputs or not inputs:\n            raise ValueError(\"release campaigns require AAF in both directions\")",
     "        inputs = listener.listener_indices(include_crf=True)\n        if not outputs or not inputs:\n            raise ValueError(\"release campaigns require AAF in both directions\")"),
    ("T5 DUT talker counter targets dropped above index 0",
     "                           for index in indices)",
     "                           for index in indices if not (device is dut and descriptor == 'stream_output' and 0 < index < 4))"),
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
    base = (run(tree, sys.executable, "-B", str(target), "--self-test"),
            run(tree, sys.executable, "-B", "-m", "behave",
                "tests/features/torture_campaign_plan.feature", "-f", "progress"))
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
            st = run(tree, sys.executable, "-B", str(target), "--self-test")
            bh = run(tree, sys.executable, "-B", "-m", "behave",
                     "tests/features/torture_campaign_plan.feature", "-f", "progress")
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
