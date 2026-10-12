#!/usr/bin/env python3
"""Apply one named mutant to <root>/sw/firmware/ctrl/test/ctrl_build.py (each
anchor must occur exactly once), for a disposable copy of the checkout.
usage: python3 -I mutate.py <root> <mutant>"""
import sys
from pathlib import Path

MUTANTS = {
    "MA-no-config-check": ("    configured(stack)\n    head = git(", "    head = git("),
    "MB-no-hash-check": ("    if held != oid:\n", "    if False:\n"),
    "MC-no-helper-config": ('["git", "-c", HELPER_CONFIG, "-C"', '["git", "-C"'),
    "MD-no-lazy-env": (', "GIT_NO_LAZY_FETCH": "1"}', "}"),
    "ME-commit-unhashed": ("    if held != oid:\n", '    if held != oid and kind != "commit":\n'),
    "MF-promisor-allowlisted": ('"remote.*.url", "remote.*.fetch",',
                                '"remote.*.url", "remote.*.fetch", "remote.*.promisor", "extensions.partialclone",'),
    "MG-root-tree-only-hashed": ("    if held != oid:\n", '    if held != oid and place in ("the pinned commit", "the pinned root tree"):\n'),
}
MUTANTS["MAD-no-config-no-lazy"] = None
root, name = Path(sys.argv[1]), sys.argv[2]
if name == "MAD-no-config-no-lazy":
    for part in ("MA-no-config-check", "MD-no-lazy-env"):
        path = root / "sw/firmware/ctrl/test/ctrl_build.py"
        text = path.read_text(encoding="utf-8"); old, new = MUTANTS[part]
        if text.count(old) != 1:
            sys.exit(f"anchor for {part} occurs {text.count(old)} times")
        path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"applied {name}")
    sys.exit(0)
path = root / "sw/firmware/ctrl/test/ctrl_build.py"
text = path.read_text(encoding="utf-8")
old, new = MUTANTS[name]
if text.count(old) != 1:
    sys.exit(f"anchor for {name} occurs {text.count(old)} times")
path.write_text(text.replace(old, new), encoding="utf-8")
print(f"applied {name}")
