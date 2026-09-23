#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe: prove a base..head Python diff adds only return annotations
and function docstrings, and re-derive the Rule 12 public-function counts.

Usage: ast_equivalence.py REPO BASE HEAD

For every *.py changed between BASE and HEAD in REPO:
  1. parse both blobs;
  2. in the HEAD tree, for each function whose BASE twin (same qualified name)
     has no return annotation, drop HEAD's; for each whose BASE twin has no
     docstring, drop HEAD's leading docstring statement;
  3. require ast.dump(BASE) == ast.dump(stripped HEAD), attributes excluded;
  4. report exactly which (function, element) pairs were stripped and the
     exact HEAD annotation text.
A second strip that removes EVERY function docstring and return annotation
from both sides is also compared, as the looser statement of the same fact.

Then, independently of any consumer script, count public functions (name not
starting with "_") lacking a full PEP 484 signature (every non-self/cls
parameter annotated, plus a return annotation) or lacking a docstring, over
every tracked *.py at BASE and at HEAD.

Exit 0 when every changed file is AST-equal after the strip; 1 otherwise.
"""

import ast
import copy
import subprocess
import sys


def git(repo: str, *args: str) -> str:
    """Run git in REPO and return stdout text."""
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True, text=True).stdout


def functions(tree: ast.AST) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    """Map qualified name -> function node, for every def in the module."""
    found: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}

    def walk(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix + child.name
                found[name] = child
                walk(child, name + ".")
            elif isinstance(child, ast.ClassDef):
                walk(child, prefix + child.name + ".")
            else:
                walk(child, prefix)

    walk(tree, "")
    return found


def has_docstring(node: ast.AST) -> bool:
    """True when the body opens with a string-constant expression."""
    body = getattr(node, "body", [])
    return bool(body) and isinstance(body[0], ast.Expr) \
        and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)


def strip_added(base: ast.AST, head: ast.AST) -> tuple[ast.AST, list[str]]:
    """Remove from HEAD only what BASE lacks: return annotations and docstrings."""
    head = copy.deepcopy(head)
    base_fns = functions(base)
    stripped = []
    for name, node in functions(head).items():
        twin = base_fns.get(name)
        if twin is None:
            stripped.append(f"{name}: NEW FUNCTION (no base twin)")
            continue
        if twin.returns is None and node.returns is not None:
            stripped.append(f"{name}: return annotation -> {ast.unparse(node.returns)}")
            node.returns = None
        base_ann = [a.annotation for a in twin.args.posonlyargs + twin.args.args + twin.args.kwonlyargs]
        head_args = node.args.posonlyargs + node.args.args + node.args.kwonlyargs
        for b_ann, arg in zip(base_ann, head_args):
            if b_ann is None and arg.annotation is not None:
                stripped.append(f"{name}: parameter {arg.arg} annotation -> {ast.unparse(arg.annotation)}")
                arg.annotation = None
        if not has_docstring(twin) and has_docstring(node):
            doc = node.body[0].value.value
            stripped.append(f"{name}: docstring ({len(doc.splitlines())} lines) first line: "
                            f"{doc.splitlines()[0]!r}")
            node.body = node.body[1:]
    return head, stripped


def strip_all(tree: ast.AST) -> ast.AST:
    """Remove every function docstring and every annotation of a def."""
    tree = copy.deepcopy(tree)
    for node in functions(tree).values():
        node.returns = None
        for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            arg.annotation = None
        if has_docstring(node) and len(node.body) > 1:
            node.body = node.body[1:]
    return tree


def rule12(tree: ast.AST) -> tuple[list[str], list[str]]:
    """Public functions lacking a full signature, and lacking a docstring."""
    unannotated, undocumented = [], []
    for name, node in functions(tree).items():
        if node.name.startswith("_"):
            continue
        params = [a for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs
                  if a.arg not in ("self", "cls")]
        if node.args.vararg is not None:
            params.append(node.args.vararg)
        if node.args.kwarg is not None:
            params.append(node.args.kwarg)
        if not all(a.annotation is not None for a in params) or node.returns is None:
            unannotated.append(f"{name}:{node.lineno}")
        if ast.get_docstring(node) is None:
            undocumented.append(f"{name}:{node.lineno}")
    return unannotated, undocumented


def main() -> int:
    """Compare the changed files and print the Rule 12 census; 0 = equivalent."""
    repo, base, head = sys.argv[1:4]
    print(f"repo {repo}\nbase {git(repo, 'rev-parse', base).strip()}\nhead {git(repo, 'rev-parse', head).strip()}")
    changed = git(repo, "diff", "--name-only", base, head).split()
    print(f"changed files: {changed}")
    ok = True
    for path in changed:
        if not path.endswith(".py"):
            print(f"NON-PYTHON CHANGE: {path}")
            ok = False
            continue
        b = ast.parse(git(repo, "show", f"{base}:{path}"))
        h = ast.parse(git(repo, "show", f"{head}:{path}"))
        print(f"\n== {path}")
        print(f"  raw AST equal: {ast.dump(b) == ast.dump(h)}")
        print(f"  module docstring equal: {ast.get_docstring(b) == ast.get_docstring(h)}")
        hs, stripped = strip_added(b, h)
        for line in stripped:
            print(f"  stripped {line}")
        exact = ast.dump(b) == ast.dump(hs)
        loose = ast.dump(strip_all(b)) == ast.dump(strip_all(h))
        print(f"  AST equal after stripping only the added elements: {exact}")
        print(f"  AST equal after stripping all def docstrings/annotations: {loose}")
        ok = ok and exact and loose and not any("NEW FUNCTION" in s for s in stripped)
    for rev in (base, head):
        files = [p for p in git(repo, "ls-tree", "-r", "--name-only", rev).split() if p.endswith(".py")]
        una, und = [], []
        for path in files:
            u1, u2 = rule12(ast.parse(git(repo, "show", f"{rev}:{path}")))
            una += [f"{path}::{x}" for x in u1]
            und += [f"{path}::{x}" for x in u2]
        print(f"\nRule 12 census at {rev[:12]}: {len(files)} tracked .py; "
              f"unannotated public {len(una)}; undocumented public {len(und)}")
        for x in una:
            print(f"  unannotated {x}")
        for x in und:
            print(f"  undocumented {x}")
    print(f"\nRESULT: {'EQUIVALENT' if ok else 'NOT EQUIVALENT'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
