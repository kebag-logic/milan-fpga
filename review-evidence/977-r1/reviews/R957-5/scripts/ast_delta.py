"""Compare the executable AST (docstrings stripped) of Python files between two commits.
Usage: python3 -I ast_delta.py <repo> <old> <new> <path>...   Exit 0 iff every file's AST is equal."""
import ast, subprocess, sys
def norm(src):
    t = ast.parse(src)
    for n in ast.walk(t):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body \
           and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], 'value', None), ast.Constant) \
           and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    return ast.dump(t, include_attributes=False)
repo, old, new, *paths = sys.argv[1:]
rc = 0
for p in paths:
    a, b = (subprocess.run(['git', '-C', repo, 'show', f'{c}:{p}'], capture_output=True, check=True).stdout for c in (old, new))
    eq = norm(a) == norm(b)
    print(f'{"EQUAL" if eq else "DIFFERENT"} {p} {old[:8]}..{new[:8]}')
    rc |= 0 if eq else 1
sys.exit(rc)
