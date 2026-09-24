#!/usr/bin/env python3
"""R273-6 static audit of direction 2: every `re.*` call (and re.compile) in
sw/builder/test_builder.py from the first `_C_` constant to the end of
test_baremetal_profile_contract(), with its flags; the calls WITHOUT ASCII
mode whose pattern can match differently under Unicode (\\w \\W \\b \\B \\s \\S
\\d \\D, IGNORECASE, or str built at run time) are listed with the argument
they read, for a human to classify as C text or not.
usage: regex_audit.py <repo-root>"""
import ast, sys, re
from pathlib import Path
src = (Path(sys.argv[1]) / "sw/builder/test_builder.py").read_text()
tree = ast.parse(src)
lines = src.splitlines()
start = next(i for i, l in enumerate(lines, 1) if l.startswith("_C_"))
func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "test_baremetal_profile_contract")
end = func.end_lineno
FUNCS = {"compile", "search", "match", "fullmatch", "finditer", "findall", "sub", "subn", "split"}
def has_ascii(call):
    txt = ast.get_source_segment(src, call)
    return "re.ASCII" in txt or "re.A " in txt or "(?a" in txt or "(?am" in txt
def pat(call):
    return ast.get_source_segment(src, call.args[0]) if call.args else ""
total = flagged = 0; rows = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and \
            isinstance(node.func.value, ast.Name) and node.func.value.id == "re" and \
            node.func.attr in FUNCS and start <= node.lineno <= end:
        total += 1
        if has_ascii(node):
            continue
        p = pat(node)
        sensitive = bool(re.search(r"\\\\?[wWbBsSdD]|IGNORECASE|re\.I\b", p)) or \
            not re.fullmatch(r'[rbf]*("[^"]*"|\'[^\']*\')(\s*[rbf]*("[^"]*"|\'[^\']*\'))*', p.strip(), re.S)
        if sensitive:
            flagged += 1
            reads = ast.get_source_segment(src, node.args[1]) if len(node.args) > 1 else "(compiled)"
            rows.append((node.lineno, node.func.attr, " ".join(p.split())[:90], " ".join((reads or "").split())[:60]))
print(f"re.* calls in lines {start}-{end}: {total}; without ASCII mode and Unicode-sensitive or built at run time: {flagged}")
for r in sorted(rows):
    print(f"{r[0]:6d} {r[1]:9s} reads={r[3]!s:60s} pattern={r[2]}")
