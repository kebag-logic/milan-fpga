#!/usr/bin/env python3
"""Reviewer probe: classify every changed token of BASE..HEAD.

Python files: compare the ASTs; report each differing node, and say whether it
is a string constant (and whether that constant is a docstring).  Other files:
print a word-level diff of each changed line after mapping U+2014 to "--", so
what is left is exactly the wording change.
Usage: delta_semantics.py <repo> <base> <head> [--mask]
--mask prints the removed side of each wording change as its length only, so
the output can be published without repeating a removed name.
"""
import ast, difflib, re, subprocess, sys

repo, base, head = sys.argv[1:4]
MASK = "--mask" in sys.argv[4:]

def git(*a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout.decode("utf-8")

files = git("diff", "--name-only", base, head).split()

def docstring_ids(tree):
    ids = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            b = n.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) and isinstance(b[0].value.value, str):
                ids.add(id(b[0].value))
    return ids

def walk_pairs(a, b, path, out, da, db):
    if type(a) is not type(b):
        out.append((path, "NODE-TYPE", repr(a)[:80], repr(b)[:80])); return
    if isinstance(a, ast.Constant):
        if a.value != b.value or type(a.value) is not type(b.value):
            kind = "str-docstring" if id(a) in da and id(b) in db else ("str-constant" if isinstance(a.value, str) and isinstance(b.value, str) else "NON-STR-CONSTANT")
            out.append((path, kind, a.lineno, a.value, b.value))
        return
    for f in a._fields:
        x, y = getattr(a, f, None), getattr(b, f, None)
        if isinstance(x, list):
            if not isinstance(y, list) or len(x) != len(y):
                out.append((path + "." + f, "LIST-LEN", len(x), len(y) if isinstance(y, list) else None)); continue
            for i, (p, q) in enumerate(zip(x, y)):
                if isinstance(p, ast.AST): walk_pairs(p, q, f"{path}.{f}[{i}]", out, da, db)
                elif p != q: out.append((f"{path}.{f}[{i}]", "FIELD", p, q))
        elif isinstance(x, ast.AST):
            if not isinstance(y, ast.AST): out.append((path + "." + f, "FIELD", x, y))
            else: walk_pairs(x, y, path + "." + f, out, da, db)
        elif x != y:
            out.append((path + "." + f, "FIELD", x, y))

def words(old, new):
    sm = difflib.SequenceMatcher(None, old.split(" "), new.split(" "), autojunk=False)
    o, n = old.split(" "), new.split(" ")
    def old_side(text):
        return f"<removed, {len(text)} chars>" if MASK else text
    return [(old_side(" ".join(o[i1:i2])), " ".join(n[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]

bad = 0
for f in files:
    a, b = git("show", f"{base}:{f}"), git("show", f"{head}:{f}")
    print(f"== {f}")
    if f.endswith(".py"):
        ta, tb = ast.parse(a), ast.parse(b)
        out = []
        walk_pairs(ta, tb, "Module", out, docstring_ids(ta), docstring_ids(tb))
        for o in out:
            if o[1] in ("str-docstring", "str-constant"):
                w = words(o[3], o[4])
                print(f"   AST {o[1]} @L{o[2]}: {w}")
            else:
                bad += 1; print("   AST NON-STRING DIFFERENCE", o)
        # comments: token-level
        import io, tokenize
        def toks(s): return [(t.type, t.string) for t in tokenize.generate_tokens(io.StringIO(s).readline) if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)]
        xa, xb = toks(a), toks(b)
        if len(xa) != len(xb): bad += 1; print("   TOKEN COUNT DIFFERS", len(xa), len(xb))
        for p, q in zip(xa, xb):
            if p != q:
                kind = {tokenize.COMMENT: "comment", tokenize.STRING: "string"}.get(p[0], "OTHER-TOKEN")
                if p[0] != q[0] or kind == "OTHER-TOKEN": bad += 1
                if kind == "comment": print(f"   TOKEN comment: {words(p[1], q[1])}")
                elif kind != "string": print("   TOKEN OTHER", p, q)
    else:
        la, lb = a.split("\n"), b.split("\n")
        if len(la) != len(lb): bad += 1; print("   LINE COUNT DIFFERS")
        for i, (p, q) in enumerate(zip(la, lb), 1):
            if p != q:
                pn = p.replace("—", "--")
                dashes = p.count("—")
                left = q.count("—")
                print(f"   L{i}: em-dash {dashes}->{left}; wording: {words(pn, q)}")
print("NON-STRING/STRUCTURAL DIFFERENCES:", bad)
