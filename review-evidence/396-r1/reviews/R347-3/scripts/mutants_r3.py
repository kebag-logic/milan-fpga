#!/usr/bin/env python3
"""R347-3 disposable mutation probe of the round-3 release code.

Usage: python3 -B mutants_r3.py <extracted-tree>

Same harness as round-2 mutants_r2.py: each mutant edits
tb/tools/torture_campaign.py inside an extracted tree (`git archive` of the
reviewed head), runs --self-test and the plan behave feature, reports KILLED
(either gate fails) or SURVIVED, names the failing self-test methods, and
restores the original bytes.  The reviewed clone is never touched.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    # Decision item 1: restore-bound eligibility ceiling.
    ("M01 restore eligibility check removed",
     "            and settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S\n", ""),
    ("M02 restore ceiling made exclusive",
     "settings.restore_bound_s <= RELEASE_RESTORE_BOUND_S",
     "settings.restore_bound_s < RELEASE_RESTORE_BOUND_S"),
    ("M03 restore ceiling relaxed to 31",
     "RELEASE_RESTORE_BOUND_S = 30\n", "RELEASE_RESTORE_BOUND_S = 31\n"),
    ("M04 soak repeat skips the shared profile checks",
     '    args["release_eligible"] &= _release_profile_eligible(settings)\n'
     '    args["max_soak_interval_s"]',
     '    args["max_soak_interval_s"]'),
    ("M05 restore default decoupled from the ceiling (31)",
     "restore_bound_s: int = RELEASE_RESTORE_BOUND_S", "restore_bound_s: int = 31"),
    # Decision item 2: tu bound.
    ("M06 tu bound set to the B.1.1 nominal 0.25 s",
     "tu_holdover_bound_s=0.5,", "tu_holdover_bound_s=0.25,"),
    ("M07 tu origin loosened to any tu edge",
     'tu_time_origin="recorded GM change or timing discontinuity",',
     'tu_time_origin="first tu edge",'),
    ("M08 tu observation resolution not required",
     'tu_observation_resolution="record measured resolution in seconds with event evidence",',
     'tu_observation_resolution="optional",'),
    ("M09 soak assertion text states a 5 s tu bound",
     "clears within 0.5 s of that event plus ",
     "clears within 5 s of that event plus "),
    ("M10 soak assertion text drops the uncorrelated-tu failure",
     "uncorrelated tu fails; ", ""),
    # Decision item 3: ADP from T0, off time recorded and not charged.
    ("M11 off time charged to the ADP window",
     "power_off_hold_in_adp_window=False,", "power_off_hold_in_adp_window=True,"),
    ("M12 required valid_time changed to 5",
     "adp_required_valid_time=10,", "adp_required_valid_time=5,"),
    ("M13 ADP start moved to the pre-cut advertisement",
     'adp_start="T0",', 'adp_start="last pre-cut ENTITY_AVAILABLE",'),
    ("M14 ADP deadline charged for the power-off hold",
     'adp_deadline="2 * pre_cut_valid_time",',
     'adp_deadline="2 * pre_cut_valid_time - power_off_hold_s",'),
    ("M15 power assertion text measures from the pre-cut advertisement",
     "valid_time measured from T0, the host-timestamped power-strip ",
     "valid_time measured from the last pre-cut ENTITY_AVAILABLE, not the power-strip "),
    ("M16 power assertion text charges the off time",
     "pre-cut advertisement age are provenance, not charged to",
     "pre-cut advertisement age are charged to"),
    ("M17 power_off_hold_s validation dropped",
     '"soak_interval_s", "power_cycles", "power_off_hold_s",',
     '"soak_interval_s", "power_cycles",'),
    ("M18 power_off_hold_s default 5",
     "power_off_hold_s: int = 8", "power_off_hold_s: int = 5"),
    ("M19 CLI --power-off-hold-s default 5",
     "default=ReleaseSettings.power_off_hold_s", "default=5"),
    # Decision item 4: topology keys.
    ("M20 topology accepts the entity_id alias",
     'part.split("=", 1)[0].strip()', 'part.split("=", 1)[0].strip().replace("entity_id", "entity")'),
    ("M21 topology accepts empty values",
     'if "=" in part and part.split("=", 1)[1].strip()}', 'if "=" in part}'),
    ("M22 topology requires crf_out only",
     '{"entity", "mac", "crf_in", "crf_out"} <= keys', '{"entity", "mac", "crf_out"} <= keys'),
    ("M23 topology requires crf_in only",
     '{"entity", "mac", "crf_in", "crf_out"} <= keys', '{"entity", "mac", "crf_in"} <= keys'),
    ("M24 topology accepts a missing mac",
     '{"entity", "mac", "crf_in", "crf_out"} <= keys', '{"entity", "crf_in", "crf_out"} <= keys'),
    ("M25 topology requires a talker shape only",
     '                or not {"listeners", "listener_index_set"} & keys):',
     '                ):'),
    # Suggestion items taken in round 3.
    ("M26 boot oracle accepts a bool restart count",
     "type(restarts) is not int", "not isinstance(restarts, int)"),
]

FAIL_RE = re.compile(r"^FAIL: (\w+) ", re.M)


def run(tree: Path, *cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=tree, capture_output=True, text=True, timeout=900)


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    target = tree / "tb/tools/torture_campaign.py"
    original = target.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    print(f"target sha256 {digest}")
    gates = ((sys.executable, "-B", str(target), "--self-test"),
             (sys.executable, "-B", "-m", "behave",
              "tests/features/torture_campaign_plan.feature", "-f", "progress"))
    base = tuple(run(tree, *g).returncode for g in gates)
    print(f"baseline self-test rc={base[0]} behave rc={base[1]}")
    if base != (0, 0):
        return 2
    text = original.decode()
    survivors = []
    try:
        for name, old, new in MUTANTS:
            count = text.count(old)
            if count != 1:
                print(f"UNAPPLIED ({count} matches)  {name}")
                survivors.append(name)
                continue
            target.write_text(text.replace(old, new))
            st, bh = (run(tree, *g) for g in gates)
            killed = st.returncode != 0 or bh.returncode != 0
            if not killed:
                survivors.append(name)
            tests = sorted(set(FAIL_RE.findall(st.stderr)))
            print(f"{'KILLED  ' if killed else 'SURVIVED'} self-test rc={st.returncode} "
                  f"behave rc={bh.returncode}  {name}  failing={','.join(tests) or '-'}")
            target.write_bytes(original)
    finally:
        target.write_bytes(original)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    print(f"restored target sha256 {digest}; survivors {len(survivors)}")
    for name in survivors:
        print(f"  survivor: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
