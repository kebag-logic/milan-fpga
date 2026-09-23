#!/usr/bin/env python3
"""AST behaviour-preservation probe for PP issue 104 / PR 105.

Usage: probe_ast_equality.py <repo> <base-rev> <head-rev>

For each changed Python file, parse base and head from git objects. At head,
strip ONLY the return annotation and the leading docstring of the two target
functions; everything else is compared verbatim with ast.dump (no positions).
Also reports: every function whose signature or docstring differs, that the
module docstrings are unchanged, and that the stripped head equals base.
Exit 0 only when both files are equal after the narrow strip AND the unstripped
head differs from base exactly in the two targets.
"""

import ast
import subprocess
import sys

TARGETS = {
    "tb/pp_top/fixture_guards.py": ("main",),
    "tb/pp_top/test_fixture_guards.py": ("test_compiler_environment_and_arguments",),
}


def show(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def strip(tree: ast.Module, names: tuple[str, ...]) -> list[str]:
    done = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
            node.returns = None
            if ast.get_docstring(node, clean=False) is not None:
                node.body = node.body[1:]
            done.append(node.name)
    return done


def funcs(tree: ast.Module) -> dict[str, tuple[str, str | None, str]]:
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[node.name] = (ast.dump(node.args), ast.dump(node.returns) if node.returns else None,
                              ast.get_docstring(node, clean=False) or "")
    return out


def main() -> int:
    repo, base, head = sys.argv[1:4]
    ok = True
    for path, names in TARGETS.items():
        b = ast.parse(show(repo, base, path))
        h = ast.parse(show(repo, head, path))
        print(f"== {path}")
        print(f"  module docstring unchanged: {ast.get_docstring(b) == ast.get_docstring(h)}")
        ok &= ast.get_docstring(b) == ast.get_docstring(h)
        fb, fh = funcs(b), funcs(h)
        changed = sorted(n for n in set(fb) | set(fh) if fb.get(n) != fh.get(n))
        print(f"  functions differing in args/returns/docstring: {changed}")
        ok &= changed == sorted(names)
        for n in names:
            print(f"  {n}: base returns={fb[n][1]} head returns={fh[n][1]}")
            print(f"  {n}: base args==head args: {fb[n][0] == fh[n][0]}")
            ok &= fb[n][0] == fh[n][0]
        raw_equal = ast.dump(b) == ast.dump(h)
        print(f"  unstripped head AST == base AST: {raw_equal} (expected False)")
        ok &= not raw_equal
        stripped = strip(h, names)
        eq = ast.dump(b) == ast.dump(h)
        print(f"  stripped {stripped}; stripped head AST == base AST: {eq}")
        ok &= eq and stripped == list(names)
    print("AST PROBE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
