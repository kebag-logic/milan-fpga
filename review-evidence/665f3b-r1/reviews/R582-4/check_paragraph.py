"""Check the gate-read paragraph of docs/testing/CI_WORKFLOWS.md: no stale
count word, and every GATE_READ_DOCS page is linked from it.
Usage: python3 -I check_paragraph.py <repo>"""
import ast, pathlib, posixpath, re, sys
repo = pathlib.Path(sys.argv[1])
src = (repo / "scripts/ci_scope.py").read_text()
tree = ast.parse(src)
pages = next(ast.literal_eval(n.value) for n in tree.body
             if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "GATE_READ_DOCS")
doc = (repo / "docs/testing/CI_WORKFLOWS.md").read_text().split("\n")
start = next(i for i, l in enumerate(doc) if "pages under `docs/` are relevant because" in l)
end = next(i for i in range(start, len(doc)) if doc[i].strip() == "")
para = "\n".join(doc[start:end])
print(f"paragraph lines {start+1}-{end}")
first = doc[start]
counts = re.findall(r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+) pages\b", first, re.I)
fail = 0
print(f"  opening: {first!r}")
if counts:
    print(f"  count word present: {counts} vs {len(pages)} pages"); fail += counts[0].lower() not in ("eight", str(len(pages)))
links = {posixpath.normpath(posixpath.join("docs/testing", t.split("#")[0]))
         for t in re.findall(r"\]\(([^)]+)\)", para)}
for p in pages:
    ok = p in links
    print(f"  {'ok  ' if ok else 'FAIL'} {p} linked in paragraph"); fail += not ok
extra = sorted(l for l in links if l.startswith("docs/") and l not in pages)
print(f"  linked docs pages not in GATE_READ_DOCS: {extra}")
print(f"pages={len(pages)} failures={fail}")
sys.exit(1 if fail else 0)
