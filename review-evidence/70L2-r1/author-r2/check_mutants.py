#!/usr/bin/env python3
"""Run both round-1 reviewers' service-grader mutants and assert their outcomes.

usage: check_mutants.py <repo> <scratch>

R412's grader_mutants.py (W0-W6) runs unchanged against <repo>. R413's
armed_mutants.py reads the head's run.py from its review clone, which does not
exist on this host, so a copy of it reads a pristine copy of <repo>'s committed
run.py instead and plants into a scratch tree of <repo>'s tracked files.
Exit 0 only when: W0 (identity) passes; W1-W5 are KILLED (W3 and W4 by name);
W6 (the armed bound without the UART allowance) passes, as a stricter rule; and
every R413 mutant is KILLED.
"""
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
R412 = Path("$REVIEWS/70L2-r412-1-packet/scripts/grader_mutants.py")
R413 = Path("$REVIEWS/70L2-r413-1-packet/probes/armed_mutants.py")
RUN = "tb/verilator/fw_service_budget/run.py"
if scratch.exists():
    shutil.rmtree(scratch)
scratch.mkdir(parents=True)

got = subprocess.run([sys.executable, str(R412), str(repo), str(scratch / "r412")],
                     capture_output=True, text=True, check=True).stdout
print(got, end="")
verdicts = dict(line.split(": ", 1)[0:2] for line in got.splitlines() if ": " in line)
expected = {"W0_identity_control": "SURVIVED", "W1_old_whole_span": "KILLED",
            "W2_unarmed_never_charged": "KILLED", "W3_first_tick_inside_duty": "KILLED",
            "W4_last_tick": "KILLED", "W5_phy_whole_span": "KILLED",
            "W6_armed_no_uart": "SURVIVED"}
for name, want in expected.items():
    assert verdicts[name].startswith(want), f"{name}: expected {want}, got {verdicts[name][:80]}"

pristine = scratch / "pristine-run.py"
pristine.write_bytes(subprocess.run(["git", "show", f"HEAD:{RUN}"], cwd=repo, check=True,
                                    capture_output=True).stdout)
tree = scratch / "r413-tree"
files = subprocess.run(["git", "ls-files", "-z"], cwd=repo, check=True, capture_output=True).stdout
subprocess.run(["rsync", "-a", "--from0", "--files-from=-", f"{repo}/", f"{tree}/"], input=files,
               check=True)
text = R413.read_text()
clone = "$REVIEWS/r413-1-70L2/" + RUN
assert text.count(clone) == 1
adapted = scratch / "r413-armed_mutants.py"
adapted.write_text(text.replace(clone, str(pristine)))
got = subprocess.run([sys.executable, str(adapted), str(tree)], capture_output=True, text=True,
                     check=True).stdout
print(got, end="")
assert "all mutants killed" in got and "SURVIVED" not in got, "an R413 mutant survived"
assert (tree / RUN).read_bytes() == pristine.read_bytes(), "R413 driver did not restore run.py"
print("MUTANTS AS EXPECTED: W0 passes, W1-W5 killed (W3 and W4 included), W6 passes as a "
      "stricter rule, all six R413 rules killed")
