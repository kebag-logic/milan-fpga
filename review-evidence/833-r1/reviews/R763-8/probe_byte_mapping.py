"""Check every round 7 reviewer mutant against its MUTANTS entry at the head, edit for edit, byte for byte.

Usage: python3 -I probe_byte_mapping.py <clone> <r7_mutants.py> <rv7_mutants.py>
Only the constant definitions and the MINE dict of each published script are executed (from the line
defining the first constant to the dict's closing brace); nothing else in either script runs.
"""
import sys
from pathlib import Path

clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as s  # noqa: E402

MAP = {  # published name -> MUTANTS name, as the PR body's round 8 table maps them
    "r7-check-before-open-sigkill": "check-before-open-for-sigkill",
    "r7-no-resume-in-grace-after-pass-1": "no-resume-later-in-grace",
    "rv7-no-resume-later-in-grace": "no-resume-later-in-grace",
    "r7-sigterm-trap-command-later-grace-resume": "sigterm-trap-command-unless-first-pass-resume",
    "rv7-sigterm-trap-command-later-grace-resume": "sigterm-trap-command-after-later-grace-resume",
    "r7-trap-window-not-later-grace": "trap-window-not-later-in-grace",
    "rv7-no-window-later-in-grace": "no-window-later-in-grace",
    "r7-sigterm-new-while-shell-stopped": "sigterm-to-new-while-shell-stopped",
    "rv7-sigterm-to-new-after-1s": "sigterm-to-new-after-1s",
}


def mine(path: str, first: str) -> dict:
    lines = Path(path).read_text().splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith(first))
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("}"))
    namespace = {}
    exec("".join(lines[start:end + 1]), namespace)
    return namespace["MINE"]


published = {**mine(sys.argv[2], "OPEN = "), **mine(sys.argv[3], "NEW = ")}
bad = 0
for name, edit in published.items():
    target = MAP.get(name)
    if target is None:
        print(f"UNMAPPED {name}")
        bad += 1
        continue
    ours = s.MUTANTS[target][2:]
    same = tuple(ours) == (tuple(edit),)
    bad += not same
    print(f"{'SAME' if same else 'DIFF'} {name} -> {target} (control {s.MUTANTS[target][0]}, words {s.MUTANTS[target][1]!r})")
print(f"published {len(published)} mapped {sum(n in MAP for n in published)} differing {bad}")
