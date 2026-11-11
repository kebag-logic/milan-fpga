"""Report duplicate literal keys in every dict display of a Python source file (argv[1]); exit 1 if any."""
import ast, sys
src = open(sys.argv[1]).read(); bad = 0; n = 0
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Dict):
        seen = {}
        for k in node.keys:
            if isinstance(k, ast.Constant):
                n += 1
                if k.value in seen:
                    bad += 1; print(f"DUP {k.value!r} lines {seen[k.value]} and {k.lineno}")
                seen[k.value] = k.lineno
print(f"constant keys={n} duplicates={bad}"); sys.exit(1 if bad else 0)
