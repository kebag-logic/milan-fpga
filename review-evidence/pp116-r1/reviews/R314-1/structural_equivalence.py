#!/usr/bin/env python3
"""Structural no-behaviour-change evidence for processor PR #117.

Usage: structural_equivalence.py <processor-repo> <base-sha> <head-sha>

For every file the range changes:
  *.sv  -> strip // and /* */ comments (string-literal aware), tokenise on
           whitespace/punctuation and require identical token streams.
  *.py  -> parse both versions with ast; report every difference between the
           two AST dumps after removing each `timeout=` keyword from
           subprocess.run calls in the BASE version (the only intended edit).
Exit 0 when every .sv token stream is identical and every .py AST is identical
to the base once the base's subprocess timeout keywords are dropped.
"""
import ast
import re
import subprocess
import sys


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def sv_tokens(text):
    out, i, n = [], 0, len(text)
    buf = []
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            buf.append(text[i:j + 1]); i = j + 1; continue
        if text.startswith("//", i):
            j = text.find("\n", i); i = n if j < 0 else j; continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2); i = n if j < 0 else j + 2; buf.append(" "); continue
        buf.append(c); i += 1
    code = "".join(buf)
    return re.findall(r"[A-Za-z_$][A-Za-z0-9_$]*|\d+'[sS]?[bBoOdDhH][0-9a-fA-FxXzZ_?]+|'[bBoOdDhH][0-9a-fA-FxXzZ_?]+|\d[\d_]*|\S", code)


class DropTimeout(ast.NodeTransformer):
    dropped = 0

    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "run" and \
                isinstance(f.value, ast.Name) and f.value.id == "subprocess":
            keep = [k for k in node.keywords if k.arg != "timeout"]
            DropTimeout.dropped += len(node.keywords) - len(keep)
            node.keywords = keep
        return node


def main():
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
            ok &= same
        elif path.endswith(".py"):
            DropTimeout.dropped = 0
            ta = ast.dump(DropTimeout().visit(ast.parse(a)))
            dropped = DropTimeout.dropped
            DropTimeout.dropped = 0
            tb_tree = DropTimeout().visit(ast.parse(b))
            still = DropTimeout.dropped
            same = ta == ast.dump(tb_tree)
            print(f"{path}: base subprocess.run timeout keywords={dropped}, head={still}; "
                  f"AST(base minus timeout) == AST(head): {same}")
            ok &= same and dropped == 1 and still == 0
        else:
            print(f"{path}: UNEXPECTED file type"); ok = False
    print("STRUCTURAL EQUIVALENCE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
