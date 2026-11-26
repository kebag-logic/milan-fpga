"""Are two Python sources the same program once docstrings are removed? usage: ast_same.py A B"""
import ast
import sys
from pathlib import Path


def body(path: str) -> str:
    """The module's AST dump, every docstring dropped."""
    tree = ast.parse(Path(path).read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return ast.dump(tree, include_attributes=False)


same = body(sys.argv[1]) == body(sys.argv[2])
print(f"{'SAME' if same else 'DIFFERENT'} program apart from docstrings: {sys.argv[1]} vs {sys.argv[2]}")
sys.exit(0 if same else 1)
