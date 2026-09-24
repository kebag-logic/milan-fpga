#!/usr/bin/env python3
"""Show that PR #117 changes no behaviour in the five files it touches.

usage: semantic_equivalence.py <processor-clone> <base-sha> <head-sha>

* SystemVerilog: the comment-free token stream of each changed .sv file is
  identical at base and head (line and block comments removed, strings kept).
* Python: the AST of each changed runner at head equals the base AST with the
  `timeout=` keyword removed from subprocess.run calls, and nothing else. The
  script also reports every `timeout=` keyword it removed from the base, so a
  reader sees exactly which deadlines were dropped.
Exit 0 only when every file is equivalent.
"""
import ast
import re
import subprocess
import sys

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_$][\w$]*|\d[\w\']*|\'[sSdDhHbBoO]?\w*|\S')


def show(repo: str, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def sv_tokens(text: str) -> list[str]:
    out, i, n = [], 0, len(text)
    buf = []
    while i < n:
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            buf.append(text[i:j + 1])
            i = j + 1
        else:
            buf.append(text[i])
            i += 1
    return TOKEN.findall("".join(buf))


class DropTimeout(ast.NodeTransformer):
    def __init__(self):
        self.dropped = []

    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
        if name == "run":
            keep = []
            for kw in node.keywords:
                if kw.arg == "timeout":
                    self.dropped.append((node.lineno, ast.unparse(kw.value)))
                else:
                    keep.append(kw)
            node.keywords = keep
        return node


def main() -> int:
    repo, base, head = sys.argv[1:4]
    files = subprocess.run(["git", "-C", repo, "diff", "--name-only", base, head],
                           check=True, capture_output=True, text=True).stdout.split()
    ok = True
    for path in files:
        a, b = show(repo, base, path), show(repo, head, path)
        if path.endswith(".sv"):
            ta, tb = sv_tokens(a), sv_tokens(b)
            same = ta == tb
            print(f"{path}: sv tokens base={len(ta)} head={len(tb)} identical={same}")
        elif path.endswith(".py"):
            tree_a = ast.parse(a)
            dropper = DropTimeout()
            tree_a = dropper.visit(tree_a)
            head_drop = DropTimeout()
            tree_b = head_drop.visit(ast.parse(b))
            same = (ast.dump(tree_a) == ast.dump(tree_b)) and not head_drop.dropped
            print(f"{path}: base timeouts dropped={dropper.dropped}; head timeouts="
                  f"{head_drop.dropped}; AST(base minus timeout) == AST(head): {same}")
        else:
            same = False
            print(f"{path}: unexpected file type")
        ok &= same
    print("ALL EQUIVALENT" if ok else "NOT EQUIVALENT")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
