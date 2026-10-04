"""Round 2 before/after: the round-1 code (2f0f5929), executed in memory under its real path (the tree
is never written), against the same planted inputs the new controls use; then the head.

  check 14: the section 4.2 user-name row with its 8x8 figure dropped, and with an extra cell
  shapes:   the tracked plan with each expected refusal's cause replaced by a text the builder never prints

Usage: before_after.py nvm-short | nvm-long | shapes-othercause PLAN WORK"""
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("$LANES/652-builder-names")
OLD = "2f0f59291080aeab934e0d72e124fb448c105e12"
USER_NAME_ROW = re.compile(r"^(\| `0x80` \.\. `0xFF` \| user name \|(?:[^|\n]*\|){3})([^|\n]*\|)$", re.M)


def load_old(rel: str, name: str):
    """The file at OLD, executed as a module under its real path, so ROOT and REPO are the lane."""
    path = LANE / rel
    source = subprocess.run(["git", "show", f"{OLD}:{rel}"], cwd=LANE, capture_output=True, text=True,
                            check=True).stdout
    sys.path.insert(0, str(path.parent))
    module = type(sys)(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


which = sys.argv[1]
if which.startswith("nvm-"):
    gate = load_old("scripts/check_nvm_record_space.py", "check_nvm_record_space")
    edit = (lambda page: USER_NAME_ROW.sub(r"\1", page, count=1)) if which == "nvm-short" else \
        (lambda page: USER_NAME_ROW.sub(r"\1\2\2", page, count=1))
    gate.SEAM.ALLOCATION_PAGE_EDIT = edit
    page = gate.ALLOCATION_PAGE.read_text()
    assert edit(page) != page, "the planted edit did not apply"
    sys.argv = [gate.__file__]
    print(f"{OLD[:8]} check_nvm_record_space with the {which[4:]} user-name row: exit {gate.main()}")
elif which == "shapes-othercause":
    sweep = load_old("syn/resmap/yosys_sweep.py", "yosys_sweep")
    sys.argv = [sweep.__file__, "--plan", sys.argv[2], "--work", sys.argv[3], "shapes"]
    print(f"{OLD[:8]} yosys_sweep shapes with every expected refusal's cause foreign: exit {sweep.main()}")
