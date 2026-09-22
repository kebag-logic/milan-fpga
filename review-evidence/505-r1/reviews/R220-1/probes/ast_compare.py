import ast, sys
def funcs(path):
    t = ast.parse(open(path).read())
    out = {}
    for n in t.body:
        if isinstance(n, ast.FunctionDef):
            body = n.body[1:] if (n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str)) else n.body
            out[n.name] = ast.dump(ast.Module(body=body, type_ignores=[]))
    return out
b = funcs("/tmp/r220-pristine/base/scripts/ci_events.py"); h = funcs("/tmp/r220-pristine/head/scripts/ci_events.py")
print("functions whose code (docstring excluded) changed:", sorted(k for k in b if k in h and b[k] != h[k]))
