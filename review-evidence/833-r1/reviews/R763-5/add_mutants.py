#!/usr/bin/env python3
"""Append this round's reviewer mutants to MUTANTS in a disposable copy of the tree.

Usage: python3 -I add_mutants.py <tree>   (never the reviewed clone)
Each mutant names no control, so `--mutants NAME... --matrix` runs it on every
owner control and the whole test; the table then shows where, if anywhere, it is red.
"""
import sys
from pathlib import Path

LEAF_RULES = ("                    if clock < deadline + 1.0 and pid in initial.values():\n"
              "                        continue\n"
              "                    if any(parent == pid and child in live for child, (parent, _start) in owned.items()):\n"
              "                        continue\n")
NEW = {
    # TESTING.md:224: two seconds after grace SIGKILL has reached every other descendant.
    "r5-parent-with-live-child-spared": (
        ("elif clock < kill_all:",
         "elif clock < kill_all or any(parent == pid and child in live for child, (parent, _start) in owned.items()):"),),
    # TESTING.md:277: the failure prints each remaining process's parent.
    "r5-report-without-current-parent": (("parent {fields[1]} ", ""),),
    # TESTING.md:277: ... and age.
    "r5-report-age-in-ticks": (("int(fields[19]) / os.sysconf('SC_CLK_TCK')", "int(fields[19])"),),
    # TESTING.md:232: a listing that dies inside every census waits 10 s more.
    "r5-vanishing-fails-at-limit": (("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= limit)"),),
    # Not stated in TESTING.md; informative: resume the shell while one other descendant lives.
    "r5-resume-with-one-live": (("and not (live - {root_pid}):", "and len(live - {root_pid}) <= 1:"),),
    # Not stated in TESTING.md; informative: kill parents at grace together with leaves.
    "r5-parents-killed-at-grace": ((LEAF_RULES, ""),),
}


def main() -> int:
    tree = Path(sys.argv[1])
    support = tree / "scripts/process_test_support.py"
    product = (tree / "scripts/owned_process.py").read_text()
    for name, edits in NEW.items():
        for old, _new in edits:
            assert product.count(old) == 1, (name, old)
    text = support.read_text()
    anchor = "\n}\n\n\ndef mutant_tree("
    assert text.count(anchor) == 1
    entries = "".join(f"    {name!r}: (None, 'reviewer probe, round 5', *{edits!r}),\n" for name, edits in NEW.items())
    support.write_text(text.replace(anchor, "\n" + entries + "}\n\n\ndef mutant_tree(", 1))
    print("\n".join(NEW))
    return 0


if __name__ == "__main__":
    sys.exit(main())
