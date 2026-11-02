#!/usr/bin/env python3
"""Check that each round 7 reviewer mutant is in MUTANTS under its behaviour name, edit byte for byte.

Usage: python3 -I r764_8_rename_check.py <repo-root> <rv7_mutants.py> <r7_mutants.py>
Reads each reviewer script's MINE dict by executing only its constant prelude (up to `MINE = {...}`).
"""
import ast
import sys
from pathlib import Path

MAP = {
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


def mine(path: Path) -> dict:
    tree = ast.parse(path.read_text())
    scope: dict = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id.isupper() for t in node.targets):
            exec(compile(ast.Module([node], []), str(path), "exec"), {}, scope)  # constants only
    return scope["MINE"]


def main() -> int:
    root = Path(sys.argv[1])
    sys.path.insert(0, str(root / "scripts"))
    import process_test_support as pts  # noqa: E402
    published = {**mine(Path(sys.argv[2])), **mine(Path(sys.argv[3]))}
    bad = 0
    for old_name, edit in sorted(published.items()):
        edits = [edit] if isinstance(edit[0], str) else list(edit)
        new = MAP.get(old_name)
        ours = list(pts.MUTANTS[new][2:]) if new in pts.MUTANTS else None
        same = ours == [tuple(e) for e in edits]
        bad += not same
        print(f"{old_name} -> {new}: {'IDENTICAL' if same else 'DIFFERENT'}; control {pts.MUTANTS[new][0] if ours else None}")
    print(f"rename check: {'PASS' if not bad else 'FAIL'} ({len(published)} published)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
