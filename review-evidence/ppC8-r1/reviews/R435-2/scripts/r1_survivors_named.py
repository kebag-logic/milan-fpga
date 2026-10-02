#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Name the gate tests that kill each round-1 survivor (reviewer-owned).

usage: r1_survivors_named.py TREE WORK

Re-plants, unchanged, the round-1 external review's surviving mutants (from
round1/lint_planted_defects.py MUTANTS) one per isolated copy, runs the gate
verbosely and prints the failing test ids. TREE is never written.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "round1"))
from lint_planted_defects import MUTANTS  # noqa: E402

SURVIVED_IN_ROUND_1 = ("cap45", "rates7", "crf-ge1", "aaf-ge1", "waiver-anytype", "waiver-anycfg",
                       "entity-cfg", "iface-subset")


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    work.mkdir(parents=True, exist_ok=True)
    for name, rel, old, new, what in MUTANTS:
        if name not in SURVIVED_IN_ROUND_1:
            continue
        copy = work / name
        if copy.exists():
            shutil.rmtree(copy)
        shutil.copytree(tree, copy, ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
        target = copy / rel
        text = target.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"{name}: INVALID at this head (pattern occurs {text.count(old)} times; the code it "
                  f"edited was rewritten) | {what}")
            shutil.rmtree(copy)
            continue
        target.write_text(text.replace(old, new), encoding="utf-8")
        proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py", "-v"],
                              cwd=copy / "tb/desc_store", capture_output=True, text=True)
        failing = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\S+ \(\S+\)(?: \[[^\]]*\])?(?: \([^)]*\))?)",
                                        proc.stderr, re.M)))
        verdict = "KILLED" if proc.returncode else "SURVIVED"
        print(f"{name}: {verdict} | {what}\n    " + "\n    ".join(failing or ["(none)"]))
        shutil.rmtree(copy)
    return 0


if __name__ == "__main__":
    sys.exit(main())
