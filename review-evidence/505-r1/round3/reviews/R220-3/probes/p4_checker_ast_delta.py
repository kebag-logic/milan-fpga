#!/usr/bin/env python3
"""p4 (R220-3): which top-level functions and module constants of
scripts/ci_events.py differ between two revisions, compared by AST with
docstrings removed, and which of the changed functions are reachable from
`check()` (the `--check` path) versus only from `selftest()`.

Usage: p4_checker_ast_delta.py <clone> <rev_a> <rev_b>
"""
import ast
import subprocess
import sys

sys.dont_write_bytecode = True


def source(clone, rev):
    return subprocess.run(["git", "-C", clone, "show", f"{rev}:scripts/ci_events.py"],
                          check=True, capture_output=True, text=True).stdout


def strip_docstrings(node):
    for n in ast.walk(node):
        body = getattr(n, "body", None)
        if (isinstance(body, list) and body and isinstance(body[0], ast.Expr)
                and isinstance(getattr(body[0], "value", None), ast.Constant)
                and isinstance(body[0].value.value, str)):
            n.body = body[1:] or [ast.Pass()]
    return node


def tops(src):
    tree = ast.parse(src)
    funcs, consts = {}, {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            funcs[n.name] = ast.dump(strip_docstrings(n), include_attributes=False)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            for t in targets:
                for name in ast.walk(t):
                    if isinstance(name, ast.Name):
                        consts[name.id] = ast.dump(n.value, include_attributes=False) if n.value else ""
        else:
            # other top-level statements (augmented assignments, subscript
            # stores such as ENV_FILE_WRITERS[...] = ...): keyed by position text
            consts[f"<stmt:{ast.unparse(n)[:80]}>"] = ast.dump(n, include_attributes=False)
    return tree, funcs, consts


def calls_graph(tree):
    graph = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names = {c.id for c in ast.walk(n) if isinstance(c, ast.Name)}
            names |= {c.attr for c in ast.walk(n) if isinstance(c, ast.Attribute)}
            graph[n.name] = names
    return graph


def reachable(graph, root, funcs):
    seen, todo = set(), [root]
    while todo:
        f = todo.pop()
        if f in seen or f not in graph:
            continue
        seen.add(f)
        todo.extend(x for x in graph[f] if x in funcs)
    return seen


def main():
    clone, a, b = sys.argv[1:4]
    ta, fa, ca = tops(source(clone, a))
    tb, fb, cb = tops(source(clone, b))
    changed = sorted(k for k in fa.keys() & fb.keys() if fa[k] != fb[k])
    added = sorted(fb.keys() - fa.keys())
    removed = sorted(fa.keys() - fb.keys())
    cchanged = sorted(k for k in ca.keys() & cb.keys() if ca[k] != cb[k])
    cadded = sorted(cb.keys() - ca.keys())
    cremoved = sorted(ca.keys() - cb.keys())
    gb = calls_graph(tb)
    from_check = reachable(gb, "check", fb)
    from_main_check = reachable(gb, "run_check", fb)
    print(f"revisions: {a} -> {b}")
    print(f"functions/classes: {len(fb)} at b; identical {len(fa.keys() & fb.keys()) - len(changed)}")
    print(f"changed: {changed}")
    print(f"added: {added}")
    print(f"removed: {removed}")
    print(f"module-level statements changed: {cchanged}")
    print(f"module-level statements added: {cadded}")
    print(f"module-level statements removed: {cremoved}")
    for f in changed + added:
        print(f"  {f}: reachable from check()={f in from_check} "
              f"from run_check()={f in from_main_check}")


if __name__ == "__main__":
    main()
