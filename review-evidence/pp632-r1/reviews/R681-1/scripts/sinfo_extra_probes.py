#!/usr/bin/env python3
"""Reviewer fault probes on E_SINFO's new words, run through tb/pp_top's own
notify_mutants.py harness (private copy per probe, --notify-only, judged on the
named-check prefix). Disposable: never committed.

usage: sinfo_extra_probes.py REPO_ROOT OUTPUT_DIR VERILATOR JOBS
"""
import concurrent.futures
import json
import sys
from pathlib import Path

root, output, verilator, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], int(sys.argv[4])
sys.path.insert(0, str(root / "tb/pp_top"))
import notify_mutants as nm  # noqa: E402

U = nm.UCODE
PROBES = (
    nm.Mutant("r_unset_arm_skips_gather", nm.NOTIFY, (
        (U, "    u('BR_STATUS', cnd=2, imm=E_SINFO + 8),      # z = unset -> the integrator\n",
            "    u('BR_STATUS', cnd=2, imm=E_SINFO + 9),      # probe: skip the gather\n"),), ("NS",)),
    nm.Mutant("r_set_arm_falls_into_gather", nm.NOTIFY, (
        (U, "    u('BRANCH', imm=E_SINFO + 9),\n",
            "    u('BRANCH', imm=E_SINFO + 8),  # probe: into the gather\n"),), ("NS4", "NS5")),
    nm.Mutant("r_skip_target_off_by_one", nm.NOTIFY, (
        (U, "    u('BR_STATUS', cnd=2, imm=E_SINFO + 17),\n",
            "    u('BR_STATUS', cnd=2, imm=E_SINFO + 16),\n"),), ("NS1", "NS4")),
    nm.Mutant("r_valid_test_inverted", nm.NOTIFY, (
        (U, "    u('READ_ST', rd=3, imm=RGN_DYNV + SEL_PTOFF),\n    u('COMPARE', ra=3, fmt=FMT_D, imm=0),\n",
            "    u('READ_ST', rd=3, imm=RGN_DYNV + SEL_PTOFF),\n    u('COMPARE', ra=3, fmt=FMT_D, imm=1),\n"),),
        ("NS1",)),
)
output.mkdir(parents=True, exist_ok=True)
work = (root, output, verilator)
records = []
with concurrent.futures.ThreadPoolExecutor(max(1, jobs)) as pool:
    for rec in pool.map(lambda m: nm.judge(m, work), PROBES):
        records.append(rec)
        print(json.dumps({k: rec.get(k) for k in ("mutant", "verdict", "missing", "failing_checks")}), flush=True)
(output / "results.json").write_text(json.dumps(records, indent=1) + "\n")
print(f"reviewer probes: {sum(r['verdict'] == 'KILLED' for r in records)} of {len(records)} KILLED")
