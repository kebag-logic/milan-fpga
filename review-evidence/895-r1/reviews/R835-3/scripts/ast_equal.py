#!/usr/bin/env python3
"""ast_equal.py A B: whether two Python sources parse to the same AST (comments ignored, docstrings compared)."""
import ast, sys
a, b = (ast.dump(ast.parse(open(p).read())) for p in sys.argv[1:3])
print('AST identical' if a == b else 'AST DIFFERS'); sys.exit(a != b)
