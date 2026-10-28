"""Print the MUTANTS dict's keys in a selftest_mutants.py read from stdin, one per line, then the count."""
import ast
import sys

tree = ast.parse(sys.stdin.read())
for node in ast.walk(tree):
    target = getattr(node, 'target', None) or (node.targets[0] if isinstance(node, ast.Assign) else None)
    if isinstance(target, ast.Name) and target.id == 'MUTANTS' and isinstance(node.value, ast.Dict):
        keys = [k.value for k in node.value.keys if isinstance(k, ast.Constant)]
        print('\n'.join(keys))
        print('count', len(keys))
