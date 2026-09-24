import ast, sys, re
src = open("sw/builder/test_builder.py", encoding="utf-8").read()
tree = ast.parse(src)
lo, hi = int(sys.argv[1]), int(sys.argv[2])
FUNCS = {"compile","search","match","fullmatch","finditer","findall","sub","subn","split"}
# map line -> innermost enclosing function
encl = {}
def walk(node, stack):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            walk(child, stack + [child.name])
        else:
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and isinstance(child.func.value, ast.Name) and child.func.value.id == "re" and child.func.attr in FUNCS:
                encl[(child.lineno, child.col_offset)] = (stack[-1] if stack else "<module>", child)
            walk(child, stack)
walk(tree, [])
for (ln, col), (fn, node) in sorted(encl.items()):
    if not (lo <= ln <= hi): continue
    pat = ast.get_source_segment(src, node.args[0]) if node.args else "?"
    flags = [ast.get_source_segment(src, a) for a in node.args[1:]] + [f"{k.arg}={ast.get_source_segment(src,k.value)}" for k in node.keywords]
    fl = " ".join(flags)
    ascii_ = "ASCII" in fl or (pat or "").startswith(("cpp_hash",)) or "(?a" in (pat or "")
    uni = bool(re.search(r"\\\\[wWbBdDsS]|\\[wWbBdDsS]", pat or "")) or "cpp_hash" in (pat or "") or bool(re.search(r"^[a-z_]+$", pat or ""))
    print(f"{ln:6} {fn[:28]:28} {node.func.attr:9} {'U' if uni else ' '}{'A' if ascii_ else ' '} {(pat or '').replace(chr(10),' ')[:70]}  |{fl[:40]}")
