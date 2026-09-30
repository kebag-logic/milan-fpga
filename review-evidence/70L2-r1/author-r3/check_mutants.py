#!/usr/bin/env python3
"""Run the round-2 reviewers' service-grader mutants and assert their outcomes.

usage: check_mutants.py <repo> <scratch>

R412-2's grader_mutants.py (W0-W6) and grader_mutants2.py (X1-X5, W0) run
unchanged against <repo>. R413-2's armed_mutants.py reads the head's run.py from
$R413_HEAD_TREE, pointed here at a pristine export of <repo>'s committed tree, and
plants into a scratch copy of <repo>'s tracked files.
Exit 0 only when: W0 passes; W1-W6 are KILLED (W3, W4 and W6 by name); X1, X2, X4
and X5 are KILLED and X3 (arming from the earliest event of any kind, which only
arms earlier and so charges more) passes; every R413 mutant is KILLED.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
R412 = Path("$REVIEWS/70L2-r412-2-packet/scripts")
R413 = Path("$REVIEWS/70L2-r413-2-packet/probes/armed_mutants.py")
RUN = "tb/verilator/fw_service_budget/run.py"
if scratch.exists():
    shutil.rmtree(scratch)
scratch.mkdir(parents=True)


def verdicts(script, where):
    got = subprocess.run([sys.executable, str(R412 / script), str(repo), str(scratch / where)],
                         capture_output=True, text=True, check=True).stdout
    print(got, end="")
    return dict(line.split(": ", 1)[0:2] for line in got.splitlines() if ": " in line)


expected = {"W0_identity_control": "SURVIVED", "W1_old_whole_span": "KILLED",
            "W2_unarmed_never_charged": "KILLED", "W3_first_tick_inside_duty": "KILLED",
            "W4_last_tick": "KILLED", "W5_phy_whole_span": "KILLED", "W6_armed_no_uart": "KILLED"}
got = verdicts("grader_mutants.py", "w")
for name, want in expected.items():
    assert got[name].startswith(want), f"{name}: expected {want}, got {got[name][:80]}"
assert "UART allowance left its armed bound" in got["W6_armed_no_uart"], got["W6_armed_no_uart"]
for name in ("W3_first_tick_inside_duty", "W4_last_tick"):
    assert "leading gap escaped" in got[name], got[name]

expected = {"X1_exempt_aem_by_name": "KILLED", "X2_armed_drops_250_base": "KILLED",
            "X3_arming_from_any_event_kind": "SURVIVED", "X4_arming_from_block_report_cycle": "KILLED",
            "X5_ends_before_arm_boundary": "KILLED", "W0_identity_control": "SURVIVED"}
got = verdicts("grader_mutants2.py", "x")
for name, want in expected.items():
    assert got[name].startswith(want), f"{name}: expected {want}, got {got[name][:80]}"

pristine = scratch / "pristine"
tree = scratch / "r413-tree"
files = subprocess.run(["git", "ls-files", "-z"], cwd=repo, check=True, capture_output=True).stdout
for target in (pristine, tree):
    subprocess.run(["rsync", "-a", "--from0", "--files-from=-", f"{repo}/", f"{target}/"], input=files,
                   check=True)
got = subprocess.run([sys.executable, str(R413), str(tree)], capture_output=True, text=True, check=True,
                     env=dict(os.environ, R413_HEAD_TREE=str(pristine))).stdout
print(got, end="")
assert "all mutants killed" in got and "SURVIVED" not in got, "an R413 mutant survived"
assert (tree / RUN).read_bytes() == (repo / RUN).read_bytes(), "R413 driver did not restore run.py"
print("MUTANTS AS EXPECTED: W0 passes; W1-W6 killed (W3, W4 and W6 by name); X1, X2, X4, X5 killed "
      "and X3 passes as a stricter rule; all six R413 rules killed")
