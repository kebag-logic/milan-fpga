import ast
from pathlib import Path
import subprocess

base = subprocess.run(["git", "show", "ffcbd33de70278ae34b533dcbadde0b36c8cba13:sw/builder/test_builder.py"], capture_output=True, text=True, check=True).stdout
head = Path("sw/builder/test_builder.py").read_text()
population = {"mutations", "census_only_mutations", "resolver_only_mutations", "retired_rule_mutations", "accepted_cases", "accepted_makefiles", "retired_rule_cases"}
def rows(source):
    result = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in population for t in node.targets):
            result.append((node.lineno, ast.dump(node, include_attributes=False)))
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) and node.target.id in population:
            result.append((node.lineno, ast.dump(node, include_attributes=False)))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "accepted_cases" and node.func.attr == "update":
            result.append((node.lineno, ast.dump(node, include_attributes=False)))
        elif isinstance(node, ast.FunctionDef) and node.name == "assert_rejected":
            result.append((node.lineno, ast.dump(node, include_attributes=False)))
    return [r for _, r in sorted(result)]
original, current = rows(base), rows(head)
position = 0
for row in original:
    position = current.index(row, position) + 1
print(f"PASS: all {len(original)} original table definitions, additions, accepted-case updates and rejection grader remain unchanged and ordered.")
print(f"Current population: {len(current)} statements; {len(current)-len(original)} added statements.")
