#!/usr/bin/env python3
"""R272-5: list every re.* call inside test_baremetal_profile_contract()
whose pattern uses \\w, \\b, \\s or \\d (Unicode-aware on str) with no
re.ASCII flag, no inline (?a) and no cpp_hash (which carries (?a)).
Usage: ascii_audit.py <clone>"""
import ast, re, sys
src = open(sys.argv[1] + "/sw/builder/test_builder.py", encoding="utf-8").read()
fn = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)
          and n.name == "test_baremetal_profile_contract")
print("gate 1b function lines", fn.lineno, fn.end_lineno)
rows = []
for n in ast.walk(fn):
    if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name) and n.func.value.id == "re"
            and n.func.attr in ("compile", "search", "match", "fullmatch",
                                "finditer", "findall", "sub", "split", "subn")
            and n.args):
        continue
    pat = ast.unparse(n.args[0])
    extra = " ".join(ast.unparse(a) for a in n.args[1:] + [k.value for k in n.keywords])
    if re.search(r"\\[wWbBsSdD]", pat) and "ASCII" not in extra \
            and "(?a" not in pat and "cpp_hash" not in pat:
        target = ast.unparse(n.args[1]) if len(n.args) > 1 else "(compiled)"
        rows.append((n.lineno, n.func.attr, target[:40], pat[:60]))
for row in sorted(rows):
    print(*row, sep="\t")
print(len(rows), "calls")
