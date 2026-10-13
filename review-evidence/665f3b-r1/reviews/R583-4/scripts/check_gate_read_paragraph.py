#!/usr/bin/env python3
"""Compare the gate-read paragraph of docs/testing/CI_WORKFLOWS.md with
scripts/ci_scope.py GATE_READ_DOCS. Usage: check_gate_read_paragraph.py <repo>"""
import ast, os, re, sys
repo = sys.argv[1]
page = os.path.join(repo, "docs/testing/CI_WORKFLOWS.md")
lines = open(page, encoding="utf-8").read().splitlines()
start = next(i for i, l in enumerate(lines) if "under `docs/` are relevant because Python" in l)
end = next(i for i in range(start, len(lines)) if lines[i].startswith("The classifier's"))
para = "\n".join(lines[start:end])
print(f"paragraph lines {start+1}..{end}")
print("first line:", lines[start])
words = re.findall(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)\s+pages\b", para, re.I)
print("count words before 'pages' in paragraph:", words)
linked = set()
for t in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", para):
    linked.add(os.path.normpath(os.path.join("docs/testing", t)))
src = open(os.path.join(repo, "scripts/ci_scope.py"), encoding="utf-8").read()
tree = ast.parse(src)
gate = None
for n in tree.body:
    if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == "GATE_READ_DOCS" for t in n.targets):
        gate = set(ast.literal_eval(n.value))
docs_linked = {p for p in linked if p.startswith("docs/")}
print("GATE_READ_DOCS (%d):" % len(gate), sorted(gate))
print("paragraph docs links (%d):" % len(docs_linked), sorted(docs_linked))
print("missing from paragraph:", sorted(gate - docs_linked))
print("extra in paragraph:", sorted(docs_linked - gate))
for p in sorted(docs_linked):
    print("exists" if os.path.exists(os.path.join(repo, p)) else "MISSING", p)
ok = gate == docs_linked and not words
print("RESULT", "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
