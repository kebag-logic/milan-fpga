"""Compare two generator sources with comments and docstrings removed (AST dump)."""
import ast, sys
def strip(path):
    t = ast.parse(open(path, encoding="utf-8").read())
    for n in ast.walk(t):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and n.body \
           and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) \
           and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return ast.dump(t)
a, b = strip(sys.argv[1]), strip(sys.argv[2])
print("AST-IDENTICAL (code beyond comments/docstrings unchanged)" if a == b else "AST-DIFFERS")
sys.exit(0 if a == b else 1)
