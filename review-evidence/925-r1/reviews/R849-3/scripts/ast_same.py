"""Compare two Python sources' ASTs (comments ignored): prints SAME or DIFFERENT."""
import ast, sys
a, b = (ast.dump(ast.parse(open(p, encoding="utf-8").read()), include_attributes=False) for p in sys.argv[1:3])
print("SAME" if a == b else "DIFFERENT")
sys.exit(0 if a == b else 1)
