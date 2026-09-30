#!/usr/bin/env python3
"""Run the round-3 review's service-grader mutants unchanged and assert their outcomes.

usage: check_grader_mutants.py <repo> <review-scripts> <scratch>
<review-scripts> holds R412-3's grader_mutants.py (W0-W6) and grader_mutants2.py
(X1-X5, W0), each run against <repo> with its own scratch directory.
Exit 0 only when W0 passes, W1-W6 are KILLED (W3, W4 and W6 by name), X1, X2,
X4 and X5 are KILLED, and X3 (arming from the earliest event of any kind, which
only arms earlier and so charges more) passes.
"""
import shutil
import subprocess
import sys
from pathlib import Path

repo, scripts, scratch = (Path(arg).resolve() for arg in sys.argv[1:4])
if scratch.exists():
    shutil.rmtree(scratch)
scratch.mkdir(parents=True)


def verdicts(script: str, where: str) -> dict[str, str]:
    """Each mutant's verdict line from one of the review's scripts."""
    got = subprocess.run([sys.executable, str(scripts / script), str(repo), str(scratch / where)],
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
shutil.rmtree(scratch)
print("GRADER MUTANTS AS EXPECTED: W0 passes; W1-W6 killed (W3, W4 and W6 by name); "
      "X1, X2, X4, X5 killed and X3 passes as a stricter rule")
