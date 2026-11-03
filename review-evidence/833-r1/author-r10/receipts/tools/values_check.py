"""Check that a commit changed no MUTANTS value and moved BLOCKING unchanged, against a base commit.

usage: python3 -I values_check.py REPO BASE HEAD   (HEAD may be WORKTREE)
Prints the entries added at HEAD, and fails if any base entry differs, moved, or vanished, or if BLOCKING's text
at HEAD (wherever it lives) differs from the base's.
"""
import ast
import subprocess
import sys
from pathlib import Path

repo, base, head = sys.argv[1:4]


def show(rev: str, path: str) -> str:
    if rev == "WORKTREE":
        return (Path(repo) / path).read_text()
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def assigned(src: str, name: str):
    for node in ast.parse(src).body:
        target = node.target if isinstance(node, ast.AnnAssign) else (node.targets[0] if isinstance(node, ast.Assign)
                                                                       else None)
        if isinstance(target, ast.Name) and target.id == name:
            return ast.literal_eval(ast.unparse(node.value))
    return None


support, test = "scripts/process_test_support.py", "scripts/test_suite_cancellation.py"
old, new = assigned(show(base, support), "MUTANTS"), assigned(show(head, support), "MUTANTS")
bad = [name for name in old if new.get(name) != old[name]]
order = list(new)[:len(old)] == list(old)
added = list(new)[len(old):]
blocking = [assigned(show(rev, path), "BLOCKING") for rev in (base, head) for path in (support, test)]
base_blocking = next(b for b in blocking[:2] if b is not None)
head_blocking = [b for b in blocking[2:] if b is not None]
print(f"MUTANTS: {len(old)} at {base}, {len(new)} at {head}; base entries changed: {bad or 'none'}; "
      f"base order kept: {order}; added in order: {added}")
print(f"BLOCKING: defined {len(head_blocking)} time(s) at {head}, identical to {base}'s: "
      f"{head_blocking == [base_blocking]}")
sys.exit(0 if not bad and order and head_blocking == [base_blocking] else 1)
